Problem Scope determines Search Radius
Status: Accepted Ngày: 2026-07-10 Sprint: O2

## Context

Case Yield (cà rốt) và case Food Cost cho hai hành vi Recursive Investigation khác nhau: cà rốt điều chỉnh ngay tức thời trên chính Reality; Food Cost cần scan lại kho Experience nền tích lũy từ trước. Ban đầu tưởng cần 2 cơ chế Observation khác nhau (tức thời vs nền).

## Decision

Không cần 2 cơ chế. Chỉ có **một trục**: bán kính quét (search radius) của Adjustment tỉ lệ với **độ rộng của vấn đề** đang FAIL — khoảng cách giữa nguyên nhân và triệu chứng.

- Vấn đề hẹp (nguyên nhân–triệu chứng cùng đối tượng) → bán kính nhỏ, gần tức thời.
- Vấn đề rộng (nguyên nhân trải rộng nhiều luồng Reality, nhiều thời điểm) → bán kính lớn, cần tổng hợp nhiều Experience.

## Consequence

"Search Radius" là thuộc tính của vấn đề, không phải cơ chế riêng của Layer 2. Khi Principle hoàn toàn rỗng (chưa từng có tiền lệ), Adjustment không có cơ sở ưu tiên → quan sát rộng hoặc escalate cho Reality Owner, không cần quy tắc đặc biệt thêm.

Liên quan: [[EPISTEMOLOGY-005 - Priority and Heuristic Search]]
```
Discovery

Scope nhỏ

↓

Search Radius nhỏ

↓

Immediate Adjustment

Ví dụ

Yield

Espresso

Dough

----------------

Scope lớn

↓

Search Radius lớn

↓

History

Experience

Leader

Customer Feedback

ERP

Supplier

Ví dụ

Food Cost

Customer Complaint

Business Performance
```