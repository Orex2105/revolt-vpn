from py3xui import AsyncApi
from config import XUISettings
import logging

logger = logging.getLogger(__name__)


def login(method):
    async def wrapper(*args, **kwargs):
        panel_url = kwargs.get('panel_url')
        if not panel_url:
            raise ValueError("panel_url обязателен для авторизации")
        try:
            xui_api = AsyncApi(
                host=panel_url,
                username=XUISettings.XUI_USERNAME,
                password=XUISettings.XUI_PASSWORD
            )
            await xui_api.login()
            kwargs['xui_api'] = xui_api
            return await method(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            return await method(*args, **kwargs)

    return wrapper