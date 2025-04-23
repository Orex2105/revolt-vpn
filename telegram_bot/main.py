import aiogram as ag
from config import BotSettings
from telegram_bot.common_handlers import common_router
import asyncio


dp = ag.Dispatcher()
dp.include_router(common_router)
bot = ag.Bot(BotSettings.get_token().token)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())