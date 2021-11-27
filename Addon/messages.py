from .config import Config


USER_MESSAGES = {
    'WE_CANNOT_SHIP': [
        'We cannot ship our core library with our addon due to Blender ',
        'license limitations, so you need to install it yourself.'],

    'RESTART_BLENDER_TO_UNLOAD_CORE': [
        'Before installing the new Core version you need '
        'to relaunch Blender.'],

    'PYFFMOCAP_OK': ['The core library has been installed successfully']
}


ERROR_MESSAGES = {
    'OS_32_BIT': [
        'Error (1010): you have a 32-bit OS or Blender. ',
        'To use our add-on you need a 64-bit OS and Blender. '
    ],

    'BLENDER_32_BIT': [
        'Error (1020): you are using a 32-bit version of Blender. ',
        'To use our add-on you need a 64-bit version of Blender. '],

    'BLENDER_TOO_OLD': [
        'Error (1030): you are using an outdated version of Blender '
        'which we don\'t support. ',
        'Please install the latest official version '
        'of Blender downloaded from their site: www.blender.org'],

    'BLENDER_WITH_UNSUPPORTED_PYTHON': [
        'Error (1040): you are using Blender with an unsupported ',
        'version of Python built in. This may happen when you install ',
        'Blender from Linux repositories. Please install an official ',
        'version of Blender downloaded from www.blender.org website.'],

    'OLD_ADDON': [
        'Error (1050): you have most likely installed an outdated ',
        'version of FaceBuilder add-on. Please download the latest one ',
        'from our web site: https://keentools.io '],

    'NUMPY_PROBLEM': [
        'Error (1060): we have detected a critical issue with '
        'NumPy Python library: ',
        'it\'s either not available or incompatible. ',
        'It can happen when Blender is not using its built-in '
        'Python libraries, ',
        'for some reason relying on the Python libraries '
        'installed in your OS. ',
        'Please try reinstalling Blender using a package from ',
        'the official Blender website: blender.org'],

    'CORE_NOT_INSTALLED': [
        'Error (1070): Core library is not installed.'],

    'INSTALLED_WRONG_INSTEAD_CORE': [
        'Error (1080): you\'ve tried to install either a corrupted archive, ',
        'or something that is not a KeenTools Core library package. ',
        'Please, remove it using the button below, then come to our site ',
        'and download a proper KeenTools Core package and try '
        'to install it again.'],

    'CORE_CANNOT_IMPORT': [
        'Error (1090): the installed Core is corrupted. ',
        'The file you\'ve tried to install seemed to be corrupted. ',
        'Please try to download and install it again. Note that ',
        'versions of the add-on and the Core library should match.'],

    'CORE_HAS_NO_VERSION': [
        'Error (1100): the loaded Core library seems to be corrupted.',
        'You can try to uninstall it using the button bellow, ',
        'and then download and install the Core again.'],

    'CORE_VERSION_PROBLEM': [
        'Error (1110): the installed Core library is outdated. '
        'You can experience issues. ',
        'We recommend you to update the addon and the Core library.'],

    'UNKNOWN': ['Unknown error (0000)']
}


def _get_text_scale_y():
    if hasattr(Config, 'text_scale_y'):
        return Config.text_scale_y
    else:
        return 0.75


def split_long_string(txt, length=80):
    return [txt[i:i + length] for i in range(0, len(txt), length)]


def draw_system_info(layout):
    import sys
    import platform
    import bpy
    box = layout.box()
    col = box.column()
    col.scale_y = _get_text_scale_y()
    col.label(
        text="Blender version: {} API: {}.{}.{}".format(
            bpy.app.version_string, *bpy.app.version))
    col.label(text="Python: {}".format(sys.version))
    arch = platform.architecture()
    col.label(text="Platform: {} / {}".format(arch[1], arch[0]))
    return box


def draw_warning_labels(layout, content, alert=True, icon='INFO'):
    col = layout.column()
    col.alert = alert
    col.scale_y = _get_text_scale_y()
    for i, c in enumerate(content):
        icon_first = icon if i == 0 else 'BLANK1'
        col.label(text=c, icon=icon_first)
    return col


def draw_labels(layout, arr):
    for t in arr:
        layout.label(text=t)


def draw_long_label(layout, txt, length=80):
    draw_labels(layout, split_long_string(txt, length))


def draw_long_labels(layout, arr, length=80):
    for txt in arr:
        draw_long_label(layout, txt, length)
