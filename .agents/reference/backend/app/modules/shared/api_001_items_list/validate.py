import re
from app.core.responses import ApiError
from .models import ListParams

def validate_params(page: str, page_size: str) -> ListParams:
    """Từ chối đầu vào không phải số nguyên ASCII trong khoảng đã duyệt."""
    if not re.fullmatch(r"[0-9]{1,6}", page) or not re.fullmatch(r"[0-9]{1,3}", page_size):
        raise ApiError(422, "INVALID_PAGE", "Tham số phân trang không hợp lệ")
    if not 1 <= int(page) <= 100000 or not 1 <= int(page_size) <= 100:
        raise ApiError(422, "INVALID_PAGE", "Tham số phân trang không hợp lệ")
    return ListParams(page=int(page), page_size=int(page_size))
