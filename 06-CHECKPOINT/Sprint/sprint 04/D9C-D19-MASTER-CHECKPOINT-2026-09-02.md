# Kurumi V8 — D.9C → D.19 Master Checkpoint

**Ngày checkpoint:** 2026-09-02 (tiếp nối [[D9-D12-MASTER-CHECKPOINT-2026-08-19]] và [[D10D-COST-STRATEGY-CHECKPOINT-2026-08-21]])
**Phạm vi:** Branch Pricing hoàn tất, VAT toàn diện, Revenue Pipeline (Doanh thu thật), Channel/Packaging, dọn hạ tầng, Payment Channel (dở dang).

Checkpoint tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON/live-UI evidence của GPT (Architecture Engine/Audit) và Gemini (Builder) qua các phiên 2026-08-21 → 2026-09-02.

---

## Phần A — D.9B/D.9C: Branch Pricing — hoàn tất với bằng chứng thật

```text
D.9B: Audit giá thật HA vs DN — nguồn 182 giao dịch nhập hàng
thật tại HA (18-24/08/2026), bình quân gia quyền, so với 20 mặt
hàng cùng tên/cùng quy cách tại DN (sau D.14C).
KẾT QUẢ: 75% mặt hàng lệch >10%, 60% lệch >15% — ĐỦ BẰNG CHỨNG
(khác hẳn D.9A cũ EVIDENCE_INSUFFICIENT). Đa số HA rẻ hơn (rau củ
tươi, gần vùng nông sản), vài case đắt hơn (Orange +56%, Dill
+25%) — pattern hợp lý theo địa lý, không phải lỗi dữ liệu.

D.9C: Build BRANCH_PRICE_OVERRIDE (sparse, 15 dòng HA) +
COST_REGISTRY_BY_BRANCH/FINAL_ASSEMBLY_COST_BY_BRANCH/
FINAL_FINISHING_COST_BY_BRANCH/FINAL_COST_BY_BRANCH — song song,
KHÔNG phá FINAL_COST cũ (hash giữ nguyên trước/sau).

D.9C-PATCH: Sửa lỗi mô hình hóa — ban đầu build cả DN/HA/WS
(414 dòng), nhưng WORKSHOP KHÔNG PHẢI chi nhánh bán hàng (là điểm
sản xuất/kho trung tâm) → sửa còn đúng DN/HA (276 dòng = 138×2).
Không đụng PRODUCTION_LOG/TRANSFER_LOG/STOCK_POSITION.

TRẠNG THÁI: CLOSED/PASS. syncCoreToTargets đã mở rộng mapping cho
BRANCH_PRICE_OVERRIDE (D.11 sync).
```

---

## Phần B — D.14: VAT toàn diện — CLOSED

