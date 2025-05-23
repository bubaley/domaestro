from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@router.get('/health', response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint для мониторинга состояния приложения.
    """
    return HealthResponse(status='healthy', service='domaestro', version='0.1.0')


@router.get('/ready')
async def readiness_check():
    """
    Readiness check endpoint для проверки готовности приложения.
    """
    # Здесь можно добавить проверки баз данных, внешних сервисов и т.д.
    return {'status': 'ready'}
