# Folder mẫu: `apps/server/app/api/`

**Trách nhiệm:** API router/version composition; mapping route phải có chứng cứ từ source.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`v1.py`](v1.md) — **HTTP router aggregator**: Định nghĩa version/prefix, mount route api01 bằng handler từ view; ánh xạ method/path nếu contract đã được duyệt.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
