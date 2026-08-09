# KURUMI V8 — D.7C-3 CHECKPOINT (WASTE_LOG Button Orchestration)

Ngày checkpoint: 2026-08-09
Track: WASTE_LOG Event → Inventory (nhân bản pattern từ D.7C PREP_LOG)
Mục tiêu: Chứng minh nút bấm WASTE_LOG có thể xử lý một mẻ khai báo hao hụt từ dữ liệu người dùng nhập → Resolver đa domain (RAW/SEMI/PREP/FINAL) → movement kho âm → staging → commit → finalize → archive/clear, đúng một lần, không ghi kho trùng khi retry.

**Quan hệ với Checkpoint D.7C chính (PREP_LOG):** D.7C-3 kế thừa toàn bộ hạ tầng đã CLOSED/PASS ở D.7C-1C→2E (Resolver core, Staging, Engine, Closure Registry, Archive pattern) — không viết lại, chỉ thêm lớp thích ứng cho `WASTE_LOG`.

Checkpoint được Claude (Constitution Keeper / Architecture Engine) tổng hợp từ log audit thật nhiều khung làm việc (GPT Architecture Engine, Claude Code Builder), đối chiếu bằng chứng raw JSON tại mỗi bước. Nguồn: phiên làm việc 2026-08-08 → 2026-08-09.

Liên quan: [[D7C-PREP-INVENTORY-CHECKPOINT-2026-08-07]] (hạ tầng kế thừa), [[WASTE-ENGINE-CHECKPOINT-2026-07-22]] (Consumption Resolver/Conversion Facade — Mục 5/7, D.6C Freeze), [[CHECKPOINT-2026-07-22]] Mục II.5 (Phase D.7 kick off), [[ADR-022 Log as Input Buffer with Leader-Triggered Orchestration]], [[Governance-Protocol]] Mục 5 (IT Decision Authority).

---

## 1. Kiến trúc Waste — khác biệt so với PREP

### Domain Router (khác PREP — PREP chỉ có RAW/PREP)

```
WASTE có 6 domain cần xử lý, PREP Core Resolver chỉ hỗ trợ RAW/PREP:

RAW                        → terminal leaf
SEMI                       → terminal leaf
PREP STANDALONE            → terminal leaf
PREP INLINE                → giao cho resolveConsumptionNode_() (Core Resolver
                              dùng chung với PREP, KHÔNG sửa)
FINAL materialized         → terminal leaf (có Assembly Detail)
FINAL non-materialized     → đọc Final Finishing Detail, route từng con theo
                              cùng boundary, consolidate cuối
```

**Quyết định kiến trúc (đã khóa, D.7C-3A-1):**

```
Phương án chọn: Waste Domain Router riêng (resolveWasteConsumption_)
Phương án bị loại: Tổng quát hóa Core Resolver
Lý do: Core Resolver đã CLOSED/PASS cho PREP, mở lại có rủi ro regression
       cao hơn lợi ích. Router riêng dùng chung activePath/path/depth/
       maxDepth/circular guard/conversion facade/consolidation — không copy
       logic, chỉ gọi lại.
```

### Movement Contract (khác PREP)

```
PREP:  1 YIELD (dương) + N CONSUMPTION (âm)
WASTE: chỉ N CONSUMPTION (âm) — KHÔNG có YIELD

Waste không có khái niệm WARNING/WAIT_REVIEW.
Routing chỉ có: OK (COMMITTED) / CRITICAL (REJECTED).
→ Cơ chế inline-confirmation (PATCH-3 của PREP) KHÔNG áp dụng cho Waste.
```

### Event Identity (đã sửa lỗi nền tảng trước khi build orchestrator)

