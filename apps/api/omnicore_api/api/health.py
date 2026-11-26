from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(tags=["health"])


@router.get("/health/live")
def health_live() -> dict[str, str]:
    return {"status": "ok", "service": "api"}


@router.get("/health/ready", response_model=None)
def health_ready(request: Request) -> JSONResponse:
    engine = getattr(request.app.state, "engine", None)
    if engine is None:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "service": "api"},
        )

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "service": "api"},
        )

    return JSONResponse(
        status_code=200,
        content={"status": "ok", "service": "api"},
    )
