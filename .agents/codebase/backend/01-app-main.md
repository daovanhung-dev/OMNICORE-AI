# Hợp đồng tệp `app/main.*`

## Quyền sở hữu và phụ thuộc

Chỉ thực hiện trách nhiệm nêu dưới đây. Không nhập tầng gọi ngược lại; cấu hình và hợp đồng dự án xác định kiểu, quyền và lỗi cụ thể.

## Biểu tượng và hợp đồng

### `create_app(config)`

Lắp ghép cấu hình, tuyến, middleware, phụ thuộc; trả đối tượng ứng dụng; không truy vấn nghiệp vụ.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `health_live()`

Trả trạng thái tiến trình; không phụ thuộc DB.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `health_ready()`

Kiểm tra phụ thuộc bắt buộc với timeout; thất bại trả trạng thái chưa sẵn sàng.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

## Bằng chứng

Khi tích hợp, ghi đường dẫn và dòng nguồn, điểm gọi, kết quả kiểm thử; chỉ đánh dấu đã xác minh khi có bằng chứng.
