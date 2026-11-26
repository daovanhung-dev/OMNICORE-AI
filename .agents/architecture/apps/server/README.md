# Folder mẫu: `apps/server/`

**Trách nhiệm:** Một backend Python minh họa, có entry, router, core, modules, service, utils, tests và DD.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`app/`](app/README.md) — Python application package; composition, inbound/outbound layers và domain module.
- [`docs/`](docs/README.md) — API design/contract của backend; chỉ là EXPECTED cho tới khi source wired.
- [`tests/`](tests/README.md) — Tập test có fixture an toàn và không kết nối production.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
