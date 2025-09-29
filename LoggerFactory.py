import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from config import LogSettings


class LoggerFactory:
    def __init__(self):
        self.BASE_DIR = Path(__file__).parent
        self.LOG_DIR = self.BASE_DIR / LogSettings.DIR_NAME
        self.LOG_DIR.mkdir(exist_ok=True)
        self._configured_loggers = set()

    def create_logger(self, name, filename=None, level=None):
        if name in self._configured_loggers:
            return logging.getLogger(name)

        if filename is None:
            filename = f"{name}.log"

        if level is None:
            level = LogSettings.LEVEL

        logger = logging.getLogger(name)
        logger.setLevel(level)

        log_file = self.LOG_DIR / filename
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=LogSettings.MAX_SIZE,
            backupCount=LogSettings.BACKUP_COUNT,
            encoding="utf-8"
        )

        formatter = logging.Formatter(LogSettings.FORMAT)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.propagate = False

        self._configured_loggers.add(name)
        return logger

logger_factory = LoggerFactory()