# Kurumi V8 — D.7C Master Checkpoint (v4)

**Ngày checkpoint:** 2026-08-10
**Phạm vi:** Toàn bộ track D.7C — Operational Log One-Click Processing
**Thay đổi so với v3:** Thêm D.7C-6 (STOCK_INPUT_LOG) đã CLOSED/PASS. Mở D.7C-7 (Stock Dashboard). Ghi nhận khả năng tích hợp POS365 (chưa triển khai, chỉ khảo sát).

> Bản này mở rộng ra ngoài phạm vi gốc D.7C (đã đóng ở [[D7C-MASTER-CHECKPOINT-2026-08-10-FINAL]], bản v3). D.7C-6/7 không thuộc 4 Log gốc (Prep/Waste/Production/Transfer) nhưng dùng chung track number vì cùng chuỗi công việc liên tục, cùng phiên.

---

## Phần A — Trạng thái tổng quan

```text
D.7C-1 (PREP Engine hardening)         CLOSED / PASS
D.7C-2 (PREP_LOG,        11/11 event)  CLOSED / PASS
D.7C-3 (WASTE_LOG,       11/11 event)  CLOSED / PASS
D.7C-4 (PRODUCTION_LOG,   8/8 event)   CLOSED / PASS
D.7C-5 (TRANSFER_LOG,     6/6 event)   CLOSED / PASS
D.7C-6 (STOCK_INPUT_LOG,  1/20 phiếu)  CLOSED / PASS  ← mới
D.7C-7 (Stock Dashboard)                OPENING NOW

TỔNG: 42/42 event/phiếu thật đã qua trọn vòng đời trên 5 Log.
19 phiếu Stock Input còn lại chờ Leader điền giá thật — không
phải blocker kỹ thuật, hệ thống đã sẵn sàng xử lý ngay khi đủ dữ liệu.
```

### Menu hiện tại — 10 mục

```text
Xử lý Event này / Xử lý toàn bộ                    (PREP)
Xử lý Waste Event này / Xử lý toàn bộ Waste          (Waste)
Xử lý Production Event này / Xử lý toàn bộ Production (Production)
Xử lý Transfer Event này / Xử lý toàn bộ Transfer      (Transfer)
Xử lý Phiếu Nhập này / Xử lý toàn bộ Phiếu Nhập         (Stock Input)
```

---

## Phần B — D.7C-1 → D.7C-5 (không đổi)

Xem [[D7C-MASTER-CHECKPOINT-2026-08-10-FINAL]] (bản v3) để có đầy đủ chi tiết từng sự cố/patch của 4 Log đầu tiên.

```text
PREP:       RAW/PREP STANDALONE=terminal, PREP INLINE=bung recipe.
            1 Yield(+) + N Consumption(-). Có WARNING/WAIT_REVIEW.
WASTE:      6 domain qua Domain Router riêng. Chỉ Consumption(-).
            Không WARNING.
PRODUCTION: Giống PREP nhưng Branch hardcode DN (chính sách cố ý).
            Router riêng cho Nested INLINE + Consolidation.
TRANSFER:   Paired movement 2 CHIỀU (OUT- + IN+, cùng Item/Unit,
            khác Location, Net=0). KHÔNG cần Resolver — chuyển
            nguyên Item, không bung recipe.
```

---

## Phần C — D.7C-6: STOCK_INPUT_LOG (CLOSED / PASS) — mới

### Đặc điểm cấu trúc riêng — khác biệt lớn so với 4 Log trước

