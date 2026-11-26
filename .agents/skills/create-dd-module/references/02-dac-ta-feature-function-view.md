# Đặc tả feature, function và view

## Feature
Mỗi feature là capability có một actor hoặc nhóm actor, giá trị, nguồn, ranh giới, tiền/hậu điều kiện, luồng chính và nhánh lỗi, rule, dữ liệu đọc/ghi, quyền, function/view, phụ thuộc, acceptance và trạng thái. Phân tách feature nếu hành vi có chủ sở hữu, tác động hoặc tiêu chí nghiệm thu độc lập. Ghi trạng thái trước/sau và điều kiện chuyển, không chỉ liệt kê nút bấm.

## Function
Mỗi function/use case mô tả trách nhiệm duy nhất và điều không làm; layer, file, symbol dự kiến, caller/callee, trigger sync/async/job, feature/rule. Input từng field: kiểu, bắt buộc, validation, nguồn, nhạy cảm. Output từng nhánh: success/validation/permission/not found/conflict/system/provider failure nếu áp dụng; không tự thêm mã HTTP. Tiền điều kiện, bất biến, hậu điều kiện thành công và thất bại. Các bước đánh số, dữ liệu đọc/ghi, điều kiện, nhánh lỗi và test. Thuật toán thực tế nếu có tính toán; pseudocode không thay thế contract. Giao dịch, khóa, idempotency, race, retry/timeout/fallback/bù trừ, audit/event/cache, quyền actor/tenant/ownership và log an toàn. Ánh xạ file/import/export và consumer. Mỗi rule hoặc nhánh độc lập có test.

## View
Ghi route hoặc entry point, actor, layout, dữ liệu, các thành phần, state (khởi tạo/tải/thành công/rỗng/lỗi/không quyền/ngoại tuyến nếu nguồn yêu cầu), action/event, guard, function gọi, navigation, focus/keyboard/responsive theo thiết kế. Với mobile, ghi lifecycle, back stack, permission thiết bị, offline/cache/sync và điều kiện khôi phục nếu có nguồn. Không tự gọi DAO/API từ UI. Chọn chiều phụ thuộc theo profile dự án; mobile thường presentation → controller/provider → use case → repository → datasource. BE API và FE screen tuân đúng kiến trúc riêng, không ép cùng một mô hình cho mọi framework.

## Import, sơ đồ, assets
Mỗi file có vai trò, imports/exports, layer, owner, function/view liên quan, nguồn xác nhận; phân biệt dự kiến và tồn tại. Sơ đồ sequence theo call chain, trạng thái theo transition, data flow theo trust boundary; link ID và cập nhật khi contract thay đổi. Ảnh sạch/đánh số ghi provenance, không lấy mockup làm runtime. Assets có mục đích, quyền sử dụng, đường dẫn, không lưu dữ liệu nhạy cảm. History ghi ngày, phiên bản, nguồn quyết định, ID thay đổi, ảnh hưởng và người duyệt nếu có.
