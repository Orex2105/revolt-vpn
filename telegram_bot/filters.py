from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from config import BotSettings

class IsAdminFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        user_id = callback.from_user.id
        return user_id in BotSettings.admins