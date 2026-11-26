# `database.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/core/database.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 1337 bytes; **SHA-256:** `67227123e0681600eaaa2fadc939fb861f65dc57723f2a9d26e847d3016b1874`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Thành phần dùng chung/hạ tầng; xác minh phạm vi tái sử dụng.

## Symbol / khai báo phát hiện

- `FunctionDef build_engine`
- `FunctionDef build_session_factory`
- `FunctionDef get_db`

## Import / phụ thuộc được phát hiện

- `collections.abc`
- `fastapi`
- `sqlalchemy`
- `sqlalchemy.engine`
- `sqlalchemy.orm`
- `sqlalchemy.pool`
- `omnicore_api.core.config`

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
