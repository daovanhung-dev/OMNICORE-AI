# Folder mẫu: `apps/`

**Trách nhiệm:** Nhóm ứng dụng minh họa theo deployable, không bắt buộc repo đích dùng monorepo.

**Mức bằng chứng:** `TEMPLATE_ONLY`, không phải cây source đã được xác minh.

## Folder con

- [`client/`](client/README.md) — Một web client TypeScript minh họa, không bắt buộc framework hoặc layout đối với dự án khác.
- [`server/`](server/README.md) — Một backend Python minh họa, có entry, router, core, modules, service, utils, tests và DD.

**Khi onboarding:** thay cây ví dụ này bằng `project/tree/` sinh từ repository thật; không tự thêm folder vào source.
