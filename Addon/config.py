class Config:
    # Version dependent
    addon_version = '2021.1.0'
    supported_blender_versions = ((2, 80), (2, 81), (2, 82), (2, 83),
                                  (2, 90), (2, 91), (2, 92), (2, 93))
    minimal_blender_api = (2, 80, 60)

    # Main Addon config names
    addon_name = 'Free Face Motion Capture'
    tab_category = 'FFMoCap'
    prefix = 'FFMOCAP'

    # dependancies_installed = []
    are_dependencies_installed = False
    available_cameras = []

    ###### PANELS #####
    panels_prefix = prefix + '_PT_'

    #panels ids
    panel_initiate_face_idname = panels_prefix + 'initiate_face'
    panel_capture_charachter_idname = panels_prefix + 'capture_charachter'
    panel_no_camera_idname = panels_prefix + 'no_camera'
    
    ###### OPERATORS #####
    operators_prefix = 'object.ffmocap_'

    #libraries install operator
    panel_install_dependancies_idname = panels_prefix + 'install_dependancies'
    operator_install_dependancies_idname = operators_prefix + 'install_dependancies'
    operator_install_dependancies_preferences_idname = operators_prefix + 'install_dependancies_preferences'

    # operators ids
    operator_initiate_face_idname = operators_prefix + 'initiate_face'
    operator_generate_rig_idname = operators_prefix + 'generate_rig'
    operator_capture_face_idname = operators_prefix + 'capture_face'

    ###### FACE EMPTIES #####
    empties_prefix = 'FFMoCap_empty_'
    group_empty_prefix = 'FFMoCap_EMPTIES_GROUP_'
    group_empty_initial_scale = 0.25
    group_empty_new_scale = 1
    group_loc = None

    ###### FACE ARMATURE #####
    armature_prefix = 'FFMoCap_Armature_'
    rig_prefix = 'FFMoCap_RIG_'
    rig_data_prefix = 'FFMoCap_RIG_rig_'
    
    num_armatures = 0
    initial_landmarks = None
    armature_points = None
    empties_names = None
    nose_loc = None
    head_loc = None
    lip_bottom_loc = None
    jaw_master_loc = None
    jaw_master = None