from fastapi import APIRouter, Depends, HTTPException

from services.auth_service import AuthService

from schemas.login import LoginRequest, LoginResponse

from config import get_settings

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()
settings = get_settings()

hashed_password = auth_service.get_password_hash(settings.fake_password)


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    if request.username != settings.fake_username or not auth_service.verify_password(
        request.password, hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token(data={"sub": request.username})
    return LoginResponse(access_token=token)