```
Vấn đề gốc: Compiler cũ sinh ID theo WST-{Branch}-{YYMMDD}-R{row_number}
            → ID đổi nếu ai chèn/xóa dòng trên WASTE_LOG. Nguy hiểm.

Đã sửa (D.7C-3A-2): Sheet counter riêng SOURCE_EVENT_SEQUENCE
  - 1 dòng/(Branch+Date), sequence tăng dần
  - Cấp ID chỉ khi Validation Status = VALID
  - Đọc-tăng-ghi atomic dưới DocumentLock
  - Ghi 1 lần vào WASTE_LOG!N, sau đó bất biến
  - Không tái sử dụng số đã cấp (chấp nhận khoảng trống)
  - Format: WST-{BRANCH}-{YYMMDD}-{SEQUENCE}, ví dụ WST-HA-260722-0001

Lý do chọn Sheet Counter thay vì PropertiesService hay Append-only Registry:
  - PropertiesService: khó audit trực tiếp bằng mắt (đã từng gây khó khăn
    thực tế ở PREP track khi cần debug session kẹt)
  - Registry đầy đủ lịch sử: phức tạp hơn mức cần thiết cho giai đoạn này
  - Sheet Counter: cân bằng — dễ nhìn, dễ audit, độ phức tạp vừa đủ
```

### `WASTE_LOG` Schema (đã audit chính xác, tránh lặp lỗi D/G như `PREP_LOG`)

```
Cột       Header                  Loại
A         Date                    MANUAL_INPUT
B         Item                    MANUAL_INPUT_DROPDOWN
C         Item Code               SYSTEM_FORMULA (ARRAYFORMULA VLOOKUP)
D         Waste Qty               MANUAL_INPUT
E         Unit                    MANUAL_INPUT_DROPDOWN
F         Reason                  MANUAL_INPUT_DROPDOWN
G         Process Stage           MANUAL_INPUT_DROPDOWN
H         Staff                   MANUAL_INPUT_DROPDOWN
I         Branch                  MANUAL_INPUT_DROPDOWN
J         Evidence                MANUAL_INPUT
K         Investigation Flag      MANUAL_INPUT_DROPDOWN
L         Loss Type               MANUAL_INPUT_DROPDOWN
M         Validation Status       SYSTEM_FORMULA (MAP, check required fields)
N         Event ID                Sheet counter ghi 1 lần, bất biến

Validation Status (M) required fields: Date, Item Code, Waste Qty, Unit,
Reason, Staff, Branch. KHÔNG check: Process Stage, Evidence, Investigation
Flag, Loss Type, Event ID.

Reason/Process Stage/Investigation Flag/Loss Type KHÔNG ảnh hưởng routing —
chỉ là field mô tả nghiệp vụ, không phải logic điều khiển compiler.
```

### `WASTE_LOG_ARCHIVE` (pattern giống `PREP_LOG_ARCHIVE`, cột khác)

```
Header thật: A:P (16 cột) — KHÔNG phải A:M như đoán ban đầu (gây 1 sự cố
index sai, đã vá — xem Mục 3).

Cột N (index 13, zero-based)  = Event ID
Cột O (index 14, zero-based)  = "Đã xử lý lúc" (Processed At)
Cột P (index 15, zero-based)  = Snapshot ID

Vùng clear khi archive+clear: A,B,D,E,F,G,H,I,J,K,L,N (12 cột manual)
Vùng giữ nguyên: C, M (2 cột formula hệ thống)
```

## 2. Trình tự Phase đã đóng

```
D.7C-3A     Waste Integration Contract Audit          COMPLETED / BLOCKED
            (tìm ra 2 blocker nền tảng: Event ID không ổn định,
             Compiler dùng explosion riêng không qua Resolver an toàn)

D.7C-3A-1   Waste Identity + Resolver Boundary Audit   COMPLETED
            (3 phương án Event ID, 2 phương án Resolver — chưa build)

D.7C-3A-2   Waste Identity + Domain Router Build       CLOSED / PASS
            - Sheet Counter Event ID
            - resolveWasteConsumption_ (6 domain)
            - Compiler gate theo Validation Status = VALID
            - Core Resolver KHÔNG bị sửa

D.7C-3B     Waste Logic Orchestrator                   CLOSED / PASS
            - scanEligibleWasteLogEvents_, lookupExactWasteLogEvent_,
              processOneWasteLogEvent_, processWasteLogBatch (tái dùng
              pattern D.7C-2B, đổi nguồn dữ liệu)
            - ENGINE_VALID_COMPILER_SOURCES thêm WASTE_COMPILER
            - archiveAndClearWasteLogRow_ (bản Waste riêng, không
              hard-code PREP_LOG)
            - PATCH-5 chunking (5 event/lượt) áp dụng nguyên cho Waste

D.7C-3C     Bind Button + Operator Feedback             PASS (build) /
                                                         IN PROGRESS (data)
            - Menu: "Xử lý Waste Event này" / "Xử lý toàn bộ Waste"
            - Message tiếng Việt riêng cho Waste (không có WAIT_REVIEW)
```

