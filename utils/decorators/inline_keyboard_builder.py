from aiogram.utils.keyboard import InlineKeyboardBuilder
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='utils.decorators.InlineKeyboardBuilder')


def inline_keyboard_builder(func):
    async def wrapper(*args, **kwargs):
        try:
            builder = InlineKeyboardBuilder()
            return await func(*args, **kwargs, builder=builder)
        except Exception as e:
            logger.error(f"Keyboard builder error: {e}", exc_info=True)
    return wrapper