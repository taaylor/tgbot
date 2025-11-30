from pydantic import BaseModel


class Headers(BaseModel):
    page: int = 0
    per_page: int = 10
    text: str