## 3. Sự cố đã gặp và đã vá (D.7C-3C)

### 3.1 Final Finishing Index — Eager Validation (đã vá)

```
Triệu chứng: Event RAW hoàn toàn không liên quan bị chặn bởi lỗi UOM
             trống ở FINAL_FINISHING_DETAIL!F16 (PKG-PAP-BAK-001).
Nguyên nhân: Router validate TOÀN BỘ Final Finishing Index trước khi
             phân luồng, thay vì chỉ validate đúng phần event cần dùng.
Đã vá (PATCH-1): Lazy validation — chỉ validate khi thực sự truy cập
             đúng dòng đó trong quá trình recurse của 1 event cụ thể.
Regression:  Event dùng dữ liệu lỗi → CRITICAL_REJECTED đúng.
             Event không đụng tới dữ liệu lỗi → không bị ảnh hưởng.
Master Data: PKG-PAP-BAK-001 UOM = "pcs" (xác nhận từ Reality Owner).
```

### 3.2 Archive Column Index Sai (đã vá)

```
Triệu chứng: Archive ghi thành công nhưng verify báo
             WASTE_ARCHIVE_VERIFY_FAILED sau khi đã ghi xong.
Nguyên nhân: Code kiểm tra sai index cột (nghĩ Snapshot ID ở cột Q/15,
             "Đã xử lý lúc" ở cột P/12 — thực tế header thật là A:P
             (16 cột), Event ID=N(13), Processed At=O(14),
             Snapshot ID=P(15)).
Đã vá (PATCH-2): Sửa đúng index theo header thật đã đọc lại.
Resume:      recoverFailedSourceFinalization_ tổng quát hóa cho
             WASTE_LOG (không hard-code PREP_LOG), resume đúng session
             kẹt ở SOURCE_FINALIZE_PENDING mà KHÔNG commit lại Ledger.
Kết quả:     WST-DN-260620-0001 phục hồi thành công, không double-write.
```

### 3.3 Unit Conversion — Mixed Code Bug + Missing Master Data (ĐANG XỬ LÝ)

```
3 event bị UNIT_CONVERSION_FAILED khi chạy Batch:

1. WST-DN-260722-0002 — PREP-BAS-OCP-001, "1 Batch" → G
   Nguyên nhân: CODE BUG — canonicalizeUnitToken_ ở Waste chỉ làm
   String(value).trim().toUpperCase(), không dùng UNIT_DICTIONARY
   mapping đã có sẵn ("1 Batch" → "BATCH"). Kết quả: "1 BATCH" thay vì
   "BATCH", không khớp key trong Conversion Facade.
   + Thiếu Conversion Rule: PREP-BAS-OCP-001 | BATCH → G

2. WST-HA-260722-0001 — PREP-BAS-OCP-001, PORTION → G
   Thiếu Conversion Rule thuần túy (không phải bug canonicalization).

3. WST-HA-260722-0002 — RAW-BAK-SOU-001, PCS → SLICE
   Thiếu Conversion Rule + phát hiện mâu thuẫn Master Data:
   LIST_ITEM ghi Purchase Pack Qty = 12 slice/loaf, nhưng Reality Owner
   xác nhận thực tế 1 ổ cắt 16-18 miếng. KHÔNG sửa trong phase này
   (để riêng, không chặn patch hiện tại).

Số liệu đã xác nhận từ Reality Owner (Thanh):
   1 Batch PREP-BAS-OCP-001  = 250 g
   1 Portion PREP-BAS-OCP-001 = 62.5 g (250g ÷ 4 pancake)
   1 PCS Sourdough = 1 SLICE (PCS và SLICE là cùng khái niệm, factor=1,
   KHÔNG phải 1:3 — correction quan trọng, lần tính đầu bị sai)

3 rule đã ghi vào CONVERSION_EXPLICIT_RULE (CER-0004/5/6), physical
readback PASS, nhưng preflightConversionFacadeCompiler trả về
BASELINE_MISMATCH vì có hard-code totalCandidates === 363 — một
magic number cần sửa thành kiểm tra đúng bản chất (readyRows all
READY, không REJECT/REVIEW/duplicate/conflict) thay vì so số cố định.
```

