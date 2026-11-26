# Lỗi
| Điều kiện | HTTP | Mã |
|---|---|---|
| Query sai định dạng/khoảng | 422 | INVALID_PAGE |
| Không mở/đọc được SQLite | 503 | DATA_UNAVAILABLE |
Định dạng: error.code và error.message. Mặc định công khai; khi bật protected_items, thiếu/sai token: 401 UNAUTHENTICATED; thiếu vai trò reader: 403 FORBIDDEN. Chế độ tùy chọn là minh họa hạ tầng, không phải nghiệp vụ mặc định.
