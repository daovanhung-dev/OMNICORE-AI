# `main.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/ai-api/omnicore_ai_api/main.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 219 bytes; **SHA-256:** `1aefd0a903f84b46ff08637cb145b08616b86149c7a84195d68d0ea3948f6b12`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên entrypoint; cần kiểm chứng qua script/bootstrap thực tế.

## Symbol / khai báo phát hiện

- `FunctionDef health_live`

## Import / phụ thuộc được phát hiện

- `fastapi`

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
