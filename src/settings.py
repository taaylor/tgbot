import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    token: str | None = Field(default=None, description="bot token")
    debug: bool = Field(default=True, description="app mode")
    admin: int = Field(default=1064716313, description="admin app")

    media: str = Field(
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "media"),
        description="all media",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


telegram_settings: TelegramSettings = TelegramSettings()
