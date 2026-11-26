# Hợp đồng tệp `core/constant/api.constants.*`

## Quyền sở hữu và phụ thuộc

Chỉ thực hiện trách nhiệm nêu dưới đây. Không nhập tầng gọi ngược lại; cấu hình và hợp đồng dự án xác định kiểu, quyền và lỗi cụ thể.

## Biểu tượng và hợp đồng

### `ApiDescriptor`

Kiểu mô tả ID, method, path và trạng thái kết nối.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

### `ApiMethod / API_BASE_PATH`

Khai báo tập phương thức và URL gốc theo cấu hình; không bịa endpoint.

- Đầu vào phải có kiểu theo công nghệ và hợp đồng được duyệt; đầu ra, lỗi và tác động phụ phải được mô tả tại tệp nguồn tương ứng.

- Nghiệm thu: kiểm thử hành vi chính, đầu vào/điều kiện bất hợp lệ nếu có; xác minh ranh giới phụ thuộc và không phát sinh tác động ngoài trách nhiệm.

## Bằng chứng

Khi tích hợp, ghi đường dẫn và dòng nguồn, điểm gọi, kết quả kiểm thử; chỉ đánh dấu đã xác minh khi có bằng chứng.
