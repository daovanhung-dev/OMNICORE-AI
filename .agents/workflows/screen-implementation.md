# Quy trình triển khai, sửa và kiểm chứng màn hình

1. Hoàn tất tiền kiểm chung. Xác định mã màn hình, tuyến, API, vai trò; đọc danh mục và chỉ mục DD. Ghi rõ phạm vi trong nhật ký.
2. Đọc toàn bộ gói DD: ảnh sạch và đánh số bằng trực quan, `images/README.md`, tài liệu 00–07, HTML thiết kế và marker liên quan. Đối chiếu xuất xứ, phiên bản, trạng thái và cổng bị chặn. Không coi thiết kế là mã chạy.
3. Truy vết từng marker, element, event, dữ liệu, quyền, API, lỗi, điều hướng, trạng thái và test. Đọc mã tuyến/trang/khung/core/shared/API hiện hữu. Lập kế hoạch theo tệp, sự kiện, thành phần tái sử dụng, kiểm thử, demo và dọn dữ liệu.
4. Tạo bốn thư mục màn hình, tuyến nhóm và khung đúng quy tắc FE. Kiểm tra trang gốc không rò nội dung sang tuyến con; giữ guard có nguồn. Không bịa API, fallback, trường, quyền hoặc trạng thái. Chỉ triển khai phần độc lập khi phụ thuộc chưa sẵn sàng.
5. Chạy kiểm thử tập trung, build, kiểm tra URL gốc và URL trực tiếp; trình diễn tuyến thật trong trình duyệt/thiết bị; thử sự kiện, trạng thái, bàn phím, kích thước và lỗi. Nếu cần dữ liệu giả, xác minh DB thử nghiệm cô lập và schema hiện hành trước khi tạo; ghi ID, xóa đúng ID theo thứ tự phụ thuộc, truy vấn xác minh đã dọn. Không truncate hoặc sửa dữ liệu thật.
6. Ghi danh mục tệp đọc, quyết định, thay đổi, lệnh/kết quả, demo, ID fixture và chứng cứ dọn; giữ trạng thái bị chặn và mâu thuẫn. Không kết luận đã chạy từ ảnh hoặc máy chủ dev.