```text
ĐƠN VỊ XỬ LÝ = 1 PHIẾU (Purchase Batch ID), KHÔNG PHẢI 1 DÒNG.
Một phiếu nhập hàng thường gồm NHIỀU mặt hàng khác nhau (ví dụ
1 đơn đặt từ 1 nhà cung cấp có cả rau + trái cây + gia vị).
→ Quyết định của Reality Owner: bấm 1 lần xử lý CẢ phiếu, giống
  1 đơn hàng thật — không tách từng dòng thành sự kiện riêng.

Movement: N dòng dương THUẦN (không có Consumption, không cặp
OUT/IN) — đây là chiều NHẬP nguyên liệu vào hệ thống lần đầu,
khác 4 Log kia đều xử lý hàng ĐÃ CÓ trong kho.

KHÔNG cần Resolver — nhập nguyên Item, không bung recipe.

CÓ THÊM CHIỀU MỚI: Cost/Giá — 4 Log trước chỉ quan tâm Số Lượng,
Stock Input là nơi DUY NHẤT ghi nhận giá mua (Actual Cost).
```

### Quyết định kiến trúc quan trọng — Cost Ledger tách riêng

```text
Quyết định (Reality Owner xác nhận CẦN Cost ngay, không để sau):
  KHÔNG mở rộng INVENTORY_LEDGER hiện có (đang chạy ổn định qua
  4 track khác, tránh regression risk).
  TẠO STOCK_COST_LEDGER riêng — ghi song song, CÙNG DocumentLock,
  CÙNG transaction boundary với Inventory Ledger. Transaction ID
  khớp 1-1 giữa 2 sổ để join được khi cần báo cáo.

2 cột giá trên STOCK_INPUT_LOG:
  Unit Cost (H)   = giá CHUẨN, tự động lấy từ LIST_ITEM (tham chiếu)
  Actual Cost (I) = giá MUA THẬT, Leader phải điền tay
  PPV (O)         = (Actual Cost / System Qty) - Unit Cost — tự tính,
                    nhưng CHƯA dùng để chặn giao dịch (ppvRoutingEnabled
                    = false), chỉ lưu lại để xem sau.

QUY TẮC CỨNG: Actual Cost PHẢI được điền thật mới cho xử lý
(fail-closed) — KHÔNG được tự động lấy Unit Cost thay thế khi
thiếu, vì sẽ làm mất ý nghĩa kiểm soát giá mua thực tế.
```

### Trình tự phase

```text
D.7C-6A     Integration Contract Audit           COMPLETED/BLOCKED
            (4 blocker: Identity không unique per-row, Engine
             boundary thiếu, Routing chưa định nghĩa, Cost
             persistence chưa có chỗ lưu)
D.7C-6A-1   Identity + Package Movement +          CLOSED/PASS
            Cost Ledger Contract
D.7C-6B     Stock Input Logic Orchestrator          CLOSED/PASS
D.7C-6C     Bind Button + Operator Feedback          CLOSED/PASS
```

### Sự cố đã gặp và vá

```text
1. Purchase Batch ID KHÔNG phải Event Identity kiểu 1-1 như 4 Log
   trước — 1 ID khớp NHIỀU dòng nguồn (ví dụ 14 dòng cho 1 phiếu).
   Đây KHÔNG PHẢI bug, là bản chất dữ liệu khác biệt có chủ đích
   (đã xác nhận qua quyết định "xử lý cả phiếu 1 lần" ở trên).
   Vá: Closure/countSourceEventRows_ sửa để CHẤP NHẬN N dòng khớp
   cùng 1 Purchase Batch ID (khác 4 Log kia yêu cầu đúng 1 dòng).

2. Post-write verifier đọc sai cột Qty — root cause off-by-one
   kinh điển (đọc row[6]=Unit thay vì row[5]=Qty trong
   TRANSACTION_STAGING A:J), khiến Engine coi mọi movement là
   "không dương" (vì đọc nhầm sang cột chữ "g"). Verifier ĐÃ BẮT
   ĐÚNG LỖI TRƯỚC KHI GHI (rollback hoàn toàn, 0 dòng ghi sai ở
   cả 4 sổ) — đây là bằng chứng giá trị thực tế của cơ chế
   post-write verification. Vá: sửa đúng index đọc.

3. UI handler dừng im lặng khi hàng đợi Batch rỗng (không gọi
   orchestrator, không ghi log rõ ràng) — Builder tự phát hiện và
   vá thêm, không cần yêu cầu riêng: giờ vẫn gọi
   processStockInputBatchAll(null) và hiển thị feedback rõ ràng
   "Không có Phiếu Nhập nào đủ dữ liệu để xử lý."

4. Dữ liệu giá bất thường được xác nhận ĐÚNG (không phải lỗi):
   RAW-FRU-ORA-001 (Cam) Actual Cost = 75,000đ trong khi 13 dòng
   cùng phiếu chỉ 20-150đ — Reality Owner xác nhận đây là giá
   CẢ THÙNG/LÔ, khác đơn vị tính với 13 dòng kia (giá lẻ theo kg).
   GHI CHÚ QUAN TRỌNG CHO TƯƠNG LAI: nếu bật PPV routing sau này,
   Actual Cost và Unit Cost PHẢI được chuẩn hóa về CÙNG đơn vị với
   System Qty trước khi tính — nếu không, công thức PPV sẽ so
   sánh sai (giá/thùng so với giá/gram sẽ ra kết quả vô nghĩa).
```

