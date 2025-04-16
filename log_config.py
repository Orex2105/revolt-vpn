import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_LEVEL = logging.ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR/"logs.log"
MAX_LOG_SIZE = 10*1024*1024
BACKUP_COUNT = 2

LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            RotatingFileHandler(
                filename=LOG_FILE,
                maxBytes=MAX_LOG_SIZE,
                backupCount=BACKUP_COUNT,
                encoding="utf-8"
            )
        ]
    )