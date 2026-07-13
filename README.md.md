# Kurumi OS — Start Here

Foundation là tầng cao nhất của Kurumi OS. Không chỉnh sửa trực tiếp. Không được tạo Foundation mới. Foundation chỉ được Freeze khi Reality chứng minh.

Mọi Architecture ↓ mọi Specification ↓ mọi Code đều phải truy ngược về Foundation.

## Start Here (đọc theo đúng thứ tự)

1. Đọc `01-GOVERNANCE/Constitution/00-Kurumi-Constitution.md` (Meta Constitution)
2. Đọc `01-GOVERNANCE/Constitution/01-Runtime-Constitution.md` (nếu làm việc trên ERP/Apps Script)
3. Đọc Checkpoint mới nhất trong `06-CHECKPOINT/`
4. Đọc Schema/Architecture liên quan trong `03-ARCHITECTURE/`
5. Đọc ADR liên quan trong `07-ADR/`
6. Tiếp tục Implementation trong `05-IMPLEMENTATION/`

## Vault Structure (đã cập nhật khớp thực tế, thay bản cũ 6-thư-mục lỗi thời)

```
00-FOUNDATION       Ontology, nguyên tắc gốc — không sửa trực tiếp
01-GOVERNANCE       Constitution (Meta + Runtime), Policies, Standards
02-TEAM             Bootstrap, Role Guide, Workflow của từng AI
03-ARCHITECTURE     Domain, Engines, Infrastructure, Patterns
04-SPECIFICATION    Đặc tả kỹ thuật chi tiết
05-IMPLEMENTATION   Code, Apps Script, Python
06-CHECKPOINT       Tiến độ dự án theo Sprint
07-ADR              Architecture Decision Records
08-REFLECTION       Sprint log, Discovery, Lessons, Mistakes
09-ASSETS           Prompt, Diagram, Template, Reference
10-EPISTEMOLOGY     Layer 2 Learning Engine (Observation→...→Adjustment)
```

## Lifecycle

```
Foundation
    ↓
Governance
    ↓
Architecture
    ↓
Specification
    ↓
Implementation
    ↓
Reality Test
    ↓
Checkpoint
    ↓
ADR
    ↓
Reflection
    ↓
Assets
```

Reality First.