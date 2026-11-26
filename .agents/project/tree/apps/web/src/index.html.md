# `index.html` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/web/src/index.html`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 297 bytes; **SHA-256:** `949bb6d4c834ee1d99f3621e73b5fc28a25cb637198b84c705be5a58c8b583cc`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Giao diện/tạo kiểu; cần đối chiếu component sở hữu.

## Symbol / khai báo phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Import / phụ thuộc được phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Quan hệ cần xác nhận

- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).
- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.
- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.

## Ghi chú kiểm tra

- Tránh suy luận nghiệp vụ hoặc chức năng chỉ từ tên file.
<!-- AUTO_CONTEXT_END -->

## Ghi chú bổ sung có xác minh (do agent/người dùng điền)

- [ ] Đường gọi vào / điều kiện kích hoạt:
- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:
- [ ] DB / API / message contract và test evidence:
