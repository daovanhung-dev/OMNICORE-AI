# Phân tích trọn gói màn hình

Đọc danh mục screen và endpoint, chọn ID/route/actor, module, viewport, version và owner. Mở toàn bộ tám tệp DD, ảnh clean/numbered, README ảnh, HTML thiết kế và marker JSON nếu có. Đọc router, pages, UI, services, models, guard, design tokens, shared UI, contract và test liên quan. Ảnh/prototype chỉ mô tả mục tiêu, không chứng minh runtime. Ảnh thiếu/trắng hoặc không cùng bố cục: ghi chênh lệch; không gán marker tưởng tượng. Nếu nhiều màn hình, lập scope từng screen/API; không đọc lan ngoài phụ thuộc.

| Mã nguồn | Tệp | Phiên bản | Mục/marker | Trạng thái | Bằng chứng | Chênh lệch |
|---|---|---|---|---|---|---|

ID: lấy danh mục đã duyệt, giữ nguyên ID nguồn; nếu thiếu có thể dùng ID nội bộ có mapping. Element `SCREEN-EL-001`, event `SCREEN-EV-001`, rule `SCREEN-BR-001`, test `SCREEN-TC-001`; API use ID liên kết catalog API chung, không tạo endpoint mới. Đánh marker từ trái sang phải, trên xuống dưới theo bố cục; nhóm thành phần lặp nếu hành vi giống nhau. Thành phần ẩn có điều kiện ghi rõ không có marker ở ảnh hiện tại. Không ghi dữ liệu cá nhân hoặc token trong ảnh.

## Chủ sở hữu thông tin

| Tệp | Nguồn duy nhất trong DD |
|---|---|
| 00-overview | mục tiêu, actor, phạm vi, nguồn, trạng thái |
| 01-ui-elements | marker, loại, binding, visibility, enable, event |
| 02-events | trigger, điều kiện, từng bước, nhánh, tác động |
| 03-data-flow | state, DTO/ViewModel, nguồn, cache, mapping |
| 04-api-integration | API ID, method/path, request/response, quyền, lỗi |
| 05-business-rules | rule, điều kiện, nơi thi hành FE/BE, ưu tiên |
| 06-navigation | entry/exit, param, guard, back/deep link |
| 07-test-cases | kỳ vọng kiểm thử và trace |

Viết overview → UI → rule → API → data → event → navigation → test; không viết event trước khi khóa contract/rule. Mọi tham chiếu liên kết về nguồn duy nhất, không lặp định nghĩa mâu thuẫn.
