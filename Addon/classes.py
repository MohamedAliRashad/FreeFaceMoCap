from .Properties import FFMOCAPProperties as Properties

from .Panels import FFMOCAP_PT_capture_face, FFMOCAP_PT_no_camera_found, FFMOCAP_PT_initiate_face

from .Operators import FFMOCAP_OT_capture_face, FFMOCAP_OT_initiate_face, FFMOCAP_OT_generate_rig

PROPERTIES_CLASSES = [
    Properties
]

PANELS_CLASSES = [
    FFMOCAP_PT_initiate_face,
    FFMOCAP_PT_capture_face,
    FFMOCAP_PT_no_camera_found
]

OPERATORS_CLASSES = [
    FFMOCAP_OT_initiate_face,
    FFMOCAP_OT_generate_rig,
    FFMOCAP_OT_capture_face,
]
