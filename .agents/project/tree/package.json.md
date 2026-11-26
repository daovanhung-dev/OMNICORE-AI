# `package.json` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `package.json`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 251 bytes; **SHA-256:** `5a751cc9382d64d3e35681e90ca69c5561d145858278974e4a0f20381463f498`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Manifest khai báo project/dependency/build tooling.

## Symbol / khai báo phát hiện

- `script web:start`
- `script web:build`
- `script web:test`

## Import / phụ thuộc được phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Quan hệ cần xác nhận

- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).
- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.
- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.

## Ghi chú kiểm tra

- Chỉ xuất tên dependency/script; không sao chép giá trị cấu hình.
<!-- AUTO_CONTEXT_END -->

## Ghi chú bổ sung có xác minh (do agent/người dùng điền)

- [ ] Đường gọi vào / điều kiện kích hoạt:
- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:
- [ ] DB / API / message contract và test evidence:
