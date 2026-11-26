# Hợp đồng tệp `app/core/responses.*`

## Quyền sở hữu và phụ thuộc

Chỉ thực hiện trách nhiệm nêu dưới đây. Không nhập tầng gọi ngược lại; cấu hình và hợp đồng dự án xác định kiểu, quyền và lỗi cụ thể.

## Biểu tượng và hợp đồng

### `ErrorDetail`

Khai báo lỗi có kiểu theo hợp đồng; không chứa stack trace.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `success_response(data, code, trace_id)`

Tạo phản hồi thành công đúng HTTP/envelope.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `error_response(error, trace_id)`

Ánh xạ lỗi có kiểu tới HTTP và mã nghiệp vụ; không lộ nội bộ.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

## Bằng chứng

Khi tích hợp, ghi đường dẫn và dòng nguồn, điểm gọi, kết quả kiểm thử; chỉ đánh dấu đã xác minh khi có bằng chứng.
