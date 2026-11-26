# Ánh xạ kiến trúc

data-access, models, pages, ui.

Router theo nhóm, widget trang điều phối, widget UI không gọi mạng. Tệp đăng ký framework chỉ lắp ghép, không sở hữu nghiệp vụ. Quy tắc logic chung áp dụng theo vai trò, không ép cú pháp framework.

## Ranh giới triển khai và bảo mật

Context nguồn có mobile entrypoint, cấu hình theme/token/component, router, lớp provider/controller, repository/datasource, storage cục bộ và tích hợp ngoài. Phải đọc composition root, platform manifests, package, route thật và vòng đời state; phân biệt local cache với session từ server. Hủy timer/stream/subscription khi dispose, chống phản hồi cũ và lặp bản ghi khi polling. Không đưa credential database hoặc nhà cung cấp AI vào APK; prototype direct DB không phải kiến trúc sản xuất. Đưa truy xuất bảo vệ về backend hoặc cơ chế có quyền tối thiểu đã duyệt. Không tự nhận diện UI đã nối chỉ từ filename. Chưa chạy Flutter trong gói.
