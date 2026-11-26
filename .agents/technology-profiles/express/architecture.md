# Ánh xạ kiến trúc

models.ts, validate.ts, query.ts, view.ts.

Router Express, middleware lỗi, inject DB adapter. Tệp đăng ký framework chỉ lắp ghép, không sở hữu nghiệp vụ. Quy tắc logic chung áp dụng theo vai trò, không ép cú pháp framework.

## Quy tắc khi áp dụng vào kho hiện hữu

Context nguồn ghi nhận một server Express dùng composition root `main`, app factory có dependency injection, router/middleware, shared ORM client và bộ phản hồi chung. Đây là mẫu khác với API FastAPI SQL thuần: không đổi router/service/repository thành bốn tệp cứng khi chưa có quyết định kiến trúc. Với dự án mới chọn bốn trách nhiệm logic, ánh xạ models/validate/query/view sang DTO/guard/repository/controller hoặc use case; ghi rõ ngoại lệ. Khởi động kết nối phụ thuộc trước listen nếu hợp đồng yêu cầu; đóng kết nối khi dừng. Kiểm tra JSON parser, trace context, error handler, optional auth và protected routes. Không sao chép cấu hình tĩnh chứa credential; dùng secret management của dự án đích. Chưa xác minh runtime Express trong gói này.
