from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth_service import AuthService

auth_scheme = HTTPBearer()
auth_service = AuthService()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    payload = auth_service.decode_token(token.credentials)
    return payload["sub"]