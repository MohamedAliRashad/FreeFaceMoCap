from ..config import Config

class Common:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = Config.tab_category

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return Config.are_dependencies_installed and not len(Config.available_cameras) == 0