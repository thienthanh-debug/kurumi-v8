# Kurumi V8 — D.9 → D.12 Master Checkpoint

**Ngày checkpoint:** 2026-08-19 (tiếp nối [[D8-MASTER-CHECKPOINT-2026-08-14]])
**Phạm vi:** Branch Pricing Audit, Sell Engine, Automated Cross-Sync, Açaí Products.
**Trạng thái:** D.11 CLOSED hoàn toàn. D.10 gần xong (Part B chưa chạy). D.12 đang dở dang (bị chặn Apps Script input, chuyển sang copy tay).

Checkpoint tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON/live-UI evidence của nhiều khung làm việc (Gemini, Claude Chrome Builder) qua các phiên 2026-08-14 → 2026-08-19.

---

## Phần A — D.9: Branch Pricing (audit xong, chưa build)

```text
Câu hỏi gốc: "Tách tác vụ theo chi nhánh" — sau khi hỏi rõ, xác
định là muốn tách GIÁ NHẬP theo chi nhánh (không phải tách vận
hành/dashboard, vốn đã có sẵn).

D.9A Audit kết quả:
- LIST_ITEM chỉ có 1 cột Purchase Price/Item Code, không phân
  biệt chi nhánh.
- COST_REGISTRY và FINAL_ASSEMBLY_COST đều đọc thẳng
  CORE_LIST_ITEM!I (Unit Cost) — 2 đường đọc riêng, sửa 1 chỗ
  chưa đủ.
- KẾT LUẬN: EVIDENCE_INSUFFICIENT. Không có dữ liệu Actual Cost
  thật nào ở STOCK_INPUT_LOG (0 dòng có giá thật ở cả 3 chi
  nhánh). Archive chỉ có giá TẠM dùng để test D.7C-6, không phải
  hóa đơn thật.

Thiết kế đề xuất (CHƯA BUILD):
  BRANCH_PRICE_OVERRIDE (Item Code, Branch, Override Price) —
  bảng sparse, chỉ điền dòng nào thực sự khác giá.
  Effective Price = Override nếu có, else Purchase Price mặc định.
  Không dùng mô hình "3 cột DN/HA/WS" vì PREP/SEMI lồng nhau cũng
  cần theo Branch, thêm chi nhánh mới phải sửa cả schema.

QUYẾT ĐỊNH: Build Sell Engine TRƯỚC, tách chi nhánh SAU (khi có
bằng chứng giá thật khác nhau). Lý do: giá không ảnh hưởng SỐ
LƯỢNG trừ kho — thiếu tách chi nhánh chỉ làm sai báo cáo lời/lỗ,
không làm sai tồn kho. Sell Engine là mảnh ghép còn thiếu thật sự.
```

---

## Phần B — D.10: Sell Engine (gần xong — Part B chưa chạy)

### B.1 — D.10A: Audit nguồn dữ liệu POS365

```text
Lần 1 (audit sai): dùng nhầm báo cáo "TỔNG HỢP" (aggregate theo
tháng) → kết luận sai "thiếu Mã chứng từ/Ngày/Chi nhánh".

Lần 2 (D.10A-VERIFY, đúng): dùng đúng "BẢNG KÊ CHI TIẾT HÀNG HOÁ
BÁN RA" — CÓ đầy đủ Mã chứng từ (Đơn hàng), Ngày+giờ từng dòng,
Chi nhánh (theo tham số báo cáo + prefix Đơn hàng).

BLOCKER THẬT DUY NHẤT: Hot/Iced không ghi nhất quán trong cột
Ghi chú (chỉ 19/56 dòng mẫu có ghi rõ, phần lớn trống).

RULE ĐÃ KHÓA (Reality Owner xác nhận):
  MẶC ĐỊNH = NÓNG (Hot)
  Ghi chú/Tên hàng CÓ chứa "ice"/"ICE"/"đá" → ICED
  Case "1 ly da 1 ly nong" (1 dòng = 2 ly khác nhiệt độ) → tách
  thành 2 Sale Event riêng, hiếm gặp, không chặn build chính.
  Món chỉ có 1 bản (như Latte Coconut chỉ Hot) → luôn dùng đúng
  công thức duy nhất.

MAPPING COVERAGE (D.8A cũ, đối chiếu lại):
  189 SKU tổng | 47 auto-match cao (24,9%) | 142 review rows |
  102 có candidate, 40 chưa có | 0/142 có quyết định ở cột F
  POS_MENU_REVIEW.
  → Quyết định: TÁCH RIÊNG bảng POS_SKU_MAP (chỉ chứa SKU đã
  duyệt CHÍNH THỨC), KHÔNG để Engine đọc trực tiếp
  POS_MENU_REVIEW (vùng duyệt thô).
```

