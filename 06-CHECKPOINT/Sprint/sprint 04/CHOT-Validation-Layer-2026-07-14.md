# CHỐT — Validation Layer, Inventory Engine V8

2026-07-14

Liên quan: [[Validation-Decision-Spec-V1]] (bảng Coverage Matrix dưới đây cũng đã được chép vào Mục 8 của spec đó — file này là bản ghi Checkpoint độc lập, không phải nguồn thứ hai khác biệt), [[CHECKPOINT-CHOT-PHIEN-2026-07-14]] (checkpoint tổng của cả phiên, trích bảng này làm bằng chứng)

## Coverage Matrix cuối cùng

| Rule | Kết quả | Evidence |
|---|:---:|---|
| Missing Event ID | ✅ PASS | ERROR_LOG |
| Missing Transaction ID | ✅ PASS | ERROR_LOG |
| Missing Item Code | ✅ PASS | ERROR_LOG, transactionId `HA-PREP-260712-02-CONS-3`, context xác nhận `itemCode` rỗng |
| Missing Qty / Not Number | ✅ PASS | Case Brown Rice (trước khi có Allow Unknown Output) |
| Qty = 0 | ✅ PASS | ERROR_LOG dòng 25, `VALIDATE_FAIL_ZERO_QTY` |
| Invalid Item | ✅ PASS | ERROR_LOG (2 bằng chứng độc lập) |
| Duplicate Transaction | ✅ PASS | ERROR_LOG (3 bằng chứng độc lập, gồm cả lần chặn đúng do Idempotency Guard hôm nay) |
| Allow Unknown Output | ✅ PASS | `INVENTORY_LEDGER` batch `DN-PREP-260712-07`, Qty = 5.100 khớp `Expected Output`; Snapshot gốc vẫn rỗng (không mutate); không có `NOT_A_NUMBER` trong lần chạy này |
| WARNING Flow (routing) | ✅ PASS | LOW YIELD → WAIT_REVIEW → Approved → COMMIT → Ledger |

**9/9 — Coverage Matrix đóng hoàn toàn.**

## Trạng thái đề xuất

**`Validation-Decision-Spec-V1.md`: đề xuất chuyển từ Draft → Frozen.**

Toàn bộ Risk Assessment 3 nhánh (NORMAL/WARNING/CRITICAL), Cleanup dọn Staging, hợp nhất Snapshot ID, Fail Closed cho Master Data, và Allow Unknown Output đều đã có bằng chứng chạy thật, không còn dòng nào dựa trên suy đoán. Đúng thẩm quyền: chỉ Thanh có quyền đóng dấu Frozen — mình chỉ đề xuất, không tự đánh dấu.

**Cập nhật 2026-07-14 (Claude, khi lưu file này vào vault):** Thanh đã xác nhận Freeze. `Validation-Decision-Spec-V1.md` hiện đã ở trạng thái FROZEN 🔒 (Rev.5), commit `031de2e`.

## Còn lại — không chặn Freeze, nhưng chưa đóng

**🚩 Flag "SessionRAM Persistence across WAIT_REVIEW"** — vẫn Open trong `08-REFLECTION/Discovery/`. Đã xác nhận không ảnh hưởng `resolveEffectiveQty()` (chạy cùng execution với GENERATE), nhưng ảnh hưởng tiềm tàng tới toàn bộ nhánh WARNING trong kịch bản thật (Manager duyệt cách xa nhiều giờ). 4 test A-D vẫn chưa chạy — để đó, không cấp bách, không phải điều kiện để Freeze Spec.

## Việc kỹ thuật nhỏ, ghi nhận không xử lý ngay

Idempotency Guard vừa hoạt động đúng thiết kế nhưng gây `FAILED` khi test batch cũ trùng Transaction ID với Ledger đã có — hành vi đúng, không phải bug. Nếu quy trình test sau này cần chạy lại cùng batch nhiều lần, nên nhớ dọn `TRANSACTION_STAGING` + đổi Transaction ID trước, tránh nhầm là lỗi mới.

## Tổng kết Sprint hôm nay

- ADR-016 (Compiler Never Silences Reality) — merged, tested.
- Validation Decision Spec — 3 nhánh Risk Assessment hoàn chỉnh, tested end-to-end cả CRITICAL/WARNING/NORMAL.
- Allow Unknown Output — merged, tested.
- Governance Protocol (🚩 Flag 4 câu hỏi + Severity + Resolution) — đã thống nhất giữa Claude/GPT/Gemini, dùng xuyên suốt phiên.
- 2 Discovery mới ghi vào vault: Compiler Automation, SessionRAM Persistence — cả hai đều đúng chỗ (không mở Mission mới, không chặn việc đang làm).

Đề xuất Thanh xác nhận Freeze `Validation-Decision-Spec-V1.md`, rồi Sprint này coi như đóng.
