# Quy trình sửa lỗi và hồi quy

1. Ghi triệu chứng, kỳ vọng/thực tế, bước tái hiện, môi trường, phiên bản, ảnh hưởng, log đã che bí mật. Kiểm tra Git và lỗi nền. Nếu chưa tái hiện, ghi `NOT_REPRODUCED` và thiếu chứng cứ.
2. Xác định tuyến/điểm gọi, truy vết toàn bộ đường thực thi tới dữ liệu, dịch vụ, phản hồi và UI. Kiểm tra hợp đồng, quyền, đầu vào, lỗi, giao dịch và phụ thuộc. Lập các giả thuyết cạnh tranh; loại bỏ bằng bằng chứng, không suy nguyên nhân từ triệu chứng.
3. Lập ca hồi quy thất bại đúng nguyên nhân trước sửa nếu khả thi; nếu không, ghi lý do. Xác định sửa nhỏ nhất ở lớp sở hữu; không vô hiệu kiểm thử hoặc nuốt lỗi để che triệu chứng.
4. Sửa theo kế hoạch lá, giữ hợp đồng và thay đổi người dùng. Nếu cần quyết định về DB/quyền/hợp đồng chưa duyệt, chặn phần đó.
5. Chạy lại ca hồi quy, bộ kiểm thử tác động và kiểm tra an toàn, diff; phân biệt lỗi nền và lỗi mới. Cập nhật nguồn, DD/ngữ cảnh khi cần và nhật ký. Báo nguyên nhân, bằng chứng, tệp thay đổi, kết quả và giới hạn.
