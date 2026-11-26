# Quy trình kiểm thử và xác minh

1. Đọc yêu cầu/DD, nguồn, hợp đồng, lệnh kiểm thử thực tế, môi trường và baseline. Ma trận theo yêu cầu: điều kiện, dữ liệu, bước, kết quả/ảnh hưởng, mức kiểm thử, rủi ro, dọn dữ liệu.
2. Phân tầng kiểm thử thuần, component/HTTP, hợp đồng, DB/dịch vụ, trình duyệt/thiết bị và smoke triển khai. Ưu tiên quyền, dữ liệu, trạng thái lỗi, biên, xung đột, đồng thời, retry và rollback có căn cứ.
3. Dùng fixture cô lập; kiểm tra đích DB trước ghi, lưu ID, xóa đúng ID và xác minh. Không seed production/shared DB. Bộ giả lập chứng minh hành vi lớp được cô lập, không chứng minh SQL, mạng hoặc triển khai.
4. Chạy ca tập trung, bộ kiểm thử liên quan và kiểm tra build/lint/kiểu/hợp đồng theo cấu hình. Lưu lệnh, mã thoát, kết quả, số lượng và môi trường. Không thay đổi hành vi để ép ca sai thành đạt.
5. Ghi ca không chạy/không thể chạy và lý do; cập nhật hồ sơ nếu có thay đổi nguồn/test, nhật ký và tiêu chí nghiệm thu. Kết quả kế hoạch khác kết quả thực thi.
