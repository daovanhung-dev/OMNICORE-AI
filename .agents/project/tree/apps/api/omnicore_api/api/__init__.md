# `__init__.py` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/omnicore_api/api/__init__.py`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 41 bytes; **SHA-256:** `2f54575006512c073bfc83e9c329634238012437c0c75e9cc8aed7d515db08eb`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên code thực thi; xác minh imports/callers và wiring.

## Symbol / khai báo phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Import / phụ thuộc được phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

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
