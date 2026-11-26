# `health.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/api/health.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 989 bytes; **SHA-256:** `41750f27684df7f617c8b2fc089ca2b8c37ff917e300136d38ce8a835e38d576`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên code thực thi; xác minh imports/callers và wiring.

## Symbol / khai báo phát hiện

- `FunctionDef health_live`
- `FunctionDef health_ready`

## Import / phụ thuộc được phát hiện

- `fastapi`
- `fastapi.responses`
- `sqlalchemy`
- `sqlalchemy.exc`

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
