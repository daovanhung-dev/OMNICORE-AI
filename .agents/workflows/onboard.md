# Quy trình — Onboard mọi loại dự án và xây dựng Agents Context

**Trigger:** chưa có context nguồn, có repository mới, thay đổi lớn kiến trúc/branch, hoặc cần cập nhật source mirror.

## O0. Tiền kiểm (read-only)

1. Xác nhận root dự án, `git status --short --branch`, file manifest, README, hướng dẫn agent/rules đang tồn tại; không thay đổi source.
2. Xác định các package/deployable thực (monorepo, single-app, library, frontend, backend, mobile, CLI, worker, embedded...) từ manifest + startup code.
3. Kiểm tra `.agents/project/PROJECT.md` có `UNCONFIGURED` hay snapshot cũ; không dùng context repo khác.

## O1. Sinh cây thư mục 1:1, mỗi folder và file có Markdown

```bash
python3 .agents/workflows/tools/build-context.py --dry-run
python3 .agents/workflows/tools/build-context.py
# Nếu context đã có và source thay đổi:
python3 .agents/workflows/tools/build-context.py --refresh
```

- Git repo: lấy tracked + untracked không bị ignore; non-Git repo: scan filesystem, bỏ cache/build/git/.agents và symlink.
- Giữ **đúng tên, đúng vị trí** mọi folder/file quan sát được; không áp tên `core`, `modules`, `features` nếu dự án không có.
- Tạo `project/tree/.../README.md` và một file Markdown tương ứng từng source file. Ví dụ *chỉ để minh họa naming*: `src/core/config.py -> tree/src/core/config.md`; `frontend/pages/home.tsx -> tree/frontend/pages/home.tsx.md`.
- `project/SOURCE_MAP.json` ánh xạ path, phân loại `PATH_ONLY` / `SOURCE_INSPECTED_STATIC`, SHA-256 với file không quá budget; không copy nội dung file gốc.
- Không đọc/ghi secret; file binary được đại diện bằng metadata, không bằng source body.

**Gate:** số ánh xạ file đúng số file nguồn được chọn, không collision; số folder README đúng số folder source kể cả root; không có path/stack riêng của repo khác.

## O1b. Living context cần được đồng bộ khi source thay đổi

- `project/STATE.md`: snapshot gần nhất, HEAD/branch, delta file và trạng thái kiểm chứng.
- `project/CHANGES.md`: lịch sử đồng bộ, không phải kiểm thử hay thay thế Git log.
- `project/COVERAGE.md`: thống kê trạng thái file.
- `project/PROJECT.md`: bổ sung entrypoint, owner, dependency, contract được xác minh thủ công, giữ note qua lần refresh.
- `project/tree/`: Markdown theo **folder và file source thực**, không nhận tên module/screen mẫu.

```bash
python3 .agents/workflows/tools/build-context.py --check
python3 .agents/workflows/tools/build-context.py --refresh
```

## O2. Tạo context thực sự có giá trị

1. Mở entrypoints, router registration, exported services, typed transport và caller chain; xác minh symbol dựa trên source thật.
2. Ghi `PROJECT.md`: ứng dụng/package owners, stack có bằng chứng, import dependency, service boundaries, DB/migration, auth/security, build/test commands.
3. Ghi chú trong file `.md` đối ứng source: caller, callee, vai trò, input/output, side effects, error paths, tests, links source. Đưa evidence và path cụ thể, không chỉ đổi nhãn tự đoán từ tên file.
4. Đọc approved BD/DD/ADR/contracts: phân biệt expected và current; ghi discrepancy.
5. Đối chiếu các tầng theo loại dự án thật; `CLIENT.md`/`SERVER.md` là checklist, không phải folder bắt buộc.

**Gate:** ít nhất một luồng nghiệp vụ được trace từ entry đến side effect và response/test nếu task có luồng; nếu chưa xác minh thì ghi `NOT_VERIFIED`.

## O3. Hoàn thiện profile và kiểm chứng

1. Ghi test/build/lint từ manifest, nhưng chỉ đánh dấu `TESTED` nếu đã chạy thật.
2. `python3 .agents/workflows/tools/agentkit.py validate`.
3. Kiểm tra diff chỉ chứa `.agents/` khi thao tác lập context.
4. Handoff gồm: file/folder coverage, stack candidate vs verified, entrypoint, uncovered runtime/data, open questions.

**Safety:** không tự `git clean/reset`, install dependency, seed DB, deploy, push, đổi firewall hoặc ghi tài liệu source ngoài `.agents/`.

## Reusable architecture examples

- Cây minh họa không cá nhân hóa: [`architecture/apps/`](../architecture/apps/README.md).
- Chỉ có **một API01** và **một Screen01** làm form tham khảo; tên `module1` là placeholder. Không ép cây ví dụ lên dự án thật.
- Khởi tạo cây context của repository đang cài bằng `build-context.py`; output vào `project/tree/`, tách hoàn toàn form minh họa `architecture/apps/`.