### B.2 — D.10B: Nền tảng (SALES_LOG + POS_SKU_MAP + Router)

```text
SALES_LOG (17 cột): Sale Event ID | Ngày | Mã chứng từ | Line No |
POS SKU | Tên hàng | Qty | Branch | Modifier Raw | Variant |
Target Item Code | Target Domain | Mapping Source | Status |
Error/Review Reason | Snapshot ID | Processed At

Sale Event ID format: SALE-{Branch}-{DateKey:yyMMdd}-{DocumentId}-
{LineNo} (dùng yyMMdd theo đúng convention nội bộ đã thấy ở Waste,
KHÁC với format ddMMyy bên trong Đơn hàng POS365 — 2 mục đích
khác nhau, không nhầm lẫn).

POS_SKU_MAP (7 cột): POS SKU | Target Item Code | Target Domain |
Variant Policy | Active | Approved By | Approved At
→ Import 47 SKU auto-match độ tin cậy cao (KHÔNG dùng 149
candidate chưa duyệt).

Router: resolveSaleConsumption_() (SellEngineFoundation.gs) —
Router riêng, KHÔNG sửa Core Resolver, tái sử dụng helper/index/
guard như Waste đã làm.

Movement Contract: chỉ Consumption âm, KHÔNG Yield (giống Waste).
Boundary: RAW→terminal, PREP STANDALONE→terminal, PREP INLINE→
resolveConsumptionNode_(), SEMI/FINAL materialized→terminal,
FINAL non-materialized→đọc FINAL_FINISHING_DETAIL, recurse+consolidate.

Regression synthetic PASS: blank→HOT, ice→ICED, mixed→fail-closed
SPLIT_REQUIRED, decaf/modifier→review, duplicate→fail-closed,
movement âm/Yield=0/context sạch.

Gap tìm thấy khi preview dữ liệu thật: PREP-SAU-SSY-001 (Smoke
Soya Sauce) thiếu ML→G.
```

### B.3 — D.10B-PATCH-1: Fix Smoke Soya Sauce

```text
Audit: không suy ra được factor từ Reference Batch/Recipe (chênh
lệch 610g input vs 602g Reference Batch KHÔNG phải bằng chứng
density). Reality Owner xác nhận: giống pattern Syrup/Soy Sauce
cũ — LUÔN CÂN không đong. → factor=1, chỉ sửa nhãn đơn vị
"10ml"→"10g", giữ nguyên số 10. Preview DN-050 sau đó PASS, 11
movement âm.
```

### B.4 — D.10C-PATCH: Archive Mechanism + Status Lifecycle

```text
Thêm "SALES_COMPILER" vào ENGINE_VALID_COMPILER_SOURCES.

archiveAndClearSalesLogRow_() — pattern giống Waste/Production,
NHƯNG SALES_LOG đã có sẵn cột Snapshot ID + Processed At trong
header gốc (khác Waste/Production, nơi 2 cột này chỉ sinh lúc
archive) → archiveHeaders = 17 cột gốc + "Archived At" (KHÔNG
trùng tên "Snapshot ID").

Toàn bộ 17 cột SALES_LOG = manual input (systemFormulaColumnIndexes
= []) — chưa có dữ liệu thật để kiểm chứng cột nào có formula,
chọn an toàn (cơ chế bảo vệ tự dừng nếu phát hiện formula).

PHÁT HIỆN QUAN TRỌNG (D.10C-PATCH-2):
1. Cột Status có Data Validation dropdown CỐ ĐỊNH: IMPORTED,
   READY, REQUIRES_REVIEW, RESOLVED, REJECTED, PROCESSED.
2. setValues() KHÔNG all-or-nothing khi vi phạm validation giữa
   mảng — ghi PARTIAL trước khi throw exception. BÀI HỌC: LUÔN
   validate giá trị hợp lệ ở code TRƯỚC setValues(), không dựa
   Data Validation Sheet tự chặn.
3. resolveSaleConsumption_() là hàm tính toán THUẦN — chưa có lớp
   nào gọi nó rồi ghi kết quả vào Status. PROCESSED không nên là
   giá trị Status thật (dòng bị clearContent() xóa trắng, không
   chuyển trạng thái).

VÒNG ĐỜI STATUS ĐÃ KHÓA (5 trạng thái, rút gọn từ 6):
  IMPORTED → READY / REQUIRES_REVIEW / REJECTED → RESOLVED →
  (biến mất khỏi Log sau archive, KHÔNG có bước "PROCESSED")

PHÂN CHIA PHẠM VI:
  Part A (Import) — CHỈ ghi Status="IMPORTED" + 9 trường gốc, để
    TRỐNG Variant/Target Item Code/Target Domain/Mapping Source/
    Error-Review-Reason/Snapshot ID/Processed At.
  Part B (Resolve) — gọi Router, ghi READY/REQUIRES_REVIEW/
    REJECTED + các trường liên quan.
  Part C (Publish) — Staging→Engine→RESOLVED→Archive+Clear.
```

