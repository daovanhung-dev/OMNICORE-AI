# Cổng thực thi và nghiệm thu

| Cổng | Bằng chứng tối thiểu | Nếu chưa đạt |
|---|---|---|
| G0 Phạm vi | yêu cầu, tuyến, owner, phiên bản, baseline dirty diff, quyền | dừng thao tác ngoài phạm vi |
| G1 Ngữ cảnh | READ_PLAN, file/đoạn đã đọc, cùng loại worklog tối đa 3, skill nguyên bản nếu có | SOURCE_REQUIRED hoặc CONTEXT_STALE |
| G2 Hợp đồng | expected/current tách riêng, API/Screen/DB trace, conflict | DISCREPANCY, chỉ làm phần độc lập |
| G3 Kế hoạch | target lá, tệp thay đổi, tiêu chí, test và rollback khi cần | không sửa trước khi xác định |
| G4 Thực thi | diff nhỏ, trách nhiệm lớp, không phá dữ liệu, không secret | sửa hoặc ghi blocker |
| G5 Xác minh | focused test, build/typecheck, scope tests, validator, runtime phù hợp | NOT_RUN / DECLARED_NOT_RUNNABLE / FAIL |
| G6 Bàn giao | diff, source/contract update, evidence từng target, cleanup, context check | không báo hoàn thành nếu cổng bắt buộc chưa đạt |

## Bằng chứng theo loại nhiệm vụ

- Coding API: kiểm tra registration, auth trước đọc bảo vệ, query bind, happy/error, rollback, response schema. Mutation: test trạng thái trước/sau và failure giữa bước. Test fake DB không chứng minh schema live.
- Coding Screen: full DD 8 phần và ảnh, marker/event/route/API matrix, reuse check, browser và cleanup fixture nếu dùng DB. Ghi từng event chưa thử. Không dùng ảnh design làm runtime.
- Fix: tái hiện trước, giả thuyết có bằng chứng, điểm lỗi thực tế, regression sau. Không đổi contract cho khớp implementation.
- DD/UTC: kiểm tra structure, traceability, từng field/event, source gaps, approval riêng. Test chưa chạy phải để trống kết quả thực tế.
- Review: đọc diff/source/test source, không sửa code, không chạy kiểm thử/build/linters hoặc đăng review từ xa. Chỉ lỗi có vị trí, kịch bản reachable, ảnh hưởng và hướng xử lý. Không tự review độc lập sau coding.
- Context: baseline và final validator, so sánh lỗi theo rule/path; baseline lỗi không phải PASS. Không mở rộng sửa unrelated.

Chỉ lệnh đã chạy có exit status thực mới được gọi là đã chạy. Exit 0 không chứng minh chất lượng nếu lệnh kiểm tra sai phạm vi. Cổng tĩnh, runtime, thiết bị, schema live và triển khai là trục riêng. Người dùng quyết định ngoại lệ nghiệp vụ; không hạ cổng để đạt điểm.
