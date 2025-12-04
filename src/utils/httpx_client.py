from typing import Any

from httpx import AsyncClient, Response

AnyJson = dict[str, Any]


class BaseBridge:
    def __init__(
        self,
        *,
        base_url: str,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.client: AsyncClient = AsyncClient(
            base_url=base_url,
            headers=headers,
        )


class HHClient(BaseBridge):

    __slots__ = ("client",)

    def __init__(self) -> None:
        super().__init__(base_url="https://api.hh.ru")

    async def fetch_vacany_by_name(
        self,
        descriptions: str,
        page: int = 0,
        per_page: int = 5,
    ) -> Response:
        return await self.client.get(
            url="/vacancies",
            params={
                "page": page,
                "per_page": per_page,
                "text": descriptions,
            },
        )
