from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils.decorators.inline_keyboard_builder import inline_keyboard_builder


@inline_keyboard_builder
async def key_settings_panel(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    builder.add(InlineKeyboardButton(text='📷 QR-код', callback_data='qr'))
    builder.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back"))

    builder.adjust(1)

    return builder