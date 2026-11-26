# Quy trình lập trình chức năng

Áp dụng `implement-feature`, `write-tests`; tạo hoặc sửa thiết kế trước nếu hợp đồng thiếu. Tiền kiểm: xác định phạm vi, Git, yêu cầu/AC, DD, kiến trúc, điểm gọi, điểm được gọi, quyền, dữ liệu, tác động phụ, phản hồi và kiểm thử. Ghi hành vi mong muốn, hiện trạng, mâu thuẫn. Không reset/clean.

## Kế hoạch
Tách mục tiêu lá theo tệp và kết quả. Xác định chủ sở hữu, hợp đồng, thứ tự phụ thuộc, rủi ro migration, tiêu chí thành công/lỗi, môi trường, rollback và dọn dữ liệu. Thiếu quyết định quan trọng thì chặn phần phụ thuộc.

## Thực thi
BE: đăng ký tuyến đúng nơi, xác thực/quyền trước truy xuất bảo vệ, kiểm tra đầu vào, truy xuất tham số hóa, xử lý nghiệp vụ và giao dịch ở chủ sở hữu, phản hồi chuẩn, lỗi và tác động phụ có cơ chế nhất quán. FE: dùng bốn thư mục, HTTP có kiểu, API đã xác minh, trạng thái tải/rỗng/lỗi/thành công, hủy yêu cầu, điều hướng và khả năng tiếp cận. Chức năng xuyên lớp áp dụng `contract-change.md`. Không sửa ngoài phạm vi.

## Kiểm chứng
Chạy kiểm thử tập trung, bộ kiểm thử liên quan, kiểm tra định dạng/lint/kiểu/build theo lệnh thực tế. Tích hợp DB/dịch vụ cô lập; trình duyệt/thiết bị thật khi cần. Kiểm tra hợp đồng, hồi quy, diff, bí mật, dữ liệu tạm và lockfile. Ghi lệnh, mã thoát, môi trường, kết quả. Dữ liệu giả không chứng minh triển khai. Làm mới hồ sơ dự án, kiểm định, ghi nhật ký; kết thúc từng mục tiêu khi đủ chứng cứ.
