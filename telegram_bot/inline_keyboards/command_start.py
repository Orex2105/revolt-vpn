from typing import Union
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils.decorators.inline_keyboard_builder import inline_keyboard_builder
from dao.select_methods_dao import get_connection_info, get_admin_info
from utils.hashing import hash_uuid5


@inline_keyboard_builder
async def command_start_inline_keyboard(user_tg_id: Union[str, int],
                                        builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:

    is_admin = await get_admin_info(tg_id=user_tg_id)

    if is_admin is not None:
        builder.row(InlineKeyboardButton(text='💻 Админ-панель', callback_data="admin_panel"))

    user_id = await hash_uuid5(str(user_tg_id))
    user_info = await get_connection_info(user_id=user_id)

    if user_info is not None:
        builder.row(InlineKeyboardButton(text='⚙️ Мой ключ', callback_data="key_settings"))

    builder.row(InlineKeyboardButton(text='ℹ️ Информация', callback_data='info'),
                InlineKeyboardButton(text='👤 Поддержка', callback_data='support'))

    return builder