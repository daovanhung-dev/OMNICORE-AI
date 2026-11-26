# Quy trình — BD/BRD → Module Detail Design

## Đầu vào

BD/BRD/epic/user story, roles, business flows, data entities, non-functional constraints, current module/source, design assets, API and tests. Mark source/owner/version. Nếu chưa có BD, giữ phần thiếu `OPEN QUESTION`; không tự viết nghiệp vụ thay chủ dự án.

## Decomposition

1. `MOD-ID` mục tiêu, boundaries và dependencies.
2. `FEATURE-ID` actor, outcome, main/alternate/failure flow, source requirement.
3. `FUNCTION-ID` inputs/outputs/validation/business rules/permission/side effects.
4. UI Views: entry/exit, state model, navigation, testable transitions.
5. API/protocol and DB relation: stable IDs, producer/consumer, error catalog and data type.
6. Source/Import map: target files/modules, reuse, cross-scope contract, migration owner.
7. Sequence/activity/ERD diagrams (nếu dựa trên nguồn), assets source/provenance, change history.

## Cổng chất lượng

- Trace `BD → Feature → Function/Rule/API → View → Test → Implementation file` hai chiều.
- Tách ba trục **DD lifecycle** (Draft/Review/Approved), **implementation** (None/Partial/Wired), **verification** (Not run/Local/Live/Deployed).
- Câu hỏi chưa chốt có impact + decision owner; không duyệt chức năng blocked và không gắn mock thành persistence.
- Review UI, validation/error, permission, data/migration và screen/API interaction bằng các role BA/Architect/QA khi có.

## Output

Folder `README`, `Overall`, `List_Features`, `Function_List`, `Views`, `Import_File`, diagrams/assets/history dùng [`../templates`](../templates). Không sửa runtime code khi chỉ được giao DD.
