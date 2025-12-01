from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import ReplyKeyboardMarkup

import texts
from inline_kb import keyboards
from telegram_ext import MessageFromUser, StartCommandWithDeepLinkObject

router = Router(name="start")


@router.message(StateFilter(None), CommandStart())
async def handler_start(
    message: MessageFromUser,
    command: StartCommandWithDeepLinkObject,
) -> None:
    await message.answer(
        text=(
            texts.WELCOME_PREMIUM_USER
            if (
                message.from_user.is_premium is not None
                and message.from_user.is_premium
            )
            else texts.WELCOME_USER
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=texts.MAIN_MENU_KEYBOARD_MARKUP,
            resize_keyboard=True,
            input_field_placeholder="Воспользуйтесь меню:",
        ),
    )

    if command.args is not None and command.args == "magic":
        await message.answer(
            text=texts.EASTER_EGGS_MESSAGE, reply_markup=keyboards.my_contacts
        )
