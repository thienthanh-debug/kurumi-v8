Recursive Investigation.md
Status: Accepted Ngày: 2026-07-10 Sprint: O2

## Context

Khi Validation FAIL, Adjustment cần tìm nguyên nhân nhưng không có khả năng tự chẩn đoán.

## Decision

Adjustment gọi lại chính Engine (Observation → Information) ở phạm vi hẹp hơn khi FAIL. Đây là **hành vi (behavior)**, không phải Node/Module mới.

```
Validation FAIL → Adjustment → Observation (targeted) → Information (targeted) → Adjustment (có nguyên nhân)
```

## Consequence

Không thêm entity vào Ontology hay Epistemology. "Diagnosis"/"Investigation" không tồn tại như khái niệm độc lập — mọi tài liệu về sau chỉ mô tả đây là Recursive Behavior của Adjustment.

Liên quan: [[EPISTEMOLOGY-004 - What is Adjustment]]

```
Diagnosis
không phải Module.

Adjustment
khi FAIL

↓

gọi lại Learning Engine

↓

Targeted Observation

↓

Targeted Information

↓

Validation

↓

Adjustment

cho đến khi tìm được Root Cause.
```