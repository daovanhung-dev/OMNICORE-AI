# Ánh xạ dữ liệu
1. Đọc query và mặc định.
2. `validate_params` kiểm tra kiểu, khoảng; sai trả INVALID_PAGE trước DB.
3. Mở kết nối chỉ đọc và bắt đầu giao dịch.
4. COUNT_ITEMS: đếm toàn bộ bảng.
5. LIST_ITEMS: ORDER BY id; LIMIT = page_size; OFFSET = (page − 1) × page_size; bind hai tham số.
6. Ánh xạ từng hàng thành Item và đóng gói ItemPage.
7. Đóng kết nối trong mọi nhánh. Lỗi SQLite trả DATA_UNAVAILABLE, không lộ chi tiết driver.
