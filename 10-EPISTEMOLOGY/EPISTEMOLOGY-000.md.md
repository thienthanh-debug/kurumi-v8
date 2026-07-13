# EPISTEMOLOGY-000 — Layer 2 Overview

Status: ✅ Frozen (phạm vi giới hạn — xem mục Backlog cuối file) Sprint: O2 Ngày chốt: 2026-07-10 Liên quan: [[FOUNDATION-000]], [[ADR-006 - Layer 2 as Nested Learning Engine]]

---

## 1. Vai trò của Layer 2

Layer 2 là **Learning Engine** của Layer 1. Nó không thay thế Foundation, không tạo Ontology mới.

Layer 2 chỉ trả lời một câu hỏi duy nhất:

> Mỗi khi Foundation chuyển từ Node A sang Node B, hệ thống đã học và chuyển hóa bằng cơ chế nào?

## 2. Kiến trúc: Nested, không phải Song song

Sai (bản đầu tiên, đã bỏ):

```
LAYER 1  (Foundation)
LAYER 2  (chạy song song, độc lập)
```

Đúng (đã chốt):

```
Reality
    │
    ├── Engine Layer 2
    ▼
Experience
    │
    ├── Engine Layer 2
    ▼
Principle
    │
    ├── Engine Layer 2
    ▼
Architecture
    │
   ...
```

Layer 2 nằm **bên trong từng mũi tên** của Layer 1. Nó không sinh Node mới. Nó là cơ chế vận hành của mũi tên.

## 3. Engine — 4 bước

```
Reality
   ↓
Observation
   ↓
Information
   ↓
Validation
   ↓
Adjustment
   ↓
Next Foundation Node
```

- **Observation** → xem [[EPISTEMOLOGY-001 - What is Observation]]
- **Information** → xem [[EPISTEMOLOGY-002 - What is Information]]
- **Validation** → xem [[EPISTEMOLOGY-003 - What is Validation]]
- **Adjustment** → xem [[EPISTEMOLOGY-004 - What is Adjustment]]
- **Priority / Heuristic Search** (cơ chế Adjustment dùng để quyết định quan sát/truy vấn gì tiếp theo) → xem [[EPISTEMOLOGY-005 - Priority and Heuristic Search]]

## 4. Nguyên tắc vận hành đã chốt

- **Layer 2 không phát minh cách học.** Nó tổ chức lại các cơ chế học mà con người đã dùng hàng nghìn năm, gắn đúng vị trí để phục vụ Foundation.
- **Helper never decides, helper only reports, State Machine decides.** Layer 2 (Adjustment) không tự chuyển Node — Adjustment kết thúc, Layer 1 mới chuyển sang Node tiếp theo.
- **Reality luôn có quyền phủ quyết Discovery.** Mọi giả thuyết kiến trúc phải được test bằng Reality (kể cả Reality dạng minh họa phản ánh đúng cơ chế vận hành thật) trước khi Freeze.
- **Validation không chẩn đoán.** Validation chỉ trả PASS/FAIL + Reason (nguồn gây lệch), không suy luận nguyên nhân sâu.
- **Adjustment không tự biết nguyên nhân.** Khi FAIL, Adjustment gọi lại chính Engine (Observation → Information) ở phạm vi hẹp hơn — đây là hành vi đệ quy (recursive behavior), không phải một Node/Module riêng.

## 5. Phạm vi đã kiểm chứng (Validated Scope)

|Phạm vi|Trạng thái|
|---|---|
|Engine cho 3 mũi tên đầu (Reality→Experience→Principle→Architecture)|✅ Kiểm chứng bằng minh họa nhất quán (cà rốt, espresso)|
|Recursive behavior (Adjustment gọi lại Engine khi FAIL)|✅ Kiểm chứng ở 2 domain kỹ năng lặp lại (cà rốt, espresso)|
|Priority = đọc ngược Principle, bán kính quét tỉ lệ độ rộng vấn đề|✅ Kiểm chứng bằng case biên (Food Cost — Principle mỏng/rỗng)|
|Engine cho nửa sau chuỗi (Architecture→Schema→System→Asset)|⏳ Backlog — chưa test|
|Định nghĩa "System"|⏳ Backlog — chưa định nghĩa|
|Compatibility Test bằng 3 Builder độc lập thật (không phải 1 AI tự đóng cả 3 vai)|⚠️ Đã làm một phần (Observation/Information/Validation Phase 1), cần tiếp tục cho các case sau|

## 6. Backlog (không được để trôi mất — bài học từ "System" bị bỏ quên lần đầu)

1. **Định nghĩa "System"** — node giữa Schema và Asset trong Layer 1, chưa từng được đóng băng chính thức.
2. **Kiểm chứng Engine cho Architecture→Schema→System→Asset** — hiện tại Engine mới được test cho nửa đầu chuỗi.
3. **Tách rõ "Priority cho Observation mới" vs "Priority cho truy vấn Experience nền"** nếu về sau việc implement cho thấy hai trường hợp cần xử lý dữ liệu khác nhau (xem thêm ghi chú trong EPISTEMOLOGY-005).