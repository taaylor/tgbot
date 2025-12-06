import os
from asyncio import sleep

from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import FSInputFile, ReplyKeyboardMarkup
from aiogram.utils.chat_action import ChatActionSender

import texts
from inline_kb import keyboards
from settings import telegram_settings
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

    match command.args:
        case "magic":
            async with ChatActionSender.typing(
                chat_id=message.from_user.id, bot=message.bot
            ):
                await sleep(2)
                await message.answer(
                    text=texts.EASTER_EGGS_MESSAGE, reply_markup=keyboards.my_contacts
                )
        case "music":
            audio: FSInputFile | str
            if handler_start.__dict__.get("music") is None:
                audio = FSInputFile(
                    path=os.path.join(telegram_settings.media, "#141.mp3")
                )
            else:
                audio = handler_start.__dict__["music"]

            msg = await message.answer_audio(audio=audio, caption="Зачитай под бит :)")

            if msg.audio is not None:
                handler_start.__dict__["music"] = msg.audio.file_id
