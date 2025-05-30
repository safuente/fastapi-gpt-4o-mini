from fastapi import APIRouter, HTTPException, Request, Body


from services.auth_service import AuthService
from schemas.login import LoginRequest, LoginResponse
from config import get_settings
from routers.rate_limiter import limiter
from doc_examples import analyze_200, login_401, common_422, common_429, login_200

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()
settings = get_settings()

hashed_password = auth_service.get_password_hash(settings.fake_password)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="""
Authenticate a user using username and password.

If the credentials are valid, an access token is returned. This token must be included in future requests using the `Authorization: Bearer <token>` header.

**Rate limited**: 5 requests per hour per IP.

    """,
    responses=login_200 | login_401 | common_422 | common_429,
)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginRequest = Body(...)):
    if payload.username != settings.fake_username or not auth_service.verify_password(
        payload.password, hashed_password
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth_service.create_access_token(data={"sub": payload.username})
    return LoginResponse(access_token=token)
