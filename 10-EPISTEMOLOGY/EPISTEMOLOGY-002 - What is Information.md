# EPISTEMOLOGY-002 — What is Information

Status: ✅ Frozen Sprint: O2 Builder phụ trách: Grok Liên quan: [[EPISTEMOLOGY-000 - Layer 2 Overview]], [[EPISTEMOLOGY-001 - What is Observation]]

---

## Định nghĩa

> **Information = Reality đã được System đọc bằng Knowledge hiện có.**

Information không phải Data. Một con số trần trụi (ví dụ: `180`) không phải Information. Chỉ khi được diễn giải qua Knowledge sẵn có (ví dụ: người biết đó là nhiệt độ lò → `180°C` → "lò đang nóng hơn hôm qua"), nó mới trở thành Information.

## Sơ đồ

```
Reality
   ↓
Observation
   ↓
System đọc (dùng Knowledge)
   ↓
Information
```

Observation **không tự sinh** Information. Giống ERP: Purchase không tự sinh Stock — Purchase chỉ tạo điều kiện, Stock được cập nhật bởi Engine. Tương tự, Observation chỉ đưa Reality vào System; Information sinh ra vì System diễn giải Observation bằng Knowledge hiện có.

## Boundary

**Được phép:**

- Diễn giải con số thô thành chỉ số có ý nghĩa (yield %, chênh lệch so với kỳ trước...)

**Không được phép:**

- Suy luận / dự đoán nguyên nhân. Bug đã sửa: "Có dấu hiệu đường dao không đều (có thể ảnh hưởng...)" — chữ "có thể" đã là suy luận, không thuộc Information. Information chỉ nên dừng ở: `Yield = 76%`, `Waste = 24%`.

## Vị trí của Knowledge

Knowledge nằm **bên trong System** (không phải một node riêng đứng sau Information). Biên giới cụ thể của Knowledge (dùng Standard nào, Experience tích lũy tới đâu) cần được giới hạn rõ khi build/test — ví dụ ở vòng test đầu tiên chỉ nên dùng Standard sẵn có trong ERP, chưa dùng Experience tích lũy, để tránh mơ hồ.

## Ví dụ (case 10kg cà rốt)

**Input (từ Observation):** 7.6kg thành phẩm / 10kg nguyên liệu.

**Output của Information:**

> Yield = 76%. Waste = 24%.

Không kèm suy luận nguyên nhân.