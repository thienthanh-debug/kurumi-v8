# Kurumi V8 — Checkpoint D.10D + Cost Strategy

**Ngày:** 2026-08-21 (tiếp nối [[D9-D12-MASTER-CHECKPOINT-2026-08-19]])

Checkpoint bởi Claude (Architect), tổng hợp thảo luận 2026-08-21.

---

## Phần A — D.10D: Event Correction Protocol (contract đã chốt, đang build)

### A.1 — Lý do cần có

```text
Sell Router có bug scale ratio (đã sửa ở D.10C-CRITICAL-PATCH):
DN-0089 (Spirulina Smoothie) đã Finalized nhưng chỉ trừ kho
1/350 lượng thật (do nhầm Qty bán=1 với 1ml thay vì nhân Portion
Size=350ml). Ledger đã ghi 7 dòng nhưng THIẾU tổng cộng -554.91g.

Không được sửa đè lên Ledger cũ (nguyên tắc append-only). Cần cơ
chế Correction Event chính thức, riêng biệt, có audit trail đầy
đủ.
```

### A.2 — Contract gốc (Claude thiết kế)

```text
Nguyên tắc:
1. Ledger append-only tuyệt đối — Correction luôn là dòng MỚI.
2. Correction hoạt động ở tầng Ledger (delta đã tính sẵn), không
   cần Router resolve lại công thức.
3. Bắt buộc con người duyệt (Approved By) trước khi Engine COMMIT.
4. 1 sự kiện gốc chỉ correction ĐÚNG 1 LẦN trong luồng chuẩn.

CORRECTION_LOG (sheet mới, Inventory Engine):
  Correction Event ID | Original Event ID | Original Event Type |
  Line No | Item Code | Delta Qty | Unit | Branch | Reason |
  Calculated By | Requested At | Approved By | Approved At |
  Status | Snapshot ID | Processed At | Archived At

Status lifecycle: DRAFT → PENDING_APPROVAL → APPROVED → RESOLVED
(nhánh lỗi: REJECTED). Engine TUYỆT ĐỐI không tự chuyển
DRAFT/PENDING_APPROVAL → APPROVED.

Tích hợp Engine: thêm CORRECTION_COMPILER vào
ENGINE_VALID_COMPILER_SOURCES, tái sử dụng state machine
(GENERATE→VALIDATE→COMMIT→VERIFY→SOURCE_FINALIZE→CLEANUP),
KHÔNG viết state machine mới.
```

### A.3 — D.10D-PATCH-1: Addendum sau audit độc lập (GPT) — đã xác nhận

```text
Bằng chứng thật phát hiện qua audit (khác giả định ban đầu):
  - INVENTORY_LEDGER thật: A:L = Snapshot ID | Event ID |
    Transaction ID | Movement Type | Date | Item Code | Qty |
    Unit | Location | Staff | Ref ID | Commit Timestamp (L1
    thiếu nhãn, cần sửa).
  - EVENT_REGISTRY thật CHỈ là bảng từ điển (Process Code | Event
    Type | Input Type | Output Type) — KHÔNG có Approved By/At,
    KHÔNG phải Closure Registry vận hành. Registry vận hành thật
    = SOURCE_EVENT_CLOSURE. (Giải quyết dứt điểm mâu thuẫn đã
    treo từ đầu track D.7C về EVENT_REGISTRY).
  - CORRECTION_LOG/ARCHIVE chưa tồn tại — cần tạo mới.
  - DN-0089: 7 Ledger transaction gốc tồn tại đủ (...CON-001 →
    ...CON-007).

4 lỗ hổng đã vá vào contract:
  1. Thêm cột "Corrects Transaction ID" vào CORRECTION_LOG (Item
     Code không đủ để định vị chính xác nếu 1 Item xuất hiện
     nhiều lần trong cùng event).
  2. Source Finalize cần expectedSourceRowCount=7 xuyên suốt
     checkpoint (giống Stock Input) — tránh SOURCE_EVENT_AMBIGUOUS.
  3. archiveAndClearCorrectionLogRows_() — bản MULTI-ROW, không
     phải singular.
  4. Synthetic PHẢI RAM-only hoặc test sheet riêng — KHÔNG được
     append-rồi-xóa Ledger thật (vi phạm chính nguyên tắc
     append-only). DN-0089 sẽ là lần physical end-to-end đầu tiên.

Claude bổ sung thêm 2 điểm khi xác nhận:
  1. Validate "Item Code/Unit/Location khớp transaction gốc" —
     dùng đúng 3 trường để định vị chính xác, tránh 2 dòng
     correction trỏ chéo nhau.
  2. Delta Qty khác 0 + kiểm tra chiều dấu hợp lý: nếu Original
     Movement Type là Consumption (âm), Correction Delta thường
     cũng nên âm trừ khi Reason ghi rõ "hoàn trả/giảm bớt" —
     không REJECTED cứng, chỉ cảnh báo thêm cho người duyệt.

TRẠNG THÁI: Contract đã CHỐT hoàn chỉnh (gốc + PATCH-1 + 2 bổ
sung). GPT đang tiến hành build hạ tầng + synthetic + regression.
DN-0089 correction thật CẦN Reality Owner đích thân điền
"Approved By" — chưa AI nào được tự duyệt thay.
```

