from typing import Generic, TypeVar
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import JSONResponse

T = TypeVar("T")

class Envelope(BaseModel, Generic[T]):
    data: T

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorEnvelope(BaseModel):
    error: ErrorDetail

class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str) -> None:
        super().__init__(code)
        self.status = status
        self.detail = ErrorDetail(code=code, message=message)

async def handle_error(request: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(status_code=exc.status, content=ErrorEnvelope(error=exc.detail).model_dump())
