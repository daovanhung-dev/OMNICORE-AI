# API01 — Mẫu Detail Design (cùng API01 trong module1)

**Loại:** `DESIGN_EXAMPLE`, không thêm API mới và không giả định endpoint thật.

## Điền khi có yêu cầu được duyệt

- API ID, method, route path, actor, permission/ownership.
- Request: header/query/path/body, type/nullability, default, validation.
- Response: status + envelope + field mapping; error/business codes.
- Data flow: authn/authz → validate → service/view → DB/provider → transaction → response.
- DB schema/migration và rollback (nếu có), bảo mật và test cases.

Dùng skill [`create-dd-api`](../../../../../../../skills/create-dd-api/SKILL.md) để sinh DD thực. Tài liệu này chỉ là ví dụ tuyến tính tương ứng `app/modules/module1/api01/`.