**TRẠNG THÁI HIỆN TẠI — CHƯA ĐÓNG:**

```
D.7C-3C-INCIDENT-PATCH-3 đã AUTHORIZED nhưng CHƯA CÓ KẾT QUẢ:
  Phần A: Sửa preflight baseline (bỏ hard-code 363)
  Phần B: Sửa canonicalization ("1 Batch" → "BATCH" qua UNIT_DICTIONARY)
  Sau đó: build+publish Facade, chạy lại Single cho 3 event, rồi Batch
  cho các event còn lại.
```

⚠️ **Lưu ý continuity:** canonicalization fix đã được authorize 1 lần trước đó nhưng KHÔNG có báo cáo thực thi (bị trôi giữa các lượt trao đổi số liệu vận hành) — đây là bài học: khi có nhiều nhánh việc song song (patch kỹ thuật + chờ số liệu vận hành), cần chủ động hỏi lại trạng thái nhánh còn treo trước khi coi là đã xong.

## 4. Hậu kiểm sạch — trạng thái vật lý (tính đến trước PATCH-3)

```
Event Waste đã hoàn tất trọn vòng đời (archive+clear+finalize):
  WST-DN-260620-0001  (Single, qua sự cố archive index — đã resume)
  WST-DN-260722-0001  (Batch lượt 1)
  WST-HA-260722-0003  (Batch lượt 1)
  = 3/11 event

Event còn eligible, CHƯA thử (giữ nguyên, an toàn):
  = 5 event

Event bị chặn UNIT_CONVERSION_FAILED, CHƯA chạm Staging (an toàn):
  WST-DN-260722-0002
  WST-HA-260722-0001
  WST-HA-260722-0002
  = 3 event

Không có double-write, không có Ledger Qty trống, không có Closure
duplicate trong toàn bộ quá trình — mọi sự cố đều dừng đúng lúc trước
khi ghi dữ liệu sai, đúng nguyên tắc Fail Closed đã giữ suốt track.
```

## 5. Nguyên tắc áp dụng nhất quán từ track PREP sang Waste

```
1. Physical readback bắt buộc trước khi tin bất kỳ completion claim nào
   — không tin lời tường thuật, luôn yêu cầu raw JSON.
2. Fail-closed tuyệt đối — lỗi giữa chừng phải dừng, không cleanup giả
   thành công, không rollback ngầm.
3. Đơn vị atomic là 1 Event — batch chỉ là vòng lặp bên ngoài, không
   phá vỡ tính atomic của từng event riêng lẻ.
4. Idempotent resume — mọi cơ chế phục hồi phải chống double-write khi
   retry sau crash (đã kiểm chứng qua nhiều lượt: PREP crash-after-clear,
   Waste crash-after-archive).
5. Business rejection ≠ orchestration failure — CRITICAL_REJECTED vẫn
   success=true ở tầng orchestrator, chỉ lỗi hạ tầng thật mới false.
6. Lazy validation — không validate toàn bộ Master Data trước khi biết
   event có cần dùng tới phần đó hay không (bài học từ Final Finishing
   Index eager validation).
7. Vá đúng gốc, không patch triệu chứng — ví dụ không đổi return thành
   throw chỉ để "kích hoạt catch", mà xử lý tường minh từng nhánh.
8. Ai quyết = Reality Owner — số liệu quy đổi, ý nghĩa dữ liệu, quyết
   định vận hành luôn cần xác nhận từ Thanh, không đoán.
```

## 6. Bước tiếp theo

```
NEXT ACTION: Chạy D.7C-3C-INCIDENT-PATCH-3 (đã AUTHORIZED)
  → Sửa baseline hard-code 363
  → Sửa canonicalization Waste
  → Build+Publish Conversion Facade (3 rule mới)
  → Chạy lại Single cho 3 event đã fail
  → Nếu PASS, Batch cho các event còn lại

SAU KHI D.7C-3C hoàn tất 11/11 event thật:
  → D.7C-3 (WASTE_LOG) coi như khép kín, tương đương D.7C-2 (PREP_LOG)
  → Quay lại roadmap gốc: WASTE → TRANSFER
  → Mở TRANSFER_LOG theo đúng pattern đã chứng minh 2 lần (PREP, WASTE)
```
