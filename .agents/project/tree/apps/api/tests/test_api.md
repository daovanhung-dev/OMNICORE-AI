# `test_api.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/tests/test_api.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 3452 bytes; **SHA-256:** `ecd5e8213d018ac3ad36ee41ba0d5b53c10f29408042723c20b03a37be4b8686`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Test/fixture; kiểm chứng hành vi trong phạm vi tương ứng.

## Symbol / khai báo phát hiện

- `FunctionDef test_health_live_is_independent_of_database`
- `FunctionDef test_health_ready_executes_database_probe`
- `FunctionDef test_health_ready_returns_safe_503_when_database_probe_fails`
- `FunctionDef test_settings_mask_database_url_and_validate_timeout`
- `FunctionDef test_database_dependency_rolls_back_errors_and_always_closes`
- `ClassDef test_database_dependency_rolls_back_errors_and_always_closes.FakeSession`
- `FunctionDef test_database_dependency_rolls_back_errors_and_always_closes.FakeSession.rollback`
- `FunctionDef test_database_dependency_rolls_back_errors_and_always_closes.FakeSession.close`
- `FunctionDef test_alembic_is_configured_without_domain_migrations`

## Import / phụ thuộc được phát hiện

- `pathlib`
- `types`
- `unittest.mock`
- `pytest`
- `alembic.config`
- `alembic.script`
- `fastapi`
- `fastapi.testclient`
- `omnicore_api.core.config`
- `omnicore_api.core.database`
- `omnicore_api.core.models`
- `omnicore_api.main`
- `sqlalchemy.exc`
- `starlette.requests`

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
