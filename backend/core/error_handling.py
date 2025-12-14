import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.core.alerts import alert_error

logger = logging.getLogger("app.errors")


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_exc_handler(request: Request, exc: Exception):
        alert_error("Unhandled exception", exc)
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
            },
        )
