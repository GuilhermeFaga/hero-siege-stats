import logging
import sys

from src.consts.logger import LOGGING_NAME

def _init_logger():
    logger = logging.getLogger(LOGGING_NAME)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname}] [{module}] {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)