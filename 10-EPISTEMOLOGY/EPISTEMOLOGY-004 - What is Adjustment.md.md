# EPISTEMOLOGY-004 — What is Adjustment

Status: ✅ Frozen Sprint: O2 Liên quan: [[EPISTEMOLOGY-000 - Layer 2 Overview]], [[EPISTEMOLOGY-003 - What is Validation]], [[EPISTEMOLOGY-005 - Priority and Heuristic Search]]

---

## Định nghĩa

Adjustment là bước cuối của Engine. Nó nhận kết quả từ Validation và:

- Nếu **PASS** → giữ nguyên nhịp độ, không can thiệp.
- Nếu **FAIL** → tìm nguyên nhân và điều chỉnh.

Adjustment **kết thúc nhiệm vụ ngay sau khi trả kết quả**. Nó không tự chuyển Node của Layer 1 — Layer 1 mới là bên quyết định chuyển sang Experience/Principle/... tiếp theo (nguyên tắc: Helper never decides, helper only reports, State Machine decides).

## Adjustment không tự biết nguyên nhân (Recursive Behavior)

Đây là Discovery quan trọng nhất của Sprint O2 về Adjustment: **Adjustment không có khả năng tự chẩn đoán.** Khi FAIL, nó phải "mượn" lại chính Engine — gọi lại Observation → Information ở phạm vi hẹp hơn, nhắm vào đúng nghi vấn.

```
Validation
   │
   ├── PASS ──────────────► Adjustment (giữ nguyên nhịp)
   │
   └── FAIL ──► Observation (thu hẹp, targeted)
                    ↓
                Information (thu hẹp)
                    ↓
                Adjustment (đã có nguyên nhân → Action)
```

**Quan trọng:** Đây **không phải một Node/Module mới** ("Diagnosis" hay "Investigation" không phải thực thể riêng trong ontology). Đây là **hành vi (behavior)** của Adjustment: nó gọi lại Engine đã có sẵn, ở phạm vi hẹp hơn. Không phình Engine, không thêm khái niệm mới.

## Vấn đề còn lại đã sửa: Adjustment gọi lại Engine — nhưng nhìn vào đâu?

Câu hỏi ban đầu: "FAIL rồi, Observation lần 2 quan sát cái gì? Dao? Cà rốt? Người? Cân? Supplier?" — Engine không tự nhiên biết chọn đúng chỗ để nhìn.

Câu trả lời (xem chi tiết ở [[EPISTEMOLOGY-005 - Priority and Heuristic Search]]): Adjustment không đoán, không random. Nó **đọc ngược Priority từ Principle đã tích lũy** để biết nên nhìn đâu trước.

## Ví dụ (case 10kg cà rốt)

**Input:** FAIL, Reason: Below Standard (76% vs 82%).

**Adjustment:**

> Đọc Principle liên quan đến Yield → Priority gợi ý kiểm tra kỹ năng cầm dao trước (tương quan cao nhất trong Experience quá khứ) → Observation thu hẹp: quan sát góc cầm dao, độ mài của dao → Information thu hẹp: dao cùn, góc cầm chưa đúng → Action: đổi góc cầm dao, mài lại dao.