# Quy trình — API Detail Design

## G0. Input & scope gate

- Ghi API ID, mục tiêu, trigger, principal, owner, consumer(s), version và trạng thái.
- Đọc requirements, BD/BRD, approved business rules, API catalog/OpenAPI, current router/DTO/auth middleware, migration/DB models, tests; ghi path/commit, không dùng link chết.
- Kiểm tra template được dự án chấp nhận. Nếu template dự án khác mặc định, ưu tiên project owner và ghi mapping; không tự đổi toàn bộ convention.

## G1. Contract reconciliation

Lập bảng `Requirement ID → API event → input/output field → rule → data source → test → status`. Phân biệt `EXPECTED` từ DD/requirement và `CURRENT` từ source/runnable tests; khi khác nhau đặt `DISCREPANCY`, owner quyết định. API signature có thể Draft nhưng source wired: ghi cả hai, đừng chọn theo cảm tính.

## G2. Request detail

Mỗi field một hàng: `name | location path/query/header/body | type | required | null/blank | default | format | bounds | normalization | validator owner | source | test`. Với upload ghi MIME/size/signature/purpose; với mutation ghi idempotency/concurrency. Không dùng field không có nguồn.

## G3. Response/error detail

Mỗi output field: `path | type | nullable | source table/provider/formula | privacy | mapping | error fallback`. Tách `success`, `businessCode`, `message`, `data`, `meta`, `traceId` **chỉ nếu project dùng envelope này**. Status HTTP ≠ business code. Error matrix ghi auth, ownership, validate, 404, conflict, DB/provider fail, timeout/retry, rollback.

## G4. Luồng dữ liệu & persistence

Theo thứ tự: parse → authn/authz/object scope → validation → query/insert/update/delete → transaction/lock → provider/outbox → map response → audit/trace. Mỗi SQL predicate/DB column có nguồn schema. Read-only: DB mutation sheet ghi `N/A` thật; mutation nhiều table: mỗi operation/table có sheet mapping riêng. Không tự invent index/migration, cache invalidation hay async policy.

## G5. Review & handoff

- Đọc đủ tám template file trong [`../templates`](../templates) hoặc template approved của project.
- `python3 .agents/workflows/tools/agentkit.py new-dd --type api --id API-001 --slug Example --output docs/dd` chỉ tạo Draft.
- Kiểm tra field mapping, lỗi/permissions, links, tests, cross-consumer behavior và open questions. Project DD approved không chứng minh API đã wired/tested/deployed.
- Ghi changelog, owner, status, missing evidence. Reject Approved nếu còn open blocking decisions.
