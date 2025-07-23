from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from utils.decorators.inline_keyboard_builder import inline_keyboard_builder

async def back_button() -> InlineKeyboardButton:
    return InlineKeyboardButton(text="⬅️ Назад", callback_data="back")


@inline_keyboard_builder
async def only_back_button_inline_keyboard(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    back_button_ = await back_button()
    builder.row(back_button_)
    return builder


@inline_keyboard_builder
async def qr_inline_keyboard(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    delete_button = InlineKeyboardButton(text='👀 Скрыть QR-код', callback_data='del_qr')
    builder.row(delete_button)
    return builder


@inline_keyboard_builder
async def yn_panel(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    yes_button = InlineKeyboardButton(text='✅ Да', callback_data='yes')
    no_button = InlineKeyboardButton(text='❌ Нет', callback_data='no')
    builder.add(yes_button, no_button)
    return builder