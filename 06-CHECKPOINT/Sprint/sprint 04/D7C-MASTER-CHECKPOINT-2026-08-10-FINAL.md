# Kurumi V8 — D.7C Master Checkpoint (v3 — FINAL)

**Ngày checkpoint:** 2026-08-10
**Phạm vi:** Toàn bộ track D.7C — Operational Log One-Click Processing
**Trạng thái:** TOÀN BỘ 4 LOG ĐÃ CLOSED/PASS. Track D.7C khép kín.

> Bản này là bản đóng track chính thức cho phạm vi gốc D.7C (Prep/Waste/Production/Transfer). Xem [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] cho phần mở rộng sau đó (D.7C-6 Stock Input, D.7C-7 Stock Dashboard) — không nằm trong phạm vi gốc track này.

---

## Phần A — Trạng thái tổng quan (FINAL)

```text
D.7C-1 (PREP Engine hardening)         CLOSED / PASS
D.7C-2 (PREP_LOG,        11/11 event)  CLOSED / PASS
D.7C-3 (WASTE_LOG,       11/11 event)  CLOSED / PASS
D.7C-4 (PRODUCTION_LOG,   8/8 event)   CLOSED / PASS
D.7C-5 (TRANSFER_LOG,     6/6 event)   CLOSED / PASS  ← mới hoàn tất
TỔNG: 36/36 event thật trên cả 4 Log đã qua trọn vòng đời
(Resolver/Router → Staging → Ledger → Finalize → Archive → Clear),
không dữ liệu mồ côi, không double-write, không Qty trống.
```

Mục tiêu track đã đạt được đầy đủ:

```text
Leader nhập 1 sự kiện vào bất kỳ Log nào (Prep/Waste/Production/
Transfer) → bấm nút → hệ thống tự động toàn bộ chuỗi xử lý → đúng
một lần, không ghi kho trùng khi retry, không cần biết gì về kỹ
thuật bên trong.
```

### Menu cuối cùng (8 mục, xác nhận trên sheet thật)

```text
Xử lý Event này              (PREP Single)
Xử lý toàn bộ                 (PREP Batch)
Xử lý Waste Event này          (Waste Single)
Xử lý toàn bộ Waste             (Waste Batch)
Xử lý Production Event này      (Production Single)
Xử lý toàn bộ Production          (Production Batch)
Xử lý Transfer Event này           (Transfer Single)
Xử lý toàn bộ Transfer               (Transfer Batch)
```

---

## Phần B — Kiến trúc chung đã chuẩn hóa qua 4 lần lặp

### Cơ chế Button (mẫu dùng chung cho mọi Log)

```text
scanEligibleXxxLogEvents_()   — quét toàn bộ, loại FINALIZED
lookupExactXxxLogEvent_(id)   — tìm ĐÚNG 1 dòng khớp ID, fail-closed
processOneXxxLogEvent_(id)    — đơn vị atomic trọn vòng đời
processXxxLogBatch(ids?)      — skip-and-continue, MAX 5 event/lượt
buildOperatorResult_()        — chuẩn hóa payload, KHÔNG UI
showOperatorFeedback_()       — tầng UI riêng, chỉ nó gọi getUi()
```

### Semantics outcome (áp dụng mọi Log)

```text
success PHẢN ÁNH: orchestrator xử lý đúng contract hay không.
success KHÔNG PHẢN ÁNH: event được chấp nhận hay bị từ chối nghiệp vụ.
COMMITTED_AND_FINALIZED / CRITICAL_REJECTED / ALREADY_FINALIZED /
INVALID_SOURCE_DATA / WAIT_REVIEW (chỉ PREP)  → success=true
success=false CHỈ khi: NOT_FOUND/AMBIGUOUS, lỗi hạ tầng thật
(schema/resolver/staging/engine FAILED/lock-timeout/exception).
Quy tắc pause: lỗi hạ tầng ở 1 event → skip-and-continue. CHỈ
WAIT_REVIEW mới pause toàn batch (chiếm Single-Event Workspace).
```

### Đặc điểm riêng của từng Log (bảng so sánh)

