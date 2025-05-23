from fastapi import APIRouter

from app.api import domains, health

router = APIRouter()
router.include_router(health.router, tags=['health'])
router.include_router(domains.router, prefix='/domains', tags=['domains'])
