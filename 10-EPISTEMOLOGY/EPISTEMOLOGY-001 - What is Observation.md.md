# EPISTEMOLOGY-001 — What is Observation

Status: ✅ Frozen Sprint: O2 Builder phụ trách: Claude Liên quan: [[EPISTEMOLOGY-000 - Layer 2 Overview]]

---

## Định nghĩa

Observation là bước đầu tiên của Learning Engine. Nó ghi nhận trực tiếp những gì giác quan hoặc công cụ đo lường được từ Reality — **chưa diễn giải, chưa so sánh, chưa gán ý nghĩa.**

## Boundary (ranh giới đã qua nhiều vòng Compatibility Test để làm sạch)

**Được phép:**

- Con số đo được trực tiếp (cân nặng, thời gian, nhiệt độ...)
- Mô tả hiện trạng thô, không kèm phán đoán ("một số lát dày, một số lát mỏng")

**Không được phép:**

- Tính toán / suy diễn tỷ lệ (ví dụ: yield %) → đó là việc của Information
- Phán đoán nguyên nhân ("tay nghề kém") → đó là việc của Validation/Adjustment
- Ngôn ngữ so sánh ngầm định chuẩn ("không đều", "quá chậm") — nếu chưa có Standard tường minh để so sánh, không được dùng từ mang tính đánh giá. Đây là bug đã từng mắc và được sửa: "đường dao không đều" (sai, có Validation ẩn bên trong) → "một số lát gọt dày, một số lát gọt mỏng" (đúng, thuần mô tả).

## Ví dụ (case 10kg cà rốt — Phase 1 Compatibility Test)

**Input:** 10kg cà rốt nguyên vỏ, giao cho phụ bếp gọt.

**Output của Observation:**

> Sau khi gọt, cân hiện 7.6kg cà rốt thành phẩm. Vỏ và phần bỏ đi: 2.4kg. Một số lát gọt dày, một số lát gọt mỏng. Thời gian gọt: X phút.

**Không nói:** "Yield 76%" (Information), "tay nghề kém" (Validation/Adjustment).

## Ghi chú kiến trúc

Contract giữa Observation và Information (bước kế tiếp) ở tầng Architecture **không cần định dạng kỹ thuật (JSON/object)**. Contract chỉ cần là mô tả bằng lời: "Observation đưa cái gì sang bước tiếp theo." Định dạng kỹ thuật thuộc về Implementation, chưa tới lượt ở Sprint O2.