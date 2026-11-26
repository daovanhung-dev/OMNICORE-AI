# Quy chuẩn ánh xạ chi tiết và cổng nguồn

## Tiếp nhận nguồn
Kiểm kê từng tài liệu đầu vào, phiên bản, chủ sở hữu, định dạng và trạng thái; tệp nén kiểm tra cây và đường dẫn an toàn trước giải nén. Đọc tất cả tệp có liên quan; ảnh và sơ đồ phải xem trực quan; bảng tính đọc từng sheet cần thiết. Lập báo cáo nguồn đã đọc, không đọc được và phần bị chặn. Mỗi khẳng định về hành vi có nguồn trực tiếp hoặc trạng thái suy dẫn/chờ duyệt.

## Bốn ma trận trước khi viết

| Ma trận | Cột bắt buộc |
|---|---|
| Sử dụng yêu cầu | Trường, kiểu, nguồn, bắt buộc, bước nhận, bước kiểm tra, bước truy vấn/ghi, phản hồi |
| Truy vấn | ID truy vấn, mục đích, bảng, alias, cột, JOIN, WHERE, GROUP BY, HAVING, ORDER BY, giới hạn, kiểu tham số, nhánh không có kết quả |
| Thay đổi dữ liệu | ID bước, bảng, cột, thao tác, giá trị nguồn, khóa, điều kiện, thứ tự, giao dịch, xử lý lỗi, rollback |
| Nguồn phản hồi | Đường dẫn JSON, kiểu, null, nguồn trực tiếp/ngoài/tính toán, quy tắc chuyển đổi, trạng thái, bước mapping |

Một trường, một cột, một điều kiện hoặc một phép gán trên một dòng. Khi JOIN nhiều bảng, mỗi điều kiện nối có hàng riêng; khi danh sách lồng nhau, mỗi thuộc tính phần tử có hàng riêng. Không ghép nhiều biến hoặc nhánh lỗi vào một ô làm mất truy vết. SQL tham số hóa, điều kiện động có bảng giá trị hợp lệ; không suy diễn cột hoặc index không có trong schema.

## Thứ tự xử lý và ranh giới giao dịch
1. Xác định header/query/path/body có nguồn; decode token nếu hợp đồng yêu cầu; phân quyền trước dữ liệu được bảo vệ.
2. Kiểm tra bắt buộc, kiểu, độ dài, enum, định dạng, khoảng, liên trường. Mỗi điều kiện liên kết một mã lỗi và mức ưu tiên.
3. Kiểm tra tồn tại/trạng thái/ownership, ghi rõ dữ liệu đọc và nhánh khi thiếu. Với mutation, ghi điều kiện khóa/cạnh tranh nếu có căn cứ.
4. Với read-only, đếm và danh sách dùng cùng bộ lọc; order ổn định. Với mutation, chỉ định thứ tự INSERT/UPDATE/DELETE, FK, ID sinh, thao tác lặp, commit/rollback; tác động ngoài DB có chính sách bù riêng.
5. Ánh xạ mỗi trường phản hồi; xác minh trước commit nếu hợp đồng yêu cầu; trả đúng HTTP/business code. Không trả stack trace, token hay PII ngoài phạm vi.

## Cổng nghiệm thu
- Cổng nguồn: đủ nguồn để kết luận hành vi; thiếu template hợp lệ thì không tự tạo định dạng thay thế.
- Cổng template: bộ sheet Markdown được duyệt ưu tiên; không mất sheet, cột hoặc liên kết; N/A giải thích rõ.
- Cổng một dòng: các bảng và JSON mapping đủ đơn vị nhỏ nhất.
- Cổng mapping: request→validate→query/mutation→DB→response→error và chiều ngược lại; không cột mồ côi, không lỗi không có nhánh.
- Cổng kỹ thuật: link, Markdown, ID, schema, hợp đồng và kiểm thử; so sánh với runtime nếu đang mô tả hiện trạng.
- Cổng bàn giao: mỗi API một folder, báo cáo kết quả, delta mã nghiệp vụ, câu hỏi mở, evidence; không báo Approved hoặc đã chạy khi còn trở ngại.

Quy trình batch áp dụng từng API độc lập. Mâu thuẫn giữa sequence/schema/contract/source được ghi rõ; không tự hòa giải. API được suy dẫn phải có người phê duyệt trước khi triển khai.
