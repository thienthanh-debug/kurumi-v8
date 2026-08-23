# Kurumi V8 — D.7C Master Checkpoint (v2)

> **Đã bị thay thế** bởi [[D7C-MASTER-CHECKPOINT-2026-08-10-FINAL]] (v3 — đóng phạm vi gốc D.7C với D.7C-5 Transfer hoàn tất) và [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] (mở rộng D.7C-6/7). Giữ lại bản này cho lịch sử, không dùng làm nguồn trạng thái hiện tại.

Ngày checkpoint: 2026-08-10 (cập nhật từ bản 2026-08-09)
Phạm vi: Toàn bộ track D.7C — Operational Log One-Click Processing
Thay đổi so với bản trước: D.7C-4 (PRODUCTION_LOG) đã chuyển từ BLOCKED sang CLOSED/PASS. 8/8 event thật đã hoàn tất trọn vòng đời.

Checkpoint tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON evidence của nhiều khung làm việc (GPT Architecture Engine, Claude Code Builder) qua các phiên 2026-08-07 → 2026-08-10.

---

## Phần A — Trạng thái tổng quan

```text
D.7C-1 (PREP Engine hardening)         CLOSED / PASS
D.7C-2 (PREP_LOG button, 11/11 event)  CLOSED / PASS
D.7C-3 (WASTE_LOG button, 11/11 event) CLOSED / PASS
D.7C-4 (PRODUCTION_LOG, 8/8 event)     CLOSED / PASS  ← cập nhật
D.7C-5 (TRANSFER_LOG)                  CHƯA BẮT ĐẦU
```

Mục tiêu chung xuyên suốt track:

```text
Leader nhập 1 sự kiện vào Log (Prep/Waste/Production/Transfer)
→ bấm nút
→ hệ thống tự: đọc công thức → tính movement kho → ghi Staging
  → Validate/Commit/Verify → Finalize nguồn → Archive → Clear Log
→ đúng một lần, không ghi kho trùng khi retry
```

Nguyên tắc nền tảng áp dụng nhất quán cho mọi Log (đúc kết qua PREP + WASTE + PRODUCTION):

1. Physical readback bắt buộc trước khi tin bất kỳ completion claim nào.
2. Fail-closed tuyệt đối — lỗi giữa chừng phải dừng, không cleanup giả thành công.
3. Đơn vị atomic là 1 Event — batch chỉ là vòng lặp bên ngoài.
4. Idempotent resume — mọi cơ chế phục hồi phải chống double-write, kể cả khi UI/session bị ngắt giữa chừng (đã kiểm chứng qua sự cố timeout thật ở Production Batch lượt 1 — không event nào bị chạy lại khi lượt 2 quét lại danh sách eligible).
5. Business rejection ≠ orchestration failure.
6. Lazy validation — không validate toàn bộ Master Data trước khi biết event có cần dùng tới phần đó hay không.
7. Vá đúng gốc, không patch triệu chứng.
8. Ai quyết = Reality Owner — số liệu quy đổi, ý nghĩa dữ liệu luôn cần Thanh xác nhận, không đoán.
9. Không mở Orchestrator (nút bấm) trước khi Resolver/Compiler nền đã an toàn — audit trước, build sau.
10. Trước khi hỏi Reality Owner một số liệu quy đổi, luôn audit lại xem rule đã tồn tại sẵn trong hệ thống chưa (CONVERSION_FACADE_COMPILER/Published) — tránh hỏi lại thông tin đã có (bài học từ việc phát hiện rule Coffee Shot từng tồn tại nhưng bị mất).
11. Conversion Rule là Master Data lâu dài — KHÔNG thuộc nhóm dữ liệu test được phép xóa/reset cùng Ledger/Archive/Closure.

---

## Phần B — D.7C-2: PREP_LOG (CLOSED / PASS)

Không đổi so với bản trước — xem chi tiết đầy đủ trong [[D7C3-WASTE-BUTTON-ORCHESTRATION-CHECKPOINT-2026-08-09]] và [[D7C-PREP-INVENTORY-CHECKPOINT-2026-08-07]].

Tóm tắt:

```text
RAW                    → terminal, trừ RAW stock
PREP + STANDALONE      → terminal, trừ PREP stock
PREP + INLINE          → bung recipe tiếp (RAM only)

D.7C-1C → 1G   Recipe Resolution → Source Finalization   CLOSED/PASS
D.7C-2A → 2E   Button Contract → Archive/Auto-clear        CLOSED/PASS

Kết quả cuối: 11/11 event PREP_LOG thật đã qua trọn vòng đời.
Ledger sạch (0 Qty trống), Archive/Closure khớp 1:1, không double-write.
```

