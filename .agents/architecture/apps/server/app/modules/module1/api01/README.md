# Folder mẫu: `apps/server/app/modules/module1/api01/`

**Trách nhiệm:** **Một** API mẫu; README tổng quan, năm file Python đối ứng với Markdown.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## File và tài liệu 1:1

- [`__init__.py`](__init__.md) — **Package boundary**: Đánh dấu package; export tối thiểu nếu codebase yêu cầu; không tự đăng ký route.
- [`models.py`](models.md) — **Typed data contract**: Định nghĩa request DTO, response DTO, type/nullability, serialization; khớp API DD.
- [`query.py`](query.md) — **Data query boundary**: Mô tả truy vấn có bind parameters / repository query theo stack thực; không nhét auth vào SQL mà thiếu kiểm tra use case.
- [`validate.py`](validate.md) — **Validation/normalization**: Kiểm tra giá trị, chiều dài, enum và chuẩn hóa dữ liệu trước persistence; không commit DB.
- [`view.py`](view.md) — **API use case/orchestrator**: Điều phối identity + ownership + validation → data/provider → commit/rollback → response; xử lý lỗi đúng contract.

## Luồng xử lý minh họa API01

`HTTP request → api/v1.py → view.py → validate.py/models.py → query.py → DB/provider → transaction → response`

Input/output, errors, authentication, authorization và DB fields phải được phê duyệt từ requirements và source thực.
File `validate.py` và `query.py` là tùy chọn trong dự án thật; không tạo file nguồn chỉ vì có trang tài liệu ví dụ.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
