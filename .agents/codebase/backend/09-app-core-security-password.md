# Hợp đồng tệp `app/core/security/password.*`

## Quyền sở hữu và phụ thuộc

Chỉ thực hiện trách nhiệm nêu dưới đây. Không nhập tầng gọi ngược lại; cấu hình và hợp đồng dự án xác định kiểu, quyền và lỗi cụ thể.

## Biểu tượng và hợp đồng

### `hash_password(password)`

Băm bằng thuật toán được duyệt, salt và cấu hình phù hợp.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `verify_password(password, hash)`

Kiểm tra an toàn; không lưu mật khẩu thô.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `needs_password_rehash(hash)`

Phát hiện tham số cũ theo chính sách; không tự ghi DB.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

## Bằng chứng

Khi tích hợp, ghi đường dẫn và dòng nguồn, điểm gọi, kết quả kiểm thử; chỉ đánh dấu đã xác minh khi có bằng chứng.
