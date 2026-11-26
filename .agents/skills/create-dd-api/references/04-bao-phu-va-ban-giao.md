# Cổng rà soát và bàn giao DD API

## Từng tệp bắt buộc

| Tệp | Nội dung nghiệm thu |
|---|---|
| 00-cover | ID, tên, module, version, chủ, trạng thái thiết kế, source và ngày |
| 01-history | phiên bản, thay đổi, nguồn quyết định, ảnh hưởng; không bịa người duyệt |
| 02-overview | mục đích, actor, method/path, quyền, bảng đọc/ghi, use case, sơ đồ và giới hạn |
| 03-request | từng field, kiểu/nguồn/vị trí, yêu cầu, chuẩn hóa, validate, JSON |
| 04-response | từng field và nguồn, null/rỗng, HTTP/mã nghiệp vụ, ví dụ hợp lệ |
| 05-data-mapping | bước thực thi, nhánh, query, mutation, transaction, map, lỗi |
| 06-errors | điều kiện, HTTP/mã nghiệp vụ, phản hồi, thứ tự, tác động, test |
| 07-db-mapping và các file thêm | mỗi bảng/thao tác, từng cột, kiểu, nguồn, điều kiện, khóa, link bước; API chỉ đọc ghi không áp dụng |

## Kiểm tra hai chiều

Request ↔ DM: mỗi field có nơi sử dụng và mọi tham số xuất phát từ nguồn. DM ↔ schema: bảng/cột/kiểu/key/constraint/alias đúng; từng condition có nguồn; các query không ghi thiếu join/limit. DM ↔ response: mỗi output có nguồn, mọi nhánh trả đúng envelope. DM ↔ lỗi: từng nhánh và mã lỗi có liên kết, không có lỗi mồ côi. Mutation ↔ DB mapping: từng cột ghi có đúng file mapping và bước; cả chiều ngược. Mỗi field, cột, điều kiện, biến, JSON property, lỗi một dòng/hàng.

## Cổng cuối

1. Kiểm kê nguồn và mẫu, fingerprint, bảng yêu cầu đầy đủ.
2. Bốn ma trận đối chiếu đã viết trước nội dung; không có gap ảnh hưởng phần tuyên bố sẵn sàng.
3. Markdown: UTF-8, tên tệp và heading đúng mẫu, bảng đúng cột, code fence đóng, JSON hợp lệ, link/anchor tồn tại, không placeholder không giải thích.
4. Kiểm tra query, map, error, transaction, quyền, bảo mật; xác minh source/runtime riêng.
5. Báo cáo từng API: đã đủ thiết kế hay bị chặn, nguồn/chênh lệch, kết quả lệnh kiểm tra, phạm vi chưa xác minh. Quyết định thiết kế do người có thẩm quyền, không dùng kết quả validator làm phê duyệt.

Tệp báo cáo theo hợp đồng dự án: `PLAN_RESULT.md` (API, thư mục, trạng thái, các cổng, nguồn); `BUSINESS_CODE_DELTA.md` (mã thêm/đổi/bỏ, lý do, consumer, phê duyệt); `OPEN_QUESTIONS.md` (mã, vấn đề, tác động, chủ quyết định, điều kiện gỡ); báo cáo kiểm định (lệnh, phiên bản, kết quả, giới hạn). Không bắt buộc ZIP nếu dự án yêu cầu thư mục Markdown. Không trộn log nguồn với nội dung hợp đồng.
