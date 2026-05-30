from src import run
from src.engine.logger import _init_logger
import sys

_init_logger()
sys.exit(run())
