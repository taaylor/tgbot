from typing import Any, Callable

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, LinkPreviewOptions

import texts
from dependencies.hh_dep import HHVacanciesFilter
from hh_api.hh_service import HHVacansy, get_hh_service
from inline_kb import keyboards
from telegram_ext import CallbackQueryExt, MessageExt
from utils.validators import command_filter

router = Router(name="hh_api")


class HHState(StatesGroup):
    waiting_for_query = State()


@router.message(command_filter("hh"))
@router.callback_query(F.data == "hh_main")
async def handler_hh(event: MessageExt | CallbackQueryExt) -> None:
    message = "Можно воспользоваться сервисом hh.ru"
    if isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer(
            text=message,
            reply_markup=keyboards.hh_main,
        )
    else:
        await event.answer(
            text=message,
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
        safe: Callable[[Any, str], str] = (
            lambda obj, attr: getattr(obj, attr, None) or na
        )
        for vacansy in vacancies:
            vacancies_message.append(
                texts.MESSAGE_VACANSY.format(
                    vacansy.name or na,
                    safe(vacansy.employer, "name"),
                    safe(vacansy.area, "name"),
                    safe(vacansy.salary, "frm"),
                    safe(vacansy.salary, "to"),
                    safe(vacansy.schedule, "name"),
                    safe(vacansy.experience, "name"),
                    vacansy.url,
                )
            )
        await message.answer(
            text="".join(vacancies_message),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=keyboards.hh_vacancies,
        )
    await state.clear()
