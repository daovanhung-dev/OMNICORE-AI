from fastapi import APIRouter, Request, Depends
from app.core.dependencies import guard_items
from app.core.responses import ErrorEnvelope
from app.modules.shared.api_001_items_list.models import ItemResponse
from app.modules.shared.api_001_items_list.view import list_items

router = APIRouter(prefix="/api/v1")

@router.get("/items", response_model=ItemResponse, dependencies=[Depends(guard_items)], responses={401: {"model": ErrorEnvelope}, 403: {"model": ErrorEnvelope}, 422: {"model": ErrorEnvelope}, 503: {"model": ErrorEnvelope}})
def items(request: Request, page: str = "1", page_size: str = "20") -> ItemResponse:
    return list_items(request.app.state.settings, page, page_size)