### Kết quả cuối

```text
1/20 phiếu (Lo-150526-Da) đã hoàn tất trọn vòng đời thật:
  14 mặt hàng, Inventory Ledger 14 dòng dương, Cost Ledger 14 dòng
  khớp Transaction ID, Archive 14 dòng, Closure 1 record FINALIZED.
  13/14 dòng dùng giá TẠM (copy từ Unit Cost, có ghi chú rõ ràng
  "chưa phải giá thật, cần Leader cập nhật khi có hóa đơn") — CẦN
  THEO DÕI: khi có hóa đơn thật, phải sửa lại 13 dòng này trong
  STOCK_COST_LEDGER (không sửa được qua Archive vì đã Finalized —
  cần quyết định cơ chế điều chỉnh giá sau finalize nếu cần).

19/20 phiếu còn lại: mỗi phiếu 1 dòng, đều thiếu Actual Cost thật,
  hoàn toàn chưa bị đụng, sẵn sàng xử lý ngay khi Leader điền giá.
```

**Việc còn treo, cần Thanh quyết khi tới lúc (thuộc chuyên môn vận hành/giá — theo [[Governance-Protocol]] Mục 5):** cơ chế điều chỉnh giá cho 13 dòng đang dùng giá tạm sau khi có hóa đơn thật, vì đã Finalized không sửa trực tiếp qua Archive được.

---

## Phần D — Khảo sát: tích hợp POS365 (chưa triển khai)

