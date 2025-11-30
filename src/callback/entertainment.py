import random

from aiogram import F, Router
from aiogram.enums.dice_emoji import DiceEmoji

from telegram_ext import CallbackQueryExt
from utils.tools import UserRandom, random_data

router = Router(name="callback entertainment")


@router.callback_query(F.data == "random_human")
async def random_human(callback: CallbackQueryExt) -> None:
    await callback.answer(text="Генерирую...", show_alert=False)
    random_user: UserRandom = random_data.random_user

    response_message = (
        "👤 <b>Имя:</b> {name}\n"
        "🏠 <b>Адрес:</b> {address}\n"
        "📧 <b>Email:</b> {email}\n"
        "📞 <b>Телефон:</b> {phone}\n"
        "🎂 <b>Дата рождения:</b> {birth_date}\n"
        "🏢 <b>Компания:</b> {company}\n"
        "💼 <b>Должность:</b> {job}\n"
    ).format(**random_user.model_dump(mode="json"))

    await callback.message.answer(text=response_message)


@router.callback_query(F.data == "lucky_game")
async def lucky_game(callback: CallbackQueryExt) -> None:
    await callback.answer()
    dice_emoji: DiceEmoji = random.choice(tuple(DiceEmoji))
    await callback.message.answer_dice(emoji=dice_emoji)
