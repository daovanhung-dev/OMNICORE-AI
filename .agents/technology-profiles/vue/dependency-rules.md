# Chiều phụ thuộc
Core và UI dùng chung không nhập module nghiệp vụ. Trang điều phối data-access, models, UI; UI không gọi HTTP. Máy chủ view điều phối validate/models/query, query không quản lý giao dịch. Áp dụng phần phù hợp với loại ứng dụng.
