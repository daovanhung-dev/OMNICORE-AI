# Ví dụ đối chiếu hoàn chỉnh cho API đọc trong bộ tham chiếu

Nguồn: [DD API](../../../reference/backend/docs/dd/API-001/02-overview.md), [models](../../../reference/backend/app/modules/shared/api_001_items_list/models.py), [validate](../../../reference/backend/app/modules/shared/api_001_items_list/validate.py), [query](../../../reference/backend/app/modules/shared/api_001_items_list/query.py), [view](../../../reference/backend/app/modules/shared/api_001_items_list/view.py). Đây là phân tích một API tham chiếu, không phải nghiệp vụ của dự án đích.

| Yêu cầu | Nguồn | Bước | Ca kiểm thử |
|---|---|---|---|
| R01: page mặc định 1, 1–100000 | 03-request | DM-01/02 | thiếu, 0, 100001, chữ |
| R02: page_size mặc định 20, 1–100 | 03-request | DM-01/02 | thiếu, 0, 101 |
| R03: đếm và danh sách theo ID | 05-data-mapping | DM-03 | trang đầu, trang sau, trang rỗng |
| R04: lỗi không lộ SQLite | 06-errors | DM-04 | DB lỗi → 503 |

| Request | Kiểu chuẩn hóa | Sử dụng | Lỗi |
|---|---|---|---|
| page | int | offset=(page−1)×page_size, data.page | INVALID_PAGE |
| page_size | int | LIMIT, offset, data.page_size | INVALID_PAGE |

| Query | Bảng | Cột/aggregate | WHERE | ORDER | Phân trang |
|---|---|---|---|---|---|
| COUNT_ITEMS | items | COUNT(*) | không | không | không |
| LIST_ITEMS | items | id | không | id ASC | LIMIT/OFFSET bind |
| LIST_ITEMS | items | name | không | id ASC | LIMIT/OFFSET bind |

Mutation: không áp dụng (API chỉ đọc). Không sinh file ghi bảng.

| Response | Nguồn | Quy tắc |
|---|---|---|
| data.items | LIST_ITEMS | mảng rỗng hợp lệ |
| data.items[].id | items.id | số nguyên |
| data.items[].name | items.name | chuỗi |
| data.total | COUNT_ITEMS | số nguyên |
| data.page | page đã chuẩn hóa | số nguyên |
| data.page_size | page_size đã chuẩn hóa | số nguyên |

Luồng: chuẩn hóa → validate (422 dừng) → đọc DB → đếm/list → map → trả 200; lỗi SQLite 503, đóng kết nối. Không tự thêm xác thực cho ví dụ công khai. Test source: [test_items.py](../../../reference/backend/tests/test_items.py). Đây không phải tuyên bố đã kiểm thử lại runtime ở lần bổ sung context này.
