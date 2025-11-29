import random

from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji

from telegram_ext import MessageExt
from utils.validators import command_filter

router = Router(name="lucky")


@router.message(command_filter("lucky"))
async def handlers_lucky(message: MessageExt) -> None:
    dice_emoji: DiceEmoji = random.choice(tuple(DiceEmoji))
    await message.answer_dice(emoji=dice_emoji)