```text
D.14A: Audit hiện trạng — LIST_ITEM/STOCK_INPUT_LOG hoàn toàn
KHÔNG có VAT. POS365 có VAT tính theo TỪNG ĐƠN HÀNG (không phải %
cố định/mặt hàng). Giá bán POS365 ĐÃ GỒM VAT (khách trả đúng số
hiển thị). Nhà hàng ĐĂNG KÝ VAT, được khấu trừ thuế đầu vào. Thuế
suất 8%, khác nhau theo loại hàng.

D.14B: Đối chiếu 163 mặt hàng (bảng báo giá MATERIAL QUOTATION
KURUMI DANANG) với LIST_ITEM — 130 khớp, 25 mới, 35 cảnh báo lệch
giá >10%.

D.14C: Phân loại 35 lệch giá — 9 lỗi đơn vị/đóng gói, 3 giá nguồn
bất thường (nghi lỗi đánh máy thừa/thiếu số 0), 23 khả năng giá
thật đổi.

D.14D: Thêm cột "VAT Category" (VAT_0/VAT_8/NO_INVOICE) vào
LIST_ITEM, backfill 137 mặt hàng, tạo 25 mặt hàng mới (nguyên
liệu nấu + bao bì + vệ sinh + văn phòng — quyết định LIST_ITEM là
"nguồn định nghĩa TẤT CẢ hàng hóa đầu vào", không chỉ nguyên liệu
nấu ăn).

D.14C-PATCH-FINAL(-2/-3): Xử lý dứt điểm 5 case giá bất thường
bằng xác nhận trực tiếp Reality Owner (không suy đoán):
  Pistachio: 760.000→462.000đ/kg (giá thật mới)
  Green Olive: sửa Pack Qty 1000→3000g (lỗi đóng gói, không phải
    giá) + tạo thêm RAW mới cho lon nhỏ 400g
  Balsamic Vinegar: giữ nguyên 499.000đ/5L (đã đúng) + tạo thêm
    RAW mới cho chai 1L/89.000đ
  Biscoff: 8.800→89.000đ (150g) + tạo thêm RAW mới 125g/59.000đ
  Smoked Liquid: giữ nguyên 90.000đ/chai (đã đúng, báo giá cũ ghi
    nhầm giá/thùng thành giá/chai)
  23 mặt hàng còn lại: cập nhật giá thật theo báo giá mới
    (Tomato, Cucumber, Avocado, Cacao Mass, Nutmeg...).

QUYẾT ĐỊNH CHIẾN LƯỢC QUAN TRỌNG: Purchase Price trong LIST_ITEM
LÀ GIÁ NET (trước thuế) — xác nhận trực tiếp Reality Owner. Nghĩa
là FINAL_COST_BY_BRANCH/FINAL_COST hiện tại ĐÃ ĐÚNG SẴN cho mục
đích tính lợi nhuận, KHÔNG cần trừ VAT thêm gì — xóa bỏ 1 hard
blocker tưởng tồn tại ở D.16A.

TRẠNG THÁI: CLOSED/PASS toàn bộ.
```

---

## Phần C — D.15A: Modifier Pattern Audit — CLOSED

```text
Audit tỷ lệ modifier (GF/đổi thành phần/dị ứng) trên dữ liệu thật
7 ngày: 2,06-2,63% tổng giao dịch — DƯỚI ngưỡng 5%.
QUYẾT ĐỊNH: KHÔNG xây Modifier Resolver tự động. Giữ REQUIRES_REVIEW
thủ công là đủ cho quy mô hiện tại.

Case cụ thể đã xử lý: HH-0248 (Cơm Burrito Bowl, "gluten free") —
build công thức GF riêng FIN-BWL-GFB-001 (Tortilla→Rice Cracker),
mapping REALITY_OWNER_GF_OVERRIDE, đã publish thật thành công.

4 SKU có tần suất GF lặp lại cao (HH-0248/0256/0403/0463) — ghi
nhận, chưa cần xây thêm công thức GF riêng ngay.
```

---

## Phần D — D.16: Monthly P&L — Revenue Pipeline — CLOSED (hạ tầng)

### D.1 — D.16A: Audit dữ liệu

```text
Doanh thu: CÓ nguồn POS365 (báo cáo theo tháng/chi nhánh).
SALES_LOG_ARCHIVE KHÔNG lưu giá bán — chỉ dùng để trừ kho.
Giá vốn: JOIN khả thi (Branch+Item Code+Qty × FINAL_COST_BY_BRANCH).
Chi phí vận hành: CÓ trong POS365 Thu&Chi (trừ Lương) — nhưng bị
gộp chung "Trả tiền mua hàng/Trả nợ", cần phân loại tay.
VAT đầu ra: CÓ chính xác trong báo cáo VAT riêng của POS365.
VAT đầu vào: schema có (VAT Category) nhưng archive tháng 7
không đủ dữ liệu thật để kiểm thử.

KHẢ NĂNG LẬP BÁO CÁO LÚC ĐÓ: Gross Profit CHƯA, EBITDA CHƯA, Net
Profit CHƯA.
```

### D.2 — D.16B/D.16C: Xây pipeline Revenue JOIN

