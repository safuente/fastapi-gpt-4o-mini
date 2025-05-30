from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from handlers import add_exception_handlers
from routers import summary_router, complete_router, translation_router, analysis_router
from config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
)

add_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(summary_router, prefix="/api")
app.include_router(complete_router, prefix="/api")
app.include_router(translation_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
