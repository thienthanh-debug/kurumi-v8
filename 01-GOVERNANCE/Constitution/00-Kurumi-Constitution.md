# KURUMI V8 OS — CONSTITUTION (Meta)

Status: Draft Approved — chờ Thanh xác nhận cuối cùng trước khi Freeze Layer: 00 — Meta / OS-level Kế thừa bởi: 01-Runtime-Constitution.md, 02-Knowledge-Constitution.md (nếu có)

## Applies To

- ERP (Runtime Engine — Apps Script)
- Knowledge OS (Obsidian)
- Python Tooling
- AI Workflow / Team
- Bất kỳ module tương lai nào (Mobile App, Desktop, Robot...) — Constitution này vẫn áp dụng, không cần viết lại.

## 0. MISSION

Kurumi V8 tồn tại để giúp Thanh xây dựng, vận hành, cải tiến và liên tục học hỏi từ vận hành nhà hàng thực tế.

ERP, Knowledge OS, Python, Apps Script, Obsidian là **công cụ thực hiện** Mission này — không phải bản thân Mission.

## 1. LUẬT TỐI CAO

- Reality is the final authority.
- Reality may invalidate any document.
- Documents never invalidate Reality.

## 2. ONTOLOGY (Tầng 1 — Frozen)

```
Reality → Experience → Principle → Architecture → Schema → System → Asset → Reality
```

**Pending Validation:**

- Định nghĩa "System" chưa chốt.
- Engine chưa kiểm chứng cho nửa sau chuỗi (Architecture → Schema → System → Asset).

## 3. EPISTEMOLOGY (Tầng 2 — Learning Engine tổng quát)

```
Observation → Information → Validation (PASS/FAIL) → Adjustment
```

- Khi FAIL, Adjustment gọi lại chính Engine ở phạm vi hẹp hơn (Recursive Behavior) — không phải Node/Module mới.
- Priority không phải thực thể riêng — là hệ quả đọc ngược Principle đã tích lũy (Heuristic, không phải xác suất toán học).
- Search Radius tỉ lệ Scope — bán kính điều tra tỉ lệ với độ rộng vấn đề, không phải cơ chế riêng.

## 4. GOVERNANCE & WORKFLOW GATE

```
Reasoning proposes
    ↓
Workflow authorizes
    ↓
Artifact Type xác định (single source of classification — chỉ Workflow quyết, Builder không tự chọn)
    ↓
Constitution áp dụng đúng Artifact Type
    ↓
Checker validates  ← chặn TRƯỚC khi thực thi
    ↓
Execution Engine executes  ← chỉ chạy nếu Checker PASS
    ↓
Reality decides
```

Nếu Checker trả FAIL, Execution Engine không được gọi. Đã kiểm chứng bằng Negative Test thật (case STOCK_SUMMARY).

## 5. LEARNING LOOP

```
Reality → Work → Problem → Reflection → Knowledge → Implementation → Reality (lặp lại)
```

**Status: Hypothesis** — không phải Frozen.

Quy luật quan sát được lặp lại xuyên suốt O1–O3, nhưng chưa đủ điều kiện Freeze:

- Chưa kiểm chứng bằng một Object hoàn toàn ngoài phạm vi dự án hiện tại.
- Vẫn chỉ có 4 Object cùng một người quan sát (Carrot, Food Cost, ERP, Python).

Điều kiện để nâng lên Frozen: Reality tiếp tục ép dừng công việc chính theo đúng quy luật này, ở tình huống mà Epistemology (mục 3) và Governance (mục 4) hiện có không giải quyết được.

Không AI nào được quyền tự ý nâng mục này lên Frozen mà chưa qua Mission → Task → Approval của Thanh.

## Change Log

- 2026-07-12: Tạo Meta Constitution, tách khỏi Runtime Constitution (06/07/2026). Sửa: thứ tự Checker/Execution Engine, trạng thái Learning Loop (Hypothesis thay vì Frozen), thêm Applies To.