```text
Phát hiện quan trọng: POS365 "Chi tiết" và "VAT theo đơn hàng" là
2 báo cáo riêng, JOIN theo Mã chứng từ — 1 VAT/đơn, không tách
theo dòng sản phẩm → cần PHÂN BỔ theo tỷ trọng.

D16C_SalesRevenueJoin.gs (RAM-only trước, sau đó wire vào live):
  - buildSalesRevenueJoinD16C_(): JOIN detail + VAT + service fee
  - Phân bổ VAT theo tỷ trọng giá dòng sau chiết khấu, số dư về
    dòng cuối
  - Service Fee tách RIÊNG (SERVICE_FEE_REVENUE_LOG, append-only,
    KHÔNG qua SALES_LOG/Sell Engine — không tạo movement kho)
  - Xử lý ZERO_TOTAL_NO_VAT (đơn giảm giá 100%/đổi điểm)
  - ALLOCATION_ONLY: dòng sản phẩm CHƯA mapping (chưa có trong
    POS_SKU_MAP) vẫn tính vào mẫu số phân bổ VAT của cả đơn (để
    reconciliation đúng orderGross), nhưng KHÔNG publish kho —
    doanh thu của nó lưu vào UNMAPPED_REVENUE_LOG (giữ lại để
    Monthly P&L không thiếu doanh thu thật)

Kiến trúc: Part D (Revenue Join) TÁCH RIÊNG khỏi Part B (resolve
công thức) — vì SALES_LOG_ARCHIVE append-only, không được archive
trước rồi sửa doanh thu sau. Flow:
  Part A (import) → Part B (resolve) → Part D (Revenue Join, cần
  đủ dữ liệu VAT Report) → Publish Gate (chỉ khi Status=READY VÀ
  Revenue Join Status ∈ {VAT_ALLOCATED, ZERO_TOTAL_NO_VAT}) →
  Part C (publish thật)

SALES_LOG mở rộng 17→22→23 cột qua nhiều đợt (Giá bán/Chiết khấu/
VAT Amount/Net Revenue/Revenue Join Status).
```

### D.3 — D.16D: Batch đầu tiên qua Revenue Pipeline (LIVE)

```text
4 đơn thật đã publish hoàn tất qua pipeline đầy đủ:
  HA270826-0074 (đơn thường)
  HA280826-0094, HA280826-0108 (đơn nhiều món, có SKU chưa mapping)
  HA280826-0103 (phức tạp nhất: 3 Sale Event + 4 Allocation-only
    + 1 Service Fee cùng lúc)
Tổng VAT phân bổ khớp tuyệt đối 0đ chênh lệch cho mọi đơn.

2 SỰ CỐ NGHIÊM TRỌNG PHÁT HIỆN VÀ VÁ TRONG QUÁ TRÌNH:

1. LỖ HỔNG CLOSURE/WRAPPER (ảnh hưởng TOÀN HỆ THỐNG, không chỉ
   Sales) — Closure có thể báo "FINALIZED" dù Archive/Clear thực
   tế THẤT BẠI (do lỗi so sánh kiểu Date trong
   verifySalesArchiveReadback_, wrapper nuốt lỗi báo success:true
   sai). ĐÃ VÁ: Closure chỉ được ghi FINALIZED SAU KHI Archive+
   Clear PASS; wrapper phải propagate lỗi thật, không nuốt. Audit
   ngược 5 sự cố finalize lịch sử (PREP/WASTE/TRANSFER/SALES) —
   xác nhận đã nhất quán sau vá.
   ⚠️ BÀI HỌC QUAN TRỌNG NHẤT: lỗ hổng này tồn tại từ TRƯỚC track
   Sales, ẩn trong state machine dùng chung — chỉ bị phát hiện
   nhờ 1 lỗi nhỏ (so sánh Date sai kiểu) làm lộ ra.

2. LỖI UNIT_CONVERSION_FAILED — 4 công thức Smoothie Bowl
   (Purple Boom, Kurumi, My Favorite, Happy Stomach) ghi nhầm
   "Choco Ball"/"Peanut Ball" đơn vị g thay vì đúng 0,5 pcs. Đã
   sửa 4 ô Unit tại Core, đồng bộ 3 nơi.

Regression 5 Log cũ + Sell + Correction đều PASS sau mỗi lần patch.

TRẠNG THÁI: D.16 CLOSED (hạ tầng). Còn thiếu để hoàn thiện Monthly
P&L thật: Chi phí vận hành (phân loại tay từ POS365 Thu&Chi, trừ
khoản trả NCC nguyên liệu đã có trong COGS) + Lương (nguồn riêng,
chưa quyết định cách nhập) + đủ 1 tháng dữ liệu SALES_LOG_ARCHIVE
tích lũy thật.
```

