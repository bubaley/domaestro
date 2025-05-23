from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.settings import SETTINGS

security = HTTPBearer()


def validate_auth_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != SETTINGS.auth_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
