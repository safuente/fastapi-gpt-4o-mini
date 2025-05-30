from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials

from services.auth_service import AuthService


class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        try:
            return await super().__call__(request)
        except HTTPException as e:
            if e.status_code == status.HTTP_403_FORBIDDEN:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            raise e


auth_scheme = CustomHTTPBearer()
auth_service = AuthService()


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    payload = auth_service.decode_token(token.credentials)
    return payload["sub"]