---

## Phần E — D.17: Channel Detection + Packaging — Phase 1 CLOSED

### E.1 — Quy tắc nhận diện Kênh Bán (chốt, có bằng chứng 562/562 đơn)

```text
GRAB FOOD                              → GRAB (ưu tiên cao nhất)
Card/Bank/Cash + TAKEAWAY/TAKE AWAY      → TAKE_AWAY
Card/Bank/Cash + INSIDE/OUTSIDE            → DINE_IN (OUTSIDE =
                                            bàn ngoài trời, vẫn
                                            ăn tại chỗ)
Trống/nhãn lạ                                → UNKNOWN, cần review

Lưu ý: KHÔNG áp dụng tuyệt đối "DINE_IN = không bao bì" — có
trường hợp món luôn cần bao bì cố định bất kể Channel (ví dụ
Turmeric Shot dùng chai thủy tinh, đã sửa đưa vào công thức thay
vì logic Channel).
```

### E.2 — 2 hệ thống Packaging độc lập, dùng chung pipeline Engine

```text
Món chính: SALES_PACKAGING_DETAIL (Product Code + Channel → Item
  Code bao bì) — Reality Owner tự điền (70% hoàn thành tại thời
  điểm checkpoint).

Extra (topping/add-on): EXTRA_PACKAGING_REVIEW (54 Extra, 10
  cột) — xét đóng chung/đóng riêng theo SỐ PHẦN THỰC TẾ, ĐỘC LẬP
  với Channel (Extra cần đóng riêng thì đóng riêng dù DINE_IN hay
  TAKE_AWAY). Soy Tempeh ≥4 phần: CHỐT dùng Rice Box, không Bowl
  450ml.

Movement nguyên liệu + bao bì GỘP vào CÙNG 1 giao dịch (không
tách đợt ghi kho).
```

### E.3 — D.17D-PHASE-1 (DEPLOYED)

```text
SALES_LOG 22→23 cột (thêm Channel).
Channel detection tại Part A.
Packaging cho MÓN CHÍNH nối vào Part B —
MISSING_PACKAGING_NORM/UNKNOWN_CHANNEL → REQUIRES_REVIEW, KHÔNG
tự publish thiếu bao bì.
Extra PACKAGING CHƯA NỐI (Phase 2).

D.17D-PHASE-2 (Extra automation): BỊ CHẶN — cần cách tự động xác
định số hộp thực tế khi đóng chung/riêng (không muốn bắt nhân
viên nhập tay). Reality Owner đang tự nghiên cứu giải pháp, CHƯA
CÓ HƯỚNG, để dành cho sau.
```

### E.4 — Sửa lỗi phát sinh trong track này

```text
Turmeric Shot: thêm Item Code mới RAW/PKG-BTL-050-001 "Glass
Bottle 50ml" (giá thật 4.956,933đ/chai từ phiếu NH190826-0009),
thêm vào công thức FIN-BEV-TMS-001 (1 pcs).
Cayenne Pepper: cập nhật giá thật 540.000đ/kg từ POS365.
→ Turmeric Shot: MISSING COST → ACTIVE (8.156,17đ/shot).
```

---

## Phần F — D.18: Dọn hạ tầng — CLOSED

### F.1 — D.18A: Retire sheet rác

