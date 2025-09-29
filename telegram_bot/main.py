from aiogram import Dispatcher
from config import BotSettings
from telegram_bot.handlers.common_handlers import common_router
from telegram_bot.handlers.admin_handlers import admin_router
from utils.cache import DataCache
import asyncio
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='tg.Main')


dp = Dispatcher()
dp.include_routers(common_router, admin_router)
bot = BotSettings.bot


async def main() -> None:
    await DataCache.startup_cache()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())