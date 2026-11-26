# Hợp đồng tệp `app/core/trace.*`

## Quyền sở hữu và phụ thuộc

Chỉ thực hiện trách nhiệm nêu dưới đây. Không nhập tầng gọi ngược lại; cấu hình và hợp đồng dự án xác định kiểu, quyền và lỗi cụ thể.

## Biểu tượng và hợp đồng

### `create_trace_id()`

Tạo mã tương quan không chứa dữ liệu cá nhân.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `validate_trace_id(value)`

Kiểm tra định dạng và độ dài trước khi tin cậy.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `set_trace_id(value)`

Gắn mã vào ngữ cảnh yêu cầu; trả dấu khôi phục.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `get_current_trace_id()`

Đọc mã trong ngữ cảnh hiện tại, không dùng biến toàn cục chia sẻ.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `reset_trace_id(token)`

Khôi phục ngữ cảnh sau yêu cầu, kể cả lỗi.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

## Bằng chứng

Khi tích hợp, ghi đường dẫn và dòng nguồn, điểm gọi, kết quả kiểm thử; chỉ đánh dấu đã xác minh khi có bằng chứng.
