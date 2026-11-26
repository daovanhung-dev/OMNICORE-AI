# Kiến trúc hệ thống — quy tắc dùng lại

## Luồng tham khảo (không khẳng định source)

`Browser/UI → data-access → API transport → router → authentication → authorization → validation → use case → DB/provider → response → UI state`

## Các ranh giới

- **Client:** trình bày, điều hướng, UX state, typed request; không giữ secret và không quyết định quyền backend.
- **Server:** xác thực, phân quyền theo tài nguyên, nghiệp vụ, transaction, providers, response mapping.
- **Contracts:** version/method/path/fields/error và producers/consumers; cần duyệt khi thay đổi.
- **Database:** schema thực, migrations, constraints, rollback. DDL checked-in không có nghĩa đã áp dụng ở môi trường.
- **Tests/deployment:** nhiều mức chứng cứ; build không có nghĩa integration pass hoặc deployed.

Không mặc định dự án phải có client, server, worker hay database riêng. Tên phần mềm, stack, URL và ownership lấy từ checkout đích.
