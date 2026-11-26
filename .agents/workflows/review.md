# Quy trình rà soát mã chỉ đọc

Chỉ kích hoạt khi được yêu cầu rà soát diff/PR/đường dẫn. Không sửa mã, test, cấu hình, tài liệu bị rà soát; không chạy test/build/lint/scanner; không đổi Git state, commit/push hoặc đăng nhận xét PR. Nhật ký chỉ ghi khi chính sách cho phép.

1. Xác định base/head hoặc phạm vi đường dẫn, phân biệt lỗi mới do diff với lỗi hiện trạng. Đọc quy tắc, kiến trúc, DD/hợp đồng, mã nguồn và mã kiểm thử liên quan.
2. Truy vết điểm gọi, điều kiện đến được, quyền, dữ liệu, tác động, giao dịch, lỗi, đồng thời, tái sử dụng và bảo mật đầu vào. Xác minh dòng nguồn hiện tại; không suy lỗi từ tên tệp.
3. Chỉ ghi phát hiện có đủ: điều kiện đến được, bằng chứng mã, tác động cụ thể, hướng khắc phục; với diff phải do thay đổi mới gây ra. P0 nghiêm trọng, P1 lớn, P2 trung bình, P3 nhỏ nhưng có tác động.
4. Báo mỗi phát hiện theo mức, tệp:dòng, hành vi, quy tắc vi phạm, tình huống, hệ quả, hướng sửa. Ghi phạm vi chưa xác minh và những kiểm thử không chạy. Không kết luận toàn bộ kho mã an toàn từ rà soát hẹp.
