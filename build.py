import os
from pathlib import Path

import PyInstaller.__main__


def add_data_arg(source: str, destination: str):
    return f"{source}{os.pathsep}{destination}"


args = [
    "hero-siege-stats.py",
    "--onefile",
    "--windowed",
    "--icon",
    "assets/icons/logo.ico",
    "--add-data",
    add_data_arg("assets", "assets/"),
]

if Path("version.txt").is_file():
    args.extend(["--add-data", add_data_arg("version.txt", ".")])

PyInstaller.__main__.run(args)
