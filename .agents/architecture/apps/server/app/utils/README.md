# Folder mẫu: `apps/server/app/utils/`

**Trách nhiệm:** Helper dùng chung; không cho business logic vượt layer.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`auth.py`](auth.md) — **Authorization helper**: Tập trung guard policy, scope/ownership/tenant, không phụ thuộc UI guard.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
