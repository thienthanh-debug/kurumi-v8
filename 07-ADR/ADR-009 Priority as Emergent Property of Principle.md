Priority is inherent in Principle
Status: Accepted Ngày: 2026-07-10 Sprint: O2

## Context

Adjustment cần biết nên nhìn đâu trước khi FAIL xảy ra (dao? cà rốt? người? cân? supplier?). Cần cơ chế chọn hướng, không phải đoán ngẫu nhiên.

## Decision

Priority không phải một entity được sinh ra hay lưu trữ riêng. Nó là **hệ quả tự nhiên** khi Principle đủ dày (Heuristic Priority, không phải mô hình xác suất/thống kê).

```
Reality → Experience → Principle → Priority (hệ quả đọc, không phải node) → Adjustment đọc ngược → Targeted Observation
```

Principle có thêm một chức năng (bên cạnh điều khiển Action đã biết từ Sprint O1): **điều hướng Learning**.

## Consequence

Không thêm Node/Module vào Ontology hay Engine. Implementation của Priority là một phép đọc/truy vấn trên Experience/Principle đã có, không phải một bảng dữ liệu riêng.

Mở: chưa chốt liệu "điều khiển Action" và "điều hướng Learning" là một thuộc tính hay hai thuộc tính cùng nguồn — quyết định khi implement.
ADR-009

Decision

Search Radius
is proportional to
Problem Scope.

References

[[Discovery — Scope]]

[[Discovery — Search Radius]]

[[EPIS-005]]

Liên quan: [[EPISTEMOLOGY-005 - Priority and Heuristic Search]]
```
Priority

không phải Entity

không phải Module

không phải Function

Priority

là thuộc tính nội tại
của Principle.

Experience

↓

Principle

↓

Priority
