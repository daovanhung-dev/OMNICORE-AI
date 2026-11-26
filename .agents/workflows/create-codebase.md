# Quy trình tạo nền mã nguồn

Đầu vào: kho mã đích, phạm vi và công nghệ đã duyệt. Đầu ra: nền chạy được trong môi trường xác minh, hợp đồng, kiểm thử và hồ sơ nguồn.

Tiền kiểm → cây thư mục → hợp đồng từng tệp/lớp/hàm → kế hoạch mục tiêu lá → khởi tạo bản địa → cấu hình và nền BE/FE → lát cắt API/màn hình → kiểm thử → hồ sơ → nghiệm thu. Nạp `../skills/create-codebase/SKILL.md`; kiểm tra tệp hiện hữu trước khi sinh, không ghi đè. Tạo phụ thuộc từ thấp đến cao; không đưa nghiệp vụ chưa duyệt vào mẫu. Ghi kết quả build/test, không báo đạt khi bị chặn. Kiểm kê và kiểm định ngữ cảnh sau khi thay đổi.

Cổng sinh nền tái lập: dùng `tools/create-codebase.py` cho hồ sơ đã hỗ trợ, sau đó kiểm tra `validators/validate_architecture.py`, biên dịch và chạy kiểm thử. Nếu đích đã có mã, không chạy bộ sinh đè; lập kế hoạch tích hợp từng tệp.
