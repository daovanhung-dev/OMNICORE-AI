# Hợp đồng sự kiện và trạng thái

Mỗi element: ID, marker/ẩn, kiểu, vị trí, nhãn, data source, kiểu, format, kích thước hoặc token theo thiết kế, trạng thái visible/enabled/disabled/read-only, validation message, event, accessibility/responsive nếu có tiêu chí. Với danh sách động, ghi item key, cardinality, lặp, empty. Mỗi tương tác và lifecycle quan trọng phải có event; event gồm trigger, chủ xử lý, guard, inputs và nguồn, chuẩn hóa/validation, từng bước xử lý, API/payload, mapping/side effect, UI/state, navigation, lỗi/retry và test. Không mặc định click tương đương Enter/hover nếu nguồn không nói.

| State | Điều kiện vào | Dữ liệu | UI | Hành động được phép | Điều kiện ra | Test |
|---|---|---|---|---|---|---|

Mô tả tải, ready, empty, lỗi, không quyền, disabled, modal, stale/cache, phân trang nếu áp dụng. Khi gọi bất đồng bộ: loading bắt đầu/kết thúc, request identity, cancel/ignore kết quả cũ, double-submit, retry, rollback UI, xử lý khi rời trang. Không tự thêm cache/timeout khi chưa xác định; ghi quyết định cần chốt. Tách DTO từ hợp đồng và ViewModel; chỉ định từng field, nguồn, phép đổi, fallback, kiểu, null/rỗng và quyền. UI phát event; pages điều phối; data-access gọi HTTP; models giữ kiểu và mapping thuần; shared dùng lại theo trách nhiệm.

| Route | Screen đích | Tham số/kiểu | Kiểm tra | Guard | Entry | Back/exit | Khi sai | Test |
|---|---|---|---|---|---|---|---|---|

Kiểm tra root và route con, tránh scaffold gốc rò sang trang khác. Không tự thêm fallback/redirect. Guard FE chỉ điều hướng, BE là thẩm quyền. Mọi navigation phải chỉ rõ destination và params; không tự gọi history.back nếu không có contract.

## Rà soát 3 vòng

UI: mọi marker và element, trạng thái và responsive theo nguồn. Kỹ thuật: route, auth, DTO, API, data mapping, event branches, race. QA: mỗi rule/element/event, happy/negative/boundary, network, auth, retry, stale khi có nguồn. Mọi thay đổi API cập nhật contract/data/events/tests; UI cập nhật ảnh/elements/events; rule cập nhật rule/event/test. Ghi history trong overview. Thiếu quyết định đánh dấu chặn, không phê duyệt.
