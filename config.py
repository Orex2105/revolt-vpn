import json
from pathlib import Path
from configparser import ConfigParser
from pydantic_models.models import BotCredentials, SubscriptionsCredentials
from aiogram import Bot
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

config = ConfigParser()
config.read(Path(__file__).parent / "config.ini", encoding='utf-8')

class DatabaseSettings:
    DB_USER = config.get('database', 'DB_USER')
    DB_PASSWORD = config.get('database', 'DB_PASSWORD')
    DB_HOST = config.get('database', 'DB_HOST')
    DB_PORT = config.get('database', 'DB_PORT')
    DB_NAME = config.get('database', 'DB_NAME')

    @classmethod
    def get_db_url(cls) -> str:
        return f'postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'

class SubscriptionApiData:
    SUB_PROFILE_TITLE = config.get('subscription_api', 'PROFILE_TITLE')
    SUB_SUPPORT_URL = config.get('subscription_api', 'SUPPORT_URL')
    SUB_UPDATE_INTERVAL = config.get('subscription_api', 'UPDATE_INTERVAL')
    PROFILE_WEB_PAGE_URL = config.get('subscription_api', 'PROFILE_WEB_PAGE_URL')
    ANNOUNCE_TEXT = config.get('subscription_api', 'ANNOUNCE_TEXT')
    ANNOUNCE_URL = config.get('subscription_api', 'ANNOUNCE_URL')
    WEB_PATH = config.get('subscription_api', 'WEB_PATH')
    DOMAIN = config.get('subscription_api', 'DOMAIN')

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
    TOKEN = config.get('bot', 'TOKEN')
    SUPPORT_URL = config.get('bot', 'SUPPORT_URL')
    INFORMATION_BLOCK = config.get('bot', 'INFORMATION_BLOCK')
    admins = json.loads(config['bot']['ADMINS'])
    bot = Bot(TOKEN)

    @classmethod
    def get_token(cls) -> BotCredentials:
        return BotCredentials(
            token=cls.TOKEN,
        )

class LogSettings:
    LOG_DIR_NAME = config.get('logging', 'DIR_NAME')
    LOG_FILE_NAME = config.get('logging', 'FILE_NAME')
    MAX_LOG_SIZE = config.getint('logging', 'MAX_SIZE')
    BACKUP_COUNT = config.getint('logging', 'BACKUP_COUNT')

    log_format_ = config.get('logging', 'FORMAT')
    if log_format_ == 'default':
        LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        LOG_FORMAT = log_format_

    log_level_ = config.get('logging', 'LEVEL')
    match log_level_:
        case 'debug': LOG_LEVEL = DEBUG
        case 'info': LOG_LEVEL = INFO
        case 'warning': LOG_LEVEL = WARNING
        case 'error': LOG_LEVEL = ERROR
        case 'critical': LOG_LEVEL = CRITICAL
        case _: LOG_LEVEL = INFO