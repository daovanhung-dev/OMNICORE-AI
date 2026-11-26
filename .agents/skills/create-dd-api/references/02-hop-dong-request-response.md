# Quy chuẩn trường đầu vào và phản hồi

## Request

Mỗi trường một dòng, kể cả trường con trong mảng, dùng đường dẫn `items[].name`. Phân biệt header, path, query, body, cookie, claim và biến nội bộ: claim hoặc biến từ DB không phải body client. Ghi kiểu truyền trên dây và kiểu sau chuẩn hóa, bắt buộc, cho phép null/rỗng, mặc định, đơn vị, độ dài, enum, biên, format, điều kiện kết hợp, ví dụ, nguồn và mã lỗi. Mặc định chỉ dùng khi thiếu, không tự thay giá trị sai bằng mặc định. Không có body ghi rõ không áp dụng; không thêm trường vì template có hàng trống. Mỗi trường phải truy đến kiểm tra, truy vấn, mutation, nhánh hoặc phản hồi; trường không dùng là chênh lệch cần giải quyết.

| Đường dẫn trường | Vị trí | Kiểu truyền | Kiểu chuẩn hóa | Bắt buộc | Null/rỗng | Mặc định | Ràng buộc | Nguồn | Bước | Lỗi |
|---|---|---|---|---|---|---|---|---|---|---|

JSON ví dụ có một property mỗi dòng; ví dụ thành công, tối thiểu, biên và lỗi chỉ khi hữu ích. Không dùng dấu ba chấm trong khối JSON hợp lệ. Không để dữ liệu thật, token hoặc khóa bí mật.

## Response

Mỗi đường dẫn bao gồm cả envelope, mảng, phần tử và metadata; nêu cardinality. Mỗi field chỉ có một nguồn hoặc phép biến đổi rõ ràng: cột DB, request đã chuẩn hóa, claim, hằng theo contract, generator, aggregate, API khác. Với trường suy dẫn ghi công thức, làm tròn, null/empty và chính sách khi nguồn lỗi. Không nhầm `[]` với `null`, 200 với 204, singleton với `Page<T>`, hoặc mã nghiệp vụ với HTTP. Ghi các trường được loại bỏ vì quyền hoặc dữ liệu nhạy cảm; không lộ exception/SQL nội bộ. Khi mutation trả dữ liệu vừa ghi, xác minh projection và serialization trước commit nếu phù hợp; không báo thành công trước commit.

| Đường dẫn trường | Kiểu | Bắt buộc/null | Nguồn | Phép đổi | Bước | Giá trị rỗng | Giới hạn quyền | Ví dụ |
|---|---|---|---|---|---|---|---|---|

## Lỗi

| Mã lỗi | Điều kiện chính xác | Bước | HTTP | Mã nghiệp vụ | Field | Phản hồi an toàn | Ưu tiên | DB/tác động | Test |
|---|---|---|---|---|---|---|---|---|---|

Mỗi nhánh lỗi một hàng. Trình tự ưu tiên lỗi theo hợp đồng; xác thực trước truy xuất bảo vệ, không dò rỉ tồn tại tài nguyên. Lỗi validation không ghi DB, lỗi sau khi ghi rollback; lỗi ngoại hệ thống không giả định rollback DB đảo được side effect. Định nghĩa retry/idempotency khi có nguồn, không mặc định retry mutation. Mọi mã lỗi phải có nguồn catalog/contract hoặc được ghi đề xuất. Mọi nhánh trong Data Mapping link đúng lỗi; lỗi không đến được từ bước nào cần bỏ hoặc xác minh.
