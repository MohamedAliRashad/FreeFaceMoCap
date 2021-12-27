import importlib
import sys
from .config import Config

def get_available_cams():
    if not Config.are_dependencies_installed:
        return []
    
    cameras = []
    if sys.platform == 'win32':
        pygrabber = importlib.import_module('pygrabber.dshow_graph')
        graph = pygrabber.FilterGraph()
        cameras = list(enumerate(graph.get_input_devices()))
    elif sys.platform == 'linux':
        v4l2ctl = importlib.import_module('v4l2ctl')
        for i in range(10):
            try:
                name = str(v4l2ctl.v4l2device.V4l2Device(i).name)
                src = str(v4l2ctl.v4l2device.V4l2Device(i).device)
                camera = (src, name)

                if len(cameras) > 0:
                    if name in list(map(lambda x: x[0], cameras)):
                        continue
                
                cameras.append(camera)
            
            except FileNotFoundError:
                continue

    return cameras

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

if __name__ == '__main__':
    print(get_available_cams())