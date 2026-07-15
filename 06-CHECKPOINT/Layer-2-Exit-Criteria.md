# Layer 2 Exit Criteria — Validation Engine

2026-07-14

Liên quan: [[Validation-Decision-Spec-V1]], [[CHOT-Validation-Layer-2026-07-14]], [[Flag — SessionRAM Persistence across WAIT_REVIEW]], [[Flag — Compiler Automation vs Frozen Contract]], [[Discovery — Truth Mapping V1]], [[Governance-Protocol]] (Mục 4, Open Flag ≠ Freeze Blocker)

Validation Engine (Layer 2) được coi là sẵn sàng Freeze khi:

- [x] Validation Coverage PASS (9/9, xem Coverage Matrix trong Validation-Decision-Spec-V1)
- [x] Unknown Output PASS (Ledger Qty = Expected Output, batch DN-PREP-260712-07)
- [x] WARNING Routing PASS (LOW YIELD → WAIT_REVIEW → Approved → COMMIT, cùng execution)
- [x] CRITICAL Routing PASS (8/9 case, còn thiếu case riêng "Missing Item Code" — đã có bằng chứng bổ sung sau)
- [x] Duplicate Guard PASS (3 bằng chứng độc lập)
- [x] Snapshot Immutability PASS (effectiveQty không mutate row.qty gốc)
- [ ] NORMAL Routing — chưa có bằng chứng tường minh riêng (chỉ có bằng chứng gián tiếp qua các batch OK). Không phải Freeze Blocker (rủi ro thấp, đường mặc định đơn giản nhất), nhưng nên bổ sung 1 test rõ ràng khi tiện.
- [ ] Session Persistence (WAIT_REVIEW qua execution boundary tách biệt thật) — Open, KHÔNG phải Freeze Blocker cho Layer 2 (xem [[Governance-Protocol]] Mục 4 + [[Flag — SessionRAM Persistence across WAIT_REVIEW]]). Blocker cho Mission Engine Lifecycle tương lai nếu test A-D fail.

## Freeze Blocker Matrix

| Flag | Severity | Freeze Blocker cho Layer 2? | Lý do |
|---|---|---|---|
| SessionRAM Persistence | 🔴 | ❌ Không | Rủi ro thuộc Engine Lifecycle (ranh giới execution), không thuộc Validation Rule |
| Compiler Automation | 🟡 | ❌ Không | Mission khác (GENERATE tự động hóa), không ảnh hưởng Validation |
| Truth Mapping | ⚪ Discovery | ❌ Không | Chưa kết luận gì, không ảnh hưởng Runtime |

## Status: Ready for Freeze

Đề xuất Thanh xác nhận Freeze Layer 2 / Validation Engine. Sau khi Freeze, Mission tiếp theo (chọn 1, không mở song song): Sell Traceback Engine / Review Workspace UI / Approval UI / Session Persistence Test A-D.
