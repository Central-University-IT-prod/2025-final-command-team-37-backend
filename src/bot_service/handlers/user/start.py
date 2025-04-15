from aiogram import Router, types
from aiogram.filters.command import CommandStart

from keyboards.start import get_start_keyboard

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer_sticker(
        'CAACAgIAAxkBAAEdWdFnxW5VFJaYu0o8krQ_0Y_W8-qVOAACAQEAAladvQoivp8OuMLmNDYE'
    )
    await message.answer(
        "✋ Добро пожаловать!\n\n"
        "<b>Нажмите на кнопку ниже для перехода в приложение</b>",
        reply_markup=get_start_keyboard()
    )
