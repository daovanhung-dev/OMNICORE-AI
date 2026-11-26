# Folder: `apps/api/omnicore_api/`

<!-- AUTO_CONTEXT_START -->
**Trách nhiệm dự kiến:** Thư mục do source thực tế khai báo; đọc các file bên dưới để xác định owner.

## Folder con hiện có

- [`api/`](api/README.md) — API/router/transport boundary
- [`core/`](core/README.md) — Hạ tầng/lõi dùng chung theo codebase thực tế

## File thực tế

- [`__init__.py`](__init__.md) — Ứng viên code thực thi; xác minh imports/callers và wiring.
- [`main.py`](main.md) — Ứng viên entrypoint; cần kiểm chứng qua script/bootstrap thực tế.

**Giới hạn:** cây này phản ánh file quan sát được; không suy ra runtime wiring, permission, deployment hay business rule.
<!-- AUTO_CONTEXT_END -->

## Ghi chú owner / dependency có bằng chứng

- [ ] Owner/feature/module:
- [ ] Entry/caller và quan hệ liên module:
- [ ] DD/contract/test tương ứng:
