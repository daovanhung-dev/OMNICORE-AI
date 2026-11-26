# Quy trình thay đổi hợp đồng xuyên lớp

1. Kiểm kê hợp đồng chuẩn, phiên bản, bên cung cấp, mọi bên tiêu thụ thực, tuyến, kiểu, DB/event, quyền, null/default, phân trang, lỗi, idempotency và test. Phân biệt khai báo, nối nguồn, chạy và triển khai.
2. Lập ma trận trường/đường dẫn/mã lỗi trước-sau, tương thích, phiên bản, rủi ro mất dữ liệu và tác động triển khai. Không đổi contract để né lỗi thiếu nguồn.
3. Duyệt kế hoạch migration/rollback, thứ tự triển khai bên cung cấp và tiêu thụ, hỗ trợ phiên bản cũ nếu cần; không tự thay quyền hay xóa cột dữ liệu.
4. Cập nhật DD/contract, hiện thực ở chủ sở hữu, sau đó bên tiêu thụ; kiểm thử từng phía, tích hợp và hợp đồng chéo, hồi quy lỗi và quyền. Ghi các phần chưa nối.
5. Triển khai chỉ trong phạm vi được phép; cập nhật tài liệu, registry, phiên bản, nhật ký, trạng thái và chứng cứ. Không báo triển khai nếu chỉ build local.
