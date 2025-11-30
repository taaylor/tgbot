from __future__ import annotations

import logging
import warnings
from typing import Any, Union

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandObject
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import (
    CallbackQuery,
    ChatMemberUpdated,
    InaccessibleMessage,
    Message,
    User,
)

import texts
from settings import TelegramSettings


class TelegramApp:
    _instance: TelegramApp | None = None

    def __new__(cls) -> TelegramApp:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._bot: Bot | None = None
        self._dispatcher: Dispatcher | None = None
        self._init: bool = False
        self.routers: list[Router] = []
        self._bot_username: str | None = None

    def include_router(self, router: Router) -> None:
        self.routers.append(router)

    async def initialize_app(self, bot: Bot, dispatcher: Dispatcher) -> None:
        if not self._init:
            self._bot = bot
            self._dispatcher = dispatcher
            self._dispatcher.include_routers(*self.routers)
            self._bot_username = (await bot.me()).username
            self._init = True

    async def initialize_from_settings(
        self,
        *,
        settings: TelegramSettings,
        storage: BaseStorage | None,
        **dispatcher_kwargs: Any,
    ) -> None:
        if settings.token is None:
            raise ValueError("BotToken is None")

        if settings.debug:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[logging.StreamHandler()],
            )

        await self.initialize_app(
            bot=Bot(
                token=settings.token,
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            ),
            dispatcher=Dispatcher(
                storage=storage,
                **dispatcher_kwargs,
            ),
        )

        if texts.BOT_COMMANDS and self._bot is not None:
            await self._bot.set_my_commands(texts.BOT_COMMANDS)

    @property
    def bot(self) -> Bot:
        if self._bot is None:
            raise ValueError("Bot not initialize")
        return self._bot

    @property
    def dispatcher(self) -> Dispatcher:
        if self._dispatcher is None:
            raise ValueError("Dispatcher not initialize")
        return self._dispatcher

    @property
    def is_initialize(self) -> bool:
        return self._init

    @property
    def bot_username(self) -> str:
        if self._bot_username is None:
            raise ValueError("Bot username is not initialized")
        return self._bot_username


with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)

    class ChatMemberUpdatedExt(ChatMemberUpdated):
        bot: Bot  # marking bot as required for mypy

    class MessageExt(Message):
        bot: Bot  # marking bot as required for mypy

    class MessageFromUser(MessageExt):
        from_user: User  # marking user as required for mypy

    class StartCommandWithDeepLinkObject(CommandObject):
        args: str  # marking args (deep link) as required for mypy

    class CallbackQueryExt(CallbackQuery):
        message: Union[Message, InaccessibleMessage]  # marking bot as required for mypy
