# Folder mẫu: `apps/server/app/core/security/`

**Trách nhiệm:** Xác thực credential/token; authorization ở use case hoặc guard có kiểm chứng.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`access_token.py`](access_token.md) — **Authentication primitives**: Xác minh chữ ký/expiry/token claims; không coi role claim là quyền tài nguyên cụ thể.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
