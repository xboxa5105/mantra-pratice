from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )
    postgres_host: str = Field(default="", validation_alias="POSTGRES_HOST")
    postgres_port: str = Field(default="", validation_alias="POSTGRES_PORT")
    postgres_user: str = Field(default="", validation_alias="POSTGRES_USER")
    postgres_password: str = Field(default="", validation_alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(default="", validation_alias="POSTGRES_DB")
