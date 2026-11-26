# Lát cắt tham chiếu V11

Một API GET danh mục và một Screen danh mục TypeScript thuần, dùng SQLite cô lập. Mặc định công khai, tùy chọn JWT/RBAC reader. Có refresh store opaque hash và xoay một lần, migration SQLite, cache TTL cục bộ, health, trace, HTTP client timeout/token bộ nhớ. Không có endpoint đăng nhập hay triển khai production, PostgreSQL pool, Redis, Angular build đã kiểm thử.

- Backend: cài requirements.txt; tại backend chạy `python -m pytest -q`. Test tích hợp dùng frontend/ cùng cấp, Uvicorn và proxy localhost, tạo DB tạm và dừng tiến trình.
- Frontend: Node.js 22, TypeScript 5.8; tại frontend chạy `npm test` (tsc và Node TAP). Dùng `python serve.py` chỉ để demo.
- Tạo DB mới: tại backend `python seed.py /tmp/danh-muc-moi.db`; chạy `DEMO_DB=/tmp/danh-muc-moi.db python -m uvicorn app.main:app_factory --factory --host 127.0.0.1 --port 8765`. Tùy chọn `DEMO_PROTECTED=1` yêu cầu JWT_SECRET (ít nhất 32 byte), JWT_ISSUER, JWT_AUDIENCE; không tự mở chế độ bảo vệ nếu chưa có hệ thống cấp token thật. Không dùng key test production.
- Migration chỉ chạy trên DB được phép: `migrate(path, folder)` ở app/core/migration.py. Dữ liệu demo chỉ xóa đúng DB vừa tạo, không xóa dữ liệu khác.
- Sinh dự án mới bằng `python3 .agents/tools/create-codebase.py --destination /duong-dan-moi --profile fastapi-typescript`. Bao gồm cả AGENTS.md và .agents, không ghi đè. Hoặc `--config .agents/engines/generator-config.json` thay cho --profile. Không cài gói tự động; không sinh cấu hình chưa xác minh.
