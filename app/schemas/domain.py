from pydantic import BaseModel, Field


class DomainRegisterRequest(BaseModel):
    domain: str = Field(..., example='example.com')
    template: str = Field(default='default', example='default')


class DomainResponse(BaseModel):
    domain: str
    success: bool
    error: str | None = None
    template: str | None = None


class ConfigsResponse(BaseModel):
    configs: list[str]


class RegenerateRequest(BaseModel):
    template: str | None = Field(
        default=None, example='default', description='Шаблон для регенерации. Если не указан, регенерирует все конфиги'
    )


class RegenerateResult(BaseModel):
    domain: str
    success: bool
    error: str | None = None
    template: str | None = None


class RegenerateResponse(BaseModel):
    results: list[RegenerateResult]
    total_processed: int
    successful: int
    failed: int