Sự cố lớn đã vá: WAIT_REVIEW resume mất effectiveQty, Archive/Clear sai phạm vi cột, Dual-mode Closure Guard, Apps Script timeout (giới hạn 5 event/lượt).

---

## Phần C — D.7C-3: WASTE_LOG (CLOSED / PASS)

Không đổi so với bản trước. Xem [[D7C3-WASTE-BUTTON-ORCHESTRATION-CHECKPOINT-2026-08-09]].

Tóm tắt:

```text
6 domain: RAW/SEMI/PREP STANDALONE/PREP INLINE/FINAL materialized/
FINAL non-materialized — xử lý qua Waste Domain Router riêng
(resolveWasteConsumption_), dùng lại Core Resolver cho nhánh PREP.

Waste chỉ có Consumption (âm), KHÔNG có Yield, KHÔNG có WARNING/
WAIT_REVIEW — chỉ OK/CRITICAL.

Event Identity: Sheet Counter (SOURCE_EVENT_SEQUENCE), theo
Branch+Date, atomic dưới DocumentLock.

D.7C-3A → 3A-2   Contract Audit → Identity + Domain Router   CLOSED/PASS
D.7C-3B          Logic Orchestrator                          CLOSED/PASS
D.7C-3C          Bind Button + 7 patch sự cố thực tế          CLOSED/PASS

Kết quả cuối: 11/11 event WASTE_LOG thật đã qua trọn vòng đời.
2 dòng INVALID_INPUT còn lại chờ người nhập bổ sung, không chặn gì.
```

7 patch đã xử lý: eager validation, archive index sai, canonicalization "1 Batch", 3 conversion rule thiếu (OCP batch/portion, STR-001 batch), 2 lỗi nhãn đơn vị nguồn (syrup, soy sauce — nên "ml" thực chất là "g" vì luôn cân, không đong), canonicalization target unit (WHOLE_CAKE).

---

## Phần D — D.7C-4: PRODUCTION_LOG (CLOSED / PASS) ⭐ cập nhật

### D.7C-4A — Audit ban đầu (COMPLETED / BLOCKED → đã giải quyết)

Schema `PRODUCTION_LOG!A:J` — 8 event thật (5 FINAL, 3 SEMI):

```text
A Batch ID (SYSTEM_FORMULA)      F Product Type (SYSTEM_FORMULA)
B Date (MANUAL)                  G Production Qty (MANUAL)
C Product Name (MANUAL DROPDOWN) H Unit (SYSTEM_FORMULA)
D SKU Code (SYSTEM_FORMULA)      I Production Staff (MANUAL DROPDOWN)
E BASE CODE (SYSTEM_FORMULA)     J Status Flag (SYSTEM_FORMULA)
```

**3 blocker nghiêm trọng tìm thấy trên dữ liệu thật — tất cả đã vá:**

1. **Identity không ổn định** (đã vá ở D.7C-4A-1). Công thức cũ: `DN-ASSM-{YYMMDD}-{ROW(A)-1}` — phụ thuộc row number. Đã sửa: Stable Batch ID bằng `SOURCE_EVENT_SEQUENCE` (theo Date, không cần Branch trong key vì chỉ có 1 chi nhánh), atomic dưới DocumentLock, format giữ nguyên `DN-ASSM-{YYMMDD}-{SEQUENCE}`.

2. **Branch hardcode "DN"** (KHÔNG PHẢI BUG — đã xác nhận với Reality Owner). Quyết định: Production chỉ diễn ra ở Workshop/DN, không có chi nhánh khác làm Production. Hardcode DN là chính sách vận hành có chủ đích, đã ghi rõ trong code, không cần sửa.

3. **Nested INLINE bị bỏ sót** — bằng chứng thật, đã vá (D.7C-4A-1). Event `DN-ASSM-260619-005`, Compiler row 73 (cũ): `PREP-COF-COS-001` (Execution Type=INLINE) từng bị giữ làm terminal consumption (-120ml) thay vì bung tiếp. Đã vá: `resolveProductionConsumption_()` viết mới, dùng Core Resolver, circular guard và consolidation chung (giống pattern Waste Domain Router). Kết quả thật sau vá: `inlineNodeExpanded: true`, `inlinePrepAbsentFromLeaves: true`, `inlineNodesResolved: 4`, `contextClean: true`.

4. **Thiếu Consolidation** — đã vá cùng patch trên. 6/8 event từng có nhiều dòng trùng Item+Unit+Location. Regression thật (Tiramisu, `DN-ASSM-260612-001`): `inputLeafCount: 20 → outputLeafCount: 12`, `mergedLeafCount: 8`, `totalsPreserved: true`. Xác nhận lại khi chạy Single thật: Ledger ghi đúng 13 dòng (1 Yield + 12 Consumption đã gộp), `PREP-NUT-SOC-001` xuất hiện đúng 1 dòng duy nhất (-277.2g) thay vì rải rác nhiều dòng.

