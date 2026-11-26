# Folder mẫu: `apps/client/src/app/features/module1/screen01/`

**Trách nhiệm:** **Một** screen mẫu; liên kết page, model, data-access, UI và test.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`data-access/`](data-access/README.md) — Feature-owned API caller, không render UI.
- [`models/`](models/README.md) — Model/ViewModel và mapper thuộc screen.
- [`pages/`](pages/README.md) — Route-level page gồm component source, HTML và CSS minh họa.
- [`ui/`](ui/README.md) — Các widget local chỉ được screen dùng.

## File và tài liệu 1:1

- [`screen01.spec.ts`](screen01.spec.ts.md) — **Screen tests**: Kiểm tra route/render, event, validation, loading/empty/error, disabled state, accessibility.

## Luồng xử lý minh họa Screen01

`app.routes.ts → screen01-page.ts (+ HTML/CSS) → screen01.service.ts → api-client.service.ts → server/api01 → screen01.model.ts → render`

Quản lý `loading/success/empty/error`, validation, unauthorized, retry và accessibility tùy requirement.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