```text
133 → 128 sheet. Retired (có backup, đã audit tham chiếu,
regression PASS mỗi lần):
  TEMP_COST_COMPILER, EVENT CORRECTION PROTOCOL,
  SYSTEM CALCULATION ZONE, ARCHITECTURE FROZEN (bản trùng Cost),
  TRANSACTION_ENGINE (+ xóa constant code liên quan)

OPENING_CHECK: GIỮ LẠI (không xóa) — Reality Owner xác nhận muốn
hoàn thiện trong tương lai (tính năng đối chiếu kiểm kê PREP
Actual vs Expected Qty, phát hiện thất thoát). Đã ẩn khỏi giao
diện nhân viên, chuyển vào khu tài liệu/backlog, ghi chú rõ còn
thiếu ARCHIVE_PREP_STOCK để hoàn thiện.
```

### F.2 — D.18B: Thu gọn Grid Size

```text
Phát hiện: nguyên nhân "nặng file" ban đầu (lý do tách 3 file từ
đầu track) có thể chủ yếu do GRID OVERSIZED (buffer khổng lồ,
50.000+ dòng cấp phát trong khi dùng thật <1.000), KHÔNG PHẢI số
lượng sheet/công thức — phát hiện có giá trị lớn, giúp giải quyết
vấn đề hiệu năng MÀ KHÔNG CẦN quyết định kiến trúc 2-file/3-file
(D.13-AUDIT chưa từng chạy, vẫn treo).

Resize 11 sheet lớn nhất (LIST_ITEM, UNIVERSAL_RECIPE_DETAIL,
FINAL_FINISHING_DETAIL ở cả 3 file + vài sheet Cost riêng) —
GIẢM 17.032.330 Ô (97,84%). 99/99 regression PASS, 0 lỗi phát sinh,
backup đầy đủ 3 file trước khi resize.
```

### F.3 — D.18B-FOLLOWUP: 56 ô #DIV/0! kế thừa

```text
Nguyên nhân: KHÔNG PHẢI thiếu Standard Yield (giữ 1,00 đúng) —
là 28 mã bao bì (PKG-*) thiếu Purchase Pack Qty + Purchase Price
(chưa từng nhập giá từ lúc tạo).

Đã đóng dứt điểm 7/28 mã (có giá thật từ phiếu nhập POS365):
  Rice Box Set, Paper Cup 350ml, Small Paper Bag, Sauce Cup 80ml
  (=POS "90ml", xác nhận cùng loại), Sandwich Wrapping Paper
  (70đ/tờ×200 tờ, giá trực tiếp Reality Owner, KHÔNG dùng giá
  cling film), Wooden Fork, Wooden Spoon.

Còn treo (chờ hóa đơn đúng quy cách):
  Paper Bowl 450ml (POS chỉ có 350ml, khác loại)
  Small Straw + Large Straw (tìm nhầm "HH-0115 Straw" = ống hút
    KIM LOẠI tái sử dụng tại quán, không phải loại dùng 1 lần cần
    tìm — 2 phiếu Kitchen Stuff nghi vấn (58.000đ/139.000đ)
    KHÔNG đủ rõ để gán, Reality Owner tạm gác, sẽ tự hỏi lại NCC)
  Sauce Cup 30ml ("Cups 70" tên không đủ rõ nghĩa để gán)
  Sandwich Paper Bag (không tìm thấy)

18 mã còn lại (Cake Board/Box, Candle, Knife, Napkin, Sticker,
Cup Tray, Bag Large/Medium) — CHƯA dùng trong công thức/quy tắc
nào, không gấp.
```

---

## Phần G — D.19A: Payment Channel — đang dở dang, bị chặn công cụ

