# Quy trình đồng bộ ngữ cảnh

Ghi nhánh/Git và phạm vi. Chạy `python3 .agents/workflows/tools/build-context.py --refresh`, kiểm tra tệp thêm/đổi/xóa; bảo toàn ghi chú thủ công. Chạy `python3 .agents/codebase/inventory.py --repo .`; đọc từng biểu tượng thay đổi, cập nhật điểm gọi, hợp đồng, DB, quyền và test; không đánh dấu đã đọc từ kiểm kê tĩnh. Cập nhật trang tổng quát khi kiến trúc/phụ thuộc thay đổi. Chạy `build-context.py --check` và `python3 .agents/tools/validate-kit.py`; ghi drift, tệp chưa đọc, test chưa chạy và chứng cứ vào nhật ký.
