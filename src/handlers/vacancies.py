from typing import Any, Callable

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from dependencies.hh_dep import HHVacanciesFilter
from hh_api.hh_service import HHVacansy, get_hh_service
from inline_kb import keyboards
from telegram_ext import CallbackQueryExt, MessageExt
from utils.validators import command_filter

router = Router(name="hh_api")


class HHState(StatesGroup):
    waiting_for_query = State()


@router.message(command_filter("hh"))
async def handler_hh(message: MessageExt) -> None:
    await message.answer(
        text="Можно воспользоваться сервисом hh.ru",
        reply_markup=keyboards.hh_main,
    )


@router.callback_query(F.data == "hh_vacancies")
async def callback_hh_vacancies_search(
    callback: CallbackQueryExt,
    state: FSMContext,
) -> None:
    await callback.answer()
    await callback.message.answer(text="Введите название вакансии:")
    await state.set_state(HHState.waiting_for_query)


@router.message(
    HHState.waiting_for_query,
    HHVacanciesFilter(hh_service=get_hh_service()),
)
async def handler_hh_vacancies(
    message: MessageExt,
    state: FSMContext,
    vacancies: str | list[HHVacansy],
) -> None:
    if isinstance(vacancies, str):
        await message.answer(text=vacancies)
    else:
        vacancies_message: list[str] = []
        na = "не указано"
        safe_func: Callable[[Any, str], str] = (
            lambda obj, attr: getattr(obj, attr, None) or na
        )
        for vacansy in vacancies:
            vacancies_message.append(
                f"""
                Наименование вакансии: {vacansy.name or na}\n
                Работодатель: {safe_func(vacansy.employer, "name")}\n
                Место работы: {safe_func(vacansy.area, "name")}\n
                Заработная плата: от {safe_func(vacansy.salary, "frm")}
                до {safe_func(vacansy.salary, "to")}\n
                График работы: {safe_func(vacansy.schedule, "name")}
                Требуемый опыт: {safe_func(vacansy.experience, "name")}
                Ссылка на вакансию: {vacansy.url}
                """
            )
        await message.answer(text="\n\n".join(vacancies_message))
    await state.clear()
