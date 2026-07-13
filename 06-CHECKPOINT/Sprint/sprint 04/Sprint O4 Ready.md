
# KURUMI V8 — CHECKPOINT

**Date:** 2026-07-14  
**Status:** Sprint O4 Ready

Liên quan: [[Sprint O3 - Meta Architecture Freeze]] (sprint liền trước), [[Constitution Keeper (khung chat này) — 2026-07-13]] (checkpoint cùng ngày, khung chat khác), [[00-Mission]] và [[01-Reality_and_Domain]] (Inventory Refactoring Project Alpha — mission của Sprint này)

## 1. Hoàn thành hôm nay

### AI Infrastructure

- Git local hoàn chỉnh.
    
- GitHub Repository online.
    
- `main` + `develop` hoạt động.
    
- Branch protection thiết lập.
    
- Claude Code kết nối thành công với repository.
    
- Runtime Layer được thiết kế (Bootstrap + Runtime Policy + Workflow).
    

**Kết luận:** AI Infrastructure hoàn thành. Không ưu tiên thêm.

---

## 2. Reality mới (Quan trọng nhất)

**Reality đã đấm:**

> Staff không thể thao tác Inventory trên điện thoại vì sheet quá nặng.

Đây là **Business Problem**, không phải Code Problem.

Theo Constitution:

```
Reality
>
Architecture
>
Implementation
```

=> Mọi công việc khác phải nhường chỗ cho vấn đề này.

---

## 3. Root Cause

Sai ở tư duy Sheet.

Hiện tại một sheet đang làm quá nhiều vai trò:

- Workspace
    
- Validation
    
- Dropdown
    
- Formula
    
- Review
    
- Transaction
    
- History
    

Đây là Mixed Responsibility.

---

## 4. Quyết định (Frozen)

Workspace **không phải Database.**

Workspace **không phải History.**

Workspace chỉ là:

> **Nơi nhân viên thao tác trong ngày (24h).**

Sau khi hoàn thành:

```
Workspace

↓

Submit

↓

Transaction

↓

Review

↓

Ledger

↓

Read Model
```

Workspace có thể:

- reset
    
- archive
    
- recreate
    

mà không ảnh hưởng lịch sử.

---

## 5. Sprint O4 Mission (Đã đổi)

Không còn:

> Inventory Engine

Mà là:

> **Inventory Refactoring Project Alpha**

Mission:

> Thiết kế lại toàn bộ kiến trúc Inventory để Workspace luôn nhẹ, tối ưu cho điện thoại, trong khi Transaction, Ledger và Read Model chịu trách nhiệm lưu trữ và tính toán.

---

## 6. Thứ tự làm việc Sprint O4

### Phase 1

Đại phẫu kiến trúc Sheet.

Không viết Apps Script.

### Phase 2

Thiết kế Data Flow mới.

### Phase 3

Migration Plan.

### Phase 4

Review.

### Phase 5

Viết lại Engine.

---

## 7. Kiến trúc mục tiêu

```
Layer 1
Workspace (24h)

↓

Layer 2
Transaction

↓

Layer 3
Ledger

↓

Layer 4
Read Models
```

Mỗi Layer chỉ có **một trách nhiệm**.

---

## 8. Nguyên tắc mới

**Workspace is disposable.**

**Ledger is permanent.**

**Read Model is reproducible.**

Đây sẽ là nguyên tắc thiết kế Inventory V8.

---

## 9. Việc đầu tiên của khung chat mới

Không code.

Không Apps Script.

Không Formula.

Bắt đầu bằng:

> **Thiết kế lại cấu trúc Sheet cho Inventory Refactoring Project Alpha.**

Mục tiêu đầu tiên:

**Tách Workspace khỏi System.**

Đây sẽ là trọng tâm của toàn bộ Sprint O4.

---

Theo mình, đây là checkpoint đủ để khung chat mới có thể tiếp tục ngay mà không cần đào lại toàn bộ lịch sử. Quan trọng nhất là đã khóa được **Reality mới**: vấn đề không còn là Engine, mà là **Workspace Architecture**. Đó sẽ là điểm xuất phát của phiên tiếp theo.