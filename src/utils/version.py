import logging
import os
import requests

from src.consts.logger import LOGGING_NAME

from ..version import version


latest_url = "https://github.com/GuilhermeFaga/hero-siege-stats/releases/latest"


def get_version():
    return version


def latest_version():
    logger = logging.getLogger(LOGGING_NAME)
    try:
        req = requests.get(latest_url)
        if req.status_code == 200:
            logger.log(logging.INFO,os.path.basename(req.url))
            return os.path.basename(req.url)
    except Exception as e:
        logger.error(f"Could not fetch latest_version starting without version check")
        pass
    return None


def current_version():
    return version
