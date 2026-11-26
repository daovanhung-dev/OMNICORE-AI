# `README.md` — source context

<!-- AUTO_CONTEXT_START -->
**Source:** `apps/api/migrations/README.md`
**Evidence:** `SOURCE_INSPECTED_STATIC`; **Size:** 286 bytes; **SHA-256:** `37313baf99083ceed819618a1565a5e91ed74f84ca1f2a751f40daa134558e92`

## Tóm tắt chức năng (chỉ dựa vào bằng chứng đã đọc)

Schema/migration/query liên quan tầng dữ liệu; xem quyền truy cập và transaction.

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
