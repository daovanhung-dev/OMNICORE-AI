# Ánh xạ dữ liệu — __ID__

## 1. Nhận dữ liệu, xác thực và phân quyền
| Bước | Biến/claim | Nguồn | Kiểu | Điều kiện | Chủ xử lý | Nhánh/lỗi |
|---|---|---|---|---|---|---|
| DM-01 | TBD | TBD | TBD | TBD | TBD | TBD |

## 2. Kiểm tra đầu vào
| Bước | Trường | Chuẩn hóa | Điều kiện | Khi sai | Mã lỗi |
|---|---|---|---|---|---|
| DM-02 | TBD | TBD | TBD | TBD | TBD |

## 3. Truy vấn
| ID | Mục đích | Bảng/alias | Cardinality | Biến kết quả | Bước |
|---|---|---|---|---|---|
| Q-01 | TBD | TBD | TBD | TBD | TBD |

| ID truy vấn | Bảng/alias | Cột chọn | Kiểu/null | Biến đích |
|---|---|---|---|---|
| Q-01 | TBD | TBD | TBD | TBD |

| ID truy vấn | Bảng nối | Kiểu nối | Điều kiện | Cardinality |
|---|---|---|---|---|
| Q-01 | TBD | TBD | TBD | TBD |

| ID truy vấn | Mệnh đề | Điều kiện/cột | Nguồn tham số | Khi áp dụng |
|---|---|---|---|---|
| Q-01 | TBD | TBD | TBD | TBD |

## 4. Nhánh kết quả, thay đổi dữ liệu và giao dịch
| Bước | Điều kiện | Hành động | Mutation ID/mapping | Kết quả | Bước tiếp/lỗi |
|---|---|---|---|---|---|
| DM-04 | TBD | TBD | TBD | TBD | TBD |

Giao dịch, khóa, kiểm tra số hàng, commit/rollback, idempotency, side effect và giải phóng tài nguyên: TBD hoặc không áp dụng có lý do.

## 5. Ánh xạ và phản hồi
| Bước | Biến/cột nguồn | Trường đích | Phép đổi | Null/rỗng | Nhánh |
|---|---|---|---|---|---|
| DM-05 | TBD | TBD | TBD | TBD | TBD |

Tham chiếu: [Yêu cầu](03-request.md), [Phản hồi](04-response.md), [Lỗi](06-errors.md), [DB](07-db-mapping.md).
