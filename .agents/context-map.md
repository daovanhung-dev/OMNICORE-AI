# Bản đồ ngữ cảnh

`AGENTS.md` gốc → `.agents/AGENTS.md` → `routing.json` + `core/agent-control.md` → hồ sơ dự án → nhật ký cùng loại → quy tắc → kiến trúc → workflow → skill → nguồn/DD/kiểm thử → chứng cứ.

| Ngữ cảnh | Nguồn chính |
|---|---|
| Quy tắc BE/FE | `rules/backend.md`, `rules/frontend.md` |
| Kiến trúc từng lớp | `architecture/BE-FE.md`, `architecture/apps/` |
| Nền tảng | `codebase/backend.md`, `codebase/frontend.md`, `codebase/symbol-contract.md` |
| Hợp đồng, cơ sở dữ liệu, hạ tầng | `architecture/CONTRACTS.md`, `DATABASE.md`, `INFRASTRUCTURE.md` |
| Định tuyến nhiệm vụ | `routing.json` |
| Tài nguyên chuyên môn | `skills/INDEX.md` |
| Trạng thái kho mã | `project/PROJECT.md`, `project/STATE.md`, `project/tree/` (sinh theo nguồn thật) |

Không có đường dẫn nào trong kiến trúc mẫu được coi là nguồn đã tồn tại của dự án đích. Kiểm tra hồ sơ và cấu hình thực tế trước khi áp dụng.

## Luồng V10

Định tuyến trả về `original_skills` cùng skill adapter; nạp thư viện nguyên bản theo `core/original-skills.md`, kiểm tra `original-skills.json` và đọc tài nguyên bắt buộc. `core/task-session.md` quy định công cụ phiên; `core/execution-gates.md` quy định cổng bằng chứng theo loại nhiệm vụ. Không đưa nguyên trạng nghiệp vụ ví dụ gốc vào `project/`.
