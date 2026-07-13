# EPISTEMOLOGY-003 — What is Validation

Status: ✅ Frozen Sprint: O2 Builder phụ trách: Gemini Liên quan: [[EPISTEMOLOGY-000 - Layer 2 Overview]], [[EPISTEMOLOGY-002 - What is Information]]

---

## Định nghĩa

Validation là **Boolean Gate**. Nó chỉ làm một việc: đối chiếu Information với Reference (Standard / Experience / Principle đã có) và trả về PASS hoặc FAIL.

```
Information
   ↓
Validation
   ↓
PASS / FAIL + Reason
```

## Boundary

**Được phép:**

- So sánh: `Information` vs `Standard` → PASS/FAIL
- Trả kèm **Reason** (Trace) — nguồn Reference nào gây ra FAIL (ví dụ: "Below Standard"), để Adjustment có cơ sở tìm hướng sửa

**Không được phép:**

- Chẩn đoán nguyên nhân sâu (Diagnosis). Bug đã sửa: `FAIL — Reason: Đường dao không đều gây hao hụt` (sai — đây là Validation kiêm Diagnosis) → `FAIL — Reason: Below Standard` (đúng — Validation chỉ biết 76% ≠ 82%, không biết ai/cái gì gây ra chênh lệch đó)
- Không cần Reference Engine phức tạp (Reference 1, Reference 2, Reference 3...). Trong đầu người vận hành thực tế không có danh sách tham chiếu — chỉ có "đúng hay sai, sai thì sửa".

## Ví dụ (case 10kg cà rốt)

**Input:** Yield = 76%, Standard = 82%.

**Output của Validation:**

> FAIL. Reason: Below Standard.

Không nói lý do sâu hơn (tay nghề, dao, nguyên liệu...) — đó là việc của Adjustment (xem [[EPISTEMOLOGY-004 - What is Adjustment]]).