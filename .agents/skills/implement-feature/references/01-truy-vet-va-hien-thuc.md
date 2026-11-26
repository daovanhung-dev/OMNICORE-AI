# Quy trình lập trình theo bằng chứng

Trước khi sửa, đọc danh mục API/screen, DD, schema, contract, source và test; ghi scope và nguồn. Với màn hình đọc cả 8 file DD, clean/numbered, ảnh/HTML/marker và đối chiếu thực tế. Phân tách kỳ vọng và hiện trạng; ghi chênh lệch, nguồn thiếu, tác động. Kế hoạch mỗi mục tiêu lá có file, symbol, hành động, test và bằng chứng. Tìm helper/component hiện có trước khi tạo mới.

| Yêu cầu/ID | Hành vi | Điểm vào | Caller → callee | Dữ liệu/side effect | Chủ lớp | File sửa | Test | Chặn |
|---|---|---|---|---|---|---|---|---|

## Backend

- models: khai báo DTO/kiểu/default và conversion thuần; không validation runtime hoặc DB. validate: kiểm tra/chuẩn hóa đầu vào, trả lỗi bằng builder chung hoặc kết quả lỗi có kiểu; không I/O. query: SQL constant hoặc khai báo ORM theo profile, không parameter binding/execute/commit. view: gọi guard/validator, bind và execute, kiểm tra dựa bản ghi, transaction, mapping và response; router chỉ đăng ký tuyến/DI. Quy tắc dự án đã duyệt quyết định ngoại lệ tệp không áp dụng; không tạo query giả nếu không có DB.
- Truy từ endpoint đến router/view, guard, validator, DB/provider, map, error, caller FE. Xác thực trước truy xuất bảo vệ. Mọi lỗi đầu vào chặn DB write; DB-backed rule ở view hoặc hàm thuần nhận dữ liệu đã đọc. Kiểm tra biến bind khớp SQL, schema và count/list cùng filter. Mutation kiểm tra số hàng, khóa và invariant, map trước commit, rollback khi lỗi, giải phóng. Dùng comment tiếng Việt cho bước có ý nghĩa; API-facing handler có mô tả ngắn trước hàm nếu convention yêu cầu. Không áp dụng máy móc cấm ValueError của một framework lên dự án khác.
- Test import composition root; sửa một lỗi import chưa đủ chứng minh app chạy. Test focused rồi suite scope, route wiring/OpenAPI, lint/type. Fake session không chứng minh SQL chạy trên DB thật.

## Frontend

- Screen có `data-access`, `models`, `pages`, `ui`; không tạo thư mục thứ năm. `pages` sở hữu state và orchestration; `ui` trình bày/phát event; `data-access` gọi API; `models` ánh xạ thuần. Tìm shared UI trước. Group route/layout theo profile, root chỉ chứa khung và outlet đúng. Kiểm tra root và URL đích mở trực tiếp, guard thật và không có scaffold dư; không tự thêm wildcard/redirect.
- Map mỗi event đến state, guard, API/payload, kết quả, lỗi, navigation và test. Kiểm soát request cũ, double submit, retry theo contract. Nếu DD bị chặn chỉ hiện thực phần độc lập; không giả API để báo đã nối.
- Demo browser local, kích hoạt từng event, keyboard/responsive theo DD. Dữ liệu demo chỉ trong DB cô lập được xác nhận; ghi ID từng fixture, xóa đúng ID theo FK và query lại xác minh; không truncate hoặc dùng DB production. Không chứng minh UI từ build/server start.

## Bàn giao

Chạy validator kiến trúc, focused test, kiểm thử liên quan; ghi command, exit code, môi trường và giới hạn. Trace thay đổi contract đến consumer, không sửa scope khác không cần thiết. Cập nhật DD/context khi quyết định thay đổi đã được duyệt, ghi discrepancy chưa xử lý. Không tự chạy review chỉ đọc như task độc lập nếu chưa được yêu cầu.
