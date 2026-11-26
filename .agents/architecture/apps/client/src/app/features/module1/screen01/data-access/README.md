# Folder mẫu: `apps/client/src/app/features/module1/screen01/data-access/`

**Trách nhiệm:** Feature-owned API caller, không render UI.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`screen01.service.ts`](screen01.service.ts.md) — **Feature data-access**: Gọi đúng endpoint contract thông qua core HTTP; map DTO/errors, không thực hiện DOM logic.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
