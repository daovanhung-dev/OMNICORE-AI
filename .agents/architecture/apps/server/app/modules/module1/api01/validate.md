# Tài liệu file mẫu: `validate.py`

**Trạng thái:** `TEMPLATE_ONLY` — chỉ minh họa trách nhiệm layer, không khẳng định dự án đích có file này.

**Source tương ứng (nếu dự án dùng cấu trúc mẫu):** `apps/server/app/modules/module1/api01/validate.py`

## Chức năng

**Validation/normalization.** Kiểm tra giá trị, chiều dài, enum và chuẩn hóa dữ liệu trước persistence; không commit DB.

## Đầu vào và đầu ra

- Đầu vào: Request model / input.
- Đầu ra: Validated input hoặc lỗi định dạng.

## Quan hệ và phạm vi

- Phụ thuộc/đường gọi cần đối chiếu: models.py, view.py.
- Tên hàm, chữ ký, HTTP method, trường dữ liệu và thực tế import phải lấy từ code của repository đích, không được suy ra từ template.

## Trình tự xác minh khi triển khai

1. Đọc file source thực tế và entrypoint/caller của nó.
2. Đối chiếu API/DD, logic quyền, DB/IO và phản hồi lỗi.
3. Kiểm tra nơi đăng ký route và consumer thực tế; mark `UNWIRED` khi cần.
4. Chạy test phù hợp khi được phép; ghi `NOT_RUN` nếu chưa chạy.

[Tài liệu của folder](README.md)
