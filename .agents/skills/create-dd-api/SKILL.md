---
name: create-dd-api
description: Tạo bộ thiết kế chi tiết API Markdown có truy vết nguồn và hợp đồng.
---
# Năng lực tạo thiết kế chi tiết API

**Trigger:** tạo/sửa/review DD API REST/GraphQL/RPC/event với nguồn requirement cụ thể. **Không** dùng skill để tự code runtime.

## Đầu vào

Approved BD/BRD/AC, API catalog/OpenAPI nếu có, current router/controller/DTO/error schema, auth guard, DB/migration, producer/consumer, template đã xác minh ở `skills/create-dd-api/templates/` hoặc template được project chỉ định. Nếu template project tồn tại, ưu tiên cấu trúc đó; ghi khác biệt.

## Procedure (gates)

1. Inventory sources + version/commit + owner/status; đọc template đủ heading và file. Nếu không có approved requirement hoặc template hợp lệ → `BLOCKED` cho phần phụ thuộc.
2. Tách expected contract và current implementation; lập Requirement Matrix `REQ-ID → endpoint/field/rule → source → status`.
3. Truy vết request field **từng dòng**: name, location, type, required, format, normalization, validation, source.
4. Truy vết response field **từng dòng**: output path, type/nullability, source (table/external/computed), privacy, error behavior.
5. Data mapping: ordered steps, guard/auth, query predicates, DB reads/writes, transaction, idempotency, error/rollback, side effects and observability.
6. Error matrix: condition → status → business code/error body → priority → user-visible result → tests.
7. API changes: compatibility & consumer impact; open questions/assumptions separated (owner, risk), never assert as facts.
8. Scaffold `python3 .agents/workflows/tools/agentkit.py new-dd --type api --id API-001 --slug CreateItem --output docs/dd`; fill all generated files with evidence and verify links/tests.

## Tệp đầu ra

`00-cover.md`, `01-history.md`, `02-overview.md`, `03-request.md`, `04-response.md`, `05-data-mapping.md`, `06-errors.md`, `07-db-mapping.md` (READ-ONLY ghi N/A). Nếu API mutate nhiều bảng, tạo `08-db-<table>-<operation>.md` **mỗi mapping một file** theo dự án; read-only API ghi N/A rõ.

## Điều kiện nghiệm thu

- Không còn placeholder trong DD được coi là ready; mỗi field/condition/error có ID hoặc một row; links hợp lệ; schema/role/HTTP/transaction đúng evidence.
- `DESIGN_ONLY` không thành `WIRED`; Approved DD chỉ có nghĩa quyết định thiết kế đã được phê duyệt.
- Test cases trace được; security/ownership/retry/error đều được review; open questions block behavior quan trọng thì không được gắn `Approved`.

## Tài nguyên kèm theo (đọc khi task chạm tới)

- [Procedure](references/procedure.md)
- [Quality gate checklist](checklists/quality-gates.md)
- [Example & limitations](examples/README.md)
- [Full Markdown templates](templates/)

## Ma trận và cổng kiểm định bắt buộc

Trước khi viết, lập danh mục nguồn, báo cáo độ bao phủ và ma trận yêu cầu; kiểm kê toàn bộ mẫu được duyệt. Nếu không có mẫu hợp lệ, dừng phần tạo DD. Lập bốn ma trận: sử dụng trường request, truy vấn (bảng/cột/JOIN/WHERE/GROUP/ORDER, tham số), thay đổi dữ liệu (INSERT/UPDATE/DELETE, thứ tự/giao dịch), nguồn từng trường phản hồi. Một trường, biến, cột, điều kiện và lỗi trên một hàng. Với mỗi bảng bị thay đổi, có mapping hai chiều giữa bước xử lý và cột DB.

DD chỉ được hoàn tất khi kiểm tra chéo Request → Data Mapping → DB → Response → Error, tham chiếu hai chiều, nguồn của mọi trường, thứ tự lỗi, phạm vi quyền, commit/rollback, tính tương thích, và câu hỏi còn mở. Tác vụ nhiều API tạo một folder cho từng API, kiểm kê trạng thái từng mục; không ghi đè mẫu dự án đã duyệt. Báo cáo kết quả, thay đổi mã nghiệp vụ và câu hỏi mở lưu riêng theo hợp đồng dự án.

- [Ma trận chi tiết và cổng nguồn](references/ma-tran-chi-tiet.md): bắt buộc đối với DD mới hoặc thay đổi hợp đồng.

## Tài nguyên bắt buộc theo thứ tự

1. [Tiếp nhận, phân loại, khóa mẫu](references/01-tiep-nhan-va-phan-loai.md) — mọi nhiệm vụ DD.
2. [Hợp đồng Request/Response/Error](references/02-hop-dong-request-response.md) — trước khóa trường.
3. [Mẫu luồng xử lý, query, mutation, giao dịch](references/03-data-mapping-patterns.md) — trước viết Data Mapping.
4. [Cổng bao phủ và bàn giao](references/04-bao-phu-va-ban-giao.md) — trước nghiệm thu.
5. [Ví dụ API đọc đã truy nguồn](examples/doi-chieu-api-doc.md) — để hiểu cách áp dụng, không dùng làm contract dự án mới.

Không chỉ đọc SKILL.md; ghi từng tài nguyên được áp dụng trong READ_PLAN và ghi kết quả từng cổng vào worklog. `agentkit.py new-dd` chỉ sinh khung mẫu, không tạo thiết kế nghiệp vụ. Mẫu tích hợp dùng khi dự án không có mẫu đã duyệt khác.

- [Ví dụ ma trận mutation và rollback](examples/mutation-pattern.md): đọc khi có ghi dữ liệu; chỉ là dữ liệu kỹ thuật giả lập.
