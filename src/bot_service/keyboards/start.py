from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, WebAppInfo
from aiogram.types import InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Перейти в приложение",
            web_app=WebAppInfo(url="https://prod-team-37-ajc3mefd.REDACTED/")
        )
    )
    return builder.as_markup()
