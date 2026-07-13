markdown

```markdown
# GPT — Architecture Supervisor
Role: Architecture Supervisor
Project: KURUMI ERP V8

---

## Nhiệm vụ

GPT giữ vai trò Architecture Supervisor.
Không phải Builder. Không phải Constitution Keeper.

**Làm:**
- Audit code Gemini viết — có vi phạm Constitution không?
- Phát hiện Architecture Drift
- Kiểm tra mỗi State Machine transition có đúng FSM không
- Báo cáo cho Reality Owner (Thanh) khi phát hiện vấn đề

**Không làm:**
- Không tự ý thêm Entity mới
- Không tự ý thêm Sheet mới
- Không tự ý thêm Rule mới
- Không viết Apps Script
- Chỉ mở lại Architecture khi Reality Owner yêu cầu

---

## Quy trình làm việc
```

Builder (Gemini) viết code  
↓  
GPT audit  
↓  
PASS → Builder tiếp tục  
FAIL → GPT báo cáo Thanh  
↓  
Thanh quyết định

```

---

## Nguyên tắc quan trọng nhất

> Architecture follows Operation.
> Not the other way around.

Nếu Reality chứng minh Architecture sai
→ GPT là người đầu tiên đề nghị sửa.

Nếu Builder drift khỏi bản vẽ
→ GPT chặn ngay.

---

## Liên kết

- [[V8-Constitution]]
- [[2026-07-06-Checkpoint]]
```
# 📍 KURUMI ERP V8 — CHECKPOINT

## Inventory Engine

**Date:**5/6/2026
**Status:** Phase 2 đang triển khai

---

# ✅ Constitution (SEALED)

Không thay đổi.

Đã khóa:

- ✅ Reality First
- ✅ Business Event is Atomic
- ✅ Helper never decides. State Machine decides.
- ✅ One Entry Point. One Engine. Multiple Sessions.
- ✅ Engine Session = One Apps Script Execution.
- ✅ TRANSACTION_STAGING thuộc Human Workflow.
- ✅ Audit failure ≠ Business Event failure.
- ✅ Validation is Read-only.

---

# ✅ Infrastructure (FROZEN)

Đã nghiệm thu.

```
CONFIG✓getWorkbook()✓getSheet()✓createEngineError()✓appendAudit()✓setExecutionState()✓
```

Đã chạy Reality Test.

PASS.

---

# ✅ Runtime

Đã hoàn thành

```
runInventoryEngine()
```

Single Entry Point.

PASS.

---

# ✅ State

## IDLE

```
STATUSFROZEN
```

Đã audit.

Đã Reality Test.

---

## GENERATE

```
STATUSFROZEN
```

Đã hoàn thành.

Đã sinh Commit Package trong RAM.

Không ghi Ledger.

Không ghi Sheet.

Đúng Constitution.

---

# 🚧 VALIDATE

```
STATUSREADY
```

Chưa build.

Spec đã chốt:

```
✓ Package exists✓ Package not empty✓ Required fields✓ Item exists✓ Location exists✓ Qty valid✓ Validation is Read-only
```

---

# 📌 Audit hôm nay

## Claude

### PASS

- Engine Session
- Single Entry Point
- TRANSACTION_STAGING không phải RAM
- WAIT_REVIEW là Terminal State
- Guard Pattern (ý tưởng)

---

### Chưa áp dụng

```
isEngineError()
```

Lý do:

Chưa cần.

Tránh over-engineering.

---

### Không đồng ý

Business State Routing trong

```
IDLE
```

Quyết định:

Business State sẽ được đọc tại

```
WAIT_REVIEW
```

vì đây mới là ranh giới Human ↔ Engine.

---

# 📌 Technical Debt

Hiện tại còn đúng **2 backlog**.

### Backlog 01

Refactor Guard Pattern.

Chưa làm.

Không ảnh hưởng Engine.

---

### Backlog 02

VALIDATE đang placeholder.

Có comment TODO.

Đúng kế hoạch.

---

# 🚦Ngày mai

Không bàn thêm kiến trúc.

Không thêm Principle.

Không thêm Entity.

Không thêm Sheet.

Làm đúng thứ tự:

```
VALIDATE↓Reality Test↓Audit↓Freeze↓WAIT_REVIEW↓Reality Test↓Freeze
```

Sau đó mới được phép chạm tới

```
COMMIT
```
Architecture is responsible for:

- Boundary
- Naming
- Flow of Truth
- Responsibility

Architecture does not implement.

Architecture reviews before Freeze.

Architecture

Specification

ADR

Implementation Review