**Sự cố phụ trong lúc vá — Conversion Rule bị mất khỏi hệ thống:**

`PREP-COF-COS-001` (Coffee Shot) ML→G factor=0.924615 — rule này đã từng được đo vật lý thật và publish (xem Phần C, track Waste), nhưng khi audit lại ở Production, rule không còn tồn tại ở bất kỳ tầng nào (Explicit Rule, Staging, Validation, Compiler, Published Facade).

Nguyên nhân xác định: một lần rebuild toàn phần trước đó không giữ được rule cũ trong `CONVERSION_EXPLICIT_RULE` — KHÔNG liên quan tới D.7C-2E (lần reset đó chỉ định xóa Ledger/Archive/Closure, không xóa Conversion Rule).

Bài học đã ghi vào Phần A (nguyên tắc 10, 11): trước khi hỏi Reality Owner một số liệu, luôn audit rule đã tồn tại sẵn chưa; Conversion Rule là Master Data lâu dài không được xóa cùng dữ liệu test.

Đã khôi phục: CER-0008, PREP-COF-COS-001, PREP, ML→G, factor=0.924615, publish thành công, regression Coffee Shot + Tiramisu đều PASS.

### D.7C-4B — Production Logic Orchestrator (CLOSED / PASS)

Tái sử dụng nguyên khối contract D.7C-2B/3B — không thiết kế lại:

```text
scanEligibleProductionLogEvents_()
lookupExactProductionLogEvent_(batchId)
processOneProductionLogEvent_(batchId)
processProductionLogBatch(ids?)   — skip-and-continue, MAX 5/lượt
buildOperatorResult_()            — dùng chung
```

Patch riêng (khác PREP/WASTE):

```text
countSourceEventRows_ sửa để nhận "Batch ID" cho PRODUCTION_LOG
archiveAndClearProductionLogRow_ viết bản riêng, đọc đúng header
thật của PRODUCTION_LOG_ARCHIVE (12 cột) trước khi code
```

Production KHÔNG có WARNING/WAIT_REVIEW — giống Waste, khác PREP. Mỗi package đúng 1 Yield dương + N Consumption âm — giống PREP, khác Waste (chỉ Consumption).

### D.7C-4C — Bind Button + Operator Feedback (CLOSED / PASS)

Menu bổ sung: "Xử lý Production Event này" / "Xử lý toàn bộ Production" → Tổng menu hiện có 6 mục (2 PREP + 2 Waste + 2 Production).

**Single Proof thật** — `DN-ASSM-260612-001` (Tiramisu): 13 dòng Ledger (1 Yield + 12 Consumption đã consolidate), Archive 1 dòng, Closure 1 record, cột formula A/D/E/F/H/J giữ nguyên.

**Batch Proof thật** — 7 event còn lại, 2 lượt (5+2): 8/8 event FINALIZED, 71 dòng Ledger batch (tổng 84 dòng Production Ledger), 0 Qty trống, 0 duplicate Transaction ID, mỗi event đúng 1 Yield, Archive/Closure khớp 1:1 với 8 event.

**Sự cố vận hành đã xử lý đúng — KHÔNG PHẢI LỖI:** Lượt 1 Batch gặp UI/session TIMEOUT sau khi 5 event đã Commit/Finalize/Archive/Cleanup xong. Lượt 2 tự động quét lại danh sách eligible, không event nào bị chạy lại — xác nhận đúng giá trị thực tế của thiết kế "mỗi lần bấm chỉ động vào event chưa FINALIZED": không cần giữ lock xuyên suốt UI session, chỉ cần trạng thái dữ liệu đúng tại mọi thời điểm.

**Kết quả cuối:** 8/8 event PRODUCTION_LOG thật đã qua trọn vòng đời — Resolver (đã vá Nested INLINE + Consolidation) → Staging → Ledger → Finalize → Archive → Clear. Không dữ liệu mồ côi, không double-write, không Qty trống.

---

## Phần E — D.7C-5: TRANSFER_LOG (chưa bắt đầu)

Sheet đã xác nhận tồn tại trong workbook, chưa audit.

Khi bắt đầu, đi đúng quy trình đã chuẩn hóa qua 3 lần (PREP, WASTE, PRODUCTION):

```text
D.7C-5A     Integration Contract Audit (read-only trước)
D.7C-5A-1   Identity + Resolver/Router Boundary (nếu phát hiện
            blocker nền — Identity không ổn định hoặc Compiler
            thiếu an toàn, đã xảy ra ở cả Waste lẫn Production)
D.7C-5B     Logic Orchestrator
D.7C-5C     Bind Button + Operator Feedback
```

