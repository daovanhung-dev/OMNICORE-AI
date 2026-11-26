# Ví dụ kỹ thuật: giao dịch ghi bản ghi và lịch sử

**Phạm vi:** dữ liệu giả lập để minh họa ma trận và transaction, không phải API thứ hai trong mã chạy tham chiếu và không phải hợp đồng của dự án đích. Giả định ví dụ: bảng `records(id, owner_id, title, version)` và `record_history(id, record_id, old_title, old_version)` có khóa ngoại; actor đã xác thực; chỉ chủ sở hữu được đổi tên; version phải khớp; title sau trim dài 1–80 ký tự. Các giả định chỉ có hiệu lực trong ví dụ.

| Yêu cầu | Điều kiện | Kết quả |
|---|---|---|
| R01 | ID dương; title hợp lệ; version nguyên dương | chuẩn hóa hoặc lỗi 422 |
| R02 | actor là chủ bản ghi | không thấy bản ghi thuộc actor → 404 theo giả định |
| R03 | version khớp | ghi tên và tăng version, sai → 409 |
| R04 | ghi bản ghi và lịch sử cùng thành công | commit, lỗi rollback cả hai |

## Request Usage Matrix
| Trường | Nguồn | Bước | Kiểm tra | Sử dụng | Nhánh lỗi |
|---|---|---|---|---|---|
| id | path | DM-02 | nguyên dương | Q1, M2 | E2 |
| title | body | DM-02 | trim, dài 1–80 | M2, phản hồi | E2 |
| version | body | DM-02 | nguyên dương | DM-04, M2 | E2/E4 |

## Query Matrix
| Query | Bảng | Cột | Điều kiện | Khóa/biến |
|---|---|---|---|---|
| Q1 | records | id | id = bind id | khóa dòng; current |
| Q1 | records | owner_id | owner_id = actor.id | khóa dòng; current |
| Q1 | records | title | như trên | current.title |
| Q1 | records | version | như trên | current.version |

Cú pháp khóa theo DB đã chọn; không xem giả định này là SQL chạy được trên mọi DB. Không có kết quả thì không ghi DB. Không trả thông tin bản ghi của actor khác.

## Mutation Matrix
| ID | Bảng | Cột | Nguồn | Bước | Điều kiện |
|---|---|---|---|---|---|
| M1 | record_history | record_id | current.id | DM-05 | insert 1 hàng |
| M1 | record_history | old_title | current.title | DM-05 | insert 1 hàng |
| M1 | record_history | old_version | current.version | DM-05 | insert 1 hàng |
| M2 | records | title | request.title đã chuẩn hóa | DM-06 | id, owner_id, version khớp |
| M2 | records | version | current.version + 1 | DM-06 | id, owner_id, version khớp |

M1 và M2 thuộc một giao dịch; schema giả định sinh `record_history.id`. Mapping DB trong DD thật cần từng file mapping theo bảng/thao tác; mỗi dòng ghi kiểu/key/null/default và link bước. Các field khác không thay đổi. Không tự gán rowcount hoặc ID giả.

## Response Source Matrix
| Trường | Nguồn | Bước | Kiểu |
|---|---|---|---|
| data.id | current.id | DM-07 | int |
| data.title | giá trị M2 đã xác nhận | DM-07 | string |
| data.version | version mới đã xác nhận | DM-07 | int |

## Data Mapping
1. DM-01: guard xác thực actor; lỗi E1, không đọc tài nguyên bảo vệ.
2. DM-02: validate id/title/version; lỗi E2 trước giao dịch.
3. DM-03: bắt đầu transaction, Q1 với owner scope; không bản ghi E3, rollback/close.
4. DM-04: so version với current.version; khác → E4, rollback/close.
5. DM-05: M1 ghi lịch sử; số hàng không đúng hoặc exception → E5, rollback.
6. DM-06: M2 update đúng khóa/owner/version; 0 hàng → E4, rollback kể cả M1; lỗi DB → E5.
7. DM-07: ánh xạ response hợp lệ, commit; lỗi map/commit → E5, không báo thành công. Giải phóng tài nguyên.
8. DM-08: trả kết quả 200 khi commit thành công. Không có event ngoài DB trong ví dụ.

| Mã | Điều kiện | HTTP | Bước | Tác động | Test |
|---|---|---|---|---|---|
| E1 | chưa xác thực | 401 | DM-01 | không ghi | T1 |
| E2 | đầu vào sai | 422 | DM-02 | không ghi | T2 |
| E3 | không thấy bản ghi của actor | 404 | DM-03 | không ghi | T3 |
| E4 | version xung đột | 409 | DM-04/06 | rollback | T4/T6 |
| E5 | lỗi ghi/map/commit | 500 | DM-05/06/07 | rollback, không lộ SQL | T5/T7 |

T1–T4 kiểm tra auth/validation/ownership/version; T5 làm M2 thất bại sau M1 để xác minh lịch sử rollback; T6 hai writer cùng version chỉ một thành công theo cơ chế DB đã chọn; T7 lỗi commit không trả 200; T8 thành công kiểm tra title/version/history. Các ca này là thiết kế minh họa, chưa thực thi. Retry mutation hoặc idempotency là quyết định riêng, không tự thêm.
