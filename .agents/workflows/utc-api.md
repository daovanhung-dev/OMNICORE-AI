# Quy trình tạo ma trận kiểm thử API
Đọc DD và nguồn; tách ca dự kiến khỏi ca đã chạy. Truy vết từng request, response, mã lỗi, quyền, giao dịch, rollback và ràng buộc dữ liệu; phân lớp đơn vị/tích hợp. Mỗi ca có ID, điều kiện, dữ liệu, bước, kết quả mong muốn và bằng chứng. Không gọi API thật khi nhiệm vụ chỉ tạo UTC. Không ghi trạng thái đạt cho ca chưa chạy.
