# `config.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/core/config.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 415 bytes; **SHA-256:** `daf01f871ea42fa99a2db08cab4d55d4fa8999d28615c552dcb6663a2e6be371`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Thành phần dùng chung/hạ tầng; xác minh phạm vi tái sử dụng.

## Symbol / khai báo phát hiện

- `ClassDef Settings`
- `FunctionDef get_settings`

## Import / phụ thuộc được phát hiện

- `pydantic`
- `pydantic_settings`

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
