# Kiến trúc máy chủ — một API minh họa

**Reference:** [`apps/server/app/modules/module1/api01/`](apps/server/app/modules/module1/api01/README.md).

## Luồng API01

`main.py → api/v1.py → module1/api01/view.py → validate.py/models.py → query.py → DB/provider → response`

| File mẫu | Nhiệm vụ |
|---|---|
| `__init__.py` | Package marker, exports nếu cần |
| `models.py` | Request/response DTO, types/nullability |
| `validate.py` | Input validation/normalization, no DB side effect |
| `query.py` | Truy vấn có bind params hoặc data-access, no autonomous commit |
| `view.py` | Auth/policy, business orchestration, transaction, response/errors |

Core liên quan: `config.py` (cấu hình), `database.py` (session), `access_token.py` (identity), `utils/auth.py` (policy). `service/provider.py` mô tả optional outbound adapter.

**Không có API mẫu thứ hai.** Dự án thật có thể dùng `controller/service/repository`, Go/.NET/Node/Java hoặc structure khác; source thực luôn là nguồn xác thực.