### A.4 — Trạng thái Sell Engine hiện tại (liên quan)

```text
D.10C Part C: 3/3 giao dịch thật Finalized (HH-0013, DN-0089,
DN-0141). Router scale-ratio bug đã vá cho giao dịch TƯƠNG LAI.
DN-0089 riêng vẫn đang THIẾU -554.91g trong Ledger, chờ Correction.

LOCKED: không mở thêm 4 dòng Sell READY còn lại + HH-0248
(REQUIRES_REVIEW) cho tới khi DN-0089 correction hoàn tất.
```

---

## Phần B — Quyết định chiến lược Cost (đã chốt)

### B.1 — 2 loại Cost, đã làm rõ ý nghĩa

```text
Cost CHUẨN (Standard) — LIST_ITEM.Purchase Price, cập nhật theo
  quý/6 tháng, dùng làm cơ sở FINAL_COST hiện có (không đổi theo
  ngày).
Cost THEO GIÁ NGÀY (Actual/Market) — STOCK_INPUT_LOG.Actual Cost,
  đã có sẵn từ D.7C-6 (nhập tay mỗi phiếu mua hàng), biến động
  theo giá chợ.
PPV (Purchase Price Variance) = chênh lệch giữa 2 loại trên — cơ
  chế TÍNH ĐÃ CÓ SẴN trong STOCK_INPUT_LOG (ppvRoutingEnabled
  hiện tắt).
```

### B.2 — Quyết định: chỉ dùng PPV, KHÔNG tính FINAL_COST theo giá ngày

```text
Lý do Reality Owner chọn: chỉ cần biết TỔNG THỂ cuối tháng (nhập/
bán/tồn/hao hụt/cost/lợi nhuận/chi phí), KHÔNG cần biết chính xác
giá vốn từng món TỪNG NGÀY.

Lựa chọn 2 (tính FINAL_COST theo giá ngày) bị loại vì độ phức
tạp không tương xứng lợi ích:
  - Cần thêm bài toán kế toán tồn kho (FIFO/bình quân gia quyền)
    — hệ thống hiện KHÔNG theo dõi "lô nào giá bao nhiêu", chỉ
    theo dõi số lượng.
  - Mỗi phiếu nhập mới sẽ lan ra tính lại hàng chục món liên quan
    (mọi món dùng nguyên liệu đó).
  - FINAL_COST sẽ thành 1 dãy số theo thời gian thay vì 1 giá trị
    cố định — cần lưu lịch sử.

QUYẾT ĐỊNH NÀY ĐƠN GIẢN HÓA ĐÁNG KỂ bài toán kiến trúc — không
cần xây thêm 1 chuỗi tính giá song song.
```

### B.3 — Monthly P&L Report (đã xác định phạm vi, CHƯA thiết kế/build)

```text
Dữ liệu đã có sẵn ở đâu (không cần xây mới):
  Nhập hàng    → STOCK_INPUT_LOG_ARCHIVE
  Bán hàng      → SALES_LOG_ARCHIVE (D.10 vừa build)
  Tồn kho        → STOCK_DASHBOARD / STOCK_POSITION
  Hao hụt          → WASTE_LOG_ARCHIVE
  Cost (giá vốn)      → FINAL_COST (dùng giá CHUẨN, theo B.2)

Còn thiếu:
  Lợi nhuận  → CẦN GHÉP: Doanh thu (SALES_LOG × Giá bán POS365) −
              Cost (FINAL_COST × Số lượng bán) — chưa có bảng nào
              làm việc ghép này.
  Chi phí vận hành → CHƯA CÓ NGUỒN DỮ LIỆU (lương, thuê mặt bằng,
                     điện nước...) — hoàn toàn mới, chưa từng
                     nhập vào hệ thống.

TRẠNG THÁI: Chỉ mới xác định PHẠM VI, CHƯA thiết kế contract,
CHƯA build. Không vội — chạy 1 lần/tháng, không bị áp lực tốc độ
như Ledger ghi liên tục hàng ngày. Có thể làm SAU khi D.10D xong.
```

---

## Phần C — Kiến trúc file (thảo luận, chưa quyết định cuối)

### C.1 — Lý do tách 3 file ban đầu (bằng chứng thật từ Reality Owner)

```text
"lên đến 60 sheet, hàng trăm hàm công thức chạy ở mỗi sheet, khá
nặng" — đây là lý do kỹ thuật CÓ THẬT, không phải tùy tiện. Bất
kỳ phương án gộp nào PHẢI tôn trọng giới hạn hiệu năng này, không
lặp lại vấn đề gốc.
```

