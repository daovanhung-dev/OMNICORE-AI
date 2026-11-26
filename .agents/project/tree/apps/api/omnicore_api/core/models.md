# `models.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/core/models.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 154 bytes; **SHA-256:** `be7a6361d1ecd1d26057ea91fe8cbb4da31c6c4c3c79dc5606d3bee3015d71a9`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên định nghĩa DTO/schema/domain model.

## Symbol / khai báo phát hiện

- `ClassDef Base`

## Import / phụ thuộc được phát hiện

- `sqlalchemy.orm`

## Quan hệ cần xác nhận

- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).
- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.
- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.

## Ghi chú kiểm tra

- Python AST được phân tích tĩnh; import không chứng minh đường chạy runtime.
<!-- AUTO_CONTEXT_END -->

## Ghi chú bổ sung có xác minh (do agent/người dùng điền)

- [ ] Đường gọi vào / điều kiện kích hoạt:
- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:
- [ ] DB / API / message contract và test evidence:
