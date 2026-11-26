# Tạo DD API — ví dụ, không phải dữ liệu thực

Ví dụ bên dưới là **mẫu diễn giải**, không phải chức năng được xác minh của repository đích.

**Scenario:** tính năng giả định `Notes` có người dùng đăng nhập. Mỗi action cần ID, owner, approved contract, expected/current và test evidence trước khi code.

- Expected: user xem danh sách ghi chú của chính mình.
- Authorization: server xác nhận principal và owner của từng note; UI guard chỉ cải thiện trải nghiệm.
- Error: chưa login 401, resource không sở hữu 403/404 theo contract được duyệt, DB fail phải có safe error.
- Status: `DESIGN_ONLY` cho tới khi kiểm tra router/query/test thực, không tự gắn WIRED.
- Evidence: `REQ-DEMO-001 → API-DEMO-001 → TEST-DEMO-001`, chỉ là mẫu.

Đọc [procedure](../references/procedure.md) rồi dùng [checklist](../checklists/quality-gates.md) với codebase thật. Không sao chép các chính sách demo nếu project khác.
