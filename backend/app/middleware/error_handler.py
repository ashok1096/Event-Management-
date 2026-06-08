"""Global exception handlers for EventPulse.

Provides a unified JSON error envelope for all errors:

{
    "error": "ExceptionType",
    "detail": "Human-readable message",
    "path": "/api/endpoint",
    "timestamp": "2026-06-07T12:00:00Z"
}
"""

import logging
from datetime import datetime, timezone

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def _error_envelope(error: str, detail: str, request: Request, status_code: int) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "detail": detail,
            "path": str(request.url.path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle all FastAPI/Starlette HTTP exceptions."""
    logger.warning(
        "HTTP exception",
        extra={"status_code": exc.status_code, "detail": exc.detail, "path": request.url.path},
    )
    return _error_envelope(
        error=exc.__class__.__name__,
        detail=str(exc.detail),
        request=request,
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic request validation errors with clear field-level messages."""
    errors = exc.errors()
    detail = "; ".join(
        f"{' -> '.join(str(loc) for loc in err['loc'])}: {err['msg']}"
        for err in errors
    )
    logger.warning(
        "Validation error",
        extra={"path": request.url.path, "errors": errors},
    )
    return _error_envelope(
        error="ValidationError",
        detail=detail,
        request=request,
        status_code=422,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected errors — never exposes stack traces to clients."""
    logger.exception(
        "Unexpected server error",
        extra={"path": request.url.path, "exception_type": type(exc).__name__},
    )
    return _error_envelope(
        error="InternalServerError",
        detail="An unexpected error occurred. Please try again later.",
        request=request,
        status_code=500,
    )
