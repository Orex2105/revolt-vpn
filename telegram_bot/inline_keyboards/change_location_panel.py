from dao.select_methods_dao import get_servers_locations
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from utils.decorators.inline_keyboard_builder import inline_keyboard_builder


@inline_keyboard_builder
async def change_location_panel(builder: InlineKeyboardBuilder) -> InlineKeyboardBuilder:
    locations = await get_servers_locations()
    
    for i in locations:
        builder.add(InlineKeyboardButton(text=i, callback_data=f"location{i}"))

    builder.adjust(2)

    return builder