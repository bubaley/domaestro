from app.core.config import CONFIGS_DIR
from app.schemas.domain import ConfigsResponse
from app.services.configs_manager import ConfigsManager


def config_exists(domain: str) -> bool:
    return ConfigsManager(CONFIGS_DIR).file_exists(build_config_name(domain))


def remove_traefik_config(domain: str) -> None:
    ConfigsManager(CONFIGS_DIR).remove_file(build_config_name(domain))


def list_traefik_configs() -> ConfigsResponse:
    return ConfigsResponse(configs=ConfigsManager(CONFIGS_DIR).list_files())


def build_config_name(domain: str) -> str:
    return f'{domain}.yaml'
