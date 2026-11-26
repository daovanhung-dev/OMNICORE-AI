---
name: create-dd-module
description: Tạo thiết kế chi tiết module.
---
# Tạo thiết kế chi tiết module

Kích hoạt chuyển BD/BRD/luồng sản phẩm thành DD module. Đọc nguồn nghiệp vụ, chủ sở hữu, đối tượng, vai trò, mục tiêu, phạm vi, trạng thái. Phân rã Feature ID → Function/API/Rule → View → Source/Import → Test. Mô tả bất biến, luồng chính/nhánh/lỗi, thực thể, quyền, dữ liệu và phụ thuộc; sơ đồ chỉ khi có căn cứ. Tách yêu cầu được duyệt, đề xuất, giả định và câu hỏi mở (chủ, tác động, quyết định). Tách trạng thái quyết định thiết kế, hiện thực, xác minh. Không đưa bí mật hoặc dữ liệu thật. Sinh gói `README.md`, `Overall.md`, `List_Features.md`, `Function_List.md`, `Views.md`, `Import_File.md`, `diagrams/README.md`, `assets/README.md`, `history/CHANGELOG.md` bằng `new-dd --type module`. Nghiệm thu khi truy vết từng feature/function/view, điều kiện, dữ liệu, kiểm thử và lịch sử; không code runtime trong tác vụ DD.

## Tài nguyên
Đọc `references/`, `checklists/`, `examples/` và `templates/` nếu có trong phạm vi nhiệm vụ.

## Tài liệu bắt buộc

Đọc [phân tích nguồn và trạng thái](references/01-phan-tich-nguon-va-trang-thai.md), [đặc tả feature/function/view/import](references/02-dac-ta-feature-function-view.md), [cổng nghiệm thu](references/03-cong-nghiem-thu-module.md), rồi mở đủ mẫu. Viết Overall trước, sau đó Features → Functions → Views → Import → sơ đồ/tài nguyên/lịch sử. Bảng registry không thay thế khối hợp đồng chi tiết từng function. Với thiết kế mobile, đọc profile Flutter hoặc profile thực tế đã duyệt; không tự thêm công nghệ. Ghi đầy đủ bốn trục trạng thái và câu hỏi mở. Không code runtime trong task thiết kế.
