import logging
import os
import subprocess
import sys
from pathlib import Path

import requests

from src.consts.logger import LOGGING_NAME


latest_url = "https://github.com/GuilhermeFaga/hero-siege-stats/releases/latest"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VERSION_FILE_PATHS = [
    Path(getattr(sys, "_MEIPASS", PROJECT_ROOT)) / "version.txt",
    PROJECT_ROOT / "version.txt",
]
DEV_VERSION = "dev"


def _read_version_file():
    for version_file in VERSION_FILE_PATHS:
        if version_file.is_file():
            version = version_file.read_text(encoding="utf-8").strip()
            if version:
                return version
    return None


def _read_git_tag():
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=True,
            text=True,
        )
        version = result.stdout.strip()
        return version or None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def get_version():
    return current_version()


def latest_version():
    logger = logging.getLogger(LOGGING_NAME)
    try:
        req = requests.get(latest_url)
        if req.status_code == 200:
            logger.log(logging.INFO, os.path.basename(req.url))
            return os.path.basename(req.url)
    except Exception:
        logger.error("Could not fetch latest_version starting without version check")
        pass
    return None


def current_version():
    return (
        os.getenv("HERO_SIEGE_STATS_VERSION")
        or _read_version_file()
        or _read_git_tag()
        or DEV_VERSION
    )


def is_release_version(version: str | None):
    return bool(version and version != DEV_VERSION)
