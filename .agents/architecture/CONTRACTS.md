# API/event contract — nguyên tắc tổng quát

- **Producer:** route/module hay event publisher thật sự.
- **Consumers:** UI/data-access, worker, downstream service; phải kiểm tra caller.
- **HTTP:** method, path, auth, headers, query/body, response, errors, status code, version.
- **Event:** topic, schema, retry, idempotency, ordering, consumer version.
- **Breaking change:** assess compatibility → approve → producer+consumer migration → tests → rollout.

API01 và Screen01 cùng mô tả **một kết nối minh họa**. Không điền URL, field hoặc DB table tùy tiện; dùng DD đã phê duyệt và source thật.