```text
Mục đích: thêm trường "Payment Channel" (Grab/Card/Cash/Bank
Transfer) vào SALES_LOG — CHỈ để báo cáo phân bổ doanh thu theo
hình thức thanh toán, KHÔNG tính toán gì thêm, KHÔNG thay thế
Channel (GRAB/TAKE_AWAY/DINE_IN) đã dùng cho Packaging.

Kế hoạch: SALES_LOG 23→24 cột, sửa đồng bộ 5 file
(SalesImportPartA.gs, SalesResolvePartB.gs, SellEngineFoundation.gs,
SalesIdentityDomainRouter.gs, D16C_SalesRevenueJoin.gs).

TRẠNG THÁI CHẶN: Apps Script web editor liên tục lỗi "chèn code
sai vị trí"/"không lưu được" — GIỐNG các sự cố UI đã gặp trước
đây (Name Box, Page_Down). Chuyển hướng dùng `clasp` (công cụ
CLI chính thức của Google, pull/push có kiểm soát, backup+hash
đối chiếu trước khi ghi) — NHƯNG Windows sandbox chặn lưu
credential (.clasprc.json). Google OAuth ĐÃ xác thực thành công
(account: thienthanh16021990@gmail.com), chỉ vướng lưu phiên.

KẾ HOẠCH TIẾP THEO: Lưu clasp credential trong thư mục workspace
được phép (né C:\Users\HP\.clasprc.json), chạy lại OAuth (Reality
Owner bấm "Cho phép" 1 lần), sau đó tiếp tục thẳng tới bước báo
cáo diff (bước 7 trong quy trình 9 bước đã thống nhất) trước khi
push. KHÔNG có dữ liệu/code nào bị ảnh hưởng trong lúc chờ.

AN TOÀN: Import Part A tạm khóa thủ công (không dùng được cho
tới khi đồng bộ xong 5 file), KHÔNG có trigger tự động, dữ liệu
cũ hoàn toàn nguyên vẹn.
```

---

## Phần H — Nguyên tắc mới đúc kết (nối tiếp 32 nguyên tắc cũ)

```text
33. Closure/trạng thái "hoàn tất" KHÔNG được ghi trước khi MỌI
    bước phụ thuộc (đặc biệt Archive+Clear) đã xác nhận PASS.
    Wrapper/hàm bọc ngoài PHẢI propagate lỗi thật ra ngoài, không
    được nuốt lỗi rồi báo "success:true" — đây là lỗ hổng nguy
    hiểm nhất vì im lặng, tự tin sai. Sau khi phát hiện 1 lần,
    PHẢI audit ngược toàn bộ track khác dùng chung cơ chế.

34. Khi phân bổ 1 giá trị tổng (VAT, chiết khấu...) cho nhiều
    dòng con theo tỷ trọng — số dư làm tròn PHẢI gán về dòng CUỐI
    (không chia đều), và TOÀN BỘ dòng liên quan (kể cả dòng chưa
    mapping/không publish được) phải tham gia mẫu số, nếu không
    tổng sẽ không khớp giá trị gốc.

35. 1 quy trình 2 tầng dữ liệu (ví dụ POS365 "Chi tiết" sản phẩm
    + "VAT theo đơn hàng" cấp đơn) không thể JOIN ngây thơ theo
    Mã chứng từ nếu không xử lý trường hợp: đơn có phí phụ thu
    (Service Fee) tách biệt khỏi dòng sản phẩm, hoặc dòng chưa
    mapping (Allocation-only) không tạo được Sale Event nhưng vẫn
    cần tính vào tổng.

36. Khi tìm giá mua thật qua tra cứu tên hàng trong hệ thống
    khác (POS365...) — PHẢI đối chiếu ĐÚNG QUY CÁCH (dung tích/
    kích thước/chất liệu), không chỉ tên gần giống. Case thật:
    "Straw" tưởng là ống hút giấy dùng 1 lần, hóa ra là ống hút
    kim loại tái sử dụng — nếu dùng nhầm sẽ gán sai giá hoàn toàn
    cho nhu cầu khác.

37. Khi công cụ chính (Apps Script web editor) liên tục không ổn
    định (chèn sai vị trí, không lưu được) — chuyển sang công cụ
    CLI có kiểm soát tốt hơn (clasp) thay vì cố dùng UI web nhiều
    lần. Ưu tiên công cụ cho phép: pull (đọc) → backup+hash →
    diff → push (ghi) → pull lại xác nhận, hơn là sửa trực tiếp
    qua giao diện dễ lỗi.

38. Lý do "hiệu năng chậm" ban đầu dẫn tới quyết định kiến trúc
    lớn (tách 3 file) có thể xuất phát từ nguyên nhân đơn giản
    hơn nhiều (grid oversized, không phải số sheet/công thức) —
    trước khi thực hiện thay đổi kiến trúc lớn, nên audit định
    lượng cụ thể nguyên nhân gốc, tránh giải quyết sai vấn đề.

39. Khi tạo Item Code mới đại diện quy cách đóng gói khác của
    cùng 1 loại sản phẩm (ví dụ Balsamic 5L vs 1L, Green Olive
    3kg vs 400g) — PHẢI tạo Item Code RIÊNG cho từng quy cách,
    không gộp chung 1 mã rồi đổi giá qua lại.
```

