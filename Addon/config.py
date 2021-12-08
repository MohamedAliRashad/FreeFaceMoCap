class Config:
    # Version dependent
    addon_version = '2021.1.0'
    supported_blender_versions = ((2, 80), (2, 81), (2, 82), (2, 83),
                                  (2, 90), (2, 91), (2, 92), (2, 93))
    minimal_blender_api = (2, 80, 60)

    # Main Addon config names
    addon_name = 'Free Face Motion Capture'
    tab_category = 'Free Face Motion Capture'
    prefix = 'FFMOCAP'

    # dependancies_installed = []
    are_dependancies_installed = False
    number_of_available_cameras = 0

    ###### PANELS #####
    panels_prefix = prefix + '_PT_'

    #panels ids
    panel_initiate_facial_empties_idname = panels_prefix + 'initiate_facial_empties'
    panel_select_charachter_idname = panels_prefix + 'select_character'
    panel_select_face_points_idname = panels_prefix + 'select_face_points'
    panel_capture_charachter_idname = panels_prefix + 'capture_charachter'
    panel_no_camera_idname = panels_prefix + 'no_camera'
    
    ###### OPERATORS #####
    operators_prefix = 'object.ffmocap_'

    #libraries install operator
    panel_install_dependancies_idname = panels_prefix + 'install_dependancies'
    operator_install_dependancies_idname = operators_prefix + 'install_dependancies'
    operator_install_dependancies_preferences_idname = operators_prefix + 'install_dependancies_preferences'

    # operators ids
    operator_initiate_facial_empties_idname = operators_prefix + 'initiate_facial_empties'
    operator_initiate_facial_armature_idname = operators_prefix + 'initiate_facial_armature'
    operator_confirm_face_location_update_idname = operators_prefix + 'confirm_face_location_update'
    operator_select_character_idname = operators_prefix + 'select_character'
    operator_deselect_character_idname = operators_prefix + 'deselect_character'
    operator_select_face_points_idname = operators_prefix + 'select_face_points'
    operator_deselect_face_points_idname = operators_prefix + 'deselect_face_points'
    operator_clear_face_points_idname = operators_prefix + 'clear_face_points'
    operator_apply_face_points_idname = operators_prefix + 'apply_face_points'
    operator_capture_face_idname = operators_prefix + 'capture_face'

    ###### FACE EMPTIES #####
    empties_prefix = 'FFMoCap_empty_'
    group_empty_name = 'FFMoCap_GROUP_empty'
    group_empty_first_location = (0, 0, 0)
    group_empty_initial_scale = 0.25
    group_empty_new_scale = 1