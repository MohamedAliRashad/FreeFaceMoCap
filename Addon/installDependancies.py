import importlib
import os
import subprocess
import sys
from pathlib import Path

import bpy

from .config import Config
from .Panels.common import Common

if sys.platform == 'win32':
    requirements_path = Path(__file__).parent / "requirements-windows.txt"
elif sys.platform == 'linux':
    requirements_path = Path(__file__).parent / "requirements-linux.txt"

def import_module(module_name, global_name=None, reload=True):
    """
    Import a module.
    :param module_name: Module to import.
    :param global_name: (Optional) Name under which the module is imported. If None the module_name will be used.
       This allows to import under a different name with the same effect as e.g. "import numpy as np" where "np" is
       the global_name under which the module can be accessed.
    :raises: ImportError and ModuleNotFoundError
    """
    if global_name is None:
        global_name = module_name

    if global_name in globals():
        importlib.reload(globals()[global_name])
    else:
        # Attempt to import the module and assign it to globals dictionary. This allow to access the module under
        # the given name, just like the regular import would.
        globals()[global_name] = importlib.import_module(module_name)

def install_pip():
    """
    Installs pip if not already present. Please note that ensurepip.bootstrap() also calls pip, which adds the
    environment variable PIP_REQ_TRACKER. After ensurepip.bootstrap() finishes execution, the directory doesn't exist
    anymore. However, when subprocess is used to call pip, in order to install a package, the environment variables
    still contain PIP_REQ_TRACKER with the now nonexistent path. This is a problem since pip checks if PIP_REQ_TRACKER
    is set and if it is, attempts to use it as temp directory. This would result in an error because the
    directory can't be found. Therefore, PIP_REQ_TRACKER needs to be removed from environment variables.
    :return:
    """
    try:
        # Check if pip is already installed
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True)
        subprocess.call([sys.executable, "-m", "pip", "install", '--upgrade', 'pip'])
    except subprocess.CalledProcessError:
        import ensurepip

        ensurepip.bootstrap()
        os.environ.pop("PIP_REQ_TRACKER", None)

def install_dependancies(module_name = '', from_requirements = True):
    if from_requirements:
        subprocess.call([sys.executable, "-m", "pip", "install", '-r', requirements_path])
    else:
        subprocess.call([sys.executable, "-m", "pip", "install", module_name])

def append_to_sys(module_name= '', from_requirements= True):
    def append_module_to_sys(module):
        try:
            out = subprocess.check_output([sys.executable, '-m', 'pip', 'show', module])
            out_str = str(out).replace('\\n', ' ').split(' ')
            idx = out_str.index('Location:')
            loc_path = out_str[idx + 1]
            if loc_path.endswith("\\r"):
                loc_path = loc_path[:-2]
            if not loc_path in sys.path:
                sys.path.append(loc_path)
        except Exception as e:
            pass
    
    if from_requirements:
        modules = None
        with open(requirements_path, 'r') as f:
            modules = f.read().split("\n")
            if modules[-1].strip() == '':
                modules.pop(-1)
        
        for module in modules:
            append_module_to_sys(module)
    else:
        append_module_to_sys(module_name)

def check_installed(module):
    if module == 'opencv-python':
        module = 'cv2'
    try:
        importlib.import_module(module)
    except:
        raise ModuleNotFoundError('')
    

class FFMOCAP_PT_warning_panel(Common, bpy.types.Panel):
    bl_label = "Dependancies installation Instructions"
    bl_idname = Config.panel_install_dependancies_idname

    @classmethod
    def poll(self, context):
        return not Config.are_dependencies_installed

    def draw(self, context):
        layout = self.layout

        lines = [f"Please install the missing dependencies for the \"{Config.addon_name}\" add-on.",
                 f"1. Open the preferences (Edit > Preferences > Add-ons).",
                 f"2. Search for the \"{Config.addon_name}\" add-on.",
                 f"3. Open the details section of the add-on.",
                 f"4. Click on the \"{FFMOCAP_OT_install_dependencies.bl_label}\" button.",
                 f"   This will download and install the missing Python packages, if Blender has the required",
                 f"   permissions.",
                 f"If you're attempting to run the add-on from the text editor, you won't see the options described",
                 f"above. Please install the add-on properly through the preferences.",
                 f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
                 f"2. Press the \"Install\" button.",
                 f"3. Search for the add-on file.",
                 f"4. Confirm the selection by pressing the \"Install Add-on\" button in the file browser."]

        for line in lines:
            layout.label(text=line)


class FFMOCAP_OT_install_dependencies(bpy.types.Operator):
    bl_idname = Config.operator_install_dependancies_idname
    bl_label = "Install Dependencies"
    bl_description = ("Downloads and installs the required python packages for this add-on. "
                      "Internet connection is required. Blender may have to be started with "
                      "elevated permissions in order to install the package")
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not Config.are_dependencies_installed

    def execute(self, context):
        try:
            install_pip()
            install_dependancies()
            append_to_sys()
        except Exception as err:
            self.report({"ERROR"}, str(err))
            return {"CANCELLED"}


        Config.are_dependencies_installed = True

        modules = None
        with open(requirements_path, 'r') as f:
            modules = f.read().split("\n")
            if modules[-1].strip() == '':
                modules.pop(-1)

        for module in modules:
            try:
                check_installed(module)
            except:
                self.report({'ERROR'}, f'Can not install the module named {module}.')
                return {'CANCELLED'}

        return {"FINISHED"}


class FFMOCAP_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout
        layout.operator(Config.operator_install_dependancies_idname, icon="CONSOLE")


DEPENDANCIES_CLASSES = [
    FFMOCAP_PT_warning_panel,
    FFMOCAP_OT_install_dependencies,
    FFMOCAP_preferences
]