# Kiến trúc tái sử dụng — chỉ một API và một Screen minh họa

Bộ tài liệu này là **template độc lập**, không gắn với bất kỳ sản phẩm hay tổ chức nào. Cây ví dụ **không phải source thực**.

## Ba phần cần phân biệt

| Phần | Mục đích | Bằng chứng |
|---|---|---|
| [`apps/server/`](apps/server/README.md) | Mô tả cấu trúc backend Python, gồm **một API `module1/api01`** | `TEMPLATE_ONLY` |
| [`apps/client/`](apps/client/README.md) | Mô tả cấu trúc frontend TypeScript, gồm **một screen `module1/screen01`** | `TEMPLATE_ONLY` |
| `../project/tree/` (chưa có khi phát hành) | Trạng thái repo hiện hành + cây file/folder đối ứng | Sinh bằng `build-context.py`, kiểm chứng theo source |

**Không chứa bộ tài liệu nguồn khổng lồ hay nhiều API/screen giả định.** Bộ kit không mặc định FastAPI/Angular: Python và TypeScript chỉ là một cặp minh họa để giải thích nhiệm vụ file; dự án đích có thể dùng bất kỳ stack và layout nào.

## Điều hướng tài liệu

- [Cây minh họa](REFERENCE_STRUCTURE.md) và [mô tả cấu trúc](PROJECT_STRUCTURE.md)
- [SERVER.md](SERVER.md), [CLIENT.md](CLIENT.md): trách nhiệm API/UI
- [SYSTEM.md](SYSTEM.md), [DATABASE.md](DATABASE.md), [CONTRACTS.md](CONTRACTS.md), [INFRASTRUCTURE.md](INFRASTRUCTURE.md), [SECURITY_TESTING.md](SECURITY_TESTING.md)
- [EXAMPLE_MAP.json](EXAMPLE_MAP.json): ánh xạ mỗi file nguồn **mẫu** tới `.md` tương ứng
- [PROJECT.md](PROJECT.md): **chỉ là form tham khảo**, trạng thái đích xem [`project/PROJECT.md`](../project/PROJECT.md)

## Khi cài vào repo mới

```bash
python3 .agents/workflows/tools/build-context.py --dry-run
python3 .agents/workflows/tools/build-context.py
python3 .agents/workflows/tools/agentkit.py validate
```

Kết quả sinh `.agents/project/tree/` với một `README.md` trên mỗi folder có thật, và một Markdown trên mỗi file source có thật. Không áp tên folder, framework, số lượng API hoặc màn hình của template lên repo đích.

**Quy tắc:** không lưu tình trạng thực tế ở `architecture/`; mọi snapshot và notes nguồn thuộc [`project/`](../project/README.md).