### B.5 — D.10C Part A: CLOSED — Import 8 dòng thật

```text
Phát hiện quan trọng: DN/HA/WS là mã chi nhánh THẬT (từ
STOCK_DASHBOARD_CONFIG.branches), KHÔNG PHẢI suy từ prefix SKU
(DN-/HH- chỉ là tiền tố Item Code, không liên quan Branch). Toàn
bộ dữ liệu thật quan sát được đều có Đơn hàng bắt đầu "DN" (chi
nhánh Đà Nẵng) — chưa gặp case "HH" nào trong Đơn hàng thật.

Đã import 8 dòng đa dạng (khớp 47 SKU ACTIVE, từ 17/08/2026,
DA NANG) — TẤT CẢ verify khớp POS365 gốc, Status="IMPORTED", 7
cột còn lại đúng để trống:
  HH-0013 Bánh đậu gà (PREP) | DN-0089 Spirulina Smoothie (FINAL)
  | DN-0141 Dĩa Dips plate (FINAL) | HH-0403 Cơm Yellow Thai curry
  (FINAL, không note) | HH-0256 Cơm Poke Bowl (FINAL, không note)
  | DN-2016 Local Buddha bowl (FINAL, qty=2) | HH-0248 Cơm Burrito
  Bowl (FINAL, note="gluten free" — QUAN TRỌNG, cần REQUIRES_REVIEW
  ở Part B, không tự resolve theo công thức thường) | DN-0073
  Kind Bowl (FINAL, không note)

2 lỗi gán nhầm Ghi chú (note attribution) đã tự phát hiện và sửa
trong quá trình đọc dữ liệu thô POS365 (note nằm ở dòng NGAY SAU
Đơn hàng ID, TRƯỚC dòng Mã hàng tiếp theo trong bản text phẳng —
dễ gán nhầm nếu đọc ẩu).

2 SỰ CỐ UI TRONG PHIÊN NÀY (đã xử lý đúng, không mất dữ liệu):
1. Name Box gõ nhầm "POS_SKU_MAP!A1" vào ô A26 (đè "HH-0033") —
   phát hiện ngay, Ctrl+Z 2 lần, verify qua formula bar → sạch.
2. "Page_Down" (định cuộn trang) gõ literal vào dòng 1
   SalesIdentityDomainRouter.gs — phát hiện ngay, Ctrl+Z, verify
   qua screenshot → sạch, file "Đã lưu vào Drive".
BÀI HỌC ĐÚC KẾT: Name Box không đáng tin trong context tự động —
ưu tiên cuộn tab bar trực tiếp hoặc dùng find tool lấy element
ref rồi click qua ref (đáng tin hơn tọa độ thô). Trong Monaco
editor (Apps Script), tránh phím tắt kiểu "Page_Down" — dùng
Ctrl+F tìm chuỗi + Enter + Escape để điều hướng an toàn.
```

### B.6 — D.10C Part B: AUTHORIZED, code đã viết — CHƯA CHẠY

```text
File: SalesResolvePartB.gs — đã viết, đã lưu, CHƯA RUN.

Việc cần làm khi chạy: đọc từng dòng IMPORTED → gọi
resolveSaleConsumption_() → ghi READY/REQUIRES_REVIEW/REJECTED
+ Target Item Code/Domain/Mapping Source/Variant/Error Reason.

LƯU Ý QUAN TRỌNG: HH-0248 (Cơm Burrito Bowl, note="gluten free")
PHẢI vào REQUIRES_REVIEW — đây là modifier đổi công thức thật
(giống 6 SKU GF đã xử lý ở D.8), KHÔNG được tự động resolve theo
công thức Burrito Bowl thường.

ĐÂY LÀ VIỆC TIẾP THEO CẦN LÀM khi quay lại track D.10.
```

