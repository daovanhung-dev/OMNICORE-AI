# Điều phối mục tiêu, nhật ký và an toàn

`target.md` là nguồn duy nhất về tiến độ đang hoạt động. Bảng có đúng ba cột `STT | Tên target | Tiến độ hoàn thiện`. Mỗi hàng là một thao tác nhỏ nhất có thể nghiệm thu độc lập, tên tiếng Việt theo dạng hành động + kết quả. Không có hàng cha hoặc mục tiêu bao trùm. Bắt đầu 0%; chỉ thay đổi khi có chứng cứ; giữ nguyên phần đã xác minh khi bị chặn. Khi đạt 100%, ghi chứng cứ vào nhật ký trước khi xóa hàng. Không giữ lịch sử trong bảng.

Nhật ký chứa `READ_PLAN`, `LEAF_TARGET_PLAN`, `PRIOR_WORKLOG_REVIEW`, `TARGET_UPDATES`, nguồn hành vi mong muốn, hiện trạng, mâu thuẫn, thao tác, kiểm thử, trở ngại. Kế hoạch đọc phải ghi đường dẫn và lý do trước khi đọc nội dung; tìm kiếm giới hạn trong đường dẫn đó. Công cụ chọn nhật ký chỉ trả siêu dữ liệu, không tự đọc nội dung.

Không tạo báo cáo tiến độ lặp lại ngoài bảng nếu người dùng không yêu cầu; quy định cấp cao hơn, an toàn và yêu cầu báo cáo rõ ràng luôn được ưu tiên. Không che giấu trở ngại. Không chạy lệnh phá hủy, thay đổi quyền, triển khai hoặc ghi dữ liệu thật ngoài phạm vi cho phép.
