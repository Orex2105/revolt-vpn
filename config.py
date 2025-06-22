import os
import dotenv
from pathlib import Path
from pydantic_models.models import BotCredentials, SubscriptionsCredentials
from aiogram import Bot
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL


dotenv.load_dotenv(Path(__file__).parent / "config.env")


class DatabaseSettings:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')

    @classmethod
    def get_db_url(cls) -> str:
        return f'postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'


class SubscriptionData:
    SUB_PROFILE_TITLE = os.getenv('SUB_PROFILE_TITLE')
    SUB_SUPPORT_URL = os.getenv('SUB_SUPPORT_URL')
    SUB_UPDATE_INTERVAL = os.getenv('SUB_UPDATE_INTERVAL')
    PROFILE_WEB_PAGE_URL = os.getenv('PROFILE_WEB_PAGE_URL')
    ANNOUNCE_TEXT = os.getenv('ANNOUNCE_TEXT')
    ANNOUNCE_URL = os.getenv('ANNOUNCE_URL')

    @classmethod
    def get_subscription_data(cls) -> SubscriptionsCredentials:
        return SubscriptionsCredentials(
            profile_title=cls.SUB_PROFILE_TITLE,
            support_url=cls.SUB_SUPPORT_URL,
            update_interval=cls.SUB_UPDATE_INTERVAL,
            profile_web_page_url=cls.PROFILE_WEB_PAGE_URL,
            announce_text=cls.ANNOUNCE_TEXT,
            announce_url=cls.ANNOUNCE_URL
        )


class BotSettings:
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(TOKEN)

    @classmethod
    def get_token(cls) -> BotCredentials:
        return BotCredentials(
            token=cls.TOKEN,
        )


class LogSettings:
    LOG_DIR_NAME = os.getenv('LOG_DIR_NAME')
    LOG_FILE_NAME = os.getenv('LOG_FILE_NAME')
    MAX_LOG_SIZE = int(os.getenv('MAX_LOG_SIZE'))
    BACKUP_COUNT = int(os.getenv('BACKUP_COUNT'))

    log_format_ = os.getenv('LOG_FORMAT')
    if log_format_ == 'default':
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        LOG_FORMAT = log_format_

    log_level_ = os.getenv('LOG_LEVEL')
    match log_level_:
        case 'debug': LOG_LEVEL = DEBUG
        case 'info': LOG_LEVEL = INFO
        case 'warning': LOG_LEVEL = WARNING
        case 'error': LOG_LEVEL = ERROR
        case 'critical': LOG_LEVEL = CRITICAL
        case _: LOG_LEVEL = INFO