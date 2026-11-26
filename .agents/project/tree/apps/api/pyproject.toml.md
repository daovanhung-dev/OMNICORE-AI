# `pyproject.toml` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/pyproject.toml`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 580 bytes; **SHA-256:** `54f1e03d65cf54adcc0c3782e5dc0e4721995fb4ba1d8ed5f849fcef473413db`

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
