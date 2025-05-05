import os
import dotenv
from pathlib import Path
from pydantic_models.models import XUICredentials, BotCredentials, SubscriptionsCredentials
from aiogram import Bot


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


class XUISettings:
    XUI_USERNAME = os.getenv('XUI_USERNAME')
    XUI_PASSWORD = os.getenv('XUI_PASSWORD')

    @classmethod
    def get_xui_data(cls) -> XUICredentials:
        return XUICredentials(
            username=cls.XUI_USERNAME,
            password=cls.XUI_PASSWORD,
        )


class BotSettings:
    TOKEN = os.getenv("BOT_TOKEN")
    bot = Bot(TOKEN)

    @classmethod
    def get_token(cls) -> BotCredentials:
        return BotCredentials(
            token=cls.TOKEN,
        )