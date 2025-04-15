from py3xui import AsyncApi
from config import XUISettings


def login(method):
    async def wrapper(*args, **kwargs):
        """
        :param args:
        :param kwargs: должен обязательно включать panel_url со ссылкой на x-ui панель
        :return:
        """
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
        except Exception as e:
            raise e
        kwargs['xui_api'] = xui_api
        return await method(*args, **kwargs)

    return wrapper