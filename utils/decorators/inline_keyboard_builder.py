from aiogram.utils.keyboard import InlineKeyboardBuilder
import logging

logger = logging.getLogger(__name__)

def inline_keyboard_builder(func):
    async def wrapper(*args, **kwargs):
        try:
            builder = InlineKeyboardBuilder()
            return await func(*args, **kwargs, builder=builder)
        except Exception as e:
            logger.error(f"Keyboard builder error: {e}", exc_info=True)
    return wrapper