# Mẫu đặc tả luồng xử lý dữ liệu theo thứ tự thực thi

Data Mapping là đặc tả thực thi, không phải bản tóm tắt SQL. Viết trước khi chốt Request/Response. Đánh số bước ổn định (DM-01, DM-02.1), mỗi bước có điều kiện vào, dữ liệu, chủ lớp, thao tác, nhánh thành công/thất bại và đích tiếp. Không nhét nhiều biến/cột/điều kiện vào một hàng. Mục không áp dụng ghi rõ lý do.

## 1. Nhận dữ liệu, xác thực và kiểm tra

1. Đọc từng header/path/query/body từ nguồn quy định; ghi mặc định và kiểu trước chuẩn hóa.
2. Xác thực, đọc từng claim được hợp đồng xác nhận; phân quyền vai trò và đối tượng theo chính sách. Không tự tin claim từ client. Không truy xuất dữ liệu bảo vệ trước guard.
3. Kiểm tra từng field: thiếu, rỗng, format, độ dài, enum, min/max, quan hệ trường. Với mỗi phép kiểm tra ghi biểu thức, giá trị lỗi, mã lỗi và bước dừng. Validator thuần không I/O; kiểm tra dựa DB ở view hoặc policy nhận bản ghi đã tải.

| Bước | Biến | Nguồn | Kiểu | Chuẩn hóa | Điều kiện | Lỗi |
|---|---|---|---|---|---|---|

## 2. Đọc dữ liệu

Một Query ID cho từng lệnh. Ghi bảng/view vật lý, alias, mục đích, cardinality, cột chọn, join, điều kiện, grouping, having, order, phân trang, bind, biến kết quả. Mỗi cột và điều kiện một dòng. Cột không xác định phải ghi gap, không tự đặt tên vật lý. Kiểm tra join 1-N gây nhân bản, `LEFT JOIN` bị biến thành `INNER JOIN` bởi điều kiện WHERE; count và list cùng filter, sắp xếp ổn định bằng tie-breaker. Phân biệt kết quả không có bản ghi, bản ghi không hợp lệ và lỗi truy vấn; danh sách rỗng không mặc định là 404.

| Query ID | Bảng/alias | Cột | Tên logic | Kiểu/null | Biến đích |
|---|---|---|---|---|---|

| Query ID | Bảng nối | Kiểu nối | Điều kiện nối | Cardinality |
|---|---|---|---|---|

| Query ID | Mệnh đề | Thứ tự | Điều kiện/cột | Nguồn tham số | Khi áp dụng |
|---|---|---|---|---|---|

| Query ID | Nhánh kết quả | Điều kiện | Bước tiếp | Mã lỗi |
|---|---|---|---|---|

Aggregate cần mô tả COUNT(*) hay COUNT(column), DISTINCT, null, nhóm và mẫu số; EXISTS không giả định số lượng. Dynamic filter chỉ ghép điều kiện tĩnh hoặc danh sách cho phép, bind giá trị; cột sort dùng allowlist. Pagination ghi đơn vị offset/cursor, công thức, max và snapshot. Không dùng nội suy đầu vào vào SQL.

## 3. Ghi dữ liệu

Mỗi Mutation ID cho một INSERT/UPDATE/DELETE/UPSERT/bulk, nêu điều kiện bản ghi, field, nguồn giá trị, default DB, audit, khóa, biến ID sinh ra, số hàng mong đợi và nhánh khi khác. Mỗi bảng × thao tác cần mapping riêng nếu khác field/điều kiện. UPDATE phân biệt trường không gửi với null; không ghi lại cột không thuộc phạm vi. INSERT trả ID do DB sinh theo schema; insert danh sách xác định thứ tự, quan hệ cha/con, giới hạn và toàn bộ hoặc từng phần. DELETE ghi xóa mềm/cứng, FK/cascade, history, trạng thái lặp. Bulk reorder nêu kiểm tra tập ID, trùng, thứ tự, khóa và hành vi thiếu phần tử. Upsert chỉ khi có unique key và semantics được duyệt; không biến check-then-insert thành bảo đảm an toàn đồng thời.

| Mutation ID | Bảng | Thao tác | Điều kiện bản ghi | Cột | Nguồn giá trị | Bước mapping | Số hàng kỳ vọng | Nhánh lỗi |
|---|---|---|---|---|---|---|---|---|

## 4. Giao dịch và ngoại hệ thống

Ghi bắt đầu ở đâu, isolation/lock nếu được xác nhận, thứ tự khóa nhất quán, các thao tác atomic, kiểm tra kết quả và dựng response, commit, rollback/close. Không mở giao dịch nếu không cần; không dùng transaction làm bằng chứng chống race khi chưa kiểm thử DB thật. API ngoài DB: timeout, mã lỗi, retry có giới hạn, khóa idempotency nếu hợp đồng quy định; không giữ lock qua mạng tùy tiện. Outbox chỉ khi thiết kế có cơ chế, event phát sau commit; ghi điều kiện bù trừ nếu gọi ngoài thất bại. Không tạo tác động giả để lấp thiết kế thiếu.

## 5. Trả kết quả

Ánh xạ từng cột/biến sang từng field response, vòng lặp và thứ tự mảng, kiểu, null/rỗng, biến đổi. Soát response mapping trước commit với mutation. Lỗi hệ thống được chuẩn hóa, log an toàn cùng trace ID khi có. Các lỗi phải link tệp Error. Không tự chọn HTTP 200/400/500 nếu nguồn dùng khác. Dọn kết nối/lock trong mọi nhánh.

## 6. Hai mẫu luồng

Đọc: nhận yêu cầu → guard nếu có → validate → query đếm/danh sách hoặc detail → phân nhánh → map → trả/giải phóng. Ghi: nhận yêu cầu → guard → validate → bắt đầu transaction → tải/khóa → kiểm tra trạng thái → update/insert/delete → kiểm tra row count → map → commit → trả; lỗi rollback, không ghi thành công giả. Đây là mẫu thứ tự, không phải contract nghiệp vụ.
