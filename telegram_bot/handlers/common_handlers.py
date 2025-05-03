from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from urllib.parse import urlparse
from telegram_bot.inline_keyboards.command_start import command_start_inline_keyboard
from telegram_bot.inline_keyboards.key_settings_panel import key_settings_panel
from config import BotSettings
from utils.cache import DataCache
from utils.greeting import set_greeting
import logging

bot = BotSettings.bot
logger = logging.getLogger(__name__)

common_router = Router()

@common_router.message(CommandStart())
async def command_start(message: types.Message):
    hi_message = set_greeting()
    keyboard = await command_start_inline_keyboard(user_tg_id=message.chat.id)
    await message.answer(f"{hi_message}, {message.chat.first_name}", reply_markup=keyboard.as_markup())


@common_router.callback_query(F.data == 'key_settings')
async def key_settings(callback: types.CallbackQuery):
    await callback.answer("⌛ Подождите...")
    user_id = callback.message.chat.id

    async with ChatActionSender.typing(bot=bot, chat_id=user_id, interval=1):
        connection = await DataCache.connection(user_id=DataCache.uuid5_hashing(str(user_id)))

        url = urlparse(connection.server.panel_url)
        host = url.hostname
        port = url.port

        server_alive = await DataCache.server_status(host=host, port=port)
        status = '🟢' if server_alive.status else '🔴'
        last_check = server_alive.last_check

        key_url = f'https://anarchyproxy.online/connection/sub/{connection.user_id}'

        keyboard = await key_settings_panel()
        await callback.message.edit_text(f'🌎 <b>Локация</b>: {connection.server.location}\n'
                                         f'📡 <b>Доступность</b>: {status} | '
                                         f'<span class="tg-spoiler">проверено в {last_check}</span>\n\n'
                                         f'<code>{key_url}</code>', parse_mode='html',
                                         reply_markup=keyboard.as_markup())


@common_router.callback_query(F.data == 'back')
async def back_to_previous_menu(callback: types.CallbackQuery):
    hi_message = set_greeting()
    keyboard = await command_start_inline_keyboard(user_tg_id=callback.message.chat.id)
    await callback.message.edit_text(f"{hi_message}, {callback.message.chat.first_name}",
                                     reply_markup=keyboard.as_markup())


@common_router.callback_query(F.data == 'qr')
async def qr_code(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    connection = await DataCache.connection(user_id=DataCache.uuid5_hashing(str(user_id)))
    data = f'https://anarchyproxy.online/connection/sub/{connection.user_id}'

    input_file = DataCache.qr(data=data)

    await callback.answer()
    await callback.message.answer_photo(photo=input_file)