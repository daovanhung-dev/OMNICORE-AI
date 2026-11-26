# Ma trận kiểm thử và phân cấp bằng chứng

Đọc nguồn DD/AC/hợp đồng, source, test config, fixtures và command thực tế. Tách test plan khỏi execution; mỗi ca có ID, requirement, lớp test, điều kiện, dữ liệu, bước, kỳ vọng quan sát được, tác động phải có/không được có, cleanup, nguồn, ưu tiên và trạng thái thiết kế. Tránh expected mơ hồ hoặc chỉ khẳng định hàm được gọi.

| ID | Yêu cầu | Cấp | Điều kiện/dữ liệu | Bước | Kỳ vọng | Tác động không được có | Cleanup | Nguồn |
|---|---|---|---|---|---|---|---|---|

- Unit: validator, mapper, state machine, business rule thuần; phân lớp tương đương và biên min−1/min/max/max+1, thiếu/null/rỗng theo contract.
- Component: UI state, event/disabled, mapping và lifecycle; fake API chỉ chứng minh component xử lý hợp đồng giả.
- HTTP: route/guard/status/envelope, path/query/body, malformed response, actor khác, object/tenant isolation, không ghi khi từ chối.
- DB/integration: schema/migration thật trên DB thử nghiệm cô lập, bind/constraint, count/list, transaction/rollback, locking/concurrency nếu liên quan; fake session không chứng minh SQL hoặc constraint.
- E2E: từ hành vi người dùng tới dữ liệu và response thật, direct route, state, retry và cleanup; không gọi snapshot là test đã chạy.

Phân tích nhánh quyết định và chuyển trạng thái; với mutation có rollback, test failure ở từng điểm có thể quan sát; idempotency và race chỉ theo requirement. Với lỗi network cần kiểm tra timeout, cancel/late response nếu có contract. Không áp dụng mọi kỹ thuật vào mọi feature; ghi không áp dụng hoặc chờ duyệt khi ngoài scope.

## Chạy và ghi nhận

Dùng fixture cô lập, xác minh target trước ghi; ghi ID và xóa đúng dữ liệu tự tạo, query xác minh cleanup. Không xóa dữ liệu có sẵn. Chạy tập trung rồi suite liên quan, typecheck/build/lint theo profile. Ghi lệnh, version, exit code, tổng pass/fail/skip, log đã che, môi trường và giới hạn. Test không chạy ghi chưa thực thi; lỗi hạ tầng tách khỏi defect; flaky không tự đổi kỳ vọng. Một test pass không chứng minh toàn bộ feature. Khi requirement chưa xác nhận, ca đề xuất không được đánh đạt. Nối UTC Screen khi cần workbook từ DD; test source và test plan là hai artifact khác nhau.
