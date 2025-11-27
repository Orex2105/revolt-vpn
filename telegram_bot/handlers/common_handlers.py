from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.utils.chat_action import ChatActionSender
from telegram_bot.inline_keyboards.command_start import command_start_inline_keyboard
from telegram_bot.inline_keyboards.key_settings_panel import key_settings_panel
from telegram_bot.common_keyboard import only_back_button_inline_keyboard, qr_inline_keyboard
from config import BotSettings, SubscriptionApiData
from utils.cache import DataCache
from utils.greeting import set_greeting
from subscription_api.subscription_api_helper import SubscriptionApiHelper
from datetime import datetime
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='tg.CommonHandler')

bot = BotSettings.bot
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
        traffic_total_spent = round(traffic.total_spent / (1024**3), 2)
        traffic_limitation_ = traffic.limitation
        traffic_limitation = round(traffic_limitation_ / (1024 ** 3), 2) if traffic_limitation_ != 0 else "♾️"
        key_url = 'https://' + SubscriptionApiData.DOMAIN + SubscriptionApiData.WEB_PATH + str(user_id)

        subscription = await DataCache.subscription(telegram_id=user_id)
        end_date_ = datetime.strptime(str(subscription.end_date), "%Y-%m-%d %H:%M:%S.%f")
        end_date = end_date_.strftime("%Y-%m-%d %H:%M")
        await callback.message.edit_text(f'🔑 <b>Ключ</b>: <code>{key_url}</code>\n'
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
    data = f'https://{SubscriptionApiData.DOMAIN}{SubscriptionApiData.WEB_PATH}{user_id}'

    input_file = DataCache.qr(data=data)
    keyboard = await qr_inline_keyboard()

    await callback.message.answer_photo(photo=input_file, caption='Отсканируй в приложении, чтобы подключиться',
                                        reply_markup=keyboard.as_markup())
    await callback.answer()


@common_router.callback_query(F.data == 'del_qr')
async def delete_qr(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()


@common_router.callback_query(F.data == 'info')
async def information(callback: types.CallbackQuery):
    keyboard = await only_back_button_inline_keyboard()
    await callback.message.edit_text(BotSettings.INFORMATION_BLOCK, reply_markup=keyboard.as_markup())
    await callback.answer()


@common_router.callback_query(F.data == 'important')
async def important_button(callback: types.CallbackQuery):
    keyboard = await only_back_button_inline_keyboard()
    await callback.message.edit_text(BotSettings.IMPORTANT_TEXT, parse_mode='html', reply_markup=keyboard.as_markup())
    await callback.answer()