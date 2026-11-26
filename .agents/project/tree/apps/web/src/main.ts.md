# `main.ts` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/web/src/main.ts`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 222 bytes; **SHA-256:** `2341253f1a947c37dfa27838951cf7e224f7abb32dff45a8d425f042b5eeed13`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Ứng viên entrypoint; cần kiểm chứng qua script/bootstrap thực tế.

## Symbol / khai báo phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Import / phụ thuộc được phát hiện

- Không phát hiện bằng phân tích tĩnh; cần đọc source khi thực thi.

## Quan hệ cần xác nhận

- Caller và route registration: **CHƯA XÁC MINH** (mở router/entrypoint và test liên quan).
- Contract/DB/provider, authz, side effects: **CHƯA XÁC MINH** nếu chưa có bằng chứng runtime.
- Test liên quan: tìm file test, đối chiếu assertions, không coi file tồn tại là test PASS.

## Ghi chú kiểm tra

- Trạng thái bộ phân tích: PARSER_UNAVAILABLE; không chứng minh hành vi runtime.
<!-- AUTO_CONTEXT_END -->

## Ghi chú bổ sung có xác minh (do agent/người dùng điền)

- [ ] Đường gọi vào / điều kiện kích hoạt:
- [ ] Luồng xử lý, trạng thái lỗi, auth/permission:
- [ ] DB / API / message contract và test evidence:
