# Quy tắc lập trình ứng dụng khách

## FE-01 — Ranh giới màn hình
`features/<nhom>/<ma>/{data-access,models,pages,ui}` là bốn thư mục trực tiếp; không có thư mục thứ năm. Mỗi nhóm có một tệp tuyến và một khung chứa vùng hiển thị tuyến con. ID theo danh mục; kiểm thử URL gốc và truy cập trực tiếp. Không suy quyền từ tên tuyến. Thành phần dùng nhiều màn hình đặt trong `shared/ui`; hộp thoại riêng trong `ui` của màn hình.

## FE-02 — Mô hình
`models` khai báo kiểu API/màn hình, enum, giá trị đã duyệt, ánh xạ/lọc/sắp xếp/chuyển đổi thuần. Không gọi HTTP, DOM, lưu trữ, điều hướng hoặc biến đổi trạng thái toàn cục. Phân biệt dữ liệu thô và mô hình hiển thị; giữ đúng null, tùy chọn, kiểu và đơn vị; không bịa trường.

## FE-03 — Truy cập dữ liệu
`data-access` sở hữu dịch vụ API, method/path/query/body, ánh xạ lỗi, hủy yêu cầu và xử lý kết quả cũ. Dùng HTTP core và phiên xác thực được duyệt; không phân tán URL gốc, token hoặc lặp yêu cầu. Không gọi DB từ trình duyệt, không giả thành công. Endpoint chưa nối phải được đánh dấu, không gửi request tùy đoán. Chính sách lưu token theo thiết kế bảo mật.

## FE-04 — Trang và thành phần
`pages` sở hữu vòng đời, trạng thái tải/thành công/rỗng/lỗi/chưa xác thực, biểu mẫu, sự kiện, điều phối dịch vụ, điều hướng, dọn đăng ký. `ui` nhận đầu vào có kiểu, phát ý định có kiểu, xử lý hiển thị cục bộ; không truy cập API trực tiếp. Mẫu HTML chỉ liên kết dữ liệu và ngữ nghĩa truy cập; CSS dùng token, responsive và phạm vi phù hợp. Không đặt nội dung tuyến riêng ở ngoài vùng hiển thị tuyến gốc. Kiểm tra biểu mẫu phía FE phục vụ UX; máy chủ quyết định quyền và dữ liệu.

## FE-05 — Thiết kế có nguồn
Đọc danh mục màn hình/API, toàn bộ DD 00–07, ảnh sạch/đánh số, bản đồ marker và HTML thiết kế. Mở ảnh trực quan. Lập truy vết marker → thành phần → sự kiện → dữ liệu → API → trạng thái → điều hướng → ca kiểm thử. Mâu thuẫn giữa tài liệu, ảnh và nguồn phải được ghi; không sao chép HTML thiết kế thành mã chạy thật hoặc tự tạo hành vi. Khi phụ thuộc bị chặn, chỉ thực hiện phần độc lập có nguồn, khóa thao tác phụ thuộc.

## FE-06 — Kiểm thử
Kiểm thử URL gốc/tuyến trực tiếp, phiên/guard, từng sự kiện và trạng thái, bàn phím, khả năng tiếp cận, kích thước hiển thị, dữ liệu sai, hủy và lỗi mạng. Chạy ứng dụng thật và kiểm tra trong trình duyệt/thiết bị khi có thể. Dữ liệu giả chỉ trong DB thử nghiệm cô lập; lưu ID, xóa đúng ID theo thứ tự phụ thuộc và xác minh đã dọn. Không coi ảnh hay máy chủ dev chạy là chứng cứ chức năng hoạt động.

## Mã kiểm định tự động

FE-001: bốn thư mục; FE-005: tác động phụ trong models; FE-006: HTTP và phụ thuộc data-access sai lớp; FE-008: route/layout nhóm; FE-010: phụ thuộc ngược vào features. Sai: `ui` gọi `fetch`; đúng: phát sự kiện, page gọi data-access. Sai: core nhập page; đúng: page nhập core qua interface đã duyệt. Kiểm định tĩnh không thay review hành vi.

## FE-07 — Ranh giới dữ liệu và import
Dữ liệu thô được giữ ở data-access; models thực hiện chuyển đổi theo contract. UI không nhập router, core, data-access hoặc screen khác; pages không gọi HTTP trực tiếp; core/shared/layout không nhập implementation feature; screen không import trực tiếp screen khác. Shared chỉ chứa thành phần thực sự dùng lại, không di chuyển vì giả thuyết tái sử dụng. Với React/Flutter đã tồn tại, ánh xạ trách nhiệm theo hồ sơ đã xác minh thay vì di chuyển thư mục hàng loạt. Giữ route gốc, direct URL, fallback và guard theo yêu cầu có nguồn. Không coi sự hiện diện của route là quyền truy cập.
