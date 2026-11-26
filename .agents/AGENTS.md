# Quy chuẩn điều phối tác nhân

## 1. Phạm vi và thẩm quyền
Mọi nhiệm vụ phân loại theo `routing.json`; đọc `context-map.md`, `project/PROJECT.md`, `project/STATE.md`, `rules/shared.md`, `core/agent-control.md` trước khi đọc sâu. Yêu cầu được duyệt và hợp đồng hiện hành là nguồn hành vi mong muốn; mã nguồn và kết quả chạy thật là nguồn hiện trạng. Không tự hòa giải mâu thuẫn. Chỉ áp dụng kiến trúc mới cho phần được phép tạo; kho mã hiện hữu giữ quy ước đã được duyệt.

## 2. Chu trình bắt buộc
1. Phân loại nhiệm vụ chính/phụ, xác định phạm vi BE/FE/DB/hạ tầng và phụ thuộc chéo.
2. Lập nhật ký, khai báo `READ_PLAN` (đường dẫn, đoạn cần đọc, lý do). Đọc tối đa ba nhật ký mới nhất cùng loại; ghi số lượng thiếu. Không tìm kiếm ngoài phạm vi đã khai báo.
3. Đọc kiến trúc, quy tắc, workflow, skill theo registry; đối chiếu nguồn thật, BD, DD, danh mục màn hình/API, sơ đồ và hợp đồng. Thêm đường dẫn mới vào kế hoạch đọc trước khi mở.
4. Lập `LEAF_TARGET_PLAN` trước khi thay đổi, mỗi mục tiêu có một thao tác, tiêu chí nghiệm thu, bằng chứng. Cập nhật `target.md`.
5. Truy vết từ điểm gọi đến điểm được gọi, xác thực/quyền, dữ liệu, giao dịch, phản hồi và kiểm thử. Chỉ sửa trong phạm vi cần thiết; bảo toàn thay đổi người dùng.
6. Thực thi quy trình đúng loại. Chạy kiểm thử phù hợp được phép; không ghi nhận đạt nếu chưa chạy. Review chỉ đọc, không chạy kiểm thử hoặc sửa mã.
7. Làm mới hồ sơ dự án, kiểm tra định tuyến, ghi bằng chứng và trở ngại; hoàn tất từng mục tiêu rồi xóa hàng đã đạt khỏi bảng đang hoạt động.

## 3. Quy tắc nạp ngữ cảnh
- Tác vụ BE: `rules/backend.md`, `architecture/BE-FE.md`, `codebase/backend.md`, DD/API và nguồn liên quan.
- Tác vụ FE: `rules/frontend.md`, `architecture/BE-FE.md`, `codebase/frontend.md`, danh mục màn hình/API, toàn bộ DD màn hình và ảnh.
- Tác vụ tạo nền: `skills/create-codebase/SKILL.md`, `codebase/symbol-contract.md`, workflow tạo nền; phải xác định công nghệ, phụ thuộc và hợp đồng trước khi tạo.
- Tác vụ xuyên lớp: đọc cả bên cung cấp và tiêu thụ; không tự thêm trường, endpoint, bảng, quyền hoặc mã lỗi.
- Chỉ khảo sát toàn bộ kho mã khi nhiệm vụ là kiểm kê toàn diện. Khi kiểm kê, công cụ tĩnh không thay cho đọc thân hàm và xác minh hành vi.

## 4. Điều kiện kết thúc
Kiểm thử đơn vị, tích hợp, giao diện và triển khai là các mức chứng cứ riêng. Không biến dữ liệu giả hoặc ảnh thiết kế thành chứng cứ chạy thật. Tệp tồn tại không chứng minh đã kết nối runtime. Thực thi `python3 .agents/tools/validate-kit.py`; khi có thay đổi mã nguồn, chạy `python3 .agents/workflows/tools/build-context.py --refresh` rồi `--check` và cập nhật kiểm kê biểu tượng. Nếu một cổng bị chặn, giữ trạng thái tương ứng, không báo hoàn tất giả.

## 5. Cổng theo hồ sơ công nghệ

Nạp `context-manifest.json` và hồ sơ công nghệ được duyệt. Chạy bộ kiểm định kiến trúc với đường dẫn BE/FE rõ ràng nếu hồ sơ có adapter. Với hồ sơ chưa có adapter, ghi chưa kiểm định tự động, thực hiện review quy tắc và kiểm thử phù hợp. Không dùng kết quả kiểm định tài liệu thay cho mã nguồn.

## 6. Điều phối thực thi có bằng chứng (V11)
Đọc `core/execution-gates.md` và `core/task-session.md`. Dùng `tools/task.py plan <tuyến>` để lấy read-set, `begin` để tạo phiên, khai báo nguồn trước khi mở nội dung; các tuyến có `original_skills` phải đọc nguyên bản theo `core/original-skills.md` cùng adapter. Không chọn skill chỉ vì có file. Mọi thao tác review giữ ranh giới chỉ đọc. Nếu kho đích chưa xác định công nghệ hoặc thiếu source, ghi trạng thái và không tự tạo nghiệp vụ. Sau coding/fix chạy cổng phù hợp, dùng phiên SQLite và receipt của adapter theo core/task-session.md; không dùng evidence tự khai hoặc argv tùy ý. Không coi tool session hoặc validator tĩnh là bằng chứng tự động về nghiệp vụ.
