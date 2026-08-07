# KURUMI V8 — D.7C CHECKPOINT

Ngày checkpoint: 2026-08-07
Track: PREP Event → Inventory
Mục tiêu hiện tại: Chứng minh một lần sản xuất từ `PREP_LOG` có thể đi từ dữ liệu người dùng nhập → hiểu recipe → tạo movement kho → staging → commit → finalize đúng một lần, không ghi kho trùng khi retry.

Checkpoint được Claude (Constitution Keeper) xác nhận nội dung nhất quán với các Flag đã nêu (Evidence Gap D.7C-1G, bỏ nhãn `TECHNICALLY LOCKED`). Nguồn: khung chat GPT/Architecture Engine, tổng hợp 2026-08-07.

Liên quan: [[CHECKPOINT-2026-07-22]] Mục II.5 (Phase D.7 kick off), [[ADR-022 Log as Input Buffer with Leader-Triggered Orchestration]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]] (D.6C — `CONVERSION_FACADE`, dùng làm published data cho track này), [[Governance-Protocol]] Mục 5 (IT Decision Authority, sinh ra từ phase này).

---

## 1. Mục tiêu nghiệp vụ của D.7C

Leader bếp chỉ cần:

```
Nhập một lần sản xuất vào PREP_LOG
→ bấm xử lý
```

Hệ thống phải tự làm:

```
PREP_LOG Event
→ hiểu công thức
→ bung các PREP INLINE
→ dừng tại RAW hoặc PREP có tồn kho thật
→ đổi đơn vị nếu cần
→ gom nguyên liệu trùng
→ tạo 1 Yield + N Consumption
→ đưa đúng một package vào staging
→ Inventory Engine xử lý
→ Ledger ghi movement đúng một lần
→ Source Event được FINALIZED đúng một lần
→ retry không được làm kho thay đổi lần thứ hai
```

**Nguyên tắc cao nhất:**

```
Reality > Sheet
Fail-closed
No partial commit
One Event = One atomic inventory operation
Không duplicate Reference Truth
Không đoán dữ liệu thiếu
```

## 2. Quyền quyết định IT — Rule mới

Đã formalize thành [[Governance-Protocol]] Mục 5 (IT Decision Authority). Tóm tắt: không bắt Thanh quyết chi tiết kỹ thuật thuần IT — Claude/GPT có quyền tự quyết/tự đóng nếu đã test tốt, an toàn, fail-closed, có khả năng phục hồi phù hợp, và không đổi ý nghĩa nghiệp vụ đã chốt. Chỉ đưa Thanh quyết khi thay đổi cách bếp vận hành, cách tính cost, ý nghĩa tồn kho/dữ liệu, quyền staff, business workflow, hoặc business rule thật.

Vocabulary trạng thái hợp lệ: `OPEN`, `CLOSED`/`PASS`, `BLOCKED`, `FAIL`. Không dùng trạng thái tự phát `TECHNICALLY LOCKED` — quyền tự khóa kỹ thuật là 1 quyền quyết định, không phải 1 status mới.

## 3. Kiến trúc PREP Inventory đã chốt

**Stock Boundary:**

```
RAW
→ terminal leaf
→ trừ RAW stock

PREP + STANDALONE
→ terminal leaf
→ trừ PREP stock

PREP + INLINE
→ không tồn kho riêng tại consumer event
→ bung recipe tiếp
```

Ví dụ: Cream Cheese Event → Soaked Cashew là STANDALONE → trừ tồn Soaked Cashew → KHÔNG bung Soaked Cashew thêm lần nữa.

Intermediate INLINE nodes chỉ tồn tại trong RAM. Không ghi chúng xuống Ledger.

## 4. D.7C-1C — Recipe Resolution

### D.7C-1C-1 — Read-only Indexes

**CLOSED / PASS**

Runtime truth:

```
PREP records       172
INLINE              82
STANDALONE          90

INLINE without recipe     0
PREP missing Item Master  0
```

Indexes:

```javascript
recipeIndex.get(parentCode) = [
  { ingredientCode, qty, unit, sourceRow }
]

prepExecutionIndex.get(prepCode) = {
  executionType, standardYield, sourceRow
}

itemIndex.get(itemCode) = {
  systemUnit, baseLocation, sourceRow
}
```

Không tạo shadow index khác trong Test Runner.

**Yield Source:** Resolver dùng `PREP_MASTER!F = Yield Qty` làm Standard Yield phục vụ recursion. `PREP_MASTER!H Standard Usable Yield` hiện chỉ là diagnostics, không tham gia Resolver.

Audit 82 INLINE: `F = H` (67), `F ≠ H` (15). Không coi 15 case khác nhau là lỗi Resolver.

