from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

logger = logging.getLogger(__name__)


def inline_keyboard_builder(method):
    async def wrapper(*args, **kwargs):
        try:
            builder = InlineKeyboardBuilder()
            builder = await method(*args, **kwargs, builder=builder)
            return builder
        except Exception as e:
            logger.error(e)
            return InlineKeyboardBuilder()
    return wrapper