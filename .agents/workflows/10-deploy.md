# Quy trình triển khai

Xác nhận quyền triển khai, môi trường, ảnh hưởng, thời gian bảo trì nếu cần, sao lưu và phương án khôi phục. Đọc hạ tầng, CI/CD, cách cấp bí mật, migration, cổng/tuyến, health và trạng thái hiện tại. Kiểm tra build/phụ thuộc, đích kết nối, quyền và backup trước thao tác. Không thay firewall hoặc DB phá hủy ngoài phạm vi phê duyệt. Chỉ thực hiện bước được phép; xác minh readiness, log đã che bí mật, kết nối, quyền và hành vi thật. Khôi phục theo phương án đã kiểm tra nếu cần; ghi lệnh, kết quả, trạng thái triển khai và trở ngại riêng với kiểm thử local.
