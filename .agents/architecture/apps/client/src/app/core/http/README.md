# Folder mẫu: `apps/client/src/app/core/http/`

**Trách nhiệm:** Typed HTTP transport, envelope/error handling và auth headers.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`api-client.service.ts`](api-client.service.ts.md) — **HTTP transport**: HTTP client typed baseURL, headers, auth injection, parse envelope/errors, cancellation/timeouts.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
