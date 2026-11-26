# Folder mẫu: `apps/client/src/app/layouts/`

**Trách nhiệm:** Route shell và chrome dùng chung.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`main-layout.ts`](main-layout.ts.md) — **App shell**: Layout cấp ứng dụng, navigation/outlet, chrome; không truy vấn dữ liệu của screen cụ thể.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
