# Áp dụng UTC vào gói DD tham chiếu

Nguồn trung lập có sẵn: [Tổng quan](../../../reference/frontend/docs/dd/SH-01/00-overview.md), [Thành phần](../../../reference/frontend/docs/dd/SH-01/01-ui-elements.md), [Sự kiện](../../../reference/frontend/docs/dd/SH-01/02-events.md), [Data flow](../../../reference/frontend/docs/dd/SH-01/03-data-flow.md), [API](../../../reference/frontend/docs/dd/SH-01/04-api-integration.md), [Rule](../../../reference/frontend/docs/dd/SH-01/05-business-rules.md), [Điều hướng](../../../reference/frontend/docs/dd/SH-01/06-navigation.md), [Kế hoạch ca](../../../reference/frontend/docs/dd/SH-01/07-test-cases.md). [UTC JSON](../../../reference/frontend/docs/UTC-SH-01.json) và [workbook](../../../reference/frontend/docs/UTC-SH-01.xlsx) là ví dụ đã có trong bộ tham chiếu; không gán kết quả thực thi từ tài liệu. Ảnh mẫu chưa xác minh; không tự gán marker.

## Truy vết theo ba tầng

| Tầng | Đơn vị kiểm tra | Ví dụ tình huống |
|---|---|---|
| Toàn màn | yêu cầu entry/state/layout | mở route, lỗi dữ liệu, rỗng |
| Thành phần | từng ID EL, thuộc tính/state | nút Trước/Tiếp theo điều kiện trang |
| Sự kiện | từng EV và từng nhánh | tải lại lỗi, tải lại khi API hồi phục |

Mỗi case yêu cầu nguồn file+mục, mã yêu cầu, đối tượng, tiền điều kiện, dữ liệu, bước tuần tự, expected độc lập và kiểm chứng được, API, độ ưu tiên và trạng thái DD. Mỗi đích navigation khác nhau tách case; không mặc định click/Enter/hover. Với rule có biên, dùng lớp tương đương và giá trị sát biên nếu contract quy định. Với race, định nghĩa hai request và thứ tự response, không gán ca đã xác nhận nếu DD không có rule. Ca thiếu DD phải ghi Chờ xác nhận, kết quả thực tế để trống. Kiểm tra requirement→test và test→requirement; tỷ lệ coverage ID không chứng minh coverage branch hoặc đã chạy.

## Thực thi công cụ

Đọc schema và bốn tài liệu trong `huong-dan/`. Trích xuất ngữ nghĩa bằng agent từ DD, không coi script giải nén/sinh workbook tự hiểu DD. Chạy kiểm tra JSON, sinh Excel, kiểm tra cấu trúc và mở workbook rà soát. Ghi lỗi công cụ, blocker, phiên bản và trạng thái review. Khi DD mới mâu thuẫn với runtime, giữ bằng chứng hai phía và đánh dấu ca liên quan, không thay expected theo source nếu chưa được duyệt.
