# Tổng quan
Trả danh sách phân trang ổn định theo ID. Nguồn dữ liệu: bảng `items`; không ghi dữ liệu. Hai truy vấn chạy trong cùng giao dịch đọc.

Chế độ công khai mặc định. Tùy chọn protected_items yêu cầu Bearer JWT hợp lệ và role reader trước khi đọc DB; không tự tạo endpoint đăng nhập.