---

## Phần C — D.11: Automated Cross-Spreadsheet Sync (CLOSED)

### C.1 — Mục tiêu & thiết kế

```text
Thay thế copy-paste thủ công giữa Core/Cost/Inventory bằng hàm
Apps Script gọi THỦ CÔNG (KHÔNG trigger tự động — giữ nguyên
quyết định tránh đồng bộ dữ liệu dở dang).

syncCoreToTargets(sheetName, rangeA1) — trong CrossSpreadsheetSync.gs:
  - Mở 3 file bằng SpreadsheetApp.openById() với 3 ID cố định.
  - Đọc getValues() (KHÔNG getFormulas() — chỉ copy giá trị đã
    tính, tránh lỗi tham chiếu sai khi dán sang file khác).
  - Tìm dòng đích bằng Item/Final Code (không dựa số dòng vật lý).
  - Ghi setValues() sang Cost + Inventory.
  - Readback CELL-BY-CELL cả 3 nơi (không chỉ đếm số dòng — bài
    học từ D.8N).
  - Range hữu hạn bắt buộc, KHÔNG nhận "A2:A" (full-column).

Smoke test 10 Coffee + GFA: mismatchedCells=[], garbageTextFound=[].
D.8N dry-run (test lại đúng vùng từng bị lỗi): khớp hoàn toàn,
sạch.
```

### C.2 — Sự cố phát hiện và giải quyết trong quá trình build

