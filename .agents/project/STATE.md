# Trạng thái hiện tại của repository

<!-- AUTO_CONTEXT_START -->
- **Last sync (UTC):** `2026-11-26T02:55:06+00:00`
- **Repository HEAD:** `e26bdd4c60cebaa8dd36d14bac0eb9a69396cf9a`; **branch:** `main`; **scan mode:** `git-tracked-and-untracked-not-ignored`
- **Files/folders:** `60` / `18`
- **Changed since previous sync:** files added `0`, modified `0`, removed `1`; folders added `0`, removed `0`
- **Git dirty entries (observed):** `11` (không hiển thị dữ liệu nhạy cảm)
- **Source index:** [SOURCE_MAP.json](SOURCE_MAP.json); [source tree](tree/README.md).
- **Application runtime/test/deployment:** `NOT_VERIFIED` / `NOT_RUN` trừ khi bổ sung bằng chứng thủ công.
<!-- AUTO_CONTEXT_END -->

## Vấn đề đang theo dõi (ghi thủ công, kèm evidence)

- `apps/api` có health live/readiness, cấu hình psycopg/SQLAlchemy sync, session dependency và Alembic; chưa có bảng nghiệp vụ hoặc migration. Unit tests dùng SQLite in-memory và engine lỗi giả lập; chưa kết nối PostgreSQL thật.
- Docker engine/CLI không khả dụng trong môi trường này; container và Compose runtime chưa được xác minh. Redis chỉ còn trong Compose, chưa được ứng dụng BE gọi.
- Session `BEINITCLEAN1126` ghi nhận các receipt kiểm chứng source/build/test theo phạm vi BE khi hoàn tất.
