# `main.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/main.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 1111 bytes; **SHA-256:** `3d3d0a9bf9b9c2db2ffecc919e8d3d949c1c1c0af25cb6ac57e360c97d2d785c`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên entrypoint; cần kiểm chứng qua script/bootstrap thực tế.

## Symbol / khai báo phát hiện

- `FunctionDef create_app`
- `AsyncFunctionDef create_app.lifespan`

## Import / phụ thuộc được phát hiện

- `collections.abc`
- `contextlib`
- `fastapi`
- `omnicore_api.api.health`
- `omnicore_api.api.v1`
- `omnicore_api.core.config`
- `omnicore_api.core.database`

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
