from aiogram import Router, Dispatcher

from . import user

router = Router()


def setup_handlers(dp: Dispatcher):
    dp.include_router(user.router)
