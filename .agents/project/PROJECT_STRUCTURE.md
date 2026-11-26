# Cấu trúc hiện tại của repository

<!-- AUTO_CONTEXT_START -->
# Project structure — generated from this repository

- Source files: **60**; source directories: **18**
- Scan: `git-tracked-and-untracked-not-ignored`; git HEAD: `e26bdd4c60cebaa8dd36d14bac0eb9a69396cf9a`
- Độ tin cậy: **PATH_VERIFIED** cho file tồn tại; **SOURCE_INSPECTED_STATIC** khi phân tích tĩnh; không khẳng định wiring/runtime.
- File-level docs trong [`tree/`](tree/README.md); ánh xạ đường dẫn trong [`SOURCE_MAP.json`](SOURCE_MAP.json).

## Cấu trúc thư mục cấp cao (tối đa 3 tầng)

- `apps/`
- `apps/ai-api/`
- `apps/ai-api/omnicore_ai_api/`
- `apps/ai-api/tests/`
- `apps/api/`
- `apps/api/migrations/`
- `apps/api/omnicore_api/`
- `apps/api/tests/`
- `apps/web/`
- `apps/web/public/`
- `apps/web/src/`
- `contracts/`
- `docs/`
- `infra/`

## Ứng viên deployable/package từ manifest

- `.`: `package.json, pyproject.toml`; tín hiệu: Python application/package
- `apps/ai-api`: `Dockerfile, pyproject.toml`; tín hiệu: Python application/package
- `apps/api`: `Dockerfile, pyproject.toml`; tín hiệu: Python application/package
- `apps/web`: `Dockerfile, package.json`; tín hiệu: Angular (dependency declared)

## Cần agent xác minh trước coding

- [ ] Entry/bootstrap và router registration
- [ ] Boundary client/server/worker/module
- [ ] DB/schema/API/event contracts thực tế
- [ ] Quy tắc bảo mật và quyền dữ liệu
- [ ] Lệnh test/build thực sự được chạy

<!-- AUTO_CONTEXT_END -->

## Quyết định kiến trúc có bằng chứng (thủ công)

- Chưa có.
