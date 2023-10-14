import os


assets_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets')

fonts_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..\\..', 'assets/fonts')


def path(file):
    return os.path.join(assets_path, file)


def font(file):
    return os.path.join(fonts_path, file)
