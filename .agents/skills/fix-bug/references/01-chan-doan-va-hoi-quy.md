# Chẩn đoán có giả thuyết và kiểm thử hồi quy

## Hồ sơ tái hiện
| Mục | Nội dung cần ghi |
|---|---|
| Điều kiện | phiên bản, commit, môi trường, actor, dữ liệu giả, config liên quan |
| Thực tế | bước tái hiện, output/error/status, log đã che nhạy cảm |
| Kỳ vọng | DD/AC/contract và nguồn; nếu không có ghi chờ quyết định |
| Phạm vi | tần suất quan sát, chức năng ảnh hưởng, hồi quy từ version nào nếu có bằng chứng |

Không thay đổi production để tái hiện. Nếu lỗi không tái hiện được, giữ trạng thái chưa xác minh và thu thêm dữ kiện phù hợp, không sửa theo cảm tính.

| Giả thuyết | Dự đoán nếu đúng | Phép kiểm tra cô lập | Kết quả | Kết luận |
|---|---|---|---|---|

Trace UI/event → route/transport → auth → validate → query/provider → DB/side effect → response → mapping UI. Phân biệt sai contract, sai implementation, schema lệch, dữ liệu, config, dependency, test hỏng. So sánh commit/diff nếu có; không đổi Git state tùy tiện. Khi lỗi nhiều tầng, kiểm tra lại điểm lắp ghép sau từng sửa. Không sửa nhiều nguyên nhân trong cùng một bước nếu không thể chứng minh riêng.

## Sửa và xác minh

Tạo test đỏ tái hiện đúng nguyên nhân (hoặc lưu bằng chứng tái hiện nếu không thể tạo test); sửa lớp sở hữu trách nhiệm; không swallow exception, bỏ guard, hạ strictness, hoặc đổi expectation để làm test xanh. Chạy lại đúng test, negative cases và suite ảnh hưởng; kiểm tra data side effect, rollback, contract và diff. Nếu test collection fail, ghi nguyên nhân và phạm vi, không báo pass. Bảo vệ thay đổi người dùng. Với lỗi DD/source khác nhau, xác nhận kỳ vọng trước khi đổi behavior. Bàn giao nguyên nhân, bằng chứng trước/sau, file/symbol, test, tác động còn lại, trạng thái và cập nhật context.
