# `pyproject.toml` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `pyproject.toml`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 339 bytes; **SHA-256:** `9c363f4fdc23cde3a262432f046f93279a99b4a8b0542e171881d0e224ee6d04`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Manifest khai báo project/dependency/build tooling.

## Symbol / khai báo phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Import / phụ thuộc được phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Quan hệ cần xác nhận

- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).
- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.
- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.

## Ghi chú kiểm tra

- Cấu hình tham khảo; dependency/service thực tế cần xác minh bằng call-chain.
<!-- AUTO_CONTEXT_END -->

## Ghi chú bổ sung có xác minh (do agent/người dùng điền)

- [ ] Đường gọi vào / điều kiện kích hoạt:
- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:
- [ ] DB / API / message contract và test evidence:
