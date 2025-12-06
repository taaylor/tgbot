from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from hh_api.hh_service import HHServise, HHVacansy
from telegram_ext import CallbackQueryExt, MessageExt


class HHVacanciesDep(Filter):

    __slots__ = ("hh_service",)

    def __init__(self, hh_service: HHServise) -> None:
        self.hh_service: HHServise = hh_service

    async def __call__(
        self,
        event: MessageExt | CallbackQueryExt,
        state: FSMContext,
    ) -> bool | dict[str, str | list[HHVacansy]]:
        state_data = await state.get_data()
        desc, page = state_data.get("descriptions"), state_data.get("page", 1)

        text: str | None = None
        if isinstance(event, Message):
            text = event.text

        if desc is None and text is None:
            return False

        vacancies = await self.hh_service.fetch_vacansy(
            descriptions=desc or text,  # type: ignore[arg-type]
            page=page,
        )
        await state.update_data(
            page=page + 1,
            descriptions=desc or text,
        )

        if vacancies is None:
            return {"vacancies": "По запросу вакансий не найдено :("}

        return {"vacancies": vacancies}
