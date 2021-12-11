import importlib
from .config import Config

def get_available_cams():
    if not Config.are_dependencies_installed:
        return 0
    cv2 = importlib.import_module('cv2')
    cameras = []
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if not cap.read()[0]:
            continue
        else:
            cameras.append(i)
        cap.release()
        cv2.destroyAllWindows()
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