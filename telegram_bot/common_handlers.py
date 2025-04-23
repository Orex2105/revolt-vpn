import datetime
from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from telegram_bot.inline_keyboards.command_start import command_start_inline_keyboard


common_router = Router()

@common_router.message(CommandStart())
async def command_start(message: types.Message):
    hour_now = datetime.datetime.now().hour
    if hour_now >= 23 or hour_now < 6:
        hi_message = "Доброй ночи"
    elif hour_now in range(6, 12):
        hi_message = "Доброе утро"
    elif hour_now in range(12, 16):
        hi_message = "Добрый день"
    else:
        hi_message = "Добрый вечер"

    keyboard = await command_start_inline_keyboard(user_tg_id=message.chat.id)
    await message.answer(f"{hi_message}, {message.chat.first_name}", reply_markup=keyboard.as_markup())