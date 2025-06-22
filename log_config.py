import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LogSettings

BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / LogSettings.LOG_DIR_NAME
LOG_FILE = LOG_DIR / LogSettings.LOG_FILE_NAME
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    logging.basicConfig(
        level = LogSettings.LOG_LEVEL,
        format = LogSettings.LOG_FORMAT,
        handlers=[
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=LogSettings.MAX_LOG_SIZE,
                backupCount=LogSettings.BACKUP_COUNT,
                encoding="utf-8"
            )
        ]
    )