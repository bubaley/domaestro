from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    auth_token: str = Field(env='AUTH_TOKEN')
    valid_cnames: list[str] = Field(default_factory=list)
    valid_ips: list[str] = Field(default_factory=list)
    model_config = SettingsConfigDict(
        env_file='.env',
        enable_decoding=False,
        extra='ignore',
    )

    @field_validator('valid_cnames', 'valid_ips', mode='before')
    @classmethod
    def decode_strings(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [str(x) for x in v.split(',')]
        return v


SETTINGS = Settings()
