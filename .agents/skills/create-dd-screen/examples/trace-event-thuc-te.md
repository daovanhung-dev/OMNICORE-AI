# Ví dụ truy vết sự kiện phân trang

Nguồn: [DD màn hình](../../../reference/frontend/docs/dd/SH-01/02-events.md), [page](../../../reference/frontend/src/app/features/shared/SH01/pages/item-page.ts), [UI](../../../reference/frontend/src/app/features/shared/SH01/ui/item-list.ts), [data-access](../../../reference/frontend/src/app/features/shared/SH01/data-access/item.service.ts). Không gán marker vì tài liệu mẫu không có ảnh đã xác minh.

| Thành phần | Event | Dữ liệu | API | Kỳ vọng/ca |
|---|---|---|---|---|
| EL-04 Trước | EV-02 | page hiện tại | GET danh sách | giảm trang nếu có, TC-03 |
| EL-05 Tiếp | EV-03 | page hiện tại, total | GET danh sách | tăng trang nếu có, TC-02 |
| EL-06 Tải lại | EV-04 | trang hiện tại | GET danh sách | lỗi/khôi phục, TC-04/05 |

Với EV-03, kiểm tra có trang kế; pages điều phối request cho page tiếp; models kiểm tra dữ liệu nhận; UI hiển thị danh sách hoặc trạng thái phù hợp; không tự thay URL/hợp đồng. Đối chiếu triển khai thực tế khi giao task coding; đây không phải kết quả chạy browser. [Ca DD](../../../reference/frontend/docs/dd/SH-01/07-test-cases.md) và [UTC JSON](../../../reference/frontend/docs/UTC-SH-01.json) là kế hoạch truy vết, không phải bằng chứng đã chạy.
