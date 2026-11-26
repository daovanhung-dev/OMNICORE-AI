# Folder mẫu: `apps/server/app/core/`

**Trách nhiệm:** Cấu hình, database, bảo mật và các cross-cutting concerns.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`security/`](security/README.md) — Xác thực credential/token; authorization ở use case hoặc guard có kiểm chứng.

## File và tài liệu 1:1

- [`config.py`](config.md) — **Typed configuration**: Đọc và kiểm tra env, flags, base URL, timeout; không hardcode secrets.
- [`database.py`](database.md) — **Database access foundation**: Tạo engine/session và helper an toàn; transaction owner vẫn là use case.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
