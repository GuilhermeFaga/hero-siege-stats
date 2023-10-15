import ctypes


def icon_fix():
    myappid = 'faga.hero_siege_stats.20231014'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
