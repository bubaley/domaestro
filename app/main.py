from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services.configs_manager import ConfigsManager
from app.api.router import router as api_router
from app.core.config import CONFIGS_DIR, TEMPLATES_DIR


@asynccontextmanager
async def lifespan(_):
    if not ConfigsManager(CONFIGS_DIR).folder_exists:
        raise RuntimeError("Missing required 'configs' folder")
    if not ConfigsManager(TEMPLATES_DIR).folder_exists:
        raise RuntimeError("Missing required 'templates' folder")
    yield


app = FastAPI(title='Domaestro', lifespan=lifespan)
app.include_router(api_router, prefix='/api')