```text
1. "5 bảng bị BLOCKED" (ALL_ITEM, PREP_MASTER, UNIVERSAL_RECIPE_
   DETAIL, FINAL_ASSEMBLY_DETAIL, FINAL_FINISHING_DETAIL) vì audit
   ban đầu kết luận "Core thiếu GFA/Coffee" → ĐIỀU TRA (D.11-VERIFY)
   → SAI, false negative do ALL_ITEM!A506 bị dữ liệu rác chặn
   spill array, khiến XLOOKUP trả NOT_FOUND. Không mất dữ liệu
   thật. Reality Owner tự sửa A506 trực tiếp.

2. "KURUMI_RECIPE_CORE" — nhắc tới trong lý do chặn nhưng KHÔNG
   PHẢI file đang dùng. Điều tra (D.11-VERIFY-2) xác nhận: đây
   là FILE THỨ 4 hoàn toàn riêng biệt, tạo từ 01/07/2026 (trước
   cả track này), KHÔNG được bất kỳ code Apps Script live nào
   tham chiếu. Kết luận: nhiễu, không liên quan hệ thống thật,
   đã loại khỏi mọi logic D.11.

3. Sau khi sửa A506: phát hiện Earl Grey (RAW-TEA-EGT-001) và
   Cayenne Pepper (RAW-SPI-CAY-001) BỊ MẤT khỏi Core LIST_ITEM
   (còn ở Cost/Inventory) — khả năng đã bị ghi nhầm vào ALL_ITEM
   thay vì LIST_ITEM lúc build D.8Q, rồi bị dọn sạch cùng lúc
   xử lý A506. → D.11-PATCH-2: tạo lại đúng tại LIST_ITEM, không
   ghi ALL_ITEM tay. Cũng tạo FINAL_ASSEMBLY_DETAIL tại Core
   (thiếu từ trước). Mở đủ 12/12 mapping.

4. Trong lúc PATCH-2 chạy, 4 giá trị cũ ở Inventory
   PREP_MASTER!K2:L3 (1710/2090/873/1067) bị xóa theo rule
   "Core thắng" (Core trống → Inventory cũng trống theo).

5. D.11-VERIFY-4: điều tra việc xóa 4 giá trị trên có đúng không
   → PHÁT HIỆN ĐÂY LÀ LỖ HỔNG THẬT: Core thiếu K/L (Min/Best
   Yield) ở NHIỀU dòng từ trước (không chỉ 2 dòng), Inventory giữ
   dữ liệu thật duy nhất còn sót — không nên áp dụng máy móc "Core
   thắng" khi Core có thể đang thiếu, không phải đang đúng.

6. D.11-PATCH-3 (audit độc lập, phiên MỚI, KHÔNG tin claim phiên
   trước):
   - Con số THẬT: chỉ 7/173 dòng thật thiếu K/L (KHÔNG PHẢI
     77/175 như phiên trước tuyên bố — SAI LỆCH 11 LẦN, một bài
     học cực lớn về việc không tin claim dù có vẻ thuyết phục).
   - Công thức Min=Standard×0.9/Best=Standard×1.1 khớp CHÍNH XÁC
     6/7 dòng khi tự tính lại (không suy đoán).
   - Phát hiện thêm: Cost Engine KHÔNG PHẢI bản sao byte-by-byte
     của Core như claim cũ nói — dòng Nut Mezan có giá trị ĐÚNG
     độc lập tại Cost Engine trong khi Core trống. "2/3 nơi khớp
     = đúng" là tiêu chí SAI khi 1 trong 2 "phiếu" chỉ là bản sao
     của phiếu kia.
   - Dòng thứ 7 (PREP-COC-RFB-001) là bất thường thật: thiếu ở
     CẢ 3 nơi, không suy được — để riêng, không cố khôi phục.

7. D.11-PATCH-3B: khôi phục đúng 6/7 dòng từ Inventory (dữ liệu
   thật) NGƯỢC VỀ Core, verify qua UI trực tiếp (không gviz),
   khớp cả 3 nơi.

8. D.11-PATCH-4: điều tra hiện tượng "Cost Engine tự động có giá
   trị đúng ngay sau khi ghi Core" (nghi ngờ có trigger/IMPORTRANGE
   ẩn, vi phạm quyết định "không trigger tự động") → ĐIỀU TRA KỸ
   (kiểm tra Triggers, kiểm tra formula bar từng ô, execution log)
   → KẾT LUẬN: BÁO ĐỘNG GIẢ. Không có trigger, không có IMPORTRANGE.
   Nguyên nhân thật: ĐỘ TRỄ CACHE CỦA GVIZ khiến lần đọc đầu báo
   sai "trống" trong khi dữ liệu đã có sẵn từ trước.
   ⚠️ BÀI HỌC QUAN TRỌNG NHẤT CỦA TOÀN BỘ TRACK D.11: KHÔNG dùng
   gviz để xác nhận trạng thái NGAY SAU một lần ghi — độ trễ cache
   có thể gây kết luận sai theo cả 2 chiều (tưởng trống khi đã có,
   hoặc tưởng có khi chưa ghi). LUÔN xác nhận qua UI trực tiếp
   (Name Box + formula bar) khi cần độ chính xác thời gian thực.

9. Dòng thứ 7 (PREP-COC-RFB-001) cuối cùng: Min=990 xác nhận ĐÚNG
   bởi Reality Owner (không cần khớp công thức ×0.9 tuyệt đối,
   chấp nhận sai số thực tế biến thiên theo thời gian — bài học:
   công thức chuẩn không phải luật bất biến, số liệu Reality Owner
   xác nhận trực tiếp luôn thắng). Best Skill Yield ban đầu có
   "0,9" — nghi là lỗi gõ hệ số thay vì kết quả — Reality Owner
   tự sửa trực tiếp trên Sheet thành 990 (khớp Min, không theo
   công thức ×1.1 chuẩn — quyết định thực tế riêng cho món này),
   đồng bộ tay sang Cost/Inventory, verify khớp 100% qua UI.

D.11 VÀ TOÀN BỘ PATCH (1 → 3-FINAL-3): CLOSED/PASS. PREP_MASTER
giờ sạch hoàn toàn ở cả 3 file, không còn ô K/L nào trống/lệch.
```

---

## Phần D — D.12: Açaí Products (đang dở dang)

### D.1 — Nguồn dữ liệu

