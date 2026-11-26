# `env.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/migrations/env.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 1119 bytes; **SHA-256:** `283ce57b819559221484ce9110ac8cee9b8219ffa0f5d9976ac867d690d2ec4c`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Schema/migration/query liên quan tầng dữ liệu; xem quyền truy cập và transaction.

## Symbol / khai báo phát hiện

- `FunctionDef run_migrations_offline`
- `FunctionDef run_migrations_online`

## Import / phụ thuộc được phát hiện

- `alembic`
- `omnicore_api.core.config`
- `omnicore_api.core.database`
- `omnicore_api.core.models`

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
