from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from telegram_bot.inline_keyboards.command_start import command_start_inline_keyboard
from telegram_bot.inline_keyboards.key_settings_panel import key_settings_panel
from config import BotSettings
from utils.cache import DataCache
from utils.greeting import set_greeting
from subscription_api.subscription_api_helper import SubscriptionApiHelper
import logging
from datetime import datetime

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
        keyboard = await key_settings_panel()

        traffic = await SubscriptionApiHelper.get_traffic(str(user_id))
        traffic_total_spent = round(traffic.total_spent / (1024**3*2), 2)
        traffic_limitation_ = traffic.limitation
        traffic_limitation = round(traffic_limitation_ / (1024 ** 3 * 2), 2) if traffic_limitation_ != 0 else "♾️"

        subscription = await DataCache.subscription(telegram_id=user_id)
        end_date_ = datetime.strptime(str(subscription.end_date), "%Y-%m-%d %H:%M:%S.%f")
        end_date = end_date_.strftime("%Y-%m-%d %H:%M")
        await callback.message.edit_text(f'🔑 <b>ID ключа</b>: <code>{user_id}</code>\n'
                                         f'📡 <b>Потрачено трафика</b>: {traffic_total_spent} ГБ / {traffic_limitation} ГБ\n'
                                         f'⏰ <b>Действует до</b> {end_date}',
                                         reply_markup=keyboard.as_markup(),
                                         parse_mode='html')


@common_router.callback_query(F.data == 'back')
async def back_to_previous_menu(callback: types.CallbackQuery):
    hi_message = set_greeting()
    keyboard = await command_start_inline_keyboard(user_tg_id=callback.message.chat.id)
    await callback.message.edit_text(f"{hi_message}, {callback.message.chat.first_name}",
                                     reply_markup=keyboard.as_markup())


@common_router.callback_query(F.data == 'qr')
async def qr_code(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    data = f'https://anarchyproxy.online/connection/sub/{user_id}'

    input_file = DataCache.qr(data=data)

    await callback.answer()
    await callback.message.answer_photo(photo=input_file, caption='Отсканируйте в приложении, чтобы подключиться')


@common_router.callback_query(F.data == 'support')
async def support_information(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(BotSettings.BOT_SUPPORT_INFORMATION, parse_mode='html')