from aiogram.filters import Filter

from hh_api.hh_service import HHServise, HHVacansy
from telegram_ext import MessageExt


class HHVacanciesFilter(Filter):

    __slots__ = ("hh_service",)

    def __init__(self, hh_service: HHServise) -> None:
        self.hh_service: HHServise = hh_service

    async def __call__(
        self,
        message: MessageExt,
    ) -> bool | dict[str, str | list[HHVacansy]]:
        if message.text is None or message.text.isdigit():
            return False

        vacancies = await self.hh_service.fetch_vacansy(descriptions=message.text)

        if vacancies is None:
            return {"vacancies": "По запросу вакансий не найдено :("}

        return {"vacancies": vacancies}
