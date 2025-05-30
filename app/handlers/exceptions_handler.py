from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi.errors import RateLimitExceeded
from exceptions import AppException
from schemas.error import ErrorResponse
import logging

logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(f"App error: {exc.error_code} - {exc.message}")
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder(
                ErrorResponse(detail=exc.message, error_code=exc.error_code)
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(
                ErrorResponse(detail=str(exc.detail), error_code="http_error")
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.warning("Validation error: %s", exc.errors())

        error_details = [
            f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        ]
        detail_msg = "; ".join(error_details)

        return JSONResponse(
            status_code=422,
            content=jsonable_encoder(
                ErrorResponse(
                    detail=f"Invalid request: {detail_msg}",
                    error_code="validation_error",
                )
            ),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled exception occurred")
        return JSONResponse(
            status_code=500,
            content=jsonable_encoder(
                ErrorResponse(
                    detail="Internal server error", error_code="internal_error"
                )
            ),
        )

    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content=jsonable_encoder(
                ErrorResponse(
                    detail="Rate limit exceeded. Try again later", error_code="rate_limit_error"
                )
            ),
        )
