# Folder mẫu: `apps/client/src/app/`

**Trách nhiệm:** Client app composition, routes/core/features/layouts/shared UI.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`core/`](core/README.md) — Infrastructure client dùng chung, tránh đặt business trong HTTP wrapper.
- [`features/`](features/README.md) — Các bounded UI features theo ownership.
- [`layouts/`](layouts/README.md) — Route shell và chrome dùng chung.
- [`shared/`](shared/README.md) — UI/helpers trung lập giữa các features.

## File và tài liệu 1:1

- [`app.routes.ts`](app.routes.ts.md) — **Client route composition**: Map URL sang layout/screen; lazy loading và guard UX theo codebase thực.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
