# Hồ sơ dự án — repository hiện tại

<!-- AUTO_CONTEXT_START -->
- **Snapshot:** `SOURCE_SCANNED_NEEDS_REVIEW`.
- **HEAD:** `e26bdd4c60cebaa8dd36d14bac0eb9a69396cf9a`; **branch:** `main`; **sync UTC:** `2026-11-26T02:55:06+00:00`.
- **Source files:** `60`; **source folders:** `18`.
- **Runtime/entrypoints/auth/data/deployment:** `NOT_VERIFIED` — cần xác nhận qua code và test.
- **Đọc tiếp:** [trạng thái](STATE.md), [cây thư mục](PROJECT_STRUCTURE.md), [bản đồ file](SOURCE_MAP.json).
<!-- AUTO_CONTEXT_END -->

verification_status: UNREVIEWED

## Kiến thức đã xác minh (agent/người dùng bổ sung)

| Mục | Đường dẫn bằng chứng và kết luận | Trạng thái |
|---|---|---|
| Entrypoints / routes | `apps/api/omnicore_api/main.py`, `api/health.py`, `api/v1.py`; health route behavior covered in `apps/api/tests/test_api.py` | SOURCE_REVIEWED; 6 API tests PASS |
| Package/module owners | `apps/api/pyproject.toml` defines package `omnicore-api`; runtime module is `omnicore_api` | SOURCE_REVIEWED |
| Data contracts / DB | `core/config.py`, `core/database.py`, `core/models.py`, `migrations/env.py`; empty SQLAlchemy metadata and no domain migration | SOURCE_REVIEWED; SQLite probe and safe failure tests PASS; live PostgreSQL unverified |
| Auth/security | Business authentication and authorization are outside this backend-foundation scope | NOT_IN_SCOPE |
| Build/test commands | `apps/api/README.md`; `uv run --package omnicore-api --extra dev pytest apps/api/tests`; lint and wheel build receipts are recorded in session `BEINITCLEAN1126` | TESTED |

Chỉ ghi sự thật sau khi đọc source/tests hoặc có xác nhận phù hợp. Script làm mới phần tự động ở trên nhưng giữ nguyên phần ghi chú này.

Chỉ đổi `verification_status` thành `SOURCE_REVIEWED` khi những ranh giới liên quan đã được đối chiếu source và có bằng chứng cụ thể. Không đồng nghĩa hệ thống đã chạy/test/deploy.
