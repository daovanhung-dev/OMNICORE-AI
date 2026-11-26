# Folder mẫu: `apps/server/app/service/`

**Trách nhiệm:** Adapters outbound tới provider; dependency injection và failure handling.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`provider.py`](provider.md) — **External provider adapter**: Adapter HTTP/storage/email/queue tùy tính năng thực; timeout/retry/idempotency khi phù hợp.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