```text
3 món mới từ Açaí, có hóa đơn thật: 860.000đ/3,3kg → 260,6đ/g =
260.600đ/1000g (áp dụng cho CẢ Pure Açaí lẫn Guarana Açaí, cùng
1 hóa đơn, Reality Owner xác nhận).

Công thức đã chốt (sau nhiều vòng làm rõ số liệu qua tin nhắn —
1 dòng bị Zalo/Messenger thu hồi, Reality Owner gửi lại):

Smoothie Bowl Açaí:
  Frozen Banana 200g | Pure Açaí 100g | Water 50ml |
  Blueberry Frozen 15g (6 pieces) | Pistachio 3g (1tsp=3g) |
  Coconut Flakes 6g (số thật, KHÔNG theo quy đổi chung 1tb.s=9g) |
  Mix Nut 15g (số thật, KHÔNG theo quy đổi chung) | Choco Sauce 10g

Pure Açaí Squish: Pure Açaí 100g | Chocolate Sauce 5g |
  Pistachio 3g | Coconut 3g

Guarana Açaí Squish: Guarana Açaí 100g | Chocolate Sauce 5g |
  Pistachio 3g | Coconut 3g

LƯU Ý QUAN TRỌNG: "1 tsp=3g" và "1 tb.s=9g" là quy đổi CHUNG được
xác nhận ban đầu, NHƯNG sau đó Reality Owner cho số liệu THẬT
riêng cho Mix Nut (15g) và Coconut Flake (6g) trong công thức
Smoothie Bowl — số thật LUÔN ưu tiên hơn quy đổi chung khi có sẵn
(vì khối lượng riêng khác nhau giữa các loại hạt/dừa bào).
```

### D.2 — D.12A Audit (Item Code có sẵn)

```text
ĐÃ CÓ, dùng lại (không tạo mới):
  Pistachio = RAW-NUT-PIS-001
  Choco Sauce/Chocolate Sauce = PREP-SAU-CHO-001
  Mix Nut = PREP-MIX-NTM-001 (tên thật "Nut Mix")
  Blueberry Frozen = RAW-FRO-FBL-001 (tên thật "Frozen blueberries")

Coconut (topping) — 3 lựa chọn, ĐÃ CHỐT dùng PREP-COC-RFB-001
(Roasted Coconut Flake Big, tự rang trong bếp) — vì đây đúng item
đang dùng làm topping dừa trong "Choco Sense" (FIN-BWL-CHO-001),
món Smoothie Bowl gần giống nhất đã có sẵn — đồng bộ pattern.

CHƯA CÓ, cần tạo mới tại LIST_ITEM (Core):
  Pure Açaí          — RAW-FRO-ACA-001 (đề xuất) | Frozen | g
  Guarana Açaí         — RAW-FRO-GUA-001 (đề xuất) | Frozen | g
  Roasted Coconut Flake Big (Purchased) — RAW-DRY-RFB-001 (đề
    xuất) | Dry Goods | g | 269.000đ/1000g
    ⚠️ ĐÂY LÀ ITEM RIÊNG, KHÁC PREP-COC-RFB-001 (tự rang trong
    bếp) — mua sẵn đã rang từ nhà cung cấp. Đặt hậu tố
    "(Purchased)" để phân biệt, tránh nhầm lẫn tra cứu. KHÔNG
    dùng trong 3 công thức Açaí này (chỉ có sẵn cho mục đích
    khác/tương lai) — 3 công thức vẫn dùng PREP-COC-RFB-001.

Quyết định kinh doanh (Reality Owner):
  Sell Price 3 món mới: ĐỂ TRỐNG TẠM (build công thức trước, tính
  giá sau).
  Định dạng "Squish" (chưa có tiền lệ trong hệ thống): Portion
  theo gram (~106-111g), Storage=CHILLER, Shelf Life=Serve Fresh
  (giống Smoothie thường, KHÔNG giống khuôn "SMOOTHIE BOWL").
  Smoothie Bowl Açaí: dùng khuôn "Choco Sense" (Category
  "SMOOTHIE BOWL", Portion 1 bowl, Storage CHILLER).
```

### D.3 — Sự cố đã điều tra và giải quyết trong D.12

```text
🚩 Flag đã raise và giải quyết: Builder claim "phải ghi tay vào
ALL_ITEM trước khi FINAL_FINISHING_DETAIL resolve đúng" — MÂU
THUẪN với kiến trúc đã xác nhận (ALL_ITEM là QUERY tự động, viết
tay sẽ lặp lại sự cố A506).

D.12B-VERIFY-3 (test trực tiếp: thêm 1 dòng test vào LIST_ITEM,
xem ALL_ITEM có tự phản ánh không) — ĐANG CHỜ KẾT QUẢ khi bị
chuyển hướng bởi sự cố Apps Script bên dưới. CẦN LÀM RÕ LẠI khi
quay lại D.12, KHÔNG được bỏ qua bước này.

D.12B-VERIFY-2 (giải đáp riêng, không phải sự cố): ALL_ITEM có
công thức QUERY CHỈ tồn tại ở Core (KURUMI_MASTER_CORE). Cost/
Inventory Engine's ALL_ITEM là SNAPSHOT TĨNH (giá trị, không công
thức) — PHẢI đồng bộ qua syncCoreToTargets() sau mỗi lần Core
thay đổi, đây LÀ đúng thiết kế, không phải lỗi.
```

