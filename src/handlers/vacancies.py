from typing import Any, Callable

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, LinkPreviewOptions, Message

import texts
from dependencies.hh_dep import HHVacanciesDep
from hh_api.hh_service import HHVacansy, get_hh_service
from inline_kb import keyboards
from telegram_ext import CallbackQueryExt, MessageExt
from utils.validators import command_filter

router = Router(name="hh_api")


def format_vacancy(vacancies: list[HHVacansy]) -> list[str]:
    vacancies_message: list[str] = []
    na = "не указано"
    safe: Callable[[Any, str], str] = lambda obj, attr: getattr(obj, attr, None) or na
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
    return vacancies_message


class HHState(StatesGroup):
    waiting_for_query = State()


@router.message(command_filter("hh"))
@router.callback_query(F.data == "hh_main")
async def handler_hh(event: MessageExt | CallbackQueryExt, state: FSMContext) -> None:
    await state.clear()
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
    await state.clear()
    await callback.answer()
    await callback.message.answer(text="Введите название вакансии:")
    await state.set_state(HHState.waiting_for_query)


@router.message(
    HHState.waiting_for_query,
    HHVacanciesDep(hh_service=get_hh_service()),
)
@router.callback_query(
    F.data == "hh_vacancies_next",
    HHVacanciesDep(hh_service=get_hh_service()),
)
async def handler_hh_vacancies(
    event: MessageExt | CallbackQueryExt,
    vacancies: str | list[HHVacansy],
    state: FSMContext,
) -> None:
    if isinstance(vacancies, str):
        match event:
            case CallbackQuery():
                await event.answer()
                await event.message.answer(text=vacancies)
            case Message():
                await event.answer(text=vacancies)
        await state.clear()
        return

    match event:
        case CallbackQuery():
            await event.answer()
            await event.message.answer(
                text="".join(format_vacancy(vacancies)),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=keyboards.hh_vacancies,
            )
        case Message():
            await event.answer(
                text="".join(format_vacancy(vacancies)),
                link_preview_options=LinkPreviewOptions(is_disabled=True),
                reply_markup=keyboards.hh_vacancies,
            )