Checklist audit đã chuẩn hóa qua 3 lần lặp — dùng lại nguyên khối câu hỏi cho D.7C-5A:

1. Schema đầy đủ — cột nào input tay, cột nào công thức hệ thống (đối chiếu `getFormula()` thật, KHÔNG suy đoán theo tên cột — bài học lặp lại 3 lần: PREP D/G, Waste A:P header, Production Batch ID).
2. Event Identity — có phụ thuộc row number không? (đã sai ở cả Waste và Production ban đầu, phải sửa cả 2 lần).
3. Compiler hiện có — dùng Resolver/Router chung hay logic riêng độc lập? Nếu riêng — đối chiếu 3 safety guard (Nested INLINE, Circular Dependency, Consolidation) bằng dữ liệu THẬT, không chỉ lý thuyết (Nested INLINE đã thật sự sai ở cả Waste và Production khi kiểm tra dữ liệu thật).
4. Movement contract — Yield dương có không, hay chỉ Consumption? Transfer có khả năng là 2 chiều (xuất kho A + nhập kho B) — CẦN XÁC NHẬN RIÊNG, chưa từng gặp pattern này ở 3 Log trước (tất cả đều 1 chiều: Waste/Production tiêu thụ, PREP tạo mới).
5. Routing NORMAL/WARNING/CRITICAL — có WARNING không?
6. Nút Single/Batch hiện có chưa.
7. Khả năng tái sử dụng Resolver/Staging/Engine/Closure/Archive từ 3 Log trước — phần nào dùng chung ngay, phần nào cần riêng.
8. Conversion Rule — audit trước khi hỏi Reality Owner bất kỳ số liệu nào (nguyên tắc 10 đã đúc kết).

---

## Phần F — Bài học continuity (để khung AI sau đọc, tránh lặp lỗi)

1. Khi có nhiều nhánh việc song song (patch kỹ thuật + chờ số liệu vận hành từ Thanh), phải chủ động hỏi lại trạng thái nhánh còn treo trước khi coi là đã xong.
2. Không tái sử dụng số hiệu Phase cho nội dung khác mà không ghi rõ CANCELLED.
3. Nhãn trạng thái ngoài 4 giá trị chuẩn (OPEN/CLOSED-PASS/BLOCKED/FAIL) không được tự phát minh và lan truyền.
4. Rule/Governance mới xuất hiện trong tài liệu cần xác minh nguồn gốc (Thanh duyệt hay AI tự đề xuất) trước khi coi là có thẩm quyền. **Áp dụng thật ngay trong track này:** một "Rule 5 — IT Decision Authority" từng bị thêm vào [[Governance-Protocol]] dựa trên nội dung relay của chính track D.7C, sau đó bị phát hiện là AI_SELF_PROPOSED chứ không phải Thanh duyệt trực tiếp — đã gỡ khỏi Governance Protocol ngày 2026-08-10, chờ Thanh xác nhận lại nếu muốn giữ.
5. Luôn yêu cầu raw JSON/Logger, không chấp nhận báo cáo tóm tắt bằng lời cho bất kỳ hành động ghi dữ liệu thật.
6. Trước khi hỏi Reality Owner một số liệu quy đổi/định lượng, audit lại xem hệ thống đã có sẵn số liệu đó chưa — tránh hỏi lại thông tin đã tồn tại. Đã xảy ra 1 lần (Coffee Shot factor 0.924615 từng có, mất đi qua rebuild, được phát hiện lại nhờ audit thay vì hỏi lại Thanh ngay).
7. Conversion Rule (`CONVERSION_EXPLICIT_RULE` và toàn bộ chuỗi Facade) là Master Data lâu dài — không thuộc nhóm dữ liệu test được phép xóa/reset. Khi thực hiện bất kỳ thao tác "dọn dữ liệu test" nào (như D.7C-2E), phải xác định rõ phạm vi KHÔNG bao gồm Conversion Rule.
8. Timeout/ngắt kết nối UI giữa lúc Batch đang chạy KHÔNG đồng nghĩa với lỗi dữ liệu — thiết kế finalized-exclusion cho phép an toàn bấm lại nhiều lần mà không double-write. Không cần hoảng khi thấy timeout; luôn hậu kiểm bằng physical readback trước khi kết luận có sự cố thật hay chỉ là UI bị ngắt.

---

Liên quan: [[D7C3-WASTE-BUTTON-ORCHESTRATION-CHECKPOINT-2026-08-09]], [[D7C-PREP-INVENTORY-CHECKPOINT-2026-08-07]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]], [[Governance-Protocol]] (Mục 4 — khuôn Flag áp dụng cho việc gỡ Rule 5).