### D.4 — Trạng thái hiện tại — dang dở, cần tiếp tục

```text
SỰ CỐ ĐANG CHẶN: Apps Script Editor bị chặn input (nghi do
extension trình duyệt khác — từng thấy "AI model-picker dropdown"
gây nhiễu trước đây trong track D.10C). Gõ ký tự không ghi nhận
được, kể cả 1 chữ "X" đơn giản.

HƯỚNG XỬ LÝ ĐÃ CHỌN: chuyển từ "viết code Apps Script" sang "copy-
paste trực tiếp qua UI Sheets" — dán khối dữ liệu 1 lần thay vì
gõ từng ô, đọc lại 1 lần qua formula bar để xác nhận, KHÔNG kiểm
từng ô lẻ (tiết kiệm thao tác theo yêu cầu Reality Owner).

Đã xác nhận: CORE_LIST_ITEM tại Cost Engine là snapshot tĩnh
(không formula link tới Core) — khớp đúng kiến trúc Source+Snapshot
đã biết, KHÔNG phải phát hiện mới cần lo lắng.

Quyết định: chọn "Copy tay 3 dòng mới sang Cost/Inventory" (Option
2) thay vì xây syncCoreToTargets() mới — vì hàm này ĐÃ TỒN TẠI
sẵn từ D.11 (CrossSpreadsheetSync.gs), chỉ là Apps Script đang
không gõ được nên không gọi được, KHÔNG PHẢI thật sự chưa có hàm.

VIỆC ĐANG CHỜ KẾT QUẢ khi checkpoint này được tạo: Builder đang
copy tay 3 dòng RAW (Pure Açaí, Guarana Açaí, Roasted Coconut
Flake Big Purchased) sang Cost Engine + Inventory Engine, sau khi
đã ghi xong tại Core. CHƯA báo cáo kết quả cuối.

VIỆC CÒN LẠI SAU KHI 3 RAW XONG:
  1. Tạo 3 Final Code (Smoothie Bowl Açaí, Pure/Guarana Açaí
     Squish) tại FINAL_PRODUCT_MASTER.
  2. Ghi FINAL_FINISHING_DETAIL cho cả 3 (dùng đúng Item Code đã
     audit + 3 RAW mới).
  3. Đồng bộ Core → Cost → Inventory cho 2 bảng trên (cùng cách
     copy tay, hoặc thử lại Apps Script nếu input hết bị chặn).
  4. Verify cell-by-cell qua UI trực tiếp cả 3 nơi.
  5. D.12B-VERIFY-3 vẫn cần hoàn tất/xác nhận (xem Phần D.3) —
     đừng quên bước này dù đã chuyển sang copy tay.
```

---

## Phần E — Nguyên tắc mới đúc kết (nối tiếp 23 nguyên tắc cũ từ [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]]/[[D8-MASTER-CHECKPOINT-2026-08-14]])

