# Tầng dữ liệu — nguyên tắc tổng quát

- Source schema/migration là thiết kế, không chứng minh database production đã apply.
- Query sử dụng bind params, xác minh constraints, owner/tenant filtering, isolation.
- Use case sở hữu atomic transaction; repository/helper không tự commit nếu policy quy định ở service.
- Backfill/destructive SQL phải có backup, target, approval và rollback.
- Test bằng dữ liệu tách biệt; không seed/truncate DB được chia sẻ.

Ví dụ `api01/query.py → query.md` nằm trong [một API mẫu](apps/server/app/modules/module1/api01/query.md). Không mặc định mọi dự án sử dụng SQL hoặc ORM.
