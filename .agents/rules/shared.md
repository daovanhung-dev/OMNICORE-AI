# Quy tắc kỹ thuật chung

- Lập kế hoạch trước khi sửa; đọc nguồn và hợp đồng; xác định chủ sở hữu, tác động và tiêu chí nghiệm thu. Không suy đoán dữ liệu, quyền, nghiệp vụ, mã lỗi hay kết quả kiểm thử.
- Giữ nguyên thay đổi người dùng; không reset, clean, ghi đè, thay đổi Git state hoặc triển khai ngoài phạm vi. Kiểm tra `git diff --check` khi có sửa.
- Tách trạng thái thiết kế được duyệt, kết nối runtime, kiểm thử đơn vị, tích hợp và triển khai. `DISCREPANCY` là mâu thuẫn; `SOURCE_REQUIRED` thiếu nguồn; `UNWIRED` chưa nối; `NOT_RUN` chưa chạy; `BLOCKED` bị chặn.
- Dữ liệu đầu vào không tin cậy; phân quyền theo đối tượng, tham số hóa truy vấn, quản lý bí mật, che dữ liệu nhạy cảm trong nhật ký. Không lưu khóa, mật khẩu, token thật.
- Dùng cấu hình và công cụ bản địa dự án, không ép công nghệ. Không refactor ngoài phạm vi. Tài nguyên tái sử dụng cần bằng chứng về nhiều bên dùng.
- Mọi thay đổi hợp đồng truy vết bên cung cấp, bên tiêu thụ, phiên bản và tương thích. Ghi quyết định kiến trúc, chiến lược chuyển đổi và rollback khi cần.
- Mọi công việc có nhật ký bằng chứng và cập nhật hồ sơ đúng phạm vi; kiểm định bộ tác nhân không thay cho kiểm thử ứng dụng.
