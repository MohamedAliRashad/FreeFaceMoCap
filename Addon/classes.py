from .Properties import FFMOCAPProperties as Properties

from .Panels import FFMOCAP_PT_select_character, FFMOCAP_PT_select_face_points, FFMOCAP_PT_capture_face, FFMOCAP_PT_no_camera_found, FFMOCAP_PT_initiate_facial_empties

from .Operators import FFMOCAP_OT_capture_face, FFMOCAP_OT_select_character, FFMOCAP_OT_deselect_character, FFMOCAP_OT_select_face_points, \
    FFMOCAP_OT_deselect_face_points, FFMOCAP_OT_apply_face_points, FFMOCAP_OT_clear_face_points,FFMOCAP_OT_initiate_facial_empties, \
    FFMOCAP_OT_confirm_face_location_update

PROPERTIES_CLASSES = [
    Properties
]

PANELS_CLASSES = [
    FFMOCAP_PT_initiate_facial_empties,
    FFMOCAP_PT_select_character,
    FFMOCAP_PT_select_face_points,
    FFMOCAP_PT_capture_face,
    FFMOCAP_PT_no_camera_found
]

OPERATORS_CLASSES = [
    FFMOCAP_OT_initiate_facial_empties,
    FFMOCAP_OT_confirm_face_location_update,
    FFMOCAP_OT_capture_face,
    FFMOCAP_OT_select_character,
    FFMOCAP_OT_deselect_character,
    FFMOCAP_OT_select_face_points,
    FFMOCAP_OT_deselect_face_points,
    FFMOCAP_OT_apply_face_points,
    FFMOCAP_OT_clear_face_points
]
