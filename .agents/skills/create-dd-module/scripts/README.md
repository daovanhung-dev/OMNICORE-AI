# DD validator for module

Tất cả scripts thực thi offline, không dùng database hoặc network. Run từ **project root**:

```bash
python3 .agents/workflows/tools/agentkit.py new-dd --type module --id DEMO-001 --slug Example --output docs/dd
python3 .agents/workflows/tools/agentkit.py validate-dd --type module --path docs/dd/DEMO-001-Example
# Strict: chỉ khi đã điền/chốt tất cả placeholder
python3 .agents/workflows/tools/agentkit.py validate-dd --type module --path docs/dd/DEMO-001-Example --strict
```

`validate-dd` chỉ kiểm cấu trúc/link/template, không phê duyệt nghiệp vụ. Xem [skill](../SKILL.md) và [quality gates](../checklists/quality-gates.md).
