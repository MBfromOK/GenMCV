import os
from pathlib import Path

SLASH = os.sep
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__))) # This is your Project Root
if Path(ROOT_DIR, 'config.ini').is_file():
    CONFIG_PATH = ROOT_DIR