| | PREP | WASTE | PRODUCTION | TRANSFER |
|---|---|---|---|---|
| Movement | 1 Yield(+) + N Consumption(-) | Chỉ Consumption(-) | 1 Yield(+) + N Consumption(-) | Đúng 2: OUT(-) + IN(+) |
| Domain xử lý | RAW, PREP | RAW/SEMI/PREP/FINAL (6 domain) | RAW, PREP (qua FINAL/SEMI recipe) | Không bung recipe — chuyển nguyên Item |
| Cần Resolver? | Có (Core Resolver) | Có (Domain Router riêng, gọi lại Core) | Có (Router riêng, gọi lại Core) | KHÔNG — chỉ paired movement builder |
| WARNING/WAIT_REVIEW | Có (LOW/OVER YIELD) | Không | Không | Không |
| Event Identity | Batch ID cột G (tĩnh) | Sheet Counter theo Branch+Date | Sheet Counter theo Date | Sheet Counter theo Date |
| Bất biến đặc thù | — | — | Consolidation trùng key | ABS(OUT)=IN, Net=0, Location khác nhau |

---

## Phần C — Tóm tắt từng Log

### D.7C-2: PREP_LOG (chi tiết đầy đủ ở [[D7C-PREP-INVENTORY-CHECKPOINT-2026-08-07]])

```text
RAW/PREP STANDALONE = terminal. PREP INLINE = bung recipe (RAM only).
Sự cố lớn: WAIT_REVIEW resume mất effectiveQty (đã vá bằng targeted
rehydration), Archive/Clear sai phạm vi cột, Dual-mode Closure Guard,
Apps Script timeout (giới hạn 5/lượt).
```

### D.7C-3: WASTE_LOG (chi tiết đầy đủ ở [[D7C3-WASTE-BUTTON-ORCHESTRATION-CHECKPOINT-2026-08-09]])

```text
6 domain qua Waste Domain Router riêng, dùng lại Core Resolver cho
nhánh PREP. 7 patch: eager validation, archive index sai,
canonicalization 1 chiều, 3 conversion rule thiếu, 2 nhãn đơn vị sai
(syrup/soy — luôn cân không đong), Compiler baseline hard-code.
```

### D.7C-4: PRODUCTION_LOG (chi tiết đầy đủ ở [[D7C-MASTER-CHECKPOINT-2026-08-10]] — bản v2)

```text
3 blocker nghiêm trọng đã vá: Identity phụ thuộc row number, Nested
INLINE bị bỏ sót thật (Coffee Shot -120ml sai), Consolidation thiếu
(Tiramisu 20→12 leaves). Branch hardcode "DN" là chính sách vận hành
cố ý (Production chỉ ở Workshop), không phải bug.
Sự cố phụ: Conversion Rule Coffee Shot (0.924615) từng mất khỏi hệ
thống qua 1 lần rebuild — khôi phục bằng audit thay vì hỏi lại Thanh.
```

### D.7C-5: TRANSFER_LOG (mới hoàn tất — chi tiết đầy đủ lần đầu)

**Đặc điểm cấu trúc riêng — khác biệt lớn nhất so với 3 Log trước:**

```text
Movement 2 CHIỀU (paired OUT/IN) — pattern chưa từng gặp:
  OUT: qty=-X tại Source Location
  IN:  qty=+X tại Destination Location (CÙNG Item, CÙNG Unit)
Bất biến bắt buộc:
  Exactly 2 movements, distinct Transaction IDs
  Source Qty < 0, Destination Qty > 0
  ABS(Source Qty) = Destination Qty
  Source Location != Destination Location
  Net Qty theo Item = 0
KHÔNG cần Resolver — Transfer chuyển nguyên Item tồn kho, không
bung recipe. PREP transfer vẫn giữ nguyên là PREP, không tách
thành nguyên liệu.
```

**Trình tự phase:**

```text
D.7C-5A     Integration Contract Audit             COMPLETED/BLOCKED
            (blocker: chưa có paired movement, chỉ 1 dòng dương
             với field From/To rời rạc)
D.7C-5A-1   Stable Identity + Paired Movement +      CLOSED/PASS
            Location Mapping + Conversion (kg→g)
D.7C-5B     Transfer Logic Orchestrator               CLOSED/PASS
D.7C-5C     Bind Button + Operator Feedback            CLOSED/PASS
```

