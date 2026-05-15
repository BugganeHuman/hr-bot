from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_end_screening_panel():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(text='✅ Отправить анкету', callback_data='end_screening')
    )
    return builder.as_markup()