---

## Phần I — Trạng thái tổng quan (tóm tắt nhanh)

```text
D.9  Branch Pricing              CLOSED — có bằng chứng thật, sparse override
D.10 Sell Engine                   CLOSED hoàn toàn (kể cả Correction)
D.11 Cross-Spreadsheet Sync          CLOSED
D.12 Açaí Products                     CLOSED
D.14 VAT                                 CLOSED — cột VAT, giá thật cập nhật
D.15 Modifier Audit                        CLOSED — giữ thủ công, không auto
D.16 Monthly P&L Revenue Pipeline            CLOSED (hạ tầng) — 4 đơn thật đã
                                             chạy qua, phát hiện+vá 2 lỗi lớn
D.17 Channel + Packaging                       PHASE 1 CLOSED, PHASE 2 (Extra
                                               auto) CHỜ Ý TƯỞNG Reality Owner
D.18 Dọn hạ tầng                                 CLOSED — 128 sheet, giảm 17M
                                                 ô, 7/28 mã bao bì có giá thật
D.19 Payment Channel                               ĐANG DỞ DANG — chờ clasp
                                                    credential setup xong
```

### Việc còn treo (không gấp, theo thứ tự gợi ý)

```text
1. D.19A — hoàn tất khi clasp credential lưu được (kỹ thuật thuần)
2. 5 mã bao bì còn thiếu giá (Bowl 450ml, Straw×2, Sauce Cup 30ml,
   Sandwich Bag) — chờ Reality Owner tìm hóa đơn đúng quy cách
3. D.17D-Phase 2 (Extra Packaging tự động) — chờ Reality Owner có
   ý tưởng tự động hóa đếm hộp
4. Monthly P&L hoàn thiện — chờ: (a) đủ 1 tháng SALES_LOG_ARCHIVE
   thật, (b) Reality Owner phân loại tay 635→16 dòng OPEX tháng 7
   từ POS365 Thu&Chi, (c) quyết định nguồn nhập Lương
5. Kiến trúc file (2-file vs 3-file) — D.13-AUDIT vẫn chưa chạy,
   nhưng D.18B (grid resize) có thể đã giải quyết phần lớn vấn đề
   hiệu năng gốc, cần đánh giá lại mức độ cấp thiết
6. Web App — tầm nhìn xa, chưa bắt đầu, để sau khi các track vận
   hành ổn định
```

**Thuộc chuyên môn vận hành/bếp của Reality Owner** (theo [[Governance-Protocol]] Mục 5 — Domain Authority): #2 (hóa đơn bao bì đúng quy cách), #3 (ý tưởng tự động hóa đếm hộp Extra), #4b (phân loại OPEX tay), #4c (nguồn nhập Lương).
**Thuần kỹ thuật IT** (AI tự xử lý khi tới lượt): #1 (clasp), #5 (đánh giá lại kiến trúc file sau grid resize), #6 (Web App, còn xa).

---

Liên quan: [[D10D-COST-STRATEGY-CHECKPOINT-2026-08-21]] (track trước, Event Correction Protocol + Cost strategy), [[D9-D12-MASTER-CHECKPOINT-2026-08-19]], [[D8-MASTER-CHECKPOINT-2026-08-14]], [[Governance-Protocol]] (Mục 5).
