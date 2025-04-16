import os
import dotenv
from pathlib import Path
from pydantic import BaseModel


dotenv.load_dotenv(Path(__file__).parent / "config.env")


class XUICredentials(BaseModel):
    username: str
    password: str
    emojis: list[str]


class DatabaseSettings:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')


    @classmethod
    def get_db_url(cls) -> str:
        return f'postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}'


class XUISettings:
    XUI_USERNAME = os.getenv('XUI_USERNAME')
    XUI_PASSWORD = os.getenv('XUI_PASSWORD')
    EMOJIS = ['🚀', '🌟', '🌐', '👽', '🤠', '⚡️']


    @classmethod
    def get_xui_data(cls) -> XUICredentials:
        return XUICredentials(
            username=cls.XUI_USERNAME,
            password=cls.XUI_PASSWORD,
            emojis=cls.EMOJIS
        )