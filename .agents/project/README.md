# Project — living context của repository thực tế

**Phân biệt rõ:** [`architecture/`](../architecture/README.md) là **kiến trúc ví dụ dùng lại** (1 API và 1 screen); `project/` là **trạng thái hiện tại có bằng chứng của source repository đã cài kit**. Không dùng ví dụ thành sự thật của repo.

## Sơ đồ

```text
project/
├── README.md             # Hướng dẫn đọc/sync trạng thái dự án
├── STATE.md              # Trạng thái snapshot: commit/branch, số file, delta, độ phủ
├── PROJECT.md            # Profile, boundaries, stack/entrypoints được người dùng xác minh
├── PROJECT_STRUCTURE.md  # Tóm tắt cây source hiện có + deployable candidates
├── COVERAGE.md           # Tỷ lệ file đã lập context và mức bằng chứng
├── SOURCE_MAP.json       # Tạo khi quét repo: đường dẫn thật -> Markdown
├── CHANGES.md            # Lịch sử cập nhật context, không phải git history
├── archive/              # Chỉ tạo khi file source bị xóa/đổi tên; bảo toàn note cũ
└── tree/                 # Chỉ tạo khi quét repo thực, mirror chính xác path source
    ├── README.md         # Tổng quan root source
    └── <folder thực>/
        ├── README.md     # Trách nhiệm/child links/file ownership
        └── <file>.md     # Source role, symbol/import, checksum, bằng chứng, ghi chú
```

## Cách sử dụng

```bash
# Chưa khởi tạo: kiểm tra trước, sau đó sinh cây thật
python3 .agents/workflows/tools/build-context.py --dry-run
python3 .agents/workflows/tools/build-context.py

# Trước khi code: xem source đã thay đổi ngoài context chưa
python3 .agents/workflows/tools/build-context.py --check

# Sau khi code/test: cập nhật context và ghi chép delta
python3 .agents/workflows/tools/build-context.py --refresh
python3 .agents/workflows/tools/build-context.py --check
python3 .agents/workflows/tools/agentkit.py validate
```

**Quy tắc cập nhật:** Khi bắt đầu task cần đọc `STATE.md` + các `tree/<scope>/README.md`, `PROJECT.md`, `.md` của file liên quan, và source thật. Khi kết thúc task coding/fix/contract/test có thay đổi file, phải chạy `--refresh`, bổ sung ghi chú kiểm chứng và xác nhận `--check` không báo drift. Không tự chạy ngầm, cron hoặc Git hooks; agent cần thực hiện bước này theo workflow.

**Mapping**: `.py` thành `.md` nếu không collision (`view.py` → `view.md`); `.ts/.tsx/.html/.css` thêm `.md` (`page.tsx` → `page.tsx.md`); source `README.md` thành `README.source.md`. Mỗi source file có một trang; mỗi thư mục có `README.md`. Không sao chép toàn bộ code/secret vào tài liệu.

**An toàn:** Script chỉ đọc file nguồn và ghi `.agents/project/`; bỏ qua `.git/`, `.agents/`, cache, symlink, file ignore. Secret chỉ được ghi metadata path, không đọc nội dung. File bị xóa/đổi tên được **lưu bản note cũ ở `archive/`**, không xóa âm thầm. Các giả định runtime vẫn `NOT_VERIFIED` nếu chưa chạy test/tracing.

**Strict-profile:** `project/PROJECT.md` có `verification_status: UNREVIEWED` ban đầu. Chỉ chuyển thành `SOURCE_REVIEWED` sau khi đã đối chiếu code + ownership/entrypoint/contract và ghi evidence vào bảng manual; đây không phải chứng nhận runtime/deployment.
