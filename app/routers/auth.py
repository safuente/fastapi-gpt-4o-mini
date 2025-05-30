from fastapi import APIRouter, HTTPException, Request, Body


from services.auth_service import AuthService
from schemas.login import LoginRequest, LoginResponse
from config import get_settings
from routers.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()
settings = get_settings()

hashed_password = auth_service.get_password_hash(settings.fake_password)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("1000/minute")
def login(request: Request, payload: LoginRequest = Body(...)):
    if payload.username != settings.fake_username or not auth_service.verify_password(
        payload.password, hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token(data={"sub": payload.username})
    return LoginResponse(access_token=token)
