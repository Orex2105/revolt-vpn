from aiogram import Dispatcher
from config import BotSettings
from telegram_bot.handlers.common_handlers import common_router
from log_config import setup_logging
from utils.cache import DataCache
import asyncio


dp = Dispatcher()
dp.include_router(common_router)
bot = BotSettings.bot


async def main() -> None:
    setup_logging()
    await DataCache.startup_cache()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())