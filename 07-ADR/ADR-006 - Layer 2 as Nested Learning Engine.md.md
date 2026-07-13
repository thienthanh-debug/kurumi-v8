# ADR-006 — Layer 2 as Nested Learning Engine

Status: Accepted Ngày: 2026-07-10 Sprint: O2 Liên quan: [[EPISTEMOLOGY-000 - Layer 2 Overview]], [[Sprint O2 — Freeze Checkpoint]]

---

## Bối cảnh

Sprint O1 đã đóng băng Ontology (Layer 1): Reality → Experience → Principle → Architecture → Schema → System → Asset → Reality (vòng lặp kín). Sprint O2 cần xây Layer 2 để giải thích cơ chế học đứng sau mỗi mũi tên chuyển hóa, nhưng không được phá vỡ hay mở rộng Ontology đã chốt.

## Quyết định

**Layer 2 là một Engine duy nhất, nested bên trong từng mũi tên của Layer 1 — không phải một Layer song song, không sinh Node mới.**

```
Reality
    │
    ├── Engine Layer 2 (Observation → Information → Validation → Adjustment)
    ▼
Experience
    │
    ├── Engine Layer 2
    ▼
Principle
   ...
```

Engine gồm 4 bước cố định, lặp lại ở mọi mũi tên:

```
Observation → Information → Validation → Adjustment
```

Khi Validation FAIL, Adjustment không tự chẩn đoán — nó gọi lại chính Engine (Observation → Information) ở phạm vi hẹp hơn, được dẫn hướng bởi **Priority** — một hệ quả đọc ngược từ Principle đã tích lũy, không phải một thực thể/Node/Module riêng.

## Lý do

1. **Nhất quán với nguyên tắc "Layer 2 không phát minh cách học"** — Engine chỉ tổ chức lại cơ chế học con người vốn đã dùng, không tạo lý thuyết mới.
2. **Nhất quán với nguyên tắc "Helper never decides, helper only reports, State Machine decides"** — Adjustment kết thúc nhiệm vụ, Layer 1 mới quyết định chuyển Node.
3. **Không phình Ontology** — mọi hành vi mới phát hiện (Recursive Behavior, Priority) đều được giải thích bằng cơ chế đọc/ghi trên dữ liệu Layer 1 đã có (Experience, Principle), không cần thêm Node mới vào Layer 1, không cần thêm Module mới vào Layer 2.
4. **Đã kiểm chứng qua nhiều domain khác biệt** — kỹ năng tay chân lặp lại (Yield cà rốt, Espresso) và vấn đề tổng hợp nhiều biến số (Food Cost) — theo đúng nguyên tắc Reality có quyền phủ quyết Discovery.

## Hệ quả

- Mọi module Layer 2 (Observation, Information, Validation, Adjustment) phải giữ boundary sạch — không được lấn sang vai trò của module kế tiếp (xem chi tiết từng file EPISTEMOLOGY-00X).
- Priority/Heuristic Search không cần thiết kế như một cơ chế riêng — nó là cách đọc Principle, cần được implement như một truy vấn trên dữ liệu Experience/Principle đã có, không phải một bảng dữ liệu mới.
- Phạm vi đã kiểm chứng hiện tại chỉ giới hạn ở 3 mũi tên đầu của Layer 1. Mở rộng sang nửa sau (Architecture→Schema→System→Asset) là Backlog, cần Sprint riêng.

## Đã cân nhắc nhưng bị loại

- **Layer 2 song song với Layer 1** — bị loại vì khiến Layer 2 tự sinh Ontology riêng, vi phạm nguyên tắc "không đưa ý tưởng mới trước khi triển khai".
- **Root Cause / Diagnosis là Node/Module riêng** — bị loại vì phình Engine không cần thiết; đã chứng minh được rằng đây chỉ là hành vi gọi lại Engine sẵn có.
- **Priority là mô hình xác suất (Bayesian/thống kê)** — bị loại vì không khớp với cách con người thực tế vận hành (ưu tiên định tính từ kinh nghiệm, không tính phần trăm).
-Layer 2

Observation

↓

Information

↓

Validation

↓

Adjustment

Layer 2 tồn tại bên trong mũi tên Layer 1.

Không tạo Node mới.