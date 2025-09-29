from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils.decorators.inline_keyboard_builder import inline_keyboard_builder
from telegram_bot.common_keyboard import back_button
from LoggerFactory import logger_factory

logger = logger_factory.create_logger(name='tg.KeySettingsPanelKeyboard')


@inline_keyboard_builder
async def key_settings_panel(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(InlineKeyboardButton(text='📷 QR-код', callback_data='qr'))
    back_button_ = await back_button()
    builder.add(back_button_)

    builder.adjust(1)

    return builder