### C.2 — 2 phương án đã bàn

```text
Phương án 1 file (GPT đề xuất ban đầu): gộp Core+Cost+Inventory
làm 1. Ưu: hết lỗi đồng bộ 3 chiều hoàn toàn. Nhược: blast radius
lớn nhất, file nặng nhất, rủi ro cao nhất khi migration.

Phương án 2 file (Reality Owner đề xuất):
  File 1 "Database" = Core + Cost (Master Data + Standard Cost,
    công thức phạm vi lớn, thay đổi ít)
  File 2 "Engine" = Inventory (Ledger, Actual Cost theo ngày, Sell
    Engine — ghi tần suất cao)
  Ưu: giảm ~50% bề mặt đồng bộ (chỉ còn 2 chiều thay vì 3), khớp
  đúng ranh giới nghiệp vụ thật (Cost chuẩn đi với Core, Cost
  ngày đi với Inventory — đã đúng chỗ từ đầu). Leader được xem
  Cost (đã xác nhận), nên không có blocker bảo mật.

QUYẾT ĐỊNH: CHƯA CHỌN PHƯƠNG ÁN NÀO. Ưu tiên đóng D.10D/DN-0089
trước. Việc audit quy mô thật (D.13-AUDIT, D.13-AUDIT-2 — đếm số
công thức phạm vi lớn ở Cost Engine, ước lượng tải nếu gộp) VẪN
CHƯA CHẠY — cần làm trước khi quyết định cuối, để không lặp lại
vấn đề đã khiến phải tách file lần đầu.
```

---

## Phần D — Việc mới vừa phát sinh, chưa thảo luận (ghi nhận, chưa xử lý)

```text
🆕 VAT / Thuế — Reality Owner vừa nêu, CHƯA thiết kế gì:
  - Giá trước thuế vs sau thuế (không rõ áp dụng cho Giá bán,
    Giá nhập, hay cả 2)
  - Giá nhập có VAT — % bao nhiêu (có thể khác nhau theo nhà cung
    cấp/loại hàng)

ĐÂY LÀ CHỦ ĐỀ RIÊNG, chưa thảo luận chi tiết. Không dồn vào lúc
này — sẽ quay lại sau khi D.10D xong, làm từng bước một. Câu hỏi
cần hỏi khi bắt đầu (không hỏi ngay bây giờ):
  1. VAT áp dụng cho Giá NHẬP (LIST_ITEM/STOCK_INPUT_LOG) hay Giá
     BÁN (POS365) hay cả 2?
  2. % VAT có cố định 1 mức chung, hay khác nhau theo nhà cung
     cấp/loại hàng (cần thêm cột riêng)?
  3. FINAL_COST/Monthly P&L cần tính trước thuế hay sau thuế?
```

---

## Phần E — Việc tiếp theo (thứ tự ưu tiên)

```text
1. GPT hoàn tất D.10D: build CORRECTION_LOG + archive, synthetic
   (RAM-only), regression 5 Log + Sell Engine.
2. Reality Owner đích thân duyệt (Approved By) cho DN-0089
   correction — GPT sẽ dừng lại chờ đúng bước này.
3. Physical readback Ledger/Closure/Archive cho DN-0089 correction.
4. Mở khóa 4 dòng Sell READY còn lại + xử lý HH-0248 (REQUIRES_REVIEW,
   cần Leader quyết định công thức gluten-free).
5. (Không vội) Thiết kế Monthly P&L Report contract.
6. (Không vội) D.13-AUDIT/D.13-AUDIT-2 — đo quy mô thật trước khi
   quyết định kiến trúc file (giữ 3 file / 2 file / khác).
7. (Chưa bắt đầu) VAT/Thuế — thảo luận riêng khi tới lượt.
```

**Việc chờ Reality Owner đích thân làm (không phải AI quyết được, theo [[Governance-Protocol]] Mục 5):**
- Bước 2 — duyệt "Approved By" cho DN-0089 correction. Đây không chỉ là chuyên môn bếp mà là kiểm soát tài chính/audit trail — bắt buộc con người, không AI nào được tự duyệt thay dù có quyền IT.
- Bước 4 — quyết định công thức gluten-free cho HH-0248.
- Bước 6/7 khi tới lượt — quyết định kiến trúc file cuối cùng (dù là bài toán IT, ảnh hưởng cách Leader thao tác hàng ngày) và trả lời 3 câu hỏi VAT.

---

Liên quan: [[D9-D12-MASTER-CHECKPOINT-2026-08-19]] (track trước, Sell Engine Part A/B + Cross-Sync), [[D8-MASTER-CHECKPOINT-2026-08-14]], [[Governance-Protocol]] (Mục 5 — Domain Authority).
