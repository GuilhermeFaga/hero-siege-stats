import os


assets_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets')

fonts_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets/fonts')

hud_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets/hud')

icons_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets/icons')


def path(file):
    return os.path.join(assets_path, file).replace('\\', '/')


def font(file):
    return os.path.join(fonts_path, file).replace('\\', '/')


def hud(file):
    return os.path.join(hud_path, file).replace('\\', '/')


def icon(file):
    return os.path.join(icons_path, file).replace('\\', '/')
