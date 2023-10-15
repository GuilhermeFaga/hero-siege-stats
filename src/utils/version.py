import os
import requests

from ..version import version


latest_url = "https://github.com/GuilhermeFaga/hero-siege-stats/releases/latest"


def get_version():
    return version


def latest_version():
    req = requests.get(latest_url)
    if req.status_code == 200:
        print(os.path.basename(req.url))
        return os.path.basename(req.url)
    return None


def current_version():
    return version