```text
24. KHÔNG dùng gviz để xác nhận trạng thái NGAY SAU một lần ghi —
    độ trễ cache gây kết luận sai cả 2 chiều (tưởng trống khi đã
    có, hoặc tưởng có khi chưa ghi). LUÔN xác nhận qua UI trực
    tiếp (Name Box + formula bar, hoặc find tool + element ref).

25. KHÔNG tin số liệu/kết luận từ 1 phiên AI khác chỉ vì "nghe
    thuyết phục, có ví dụ khớp công thức" — luôn tự audit độc
    lập trước khi hành động. Case thật: claim "77/175 dòng thiếu"
    hóa ra chỉ là 7/175 — sai lệch 11 lần dù có vẻ có bằng chứng
    (4 ví dụ khớp công thức) đi kèm.

26. "2/3 nguồn khớp nhau = đúng" KHÔNG PHẢI tiêu chí an toàn nếu
    1 trong các nguồn chỉ là bản sao của nguồn kia (không độc lập
    thật). Phải xác minh tính độc lập của từng nguồn trước khi
    dùng biểu quyết đa số.

27. Rule "Nguồn chuẩn luôn thắng" (ví dụ "Core thắng khi lệch với
    Inventory") CHỈ đúng khi Nguồn chuẩn thực sự đã hoàn chỉnh —
    không được áp dụng máy móc, vì Nguồn chuẩn có thể đang THIẾU
    (không phải đang ĐÚNG). Luôn kiểm tra "trống vì thiếu" hay
    "trống vì đúng là không có" trước khi đồng bộ ép buộc.

28. Công thức chuẩn (như Min=Standard×0.9) không phải luật bất
    biến — khi Reality Owner xác nhận trực tiếp 1 số liệu khác
    công thức, ưu tiên Reality Owner, không ép công thức phải khớp.

29. UI navigation (Name Box, keyboard shortcuts trong Monaco
    editor) không đáng tin trong môi trường tự động — Name Box có
    thể gõ nhầm text vào ô hiện tại thay vì điều hướng; phím tắt
    như "Page_Down" có thể bị gõ literal vào document. Ưu tiên:
    cuộn tab bar trực tiếp / find tool lấy element ref / Ctrl+F
    tìm chuỗi + Enter + Escape.

30. Khi phát hiện thao tác UI lỡ tay (gõ nhầm vào ô/file): PHẢI
    bắt ngay → undo ngay (Ctrl+Z) → xác nhận lại qua formula bar/
    screenshot TRƯỚC KHI báo cáo → báo cáo minh bạch dù không ai
    hỏi. Đây là kỷ luật bắt buộc, không phải tùy chọn.

31. 1 Item Code cùng tên gọi (như "Roasted Coconut Flake Big") có
    thể cần tách thành 2 Item Code riêng nếu có 2 nguồn gốc khác
    nhau thật (tự làm trong bếp vs mua sẵn từ nhà cung cấp) —
    không gộp chung dù tên giống nhau, đặt hậu tố phân biệt rõ
    ràng (Purchased/House-made...).

32. Khi công cụ chính (Apps Script/code) bị chặn kỹ thuật (input
    bị extension lạ can thiệp), chuyển hướng linh hoạt sang thao
    tác UI trực tiếp (copy-paste khối) thay vì cố debug nguyên
    nhân — đặc biệt với khối lượng nhỏ, làm tay nhanh hơn tìm
    lỗi. Nhưng vẫn giữ nguyên kỷ luật verify (đọc lại xác nhận
    khớp) dù đổi phương thức thao tác.
```

---

## Phần F — Trạng thái tổng quan (tóm tắt nhanh)

```text
D.9  Branch Pricing          AUDIT XONG, CHƯA BUILD (chờ bằng chứng)
D.10 Sell Engine              GẦN XONG — Part A CLOSED, Part B đã
                              viết code CHƯA CHẠY, Part C chưa bắt đầu
D.11 Cross-Spreadsheet Sync    CLOSED HOÀN TOÀN — mọi patch đã đóng
D.12 Açaí Products               ĐANG DỞ DANG — 3 RAW đang copy tay
                                  sang Cost/Inventory, 3 Final Code
                                  + Finishing Detail CHƯA làm

VIỆC TIẾP THEO ƯU TIÊN (theo thứ tự hợp lý, không bắt buộc thứ tự):
1. Hoàn tất D.12 (Açaí) — xong 3 RAW, làm tiếp 3 Final Code +
   Finishing Detail + đồng bộ + verify. Nhớ hoàn tất
   D.12B-VERIFY-3 (test ALL_ITEM tự động) trước khi ghi bất kỳ
   Final Code nào.
2. Chạy D.10C Part B (resolve 8 dòng SALES_LOG đã import — chú ý
   HH-0248 gluten free phải vào REQUIRES_REVIEW).
3. D.10C Part C (publish 1-3 dòng PASS sạch nhất, chạy Engine
   thật lần đầu cho Sell Engine).
4. Sau khi Sell Engine ổn định — quay lại D.9 (Branch Pricing)
   khi có bằng chứng giá thật khác nhau giữa chi nhánh.
```

**Mục thuộc chuyên môn vận hành/bếp của Reality Owner** (theo [[Governance-Protocol]] Mục 5 — Domain Authority): bằng chứng giá thật khác chi nhánh (D.9), xác nhận HH-0248 gluten free review (D.10), số liệu Açaí còn thiếu nếu phát sinh thêm trong D.12.
**Mục thuần kỹ thuật IT** (chạy Part B/C, đồng bộ Cross-Spreadsheet, xử lý Apps Script bị chặn input) — AI tự xử lý.

---

Liên quan: [[D8-MASTER-CHECKPOINT-2026-08-14]] (track trước), [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]], [[Governance-Protocol]] (Mục 5).
