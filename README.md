# Universal Agent Kit V11.0

Bộ công cụ điều phối tác nhân lập trình: kiến trúc, quy tắc, codebase, workflow, skill, kiểm định và nghiệm thu theo bằng chứng.

## Cài đặt

Sao chép `AGENTS.md` và `.agents/` vào thư mục gốc dự án. Nếu dự án đã có chỉ dẫn, hợp nhất điểm vào thay vì ghi đè. Chạy:

```bash
python3 .agents/tools/validate-kit.py
python3 .agents/tools/import-original-skills.py --check
python3 .agents/workflows/tools/build-context.py --refresh
```

## Giao nhiệm vụ

Giao yêu cầu cho coding agent và yêu cầu thực hiện theo `AGENTS.md`. Đọc `.agents/core/task-session.md` để sử dụng công cụ quản lý phiên; ví dụ định tuyến:

```bash
python3 .agents/tools/task.py plan coding-api
```

## Tạo codebase và DD

```bash
python3 .agents/tools/create-codebase.py --destination /duong-dan-moi --profile fastapi-typescript
python3 .agents/workflows/tools/agentkit.py new-dd --type api --id API-002 --slug Mau --output docs/dd --template original
```

Hồ sơ sinh nền hiện hỗ trợ FastAPI, SQLite và TypeScript. Xem `.agents/reference/README.md` để khởi động mã tham chiếu. Chọn template đã được dự án duyệt; không tự áp dụng nghiệp vụ ví dụ của skill nguyên bản. Kiểm định DD về cấu trúc không thay thế phê duyệt nội dung nghiệp vụ.

## Kiểm thử công cụ

```bash
python3 -m unittest discover -s .agents/validators/tests -v
```

Thực hiện kiểm tra và nghiệm thu theo `.agents/core/execution-gates.md` và `.agents/core/engine-limits.md`. Các tuyến chưa có adapter phải giữ trạng thái bị chặn. Sử dụng có giám sát; không xem kết quả kiểm định cơ học là chứng nhận production.
