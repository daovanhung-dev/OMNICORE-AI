import sqlite3
from app.core.config import Settings
from app.core.database import get_db
from app.core.responses import ApiError
from .models import Item, ItemPage, ItemResponse
from .query import COUNT_ITEMS, LIST_ITEMS
from .validate import validate_params

def list_items(settings: Settings, page: str, page_size: str) -> ItemResponse:
    """Kiểm tra trước khi đọc; hai truy vấn cùng một ảnh chụp giao dịch."""
    params = validate_params(page, page_size)
    try:
        with get_db(settings) as db:
            db.execute("BEGIN")
            total = db.execute(COUNT_ITEMS).fetchone()[0]
            rows = db.execute(LIST_ITEMS, (params.page_size, (params.page - 1) * params.page_size)).fetchall()
            return ItemResponse(data=ItemPage(items=[Item(**dict(row)) for row in rows], total=total, page=params.page, page_size=params.page_size))
    except sqlite3.Error as exc:
        raise ApiError(503, "DATA_UNAVAILABLE", "Dữ liệu tạm thời không khả dụng") from exc
