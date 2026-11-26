# Folder mẫu: `apps/server/app/`

**Trách nhiệm:** Python application package; composition, inbound/outbound layers và domain module.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`api/`](api/README.md) — API router/version composition; mapping route phải có chứng cứ từ source.
- [`core/`](core/README.md) — Cấu hình, database, bảo mật và các cross-cutting concerns.
- [`modules/`](modules/README.md) — Các domain bounded contexts; moduleN chỉ là placeholder.
- [`service/`](service/README.md) — Adapters outbound tới provider; dependency injection và failure handling.
- [`utils/`](utils/README.md) — Helper dùng chung; không cho business logic vượt layer.

## File và tài liệu 1:1

- [`main.py`](main.md) — **Composition root**: Tạo application, lắp middleware/exception handler, đăng ký API router; cấp vòng đời tài nguyên.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