**Recipe Quantity:** Resolver dùng `UNIVERSAL_RECIPE_DETAIL QTY_GROSS`, không dùng `QTY_NET` để trừ kho. Ý nghĩa: `Inventory Consumption = lượng thực sự phải lấy khỏi kho`.

## 5. Unit / Conversion Contract

Full audit: `INLINE = 82`, `Recipe edges = 394`.

Phát hiện conversion thật: `PREP-COF-COS-001` System Unit = g, Consumer recipes: 60 ml, 30 ml.

Thanh đo vật lý: `55.7g = 60ml`, `92.7g = 100ml`, `92.0g = 100ml`, Total: `240.4g = 260ml`.

Conversion thật đang dùng: `PREP-COF-COS-001, PREP, ML → G, factor = 0.924615`. Chiều `G → ML` đã bị xóa vì không có consumer hiện tại. Rule: **No Consumer → No Field / No Record**.

## 6. D.7C-1C-2B-0 — Conversion Runtime Index

**CLOSED / PASS**

`CONVERSION_FACADE` là published data của D.6C. D.6C Frozen, không sửa Compiler/Publisher. Reader runtime thuộc D.7C: `buildConversionIndex_()`.

Key: `ITEM_CODE | SOURCE_CANONICAL_UNIT` (VD: `PREP-COF-COS-001|ML`). Value giữ: `itemCode, domain, sourceUnit, targetUnit, factor, sourceRow`.

Runtime tests PASS: `DIRECT_MATCH`, `EXPLICIT_CONVERSION`, `UNIT_CONVERSION_FAILED`, `UNIT_CONVERSION_TARGET_MISMATCH`, duplicate fail-closed.

Unit canonicalization ở runtime: `g→G, ml→ML, kg→KG`. Không sửa toàn bộ sheet chỉ để uppercase.

## 7. D.7C-1C-2B-1 — Core Recursive Resolver

**CLOSED / PASS**

Core: `resolveConsumptionNode_(request, context)`. 100% RAM. Không được đọc/ghi Sheet.

Contract:

```
requiredQty
→ normalize về System Unit của node
→ RAW? return leaf
→ STANDALONE? return leaf
→ INLINE?
     scale = requiredQtySystem / Yield F
     child qty = recipe QTY_GROSS × scale
     recurse
```

Quantity trong Resolver luôn dương. Dấu âm chỉ xuất hiện ở Movement Package.

**Runtime tests:**
- Case 1: `PREP-COO-CBR-001` STANDALONE, Request 1 KG, Conversion KG→g factor 1000, Result 1000g. PASS.
- Case 2: INLINE chứa explicit conversion. PASS.
- Case 3: Nested INLINE. PASS.

Sau mọi run: `activePath.size=0, path.length=0, depth=0`.

## 8. D.7C-1C-3 — Safety Guards

**CLOSED / PASS**

Synthetic RAM tests:
- `A → B → A` → `CIRCULAR_DEPENDENCY_DETECTED`. PASS.
- Recursive depth vượt giới hạn → `MAX_RECURSION_DEPTH_EXCEEDED`. PASS.
- Child lỗi → toàn parent FAIL, không partial leaves. PASS.

Sau failure có thể chạy event mới thành công. State cleanup: `activePath=empty, path=empty, depth=0`. PASS.

## 9. D.7C-1C-4 — Leaf Consolidation

**CLOSED / PASS**

Core: `consolidateConsumptionLeaves_(leaves)`.

Consolidation key: `Item Code + Canonical Unit + Base Location`. Không convert Qty lần hai.

Real case: `PREP-BAT-BRO-001` — Resolver leaves 13, Consolidated leaves 12, Merged 1. Water: `9.6g + 250g = 259.6g`. Totals preserved = true.

## 10. D.7C-1C-5 — Single PREP Event Preview

**CLOSED / PASS**

Real event: `HA-PREP-260730-07`, `PREP-COO-RVG-001`, Batch Multiplier = 2, Actual Output = 3000g.

Preview: Exactly 1 Yield + `PREP-COO-RVG-001` 3000g.

Consumption:
```
RAW-VEG-ZUC-001   1684 g
RAW-VEG-EGG-001   1956 g
RAW-VEG-RBP-001    976 g
RAW-DRY-GAP-001      8 g
RAW-DRY-ONP-001      8 g
RAW-SPI-RUS-001      8 g
RAW-OIL-COO-001    200 g
RAW-SEA-PSA-001     24 g
```