**Sự cố đã gặp và xử lý:**

```text
1. Header "Tranfer ID" viết thiếu chữ "s" trong dữ liệu gốc — GIỮ
   NGUYÊN chính tả cũ (không tự sửa lỗi chính tả trên sheet production),
   code đọc đúng tên cột thật.

2. Location Mapping — audit dữ liệu thật trước khi code (không suy
   đoán): From/To ghi tên chi nhánh thật ("Da Nang", "Workshop", "Hoi
   An"), map đúng sang BranchPrefix_Domain (DN_RAW, WS_FINAL, HA_SEMI...)
   thay vì placeholder chung "BRANCH_STOCK/WORKSHOP_STOCK" của bản cũ.

3. RUN_SELECTOR_SELECTION_RACE — sự cố vận hành con người, không phải
   lỗi logic. Khi file mới lưu, hàm đầu tiên trong Run selector của
   Apps Script Editor tự động thành default; thao tác bấm Run mà
   không xác nhận lại tên hàm đang chọn đã khiến processTransferLogBatch
   chạy ngoài kế hoạch trên TR-260622-01.
   Hậu quả: KHÔNG PHẢI SỰ CỐ DỮ LIỆU. Event đó hoàn tất hợp lệ (Ledger
   đúng, Closure FINALIZED, Archive lưu đủ). Chỉ Archive bước đầu fail
   (sheet đích chưa tồn tại lúc đó) → Engine tự resume đúng phần
   Finalize/Archive/Cleanup còn thiếu, KHÔNG quay lại COMMIT, KHÔNG
   double-write. Đây là bằng chứng sống cho giá trị thực tế của cơ
   chế idempotent resume đã xây dựng xuyên suốt track.
   Vá: dọn 2 helper wrapper (setup/migration đã hoàn thành nhiệm vụ)
   khỏi Run selector trước khi bind nút chính thức.
```

**Kết quả cuối:** 6/6 event TRANSFER_LOG thật đã hoàn tất trọn vòng đời — 5 event chạy qua đúng menu chính thức, 1 event (TR-260622-01) hoàn tất qua sự cố Editor nhưng vẫn đúng và an toàn nhờ idempotent resume. 12 dòng Ledger (6×2), 6 Closure record, 6 Archive record, 0 duplicate, 0 Qty trống, mọi cặp Net=0.

---

## Phần D — Nguyên tắc nền tảng (đúc kết cuối cùng qua 4 lần lặp)

```text
1. Physical readback bắt buộc trước khi tin bất kỳ completion claim.
2. Fail-closed tuyệt đối — lỗi giữa chừng phải dừng, không cleanup
   giả thành công.
3. Đơn vị atomic là 1 Event — batch chỉ là vòng lặp bên ngoài.
4. Idempotent resume — chống double-write kể cả khi UI/session/Editor
   bị ngắt hoặc thao tác nhầm giữa chừng (đã kiểm chứng thật 2 lần:
   Production Batch timeout, Transfer Run Selector Race).
5. Business rejection ≠ orchestration failure.
6. Lazy validation — không validate toàn bộ Master Data trước khi
   biết event có cần dùng tới phần đó hay không.
7. Vá đúng gốc, không patch triệu chứng.
8. Ai quyết = Reality Owner — số liệu quy đổi, ý nghĩa dữ liệu luôn
   cần Thanh xác nhận, không đoán.
9. Không mở Orchestrator (nút bấm) trước khi Resolver/Compiler nền
   đã an toàn — audit trước, build sau. Áp dụng đúng 4/4 lần.
10. Trước khi hỏi Reality Owner một số liệu quy đổi, luôn audit xem
    rule đã tồn tại sẵn trong hệ thống chưa.
11. Conversion Rule là Master Data lâu dài — KHÔNG thuộc nhóm dữ liệu
    test được phép xóa/reset cùng Ledger/Archive/Closure.
12. [MỚI] Không tự sửa lỗi chính tả/format trong dữ liệu Master hiện
    có (như "Tranfer ID") chỉ vì phát hiện ra khi audit — giữ nguyên
    parity với dữ liệu thật, code thích ứng theo dữ liệu chứ không
    ép dữ liệu theo code.
13. [MỚI] Rủi ro "Run Selector Selection Race" khi thao tác qua Apps
    Script Editor trực tiếp — luôn xác nhận lại tên hàm đang chọn
    trước khi bấm Run, đặc biệt sau khi vừa lưu/thêm file mới. Dọn
    dẹp helper wrapper tạm thời (setup/migration) khỏi Run selector
    ngay sau khi hoàn thành nhiệm vụ, không để chúng tồn tại lâu dài
    làm tăng rủi ro chạy nhầm.
14. [MỚI] Khi audit một Log mới, luôn kiểm tra xem Movement Contract
    có khác biệt cấu trúc so với các Log trước không (ví dụ Transfer
    là 2 chiều trong khi 3 Log kia đều 1 chiều) — không mặc định
    mọi Log đều có cùng shape dữ liệu.
```

