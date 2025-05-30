from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import RedirectResponse


from handlers import add_exception_handlers
from routers import (
    summary_router,
    complete_router,
    translation_router,
    analysis_router,
    auth_router,
)
from config import get_settings
from routers.rate_limiter import limiter


settings = get_settings()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
BASE_API_URL = f"{settings.api_prefix}{settings.api_version}"

app.include_router(summary_router, prefix=f"{BASE_API_URL}")
app.include_router(complete_router, prefix=f"{BASE_API_URL}")
app.include_router(translation_router, prefix=f"{BASE_API_URL}")
app.include_router(analysis_router, prefix=f"{BASE_API_URL}")
app.include_router(auth_router, prefix=f"{BASE_API_URL}")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
