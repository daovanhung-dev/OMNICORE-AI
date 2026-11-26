# Folder mẫu: `apps/server/tests/`

**Trách nhiệm:** Tập test có fixture an toàn và không kết nối production.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`test_api01.py`](test_api01.md) — **API regression tests**: Test happy, invalid input, unauthenticated, forbidden ownership, DB/provider failure, rollback; fixtures độc lập.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
