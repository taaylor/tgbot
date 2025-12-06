import os

from pydantic import BaseModel, Field, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseModel):
    host: str = Field(default="localhost", description="redis host")
    port: int = Field(default=6379, description="redis port")
    fsm_db: int = Field(default=0, description="redis database")
    password: str = Field(default="1234", description="redis password")
    user: str = Field(default="redis_user", description="redis user")
    user_password: str = Field(default="1234", description="redis user password")

    @computed_field
    @property
    def dsn(self) -> str:
        return RedisDsn.build(
            scheme="redis",
            username=self.user,
            password=self.user_password,
            host=self.host,
            port=self.port,
            path=str(self.fsm_db),
        ).unicode_string()


class TelegramSettings(BaseSettings):
    token: str | None = Field(default=None, description="bot token")
    debug: bool = Field(default=True, description="app mode")
    admin: int = Field(default=1064716313, description="admin app")
    redis: RedisSettings = RedisSettings()

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