Đã chứng minh: `Consumption = Recipe Qty × Batch Multiplier` — không tính ngược từ Actual Output. Thay Actual Output giả lập: Yield thay đổi, Consumption không thay đổi. PASS.

11 event thật trong `PREP_LOG` đều preview thành công. *(Ghi chú Constitution Keeper: chi tiết đầy đủ của 10/11 event còn lại không có trong bản checkpoint rút gọn này — chỉ có `HA-PREP-260730-07` được trình bày chi tiết. Nếu cần đối chiếu lại, bằng chứng nằm ở phiên làm việc gốc, không phải ở đây.)*

Không có event thật nào lúc đó cần INLINE/conversion; hai behavior này đã được chứng minh độc lập bằng Core tests nên không tạo fake data để làm đẹp coverage.

Workbook đang có typo thật: `Batch Mulitipiler`. Reader đọc theo Reality hiện tại. Không sửa Sheet chỉ vì typo.

## 11. D.7C-1C — Overall

```
D.7C-1C Recipe Resolution
CLOSED / PASS
```

Regression: Indexes PASS, Conversion PASS, Recursive Resolver PASS, Safety Guards PASS, Consolidation PASS, Single Event Preview PASS.

Không mở lại nếu không có Reality mới làm thay đổi contract.

## 12. D.7C-1D — Stock Movement Package

**CLOSED / PASS**

Core: `buildPrepMovementPackage_(preview)`. Thuần RAM.

Mapping:
```
Da Nang:  RAW → DN_RAW,  PREP → DN_PREP
Hoi An:   RAW → HA_RAW,  PREP → HA_PREP
Workshop: RAW → WS_RAW,  PREP → WS_PREP
```

Movement signs: YIELD positive, CONSUMPTION negative.

Transaction IDs: `EventID-YIELD`, `EventID-CON-001`, `EventID-CON-002`, ...

Tests: `realHoiAnPassed=true, daNangMappingPassed=true, workshopMappingPassed=true, transactionIdsUniquePassed=true, invalidLocationFailClosed=true, exactlyOneYieldPassed=true, regressionPassed=true, allPassed=true`.

Real HA event chứng minh: RAW ingredient → HA_RAW, STANDALONE PREP input → HA_PREP, Yield PREP → HA_PREP.

## 13. D.7C-1E — Single Package → Staging

`TRANSACTION_STAGING` physical contract:
```
A Snapshot ID
B Event ID
C Transaction ID
D Date
E Item Code
F Qty
G Unit
H Location
I Staff
J Ref ID
```

A được staging formula quản lý. Publisher chỉ được ghi `B:J`.

Staging preflight đã có từ 1A. Workspace sạch phải chứng minh: `E2=IDLE, payloadRows=0, B1 formula intact, A6 formula intact, metadata clean`.

Cleanup đã sửa đúng: `clear B6:J, preserve A6, preserve B1, reset E2=IDLE`.

### D.7C-1E-0 — Mapping Preview

**CLOSED / PASS**

Audit parity xác nhận: `Ref ID = p_id = Batch ID = Event ID`.

Core: `buildStagingRowsFromMovementPackage_()`.

Real test event: `HA-PREP-260727-01`.

Evidence: `movements=7, mapped rows=7, 9 columns B:J=true, column order correct=true, Ref ID parity=true, Snapshot A untouched=true, broken leaf failclosed=true, allPassed=true`.

At that test point: `TRANSACTION_STAGING not written, Engine not run, Ledger not touched, PREP_LOG not touched`.

## 14. D.7C-1F / 1G — Important Current Context

Sau 1E, track đã tiến tới controlled Inventory processing và Source Event Finalization. `D.7C-1G` đã được báo cáo là `Source Event Finalization — CLOSED / PASS`, có các bước `1G-2`, `1G-3`.

Tuy nhiên **không được dùng trạng thái này làm dependency chắc chắn cho phase sau ngay lúc này**, vì phát hiện một Evidence Gap.

## 15. 🚩 Current Flag — D.7C-1G Evidence Gap

Vấn đề không phải đã thấy implementation sai. Vấn đề là các bước ghi thật cuối của `1G` được báo bằng bảng/tường thuật, nhưng thiếu raw runtime evidence tương đương các phase trước: không có JSON Logger gốc, không có read-only physical verification cuối.

Khi 1G-2 mới xong, gap chỉ nằm ở một bước. Giờ vì toàn bộ `D.7C-1G` đã được ghi CLOSED/PASS, gap này trở thành nền của dependency tiếp theo.

**Checkpoint hiện tại phải ghi:**
```
D.7C-1G implementation behavior → PASS theo chuỗi test/report hiện tại
D.7C-1G evidence closure        → CHƯA ĐỦ
D.7C-1G dependency status       → CHƯA DÙNG LÀ NỀN KHÓA CHẮC CHẮN
```

