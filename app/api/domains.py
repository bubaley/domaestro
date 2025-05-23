from fastapi import APIRouter, Depends

from app.core.auth import validate_auth_token
from app.schemas.domain import (
    ConfigsResponse,
    DomainRegisterRequest,
    DomainResponse,
    RegenerateRequest,
    RegenerateResponse,
)
from app.services.domain_service import regenerate_configs, register_domain, validate_domain
from app.utils.traefik import list_traefik_configs

router = APIRouter(dependencies=[Depends(validate_auth_token)])


@router.post('/register', response_model=DomainResponse)
def register(request: DomainRegisterRequest):
    return register_domain(request)


@router.post('/validate', response_model=DomainResponse)
def validate(request: DomainRegisterRequest):
    return validate_domain(request)


@router.get('/configs', response_model=ConfigsResponse)
def get_configs():
    return list_traefik_configs()


@router.post('/regenerate', response_model=RegenerateResponse)
def regenerate(request: RegenerateRequest):
    return regenerate_configs(request)