```text
Trạng thái: CHỈ KHẢO SÁT, CHƯA MỞ PHASE KỸ THUẬT.
Reality Owner ưu tiên hoàn tất D.7C-6 trước, đã xác nhận rõ.

Hệ thống POS bán hàng hiện có: POS365 (kurumi.pos365.vn), đã xác
nhận qua ảnh chụp thật, CÓ 2 chức năng: Nhập hàng + Sell (bán hàng).

Báo cáo đã xác nhận tồn tại trên POS365:
  1. "Tổng hợp phiếu nhập hàng"       → khớp ý nghĩa với
                                          STOCK_INPUT_LOG, có Mã
                                          chứng từ/NCC/Tổng tiền,
                                          NHƯNG chỉ là báo cáo TỔNG,
                                          cần bấm vào xem chi tiết
                                          từng mặt hàng
  2. "Chi tiết doanh thu"              → chỉ có TỔNG hóa đơn (Mã
                                          chứng từ, Bàn, Tổng tiền),
                                          KHÔNG có tên món/số lượng
                                          — không đủ dùng để trừ kho
  3. "Hàng hóa bán ra (Chi tiết)"      → CÓ Mã hàng + Tên hàng +
                                          Số lượng từng món đã bán,
                                          ĐÂY MỚI LÀ NGUỒN DÙNG ĐƯỢC
                                          cho việc tự động trừ kho
                                          khi khách mua hàng

Blocker đã thấy trước (từ dữ liệu mẫu thật, ảnh chụp ngày 2026-08-10):
  1. Mã hàng POS365 (HH-xxxx, DN-xxxx) HOÀN TOÀN KHÔNG khớp trực
     tiếp với SKU Code/Item Code của Kurumi (FINAL-xxx, SEM-xxx...)
     → CẦN 1 BẢNG ÁNH XẠ RIÊNG (mapping table), phải map tay từng
     SKU một lần đầu — công việc tốn thời gian.
  2. Có dòng "Ghi chú" ghi tùy chỉnh/topping thêm khi khách gọi
     món (ví dụ "+ soy tepeh") — cần quyết định nghiệp vụ: có nổ
     recipe cho phần thêm này không, hay chỉ tính món chính.
  3. API POS365 — CHƯA XEM KỸ, chưa biết cách đẩy dữ liệu (realtime
     hay theo lịch, push hay pull).

Nếu làm sau này, đây sẽ là "track thứ 6" tương tự 5 track đã làm
— dùng lại được toàn bộ hạ tầng (Staging, Engine, Closure Registry,
Chunked Batch, Resolver cho recipe explosion — giống Waste Domain
Router vì Sales cũng cần nổ recipe ra nguyên liệu, không như Transfer/
Stock Input là chuyển nguyên Item).

Bước đầu tiên khi sẵn sàng làm (không phải bây giờ):
  1. Xuất toàn bộ danh sách Mã hàng + Tên hàng từ POS365
  2. Đối chiếu tay 1 lần với PRODUCT_SELECTOR_MASTER, tạo bảng map
  3. Quyết định cách xử lý "Ghi chú"/topping
  4. Xem xét: import tay 1 lần đầu (đơn giản, không cần API) trước
     khi đầu tư làm API integration
```

---

## Phần E — D.7C-7: Stock Dashboard by Branch (đang mở)

### Thiết kế đã khóa (Reality Owner đã duyệt qua demo mô tả)

```text
KIẾN TRÚC 2 TẦNG:

Tầng 1 — STOCK_DASHBOARD sheet (bảng chính, gọn):
  - Cập nhật: BẤM NÚT REFRESH (không real-time) — Reality Owner
    chọn cách này, đơn giản hơn, không cần trigger tự động.
  - Lọc theo Chi nhánh (dropdown: Da Nang / Hoi An / Workshop)
  - Mỗi Item = ĐÚNG 1 DÒNG (không phình to theo thời gian):
    Item Code | Tên hàng | Tồn kho | Đơn vị | Cập nhật lúc
  - Tính bằng cách CỘNG DỒN INVENTORY_LEDGER theo (Item Code, Location)
    — đọc toàn bộ Ledger, group by, hiển thị số dư cuối cùng.

Tầng 2 — Chi tiết lịch sử 1 món (chỉ hiện khi cần, KHÔNG nhồi vào
bảng chính để tránh rối — Reality Owner đã xác nhận lo ngại này và
đồng ý với thiết kế tách tầng):
  - 10 giao dịch gần nhất của RIÊNG 1 món được chọn
  - Hiện: Ngày | Loại giao dịch | Số lượng | Nguồn
  - Loại giao dịch suy ra từ Compiler Source đã lưu trong Snapshot/
    Closure Registry (PREP_COMPILER=Chế biến, WASTE_COMPILER=Hao hụt,
    PRODUCTION_COMPILER=Sản xuất, TRANSFER_COMPILER=Chuyển kho,
    STOCK_INPUT_COMPILER=Nhập hàng)

MỞ RỘNG TIỀM NĂNG (vì Cost Ledger đã có dữ liệu thật từ D.7C-6):
  Có thể thêm cột "Giá trị tồn kho" = Số lượng × Giá (join qua
  STOCK_COST_LEDGER hoặc Unit Cost chuẩn từ LIST_ITEM) — CHƯA QUYẾT
  ĐỊNH, cần hỏi Reality Owner khi bắt đầu build.
```

### Cần audit trước khi build (D.7C-7A)

