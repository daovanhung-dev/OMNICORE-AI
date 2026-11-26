# Quy trình tạo và cập nhật thiết kế chi tiết

Chọn năng lực DD API, DD màn hình hoặc DD module theo phạm vi. Không dùng DD thay cho mã chạy.

1. Xác định ID, chủ sở hữu, đối tượng, vai trò, luồng, nguồn BD/BRD/AC, phiên bản, DD liên quan, lược đồ, API, ảnh và mã nguồn. Ghi thiếu nguồn/mâu thuẫn, chủ quyết định, tác động.
2. Đọc bộ mẫu hiện hành đầy đủ; ưu tiên mẫu đã duyệt của dự án. Lập ma trận truy vết yêu cầu và trạng thái từng nguồn; tách hành vi mong muốn và hiện trạng.
3. Tạo gói bằng năng lực tương ứng; điền từng tệp theo hợp đồng. API: request/response/mapping/lỗi/DB/giao dịch. Màn hình: thành phần/sự kiện/dữ liệu/API/điều hướng/test. Module: feature/function/view/import/sơ đồ/tài nguyên/lịch sử.
4. Kiểm tra tham chiếu hai chiều, nguồn từng trường/điều kiện, quyền, lỗi, dữ liệu, ca kiểm thử và độ bao phủ. Không tự điền phần chưa có nguồn. Duy trì các trục phê duyệt thiết kế, triển khai và xác minh riêng.
5. Dùng `agentkit.py validate-dd` với loại và đường dẫn gói; kiểm tra chặt khi bàn giao thiết kế đã sẵn sàng. Ghi quyết định còn mở, tệp, kết quả và nhật ký. Chỉ chuyển lập trình khi hành vi thuộc phạm vi đã được duyệt.
