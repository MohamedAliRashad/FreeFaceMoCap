from ..config import Config

class Common:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = Config.tab_category

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return Config.are_dependancies_installed and not Config.number_of_available_cameras == 0