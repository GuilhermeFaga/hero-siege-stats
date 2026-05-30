import ctypes
import sys


def icon_fix():
    if not sys.platform.startswith("win32"):
        return

    myappid = "faga.hero_siege_stats.20231014"  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
