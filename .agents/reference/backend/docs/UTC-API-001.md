# Ma trận kiểm thử API
| Mã | Điều kiện | Kỳ vọng | Mã kiểm thử |
|---|---|---|---|
| API-T01 | GET mặc định | 200; ID 1,2 | test_success |
| API-T02 | page=2,size=1 | ID 2 | test_pagination |
| API-T03 | Trang vượt dữ liệu | Mảng rỗng | test_empty |
| API-T04 | Query sai (6 biến thể) | 422; INVALID_PAGE | test_invalid |
| API-T05 | DB vắng | 503; DATA_UNAVAILABLE | test_missing_db |
| API-T06 | Query sai, DB vắng | 422 trước DB | test_invalid_precedes_db |
| API-T07 | Seed vào tệp đã có | Không ghi đè | test_seed_no_overwrite |
