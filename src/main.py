import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiogram.fsm.storage.redis import RedisStorage

from callback import entertainment as entertainment_callback
from handlers import entertainment, start, vacancies
from settings import telegram_settings
from telegram_ext import TelegramApp


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    app: TelegramApp = TelegramApp()

    # routing sections
    app.include_router(start.router)
    app.include_router(entertainment.router)
    app.include_router(entertainment_callback.router)
    app.include_router(vacancies.router)

    await app.initialize_from_settings(
        settings=telegram_settings,
        storage=RedisStorage.from_url(telegram_settings.redis.dsn),
    )
    await app.bot.delete_webhook(drop_pending_updates=True)
    # TODO: warning polling
    await app.dispatcher.start_polling(app.bot)

    yield

    await app.dispatcher.stop_polling()
    await app.dispatcher.storage.close()
    await app.bot.session.close()


async def main() -> None:
    async with lifespan():
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (RuntimeError, KeyboardInterrupt):
        pass
