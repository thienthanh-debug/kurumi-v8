Mỗi Discovery phải trả lời được 10 câu hỏi.

---

# 1. Context

Tại sao vấn đề này xuất hiện?

```
## Context

Sprint O2

Mục tiêu:
Build Learning Engine.

Trong lúc build xuất hiện câu hỏi:

"Adjustment biết phải nhìn Reality nào trước?"
```

---

# 2. Initial Hypothesis

Lúc đầu cả team nghĩ gì?

```
## Initial Hypothesis

Diagnosis là một Module.

Validation

↓

Diagnosis

↓

Adjustment
```

---

# 3. Reality Used

Đã dùng Reality nào để phá giả thuyết?

Đây cực kỳ quan trọng.

```
## Reality Used

Reality 01
Carrot Yield

Reality 02
Espresso

Reality 03
Food Cost

Reality 04
Customer Complaint
```

Sau này đọc sẽ biết Discovery này dựa trên bằng chứng nào.

---

# 4. Builder Opinions

Đây không phải log.

Chỉ ghi ý chính.

Ví dụ

```
## Claude

Search Strategy
=
Read Principle backward.

---

## Gemini

Priority
đến từ Probability.

---

## Grok

Adjustment
tự Investigation.
```

Không copy nguyên chat.

---

# 5. Bugs Found

Đây là vàng.

```
## Bugs

Bug 01

Validation
làm Diagnosis.

---

Bug 02

Probability
được coi là Entity.

---

Bug 03

Search Strategy
tạo Ontology mới.

---

Bug 04

Observation
đã diễn giải.
```

Sau vài Sprint sẽ thấy AI hay mắc lỗi gì.

---

# 6. Turning Point

Đây là phần hiếm AI nào ghi.

Nhưng theo tui nó quan trọng nhất.

Ví dụ.

```
## Turning Point

Food Cost.

Thanh giải thích:

Không phải
Observation mới.

Mà đã scan liên tục
trong quá trình vận hành.

Điều này khiến toàn bộ giả thuyết
hai loại Observation
bị loại bỏ.

Discovery đổi hướng.
```

Đây là thời điểm Discovery đổi hướng.

---

# 7. Final Discovery

Đây mới là phần freeze.

Ví dụ.

```
## Final Discovery

Learning Engine
không thay đổi.

Problem Scope

↓

Search Radius.

Scope nhỏ

↓

Immediate Loop.

Scope lớn

↓

Broader Search.

Không tạo module mới.
```

---

# 8. Impact

Ảnh hưởng tới đâu?

```
## Impact

Foundation

Reality

Experience

Principle

ADR

Learning Engine

Bootstrap

GPT

Claude

Gemini

Grok
```

Đây là bản đồ ảnh hưởng.

---

# 9. Open Questions

Đừng để mất.

```
## Open Questions

Cross-domain.

Medical.

Finance.

Psychology.

Need Verification.
```

Sau này Sprint O5 có thể quay lại.

---

# 10. Lessons

Ví dụ

```
## Lessons

Discovery đẹp
không phải Evidence.

Reality
luôn phủ quyết Discovery.

Không tạo Ontology
khi Foundation
đã giải thích được.
```

---

# Sau vài Sprint Reflection sẽ thành thế này

```
08-REFLECTION

Sprint

    Sprint01-Ontology.md

    Sprint02-LearningEngine.md

    Sprint03-ReadEngine.md

Discovery

    Recursive.md

    SearchRadius.md

    Priority.md

    Scope.md

Lessons

    AI Coordination.md

    Architecture.md

    Reality Testing.md
    
Hành trình: Layer 2 khởi đầu như một Layer song song tự sinh Node mới → sửa thành nested Engine bên trong mũi tên Layer 1 → phát hiện Recursive Behavior (Adjustment gọi lại Engine khi FAIL) qua 2 domain kỹ năng (cà rốt, espresso) → nghi ngờ cần 2 cơ chế Observation → Reality Owner bẻ gãy giả thuyết bằng case Food Cost → rút gọn về một trục: Search Radius tỉ lệ độ rộng vấn đề → phát hiện Priority là hệ quả tự nhiên của Principle, không phải entity mới.

Kết quả: Engine 4 bước (Observation→Information→Validation→Adjustment) Frozen cho 3 mũi tên đầu Layer 1. Recursive Behavior + Priority + Search Radius Frozen. Nửa sau Layer 1 (Architecture→Schema→System→Asset) và Node "System" — Backlog cho Sprint sau.

Chi tiết: [[Sprint O2 — Freeze Checkpoint]]