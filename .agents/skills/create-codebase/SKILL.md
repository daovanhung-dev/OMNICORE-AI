---
name: create-codebase
description: Tạo hoặc mở rộng nền mã nguồn theo hợp đồng kiến trúc đã duyệt, có kiểm thử và truy vết.
---
# Năng lực tạo nền mã nguồn

Kích hoạt khi tạo dự án mới, chuẩn hóa nền hiện có hoặc bổ sung thành phần dùng chung. Đầu vào: phạm vi, công nghệ, phiên bản, quản lý gói, mô hình triển khai, nguồn BD/DD/hợp đồng, chính sách dữ liệu và quyền. Chưa xác định công nghệ hoặc hợp đồng thì chỉ lập đặc tả, không tự chọn nghiệp vụ.

1. Kiểm kê kho mã, tệp cấu hình, build/test và Git; giữ mã hiện có. Nạp `codebase/INDEX.md`, BE/FE và quy tắc chung.
2. Lập cây nguồn theo lớp; mỗi thư mục/tệp/lớp/hàm có hợp đồng, phụ thuộc, lỗi, kiểm thử và điểm lắp ghép. Chọn thành phần thực sự cần thiết; ghi phần không áp dụng.
3. Dùng công cụ khởi tạo bản địa; khóa phụ thuộc; cấu hình mẫu chỉ chứa tên biến và giá trị không bí mật. Không ghi đè tệp hoặc tự cài dịch vụ ngoài nếu chưa được phép.
4. BE: khởi động/config → trace/lỗi → DB/session nếu có → xác thực nếu có → router → bộ thích nghi → một lát cắt API có kiểm thử.
5. FE: khởi động/router → cấu hình/HTTP/envelope → phiên nếu có → layout/tokens/shared UI → một lát cắt màn hình kết nối API được duyệt.
6. Kiểm tra import, build, kiểu, lint, unit, tích hợp cô lập và tuyến thực tế; kiểm tra không lộ bí mật. Ghi rõ phần chưa chạy.
7. Sinh kiểm kê và hồ sơ đối xứng, đọc từng biểu tượng thuộc phạm vi; cập nhật quyết định kiến trúc, nhật ký và mục tiêu lá. Chỉ nghiệm thu phần có đủ chứng cứ.

Đầu ra: mã nền, cấu hình, kiểm thử, hợp đồng, hồ sơ từng biểu tượng và kết quả xác minh. Không tuyên bố hoàn thành mọi nghiệp vụ chỉ từ nền khởi động được.

## Bộ sinh nền có thể tái lập

Sau khi hồ sơ `fastapi-typescript` được duyệt, chạy `python3 .agents/tools/create-codebase.py --destination <thu-muc-moi> --profile fastapi-typescript`. Công cụ từ chối đích đã tồn tại; không cài phụ thuộc; không tạo nghiệp vụ thật. Kiểm tra nền bằng `validators/validate_architecture.py`, pytest, tsc, kiểm thử trình duyệt; xem `reference/README.md` và `technology-profiles/INDEX.md`. Nếu công nghệ khác, chỉ lập đặc tả hoặc dùng công cụ bản địa đã được phê duyệt; không báo bộ sinh hỗ trợ.

## Context thực thi bắt buộc

Đọc [hợp đồng thực thi và bảng bằng chứng](references/01-dac-ta-va-khoi-tao.md) trước khi lập kế hoạch. Áp dụng từng cổng tương ứng phạm vi, lưu bằng chứng và giới hạn trong worklog; không chỉ dựa vào mô tả ngắn ở SKILL.md.
