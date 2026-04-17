from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.common.exception.base_exception import AppException

if TYPE_CHECKING:
    from fastapi import FastAPI

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(_req: Request, exc: AppException) -> JSONResponse:
        logger.warning("AppException: %s (%s)", exc.message, exc.code)
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": {"code": exc.code, "message": exc.message}},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_req: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "error": {"code": "VALIDATION_ERROR", "message": str(exc.errors())},
            },
        )

    @app.exception_handler(Exception)
    async def generic_handler(_req: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": {"code": "INTERNAL_ERROR", "message": "Internal server error"},
            },
        )
