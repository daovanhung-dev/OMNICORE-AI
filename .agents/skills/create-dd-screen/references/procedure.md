# Quy trình — DD màn hình (8 documents)

## G0. Screen identity

- Screen ID duy nhất, name, scope/feature, actor, route/deep link, entry/exit, desktop/mobile variants, source design version và current UI source.
- Nếu có ảnh clean/numbered và HTML/Figma, đọc cả hình và marker metadata; nếu không, đánh dấu `NO_VISUAL_SOURCE`, không tự tạo marker/ảnh giả để chứng minh UI.

## G1. UI element contract

Mỗi interactive element `EL-ID` có role, label, visible, disabled, state, data source, event ID. Marker `#n → EL-ID` phải map 1:1 và không trùng. Ảnh chỉ biểu diễn một state; loading, empty, error, forbidden, offline, retry phải được thiết kế trong DD khi phù hợp.

## G2. Rule + API trước event

Viết `BR-ID` với condition/priority, owner client vs server, authorization source, effect. Map `API-ID` tới method/path/request/response/errors/validation từ contract hoặc source; route metadata không có nghĩa là HTTP caller. UI chỉ guard UX; backend xác thực permission/ownership.

## G3. Luồng dữ liệu

`API DTO → normalize/mapping → ViewModel → state → rendered UI`; ghi local vs persisted, optimistic rollback, stale-result guards, cache, pagination, cancellation and race.

## G4. Sự kiện & navigation

Mỗi `EV-ID`: trigger → precondition → input/source → normalize → steps → API/side effect → UI state → navigation → errors/retry → test cases. Navigation ghi path/query/params/authorization/deep-link-invalid/back semantics.

## G5. Tests & trace

`marker → EL-ID → EV-ID → BR-ID / API-ID → TC-ID`. Test happy, empty/error, invalid, unauthorized, refresh/retry, rapid clicks, accessibility, responsive. Điều kiện không có nguồn: `OPEN QUESTION` với owner và ảnh hưởng; không biến giả định thành Approved.

## Files

`00-overview.md`, `01-ui-elements.md`, `02-events.md`, `03-data-flow.md`, `04-api-integration.md`, `05-business-rules.md`, `06-navigation.md`, `07-test-cases.md` và `images/README.md` mô tả provenance. Template [bundled](../templates).
