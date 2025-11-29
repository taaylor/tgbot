from aiogram.types import BotCommand, KeyboardButton

COMMAND_DESCRIPTIONS = {
    "/support": "Обращение в поддержку",
    "/hh": "Вакансии на hh",
    "/lucky": "Испытать удачу",
}

BOT_COMMANDS: list[BotCommand] = [
    BotCommand(command=command, description=desc)
    for command, desc in COMMAND_DESCRIPTIONS.items()
]

MAIN_MENU_KEYBOARD_MARKUP: list[list[KeyboardButton]] = [
    [KeyboardButton(text=command.description) for command in BOT_COMMANDS[:2]],
    [KeyboardButton(text=BOT_COMMANDS[-1].description)],
]


WELCOME_PREMIUM_USER = """
Привет, мой дорогой премиум-пользователь 🌟
"""

WELCOME_USER = """
Привет, мой добрый пользователь!
"""

EASTER_EGGS_MESSAGE = """
<b>Ты нашёл секретную информацию о боте ✨</b>
<b>Разработчик:</b> Максим
<b>Telegram:</b> <a href="https://t.me/taaaylor">@taaaylor</a>
<i>Это его самый первый разработанный бот ;)</i>
"""
