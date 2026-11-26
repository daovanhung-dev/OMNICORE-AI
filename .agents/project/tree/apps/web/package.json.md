# `package.json` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/web/package.json`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 779 bytes; **SHA-256:** `77213708d496056d15853310eeca5ebf0514c7b1264ecec684ca8d1af32c474e`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Manifest khai báo project/dependency/build tooling.

## Symbol / khai báo phát hiện

- `script ng`
- `script start`
- `script build`
- `script watch`
- `script test`

## Import / phụ thuộc được phát hiện

- `dependency @angular/common`
- `dependency @angular/compiler`
- `dependency @angular/core`
- `dependency @angular/forms`
- `dependency @angular/platform-browser`
- `dependency @angular/router`
- `dependency rxjs`
- `dependency tslib`

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