Không rollback code. Không chạy lại publish. Không tạo thêm registry record. Không commit lại Ledger.

## 16. Next Action — Finalization Evidence Audit

Bước tiếp theo duy nhất: `test_D7C_1G_FinalizationEvidenceAudit()`. **READ-ONLY ONLY.** Không làm bất kỳ write nào.

Mục tiêu bằng ngôn ngữ vận hành: Chứng minh rằng một lần sản xuất đã xử lý xong được ghi nhận hoàn tất đúng một lần, và việc retry/finalize không làm kho tăng giảm lần thứ hai. Audit phải kiểm tra Event đã dùng ở flow thật.

**Tối thiểu:**
- **Registry:** `matchingRows=1, finalizedRows=1, duplicateFinalized=false`.
- **Ledger:** Package đã commit dự kiến 7 movements. Phải chứng minh `matchingMovementCount=7, Transaction IDs unique, duplicateTransactions=[], không có movement thứ 8`.
- **Staging:** `matchingPayloadRows=0`. Event đã hoàn tất không được còn payload ở trạm tạm.
- **Source Event:** Kiểm trạng thái cuối của source theo contract 1G hiện hành. Không tự phát minh business meaning mới nếu source status hiện tại có convention riêng.

## 17. Raw Evidence Format bắt buộc

Lần này không chỉ trả bảng tóm tắt. Phải giữ raw Logger JSON, ví dụ:

```json
{
  "success": true,
  "eventId": "...",
  "registry": {
    "matchingRows": 1,
    "finalizedRows": 1,
    "duplicateFinalized": false,
    "sourceRows": []
  },
  "ledger": {
    "matchingMovementCount": 7,
    "uniqueTransactionIds": true,
    "duplicateTransactions": [],
    "sourceRows": []
  },
  "staging": {
    "matchingPayloadRows": 0
  },
  "checks": {
    "exactlyOneFinalizedRecord": true,
    "ledgerCountExpected": true,
    "transactionIdsUnique": true,
    "stagingClean": true
  },
  "allPassed": true
}
```

Tên field có thể khác nếu code hiện tại dùng contract khác, nhưng bằng chứng vật lý phải tương đương.

## 18. Điều kiện đóng D.7C-1G

Nếu read-only audit chứng minh:
```
FINALIZED records  = exactly 1
Ledger movements   = exactly 7
Transaction IDs    = unique
Duplicate movement = none
Staging payload    = 0
Source final state = correct
allPassed          = true
```

→ AI tự đóng `D.7C-1G — CLOSED / PASS` và được phép dùng làm dependency cho phase sau (đúng [[Governance-Protocol]] Mục 5 — IT Decision Authority). Không cần Thanh phê duyệt kỹ thuật thêm.

Nếu một check fail: **không tuyên bố toàn D.7C-1G hỏng.** Chỉ mở đúng điểm bất thường và điều tra Reality.

## 19. Những thứ KHÔNG được làm ở bước hiện tại

```
✗ Không publish lại Event
✗ Không append Registry
✗ Không commit Ledger
✗ Không sửa PREP_LOG
✗ Không clear Staging bằng tay để làm test PASS
✗ Không tạo Event giả
✗ Không thay Transaction ID
✗ Không thay implementation 1G nếu chưa thấy lỗi vật lý
```

Chỉ đọc.

## 20. Checkpoint ngắn cho AI mới

```
KURUMI V8 / D.7C PREP INVENTORY

CLOSED/PASS:
- 1C Recipe Resolution (indexes, unit contract, conversion runtime,
  recursive resolver, cycle/depth guards, consolidation, single-event preview)
- 1D Stock Movement Package
- 1E-0 Single Package → Staging mapping preview

Architecture:
RAW = terminal stock
PREP STANDALONE = terminal stock
PREP INLINE = recursively explode
Consumption = Recipe Gross Qty × Batch Multiplier
Yield = Actual Output
One Event = one atomic package
Fail any branch = fail whole event

Current concern:
D.7C-1G Source Event Finalization was reported CLOSED/PASS,
but final physical evidence is incomplete.
Do NOT republish or modify data.

NEXT:
Run read-only test_D7C_1G_FinalizationEvidenceAudit().

Must prove:
- exactly 1 FINALIZED registry record
- exactly 7 Ledger movements
- unique Tx IDs
- no duplicate movement
- staging has 0 rows for finalized event
- source event final state correct
- raw Logger JSON retained

If all PASS:
D.7C-1G CLOSED/PASS becomes a valid dependency.
```
