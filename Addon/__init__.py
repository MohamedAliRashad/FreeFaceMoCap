'''
Copyright (C) 2021 Rashad and Emam

Created by Rashad and Emam

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
# import bpy

bl_info = {
    "name": "Free Face Motion Capture 2021.1.0",
    "author": "Rashad and Emam",
    "version": (2021, 1, 0),
    "blender": (2, 80, 0),
    "location": "Animation",
    "description": "Free Face Tracking Module for facial motion capture in Blender.",
    "category": "Animation",
    "warning": "Requires installation of dependencies",
    "wiki_url":"https://github.com/MohamedAliRashad/FreeFaceMoCap",
    "tracker_url": "https://github.com/MohamedAliRashad/FreeFaceMoCap/issues",
}

from .installDependancies import DEPENDANCIES_CLASSES, append_to_sys
append_to_sys()

import os
import sys
from threading import Thread

import bpy

from .config import Config
from .messages import (ERROR_MESSAGES, draw_warning_labels, draw_system_info,
                       draw_long_label, draw_long_labels)

from .Properties import SelectCharProp, SelectPointsProp
from .classes import PROPERTIES_CLASSES, PANELS_CLASSES, OPERATORS_CLASSES
from .utils import get_number_of_cams

def _is_platform_64bit():
    import platform
    return platform.architecture()[0] == '64bit'

def _is_python_64bit():
    return sys.maxsize > 4294967296  # 2**32


def _is_config_latest():
    return Config.addon_version == '2021.1.0'


def _is_blender_too_old():
    return bpy.app.version < Config.minimal_blender_api

def _can_load():
    return _is_platform_64bit() and _is_python_64bit() and \
           _is_config_latest() and not _is_blender_too_old()

if not _can_load():
    class FFMOCAPCannotLoadPreferences(bpy.types.AddonPreferences):
        bl_idname = Config.addon_name
        def draw(self, context):
            layout = self.layout
            box = layout.box()

            if not _is_platform_64bit():
                draw_warning_labels(box, ERROR_MESSAGES['OS_32_BIT'],
                                    alert=True, icon='ERROR')
                draw_system_info(layout)
                return

            if not _is_python_64bit():
                draw_warning_labels(box, ERROR_MESSAGES['BLENDER_32_BIT'],
                                    alert=True, icon='ERROR')
                draw_system_info(layout)
                return

            if not _is_config_latest():
                msg = ['Before installing a new add-on version you need '
                       'to relaunch Blender.']
                draw_warning_labels(box, msg, alert=True, icon='ERROR')
                draw_system_info(layout)
                return

            if _is_blender_too_old():
                draw_warning_labels(box, ERROR_MESSAGES['BLENDER_TOO_OLD'],
                                    alert=True, icon='ERROR')
                draw_system_info(layout)
                return

            draw_warning_labels(box, ERROR_MESSAGES['UNKNOWN'],
                                alert=True, icon='ERROR')
    
    def register():
        bpy.utils.register_class(FFMOCAPCannotLoadPreferences)


    def unregister():
        bpy.utils.unregister_class(FFMOCAPCannotLoadPreferences)

else:
    CLASSES_TO_REGISTER = PROPERTIES_CLASSES + PANELS_CLASSES + OPERATORS_CLASSES

    def register():
        try:
            import numpy
            import cv2
            import mediapipe
            Config.are_dependancies_installed = True
            Config.number_of_available_cameras = get_number_of_cams()
        except:
            Config.are_dependancies_installed = False
        

        for cls in DEPENDANCIES_CLASSES:
            bpy.utils.register_class(cls)

        for cls in CLASSES_TO_REGISTER:
            bpy.utils.register_class(cls)
        
        bpy.types.Scene.ffmocap_props = bpy.props.PointerProperty(type= PROPERTIES_CLASSES[0])
        bpy.types.Scene.selected_char_prop = SelectCharProp()
        bpy.types.Scene.points_prop = SelectPointsProp()



    def unregister():
        for cls in DEPENDANCIES_CLASSES:
            bpy.utils.unregister_class(cls)

        for cls in CLASSES_TO_REGISTER:
            bpy.utils.unregister_class(cls)

        del bpy.types.Scene.ffmocap_props
        del bpy.types.Scene.selected_char_prop
        del bpy.types.Scene.points_prop


if __name__ == '__main__':
    register()