---

## Phần E — Trạng thái Governance (cập nhật riêng)

```text
Rule 5 (IT Decision Authority) trong Governance-Protocol.md đã được
GỠ BỎ — xác nhận là AI_SELF_PROPOSED, chưa từng có Thanh duyệt trực
tiếp. Đã thay bằng ghi chú giải thích lý do gỡ và điều kiện để thêm
lại nếu Thanh thật sự muốn chính thức hóa.
Đây là hành động ĐÚNG, khớp với audit đã thực hiện nhiều lượt trước
trong chính track này.
```

Cập nhật thực tế (2026-08-10, cùng phiên): Thanh đã trực tiếp xác nhận nội dung Mục 5 mới — "Domain Authority" (hỏi Thanh khi đụng chuyên môn vận hành bếp, không hỏi khi thuần kỹ thuật IT). Xem [[Governance-Protocol]].

---

## Phần F — Track D.7C: khép kín

```text
Toàn bộ mục tiêu ban đầu của D.7C đã đạt được:
"Leader bấm nút → hệ thống tự động toàn bộ compile → validate →
commit → verify → clear, đúng một lần" — cho CẢ 4 loại sự kiện vận
hành (Prep/Waste/Production/Transfer).
Không còn Log nào trong roadmap gốc (WASTE → TRANSFER) chưa xử lý.
Không có blocker nào còn treo ở bất kỳ track nào trong 4 track.
Việc còn lại (nếu có, thuộc phạm vi ngoài D.7C):
- Vận hành thực tế lâu dài: theo dõi có phát sinh Log mới nào khác
  cần cùng pattern không (ví dụ Adjustment, Return...)
- Dọn dẹp kỹ thuật định kỳ: rà soát Run selector định kỳ tránh tích
  tụ helper cũ (bài học từ 2 sự cố Run Selector đã gặp)
- Sprint/Mission tiếp theo: do Reality Owner (Thanh) quyết định dựa
  trên nhu cầu vận hành thực tế của bếp.
```

Ghi chú thực tế: ngay trong cùng phiên, track đã mở rộng tiếp sang D.7C-6 (Stock Input) và D.7C-7 (Stock Dashboard) — xem [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]]. "Khép kín" ở đây chỉ đúng cho phạm vi gốc 4 Log (Prep/Waste/Production/Transfer).

---

Checkpoint cuối cùng của phạm vi gốc track D.7C, tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON evidence của nhiều khung làm việc (GPT Architecture Engine, Claude Code Builder) qua các phiên 2026-08-07 → 2026-08-10.

Liên quan: [[D7C-MASTER-CHECKPOINT-2026-08-10]] (bản v2, trước khi Transfer hoàn tất), [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] (mở rộng D.7C-6/7), [[D7C-PREP-INVENTORY-CHECKPOINT-2026-08-07]], [[D7C3-WASTE-BUTTON-ORCHESTRATION-CHECKPOINT-2026-08-09]], [[Governance-Protocol]].
