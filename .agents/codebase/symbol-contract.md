# Quy chuẩn đặc tả từng lớp, hàm và tệp

Mỗi thư mục mô tả mục tiêu, tệp sở hữu, phụ thuộc vào/ra, quy tắc đặt mã và kiểm thử. Mỗi tệp mô tả đường dẫn, nhiệm vụ, tệp gọi, tệp được gọi, cấu hình, giao dịch và quyền. Mỗi lớp có trách nhiệm, constructor, thuộc tính, bất biến, vòng đời, phương thức công khai/nội bộ. Mỗi hàm có chữ ký kiểu, ý nghĩa từng tham số, kết quả, lỗi, điều kiện trước/sau, tác động phụ, giao dịch, đồng thời, điểm gọi và test.

| Biểu tượng | Chữ ký | Đầu vào | Đầu ra/lỗi | Tác động | Điểm gọi | Kiểm thử | Chứng cứ dòng nguồn |
|---|---|---|---|---|---|---|---|

Mã không có nguồn hoặc hợp đồng được duyệt không được tự điền như sự thật. Kết quả AST và nhận diện cú pháp chỉ là kiểm kê tĩnh. Không đánh dấu VERIFIED nếu chưa đọc thân hàm; không đánh dấu kiểm thử đạt nếu chưa chạy.
