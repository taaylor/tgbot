import logging
from functools import lru_cache

from httpx import Response
from pydantic import BaseModel, ConfigDict, Field

from utils.httpx_client import HHClient


class NameField(BaseModel):
    name: str | None = None


class BasePydantic(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Salary(BasePydantic):
    frm: int | float | None = Field(alias="from", default=None)
    to: int | float | None = None


class Employer(BasePydantic, NameField):
    # name field for mypy
    pass


class Area(BasePydantic, NameField):
    # name field for mypy
    pass


class Experience(BasePydantic, NameField):
    # name field for mypy
    pass


class Schedule(BasePydantic, NameField):
    # name field for mypy
    pass


class HHVacansy(BasePydantic, NameField):
    url: str
    salary: Salary | None = None
    employer: Employer | None = None
    area: Area | None = None
    schedule: Schedule | None = None
    experience: Experience | None = None


class HHServise:
    __slots__ = ("hh_client",)

    def __init__(self, hh_client: HHClient) -> None:
        self.hh_client: HHClient = hh_client

    async def fetch_vacansy(
        self,
        descriptions: str,
        page: int = 1,
    ) -> list[HHVacansy] | None:
        try:
            vacancies: Response = (
                await self.hh_client.fetch_vacany_by_name(
                    descriptions=descriptions,
                    page=page - 1,
                )
            ).raise_for_status()
        except Exception as error:
            logging.warning(f"Error HH service: {error}")
            return None

        if not vacancies.content:
            logging.info("No content HH service")
            return None

        vacancies_result: list[HHVacansy] = []
        for vacansy in vacancies.json()["items"]:
            vacancies_result.append(HHVacansy.model_validate(vacansy))
        return vacancies_result


@lru_cache
def get_hh_service() -> HHServise:
    return HHServise(hh_client=HHClient())