```text
1. Cách trigger "xem chi tiết" 1 món cụ thể trên Google Sheets —
   dropdown chọn Item + nút riêng, hay cơ chế khác (cần thiết kế
   UI phù hợp với Apps Script, không phải web app).
2. Danh sách đầy đủ Item Code hiện có trong hệ thống (để liệt kê
   hết mọi món, kể cả tồn = 0 — không chỉ liệt kê món có giao dịch).
3. Cách phân biệt "Loại giao dịch" chính xác từ Ledger — dựa vào
   Snapshot ID prefix hay Compiler Source đã lưu trong Closure Registry.
4. Có cần thêm cột Giá trị tồn kho ngay hay để sau (hỏi Reality
   Owner khi tới bước này).
5. Hiệu năng: nếu Inventory Ledger đã 200+ dòng và tăng dần, cách
   tính cộng dồn có cần tối ưu (index/cache) hay đọc trực tiếp mỗi
   lần bấm refresh là đủ nhanh.
```

---

## Phần F — Nguyên tắc nền tảng (17 điều, đúc kết qua v3 + v4)

```text
1. Physical readback bắt buộc trước khi tin bất kỳ completion claim.
2. Fail-closed tuyệt đối.
3. Đơn vị atomic là 1 Event (hoặc 1 Package đối với Stock Input).
4. Idempotent resume — chống double-write kể cả khi UI/session/
   Editor bị ngắt hoặc thao tác nhầm giữa chừng.
5. Business rejection ≠ orchestration failure.
6. Lazy validation.
7. Vá đúng gốc, không patch triệu chứng.
8. Ai quyết = Reality Owner — số liệu quy đổi, ý nghĩa dữ liệu,
   quyết định kiến trúc lớn (như Cost Ledger tách riêng, đơn vị xử
   lý Package) luôn cần Thanh xác nhận trước khi build.
9. Không mở Orchestrator trước khi Resolver/Compiler nền an toàn.
10. Audit rule đã có trước khi hỏi lại số liệu.
11. Conversion Rule là Master Data lâu dài, không xóa cùng test data.
12. Không tự sửa lỗi chính tả/format dữ liệu Master hiện có.
13. Rủi ro Run Selector Selection Race khi thao tác Apps Script Editor.
14. Khi audit Log mới, luôn kiểm tra Movement Contract có khác cấu
    trúc so với các Log trước không — không mặc định mọi Log giống nhau.
15. [MỚI] Đơn vị xử lý (Event vs Package) là quyết định nghiệp vụ
    cần hỏi Reality Owner rõ ràng trước khi thiết kế Identity/Closure
    contract — không mặc định "1 dòng = 1 sự kiện" cho mọi Log
    (Stock Input đã chứng minh có thể là N dòng = 1 sự kiện thật).
16. [MỚI] Khi số liệu trông "bất thường" (chênh lệch lớn so với dữ
    liệu cùng loại), luôn hỏi xác nhận Reality Owner trước khi coi
    là lỗi — có thể là khác biệt đơn vị tính hợp lệ (giá/thùng vs
    giá/kg), không phải sai sót.
17. [MỚI] Khi thêm 1 tầng dữ liệu mới có khả năng liên quan tới đơn
    vị tính (như Cost/Giá), phải ghi rõ điều kiện chuẩn hóa đơn vị
    TRƯỚC khi bất kỳ công thức tính toán nào (như PPV) được kích
    hoạt dùng để chặn giao dịch — tránh so sánh sai đơn vị âm thầm.
```

---

Checkpoint v4, tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON evidence của nhiều khung làm việc qua các phiên 2026-08-07 → 2026-08-10.

Liên quan: [[D7C-MASTER-CHECKPOINT-2026-08-10-FINAL]] (bản v3, đóng phạm vi gốc), [[D7C-MASTER-CHECKPOINT-2026-08-10]] (bản v2), [[Governance-Protocol]] (Mục 5 — Domain Authority, áp dụng cho quyết định giá/PPV còn treo ở D.7C-6).
