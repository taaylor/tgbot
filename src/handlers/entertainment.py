from aiogram import Router
from aiogram.enums import DiceEmoji

from inline_kb import keyboards
from telegram_ext import MessageExt
from utils.validators import command_filter

router = Router(name="entertainment")


@router.message(command_filter("entertainment"))
async def handler_entertainment(message: MessageExt) -> None:
    await message.answer(
        text=f"Список развлечений {DiceEmoji.DICE.value}",
        reply_markup=keyboards.entertainments,
    )
