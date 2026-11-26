# Folder mẫu: `apps/client/src/app/core/`

**Trách nhiệm:** Infrastructure client dùng chung, tránh đặt business trong HTTP wrapper.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`http/`](http/README.md) — Typed HTTP transport, envelope/error handling và auth headers.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
