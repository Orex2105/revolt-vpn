import datetime
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from telegram_bot.inline_keyboards.command_start import command_start_inline_keyboard
from telegram_bot.inline_keyboards.key_settings_panel import key_settings_panel
from utils.hashing import hash_uuid5
from utils.ping import server_ping
from dao.select_methods_dao import get_connection_info
from config import BotSettings

bot = BotSettings.bot

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


@common_router.callback_query(F.data == 'key_settings')
async def key_settings(callback: types.CallbackQuery):
    await callback.answer("⌛ Подождите...")
    user_id = callback.message.chat.id

    async with ChatActionSender.typing(bot=bot, chat_id=user_id):
        connection = await get_connection_info(user_id=await hash_uuid5(str(user_id)))
        host = connection.server.address

        server_alive = '🟢' if server_ping(host=host) else '🔴'
        delay = server_ping(host=host)

        key_url = f'https://anarchyproxy.online/connection/sub/{connection.user_id}'

        keyboard = await key_settings_panel()
        await callback.message.answer(f'🌐 <b>Локация</b>: {connection.server.location}\n'
                                      f'👀 <b>Доступность</b>: {server_alive}\n'
                                      f'⏱️ <b>Задержка</b>: {delay} ms  \n\n'
                                      f'<code>{key_url}</code>', parse_mode='html',
                                      reply_markup=keyboard.as_markup())