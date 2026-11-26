# `docker-compose.yml` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `docker-compose.yml`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 1369 bytes; **SHA-256:** `2d65933f233148474f20f131ddd4d7799a49cf19fc1db53e1c0a479626be8880`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Chưa xác định từ tên; phải mở source/metadata khi task liên quan.

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
