# Kurumi V8 — D.8 Master Checkpoint

**Ngày checkpoint:** 2026-08-14
**Phạm vi:** POS Menu Reconciliation (món ăn + đồ uống), kiến trúc Core/Cost/Inventory 3-spreadsheet, Standing Protocol đồng bộ.
**Trạng thái:** D.8 (món ăn) và D.8 Drink Engine đều CLOSED. Track song song của GPT (FINAL_COST, Range Optimization) đang chạy độc lập, xem Phần F.

Checkpoint tổng hợp bởi Claude (Constitution Keeper / Architecture Engine), đối chiếu từ raw JSON evidence của nhiều khung làm việc (GPT Architecture Engine, Gemini Builder, Claude Chrome Builder) qua các phiên 2026-08-11 → 2026-08-14.

Tiếp nối [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] — track trước (D.7C) đóng ở 5 Log + mở D.7C-7 Stock Dashboard; D.8 là track kế tiếp, phạm vi chuyển từ vận hành kho sang đối chiếu Menu/POS.

---

## Phần A — Kiến trúc nền tảng phát hiện trong track này

### A.1 — Core/Cost/Inventory là 3 spreadsheet RIÊNG BIỆT

```text
Phát hiện giữa chừng track D.8 — trước đó toàn bộ D.7C và đầu D.8
đều thao tác trong 1 workbook duy nhất (KURUMI_INVENTORY_ENGINE).
Thực ra hệ thống có 3 file Google Sheets tách biệt:

Core Engine (NGUỒN GỐC — Master Data/Recipe):
  https://docs.google.com/spreadsheets/d/1N-qn5k3y5szFbfEcyjAzoAo74znI6W09STwNI32gpP4
  Sheets: LIST_ITEM, ALL_ITEM, PREP_MASTER, UNIVERSAL_RECIPE_DETAIL,
  SEMI_PRODUCT_MASTER, FINAL_PRODUCT_MASTER, FINAL_FINISHING_DETAIL,
  EXTRA_PRODUCT_MASTER, PLACEMENT_MASTER, CODE_DICTIONARY,
  NAME_MAPPING, ARCHITECTURE_FROZEN, CONVERSION_EXPLICIT_RULE,
  CONVERSION_FACADE_COMPILER, UNIT_DICTIONARY

Cost Engine (MIRROR — tính giá vốn):
  https://docs.google.com/spreadsheets/d/1CrNIoiuvDgZFsTGpIvV7l3gtXresu-smp3_DicjgxlA
  Sheets: TEMP_COST_COMPILER, CORE_LIST_ITEM, CORE_ALL_ITEM,
  CORE_PREP_MASTER, CORE_RECIPE_DETAIL, CORE_SEMI_MASTER,
  CORE_FINAL_MASTER, CORE_FINAL_FINISHING, FINAL_FINISHING_COST
  (bảng tự tính giá qua ARRAYFORMULA), FINAL_COST, COST_REGISTRY

Inventory Engine (SNAPSHOT — vận hành thật, Ledger/Log):
  https://docs.google.com/spreadsheets/d/1rngAxx1AHHXSOWmdQu_NtsHeaL7sywtHEf9Q8jEK_AE
  Toàn bộ D.7C (5 Log + Dashboard) + bản sao Master Data để
  Resolver/Engine đọc trực tiếp (không cross-spreadsheet reference)
```

### A.2 — Standing Protocol (áp dụng BẮT BUỘC cho mọi sửa Master Data)

```text
Quyết định: KHÔNG dùng trigger tự động (rủi ro đồng bộ dữ liệu
dở dang giữa chừng). Mỗi lệnh build/sửa Master Data PHẢI kết thúc
bằng đúng 3 bước, coi là 1 phần bắt buộc của chính lệnh đó:

  1. Sửa tại Core Engine, regression PASS.
  2. Đồng bộ đúng phần vừa đổi sang Cost Engine → Inventory Engine.
  3. Physical readback CELL-BY-CELL cả 3 nơi (không chỉ đếm số
     dòng — bài học từ sự cố D.8N, xem Phần D). Chỉ báo CLOSED/PASS
     khi khớp 100% cả 3 nơi.

Nếu bước 2/3 thất bại → báo CLOSED_AT_CORE_ONLY, không báo PASS.
```

---

## Phần B — Track D.8: POS Menu Reconciliation (món ăn)

### B.1 — Nguồn dữ liệu đối chiếu

```text
1. POS365 export "Hàng hóa bán ra (Chi tiết)" — 189 SKU duy nhất
   tháng 7/2026 (sau khi gộp trùng do khuyến mãi).
2. 9 tài liệu Kitchen Bible (docx) — công thức chuẩn gốc từ bếp,
   phủ ~50 món: Breakfast, Sandwich, Toast, Smoothie Bowl, Dream
   Bowl, Salad, Plate/Burger, Slavic, Soup, Pasta.
3. Products.xlsx (952 SKU toàn bộ POS365) + Materials.xlsx —
   dùng để audit đầy đủ nhóm DRINKS (96 SKU).
```

### B.2 — Kết quả audit ban đầu (D.8A)

```text
MATCHED: 47 | PARTIAL_MATCH: 91 | MISSING: 51 (tổng 189)
→ Tạo sheet POS_MENU_REVIEW (142 dòng cần Reality Owner duyệt
  tay, sắp xếp theo doanh số giảm dần, dropdown quyết định).
```

### B.3 — 6 SKU Gluten Free đặc biệt (D.8C → D.8G)

```text
Phát hiện quan trọng: 2 công thức GF đang trỏ NHẦM sang công thức
mì thường (rủi ro trừ sai kho nếu không bắt kịp):

DN-0130 GF Pomodoro    → tạo mới FIN-PAS-GFP-001 (đổi 1 dòng mì
                          CLP→CGF, giữ nguyên 170g)
HH-0522 GF Stroganoff   → tạo mới FIN-PAS-GFS-001 (tương tự)
HH-0318 GF Pesto          → hoàn toàn chưa có công thức (cả bản
                            thường cũng chưa) — xây từ đầu, xác
                            nhận Reality Owner: hành trắng, dầu
                            dừa 10g (là số cân, không phải ml),
                            nước 100g (1:1)
DN-0018 GF Alfredo           → tương tự Pesto
DN-0140/DN-0075 bánh GF        → base đã đúng, chỉ thiếu conversion
                                Portion→Whole Cake = 1/12 (12
                                phần/ổ, Reality Owner xác nhận)
```

### B.4 — Đối chiếu Kitchen Bible (D.8I)

```text
45/45 công thức trích từ Bible đối chiếu với hệ thống:
  43 khớp Final Code có sẵn
  2 hoàn toàn thiếu Final Code: HH-0106 Pasta Pesto (thường),
    HH-0194 Vegan Alfredo (thường) — mirror ngược từ bản GF vừa
    build, đổi CGF→CLP
  3 "MISSING" nhưng thực ra ĐÃ CÓ mã đúng (chỉ candidate sai):
    Caesar Salad, Nutty Toast, Kurumi Smoothie Bowl
  2 candidate trỏ sai: Italian Baguette Brie, Tomato Cream Soup
  4 lệch định lượng — Reality Owner chọn "theo Bible":
    Caesar (tempeh 40→45g, crouton 10→20g)
    Nutty Toast (chocolate 30→20g)
    Italian Baguette Brie (sửa lại toàn bộ topping)
    Kurumi Bowl — audit lần đầu SAI (kết luận "thiếu base" nhưng
    thực ra đã có tham chiếu PREP-BAS-KRB-001 đúng — không sửa,
    bài học: kiểm tra chuỗi tham chiếu PREP trước khi kết luận
    "thiếu")
```

### B.5 — Nhóm D.8H — chờ tài liệu bổ sung (CHƯA XONG)

```text
Carrot Cake (nhiều size), Whole Brownie, Crafty Cow 125ml/260ml,
8 món Oat/Coconut Milk — CHƯA build vì thiếu Kitchen Bible
Cakes/Drinks. Brownie hiện là 1/2 MISSING COST còn lại trong
FINAL_COST (xem Phần F).
```

---

## Phần C — Track D.8 Drink Engine (đã đóng)

### C.1 — Nguồn dữ liệu

```text
Cost_Drink.xlsx — 37 biến thể đầy đủ định lượng (đơn vị kg/L,
quy đổi 1kg=1000g, 1L=1000ml=1000g) + giá mua thật + tỷ lệ cost.
Ảnh chụp menu thật (Coffee/Tea/Smoothie/Juice) để xác nhận tên/
giá/cấu trúc SKU.
```

### C.2 — Audit ban đầu (D.8J)

```text
MATCHED_EXACT: 3 | MATCHED_WITH_DIFFERENCES: 4 | MISSING: 30
Turmeric Shot: MISSING_NO_SOURCE (không có trong Cost_Drink.xlsx
lẫn Kitchen Bible — công thức riêng từ Reality Owner sau này).
```

### C.3 — Phát hiện cấu trúc SKU quan trọng (D.8K)

```text
Xác nhận qua khảo sát trực tiếp POS365 (Danh sách hàng hóa):

Loại SỮA (Oat/Coconut) → 2 SKU RIÊNG, 2 Final Code riêng.
Nhiệt độ (Nóng/Đá)      → KHÔNG tách SKU trên POS, NHƯNG Reality
                          Owner xác nhận CÓ 2 công thức khác nhau
                          (định lượng sữa/đá khác nhau thật) —
                          vẫn build 2 Final Code riêng dù chung 1
                          SKU bán (vấn đề "chọn đúng công thức khi
                          bán" để dành cho Sales Engine tương lai
                          — Modifier Resolver, chưa build).
Mã CŨ (tiền-tách-sữa)    → tồn kho âm RẤT lớn, không ghi loại sữa
                          → bỏ qua, không build (VD: HH-0073
                          Cappuccino cũ, HH-0075 Matcha Latte cũ).
Latte Coconut             → CHỈ có bản Nóng, không bán đá (xác
                            nhận riêng, khác pattern chung).
```

### C.4 — Nền tảng kỹ thuật cần dựng trước khi build (D.8J-PATCH-1-EXT, PATCH-2, PATCH-3)

```text
1. Di dời TOÀN BỘ Conversion Architecture (UNIT_DICTIONARY,
   CONVERSION_EXPLICIT_RULE, CONVERSION_FACADE_COMPILER) từ chỗ
   duy nhất (Inventory) sang đúng vị trí Source+Snapshot (Core là
   gốc, Cost/Inventory nhận sync) — bao gồm cả 12 rule cũ đã có
   từ D.6C-D.7C, không chỉ rule mới.

2. Thêm canonical unit "SHOT" — PREP-COF-COS-001 SHOT→ML=30, chuỗi
   quy đổi: 1 Shot → 30ml → 27,73845g (dùng factor ML→G=0.924615
   đã có từ trước).

3. Tạo 6 Item Code RAW mới (Matcha Powder, Coconut Milk Powder,
   Coconut Juice*, Fresh Turmeric, Chamomile Tea, Artichoke Tea)
   + 2 Item Code sau này (Earl Grey Tea, Cayenne Pepper).

   *Coconut Juice: PHÁT HIỆN QUAN TRỌNG — không phải RAW mua sẵn,
   mà PHẢI tái cấu trúc thành PREP (Fresh Coconut RAW mới → chiết
   xuất 300ml/quả, Execution Type=STANDALONE) vì Reality Owner xác
   nhận "nhập dừa quả tươi, tự chặt lấy nước" — đúng Stock Boundary
   RAW→PREP đã áp dụng suốt track D.7C.
```

### C.5 — Build 3 đợt

```text
Đợt 1 (D.8L) — Coffee cơ bản, 10 Final Code:
  Espresso, Americano Hot/Iced, Cappuccino Oat/Coconut Hot/Iced,
  Latte Oat Hot/Iced, Latte Coconut Hot.

Đợt 2 (D.8O) — Coffee/Matcha/Chocolate mở rộng, 10 Final Code:
  Bumble Coffee, Salted Coffee, Coconut Coffee, Turmeric Latte
  Oat/Coconut (2 mã riêng), Hot Chocolate, Coconut Chocolate,
  Cloudy Matcha, Tiramisu Cappuccino, Strawberry Matcha.

Đợt 3 (D.8Q) — Bổ sung ngoài Cost_Drink.xlsx:
  Turmeric Shot (công thức trực tiếp từ Reality Owner, batch 5
  chai: Nghệ 1g, Gừng 1,6g, Cam 105g[3 trái×175g÷5], Chanh 13g
  [1 trái×65g÷5], Cayenne 0,2g).
  Earl Grey Tea Pot (trà rời 5g + Water 500g).
```

### C.6 — Sự cố nghiêm trọng đã xảy ra và cách xử lý (D.8N)

```text
Phát hiện: dữ liệu chat/chỉ thị (nguyên văn "AUTHORIZED Đợt 1",
"Americano Hot:"...) bị DÁN NHẦM vào giữa các ô công thức Alfredo
GF (FIN-PAS-GFA-001) tại Inventory Engine — không phải lỗi logic,
là lỗi thao tác vật lý (có thể do copy-paste sai vùng qua UI).

Xử lý: dừng NGAY mọi việc khác, dùng Core Engine (đã xác nhận
sạch) làm nguồn chuẩn, xóa sạch dòng rác, ghi lại đúng 11 dòng
theo Core, đọc lại đối chiếu 1-1, kiểm tra Final Code lân cận
không bị lan.

BÀI HỌC ĐÃ ĐÚC KẾT (áp dụng từ đây về sau):
- Physical readback phải là CELL-BY-CELL, không chỉ đếm số dòng
  khớp (số dòng khớp không đảm bảo nội dung đúng).
- Khi thao tác qua giao diện AI có khả năng "click UI + chụp màn
  hình" (như Claude trong Chrome), rủi ro cao hơn thao tác qua
  Apps Script trực tiếp — ưu tiên viết script ghi hàng loạt thay
  vì click từng ô, vừa an toàn hơn vừa tiết kiệm token.
- Sau mỗi lần sửa lỗi khẩn cấp, phải kiểm tra vùng LÂN CẬN không
  bị ảnh hưởng, không chỉ vùng đã biết lỗi.
```

### C.7 — Reconciliation cuối (D.8P, D.8Q)

```text
38/38 biến thể từ Cost_Drink.xlsx + 2 công thức ngoài nguồn
(Turmeric Shot, Earl Grey) — TẤT CẢ đã BUILT, khớp cell-by-cell
3 nơi, không rác text.

Patch nhỏ trong quá trình: Purple Smoothie thiếu Item Code cho
dòng Ice — bổ sung RAW-UTI-ICE-001 (đá viên chuẩn, dùng chung).

TRACK D.8 DRINK ENGINE: CLOSED.
```

---

## Phần D — Nguyên tắc mới đúc kết trong track D.8

Tiếp nối 17 nguyên tắc đã có từ track D.7C (xem [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] Phần F):

```text
18. Đơn vị xử lý "trái/quả" (pcs) của nguyên liệu tươi phải quy
    đổi ra gram theo pattern ĐÃ CÓ trong hệ thống (audit công thức
    tương tự đã build trước — ví dụ Orange Juice dùng gram không
    dùng pcs), không tự đặt cách mới. Khi cần số cân thật (ví dụ
    "3 trái cam"), luôn hỏi Reality Owner cân nặng trung bình/trái,
    không đoán.

19. Trước khi audit tìm "thiếu công thức", phải kiểm tra CHUỖI
    THAM CHIẾU PREP đầy đủ (Final → Prep → Raw), không chỉ nhìn
    thẳng vào FINAL_FINISHING_DETAIL tìm nguyên liệu thô — bỏ sót
    bước này gây kết luận sai (case Kurumi Bowl).

20. Vật lý ghi dữ liệu (physical readback) phải là CELL-BY-CELL,
    không chỉ đếm tổng số dòng — số dòng khớp không đảm bảo nội
    dung từng ô đúng (sự cố D.8N).

21. Khi phát hiện dữ liệu bị hỏng (rác text, sai lệch bất thường),
    dừng NGAY mọi việc khác, xác định nguồn SẠCH đáng tin cậy nhất
    trước (thường là Core Engine — nơi ít bị thao tác thủ công
    nhất), dùng nó để sửa các nơi khác, và kiểm tra vùng lân cận
    không bị lan.

22. Đơn vị xử lý (SKU) trên POS không nhất thiết khớp 1-1 với số
    lượng Final Code cần build — 1 SKU có thể cần 2 công thức
    (như Latte theo Nóng/Đá) nếu định lượng thực tế khác nhau, dù
    hệ thống order hiện tại chưa phân biệt được lúc bán (vấn đề để
    dành cho Modifier Resolver/Sales Engine tương lai).

23. Khi nhiều AI (Claude, GPT, Gemini) cùng làm việc song song
    trên cùng 1 track, cần: (a) phân công rõ phạm vi tránh dẫm
    chân, (b) dùng Final Code/SKU làm khóa đối chiếu thay vì đếm
    đầu việc (dễ đếm sai khi 1 "món" thực ra là N biến thể), (c)
    khi 1 khung "đứng hình"/gián đoạn, khung khác tiếp quản cần
    xác nhận lại trạng thái bằng bằng chứng, không tự tin theo lời
    kể.
```

---

## Phần E — Trạng thái file/sheet quan trọng (để tra cứu nhanh)

```text
POS_MENU_REVIEW (Inventory Engine) — 142 dòng, đa số đã duyệt.
Còn nhóm D.8H (Carrot Cake, Brownie, Crafty Cow, 8 món Oat/Coconut
Milk) đang tô đỏ, chờ Kitchen Bible Cakes/Drinks bổ sung.

drink_recipes_raw.json, kitchen_bible_recipes.json,
pos_menu_189_items.csv — file tham chiếu gốc đã trích xuất, còn
giữ lại được nếu cần đối chiếu lại sau này.

CONVERSION_EXPLICIT_RULE (Core) — 15 rule tính đến nay: ML→G
Coffee(0.924615), BATCH→G OCP(250)/STR(2410), PORTION→G
OCP(62.5), PCS→SLICE Sourdough(1), KG→G Transfer×2, PORTION→
WHOLE_CAKE bánh GF×2(1/12), SHOT→ML Coffee(30).
```

---

## Phần F — Track song song của GPT (không thuộc phạm vi D.8, tham khảo)

```text
GPT đang phụ trách riêng FINAL_COST + Range Optimization —
không phải phần Claude audit trực tiếp trong track này, ghi lại
để tra cứu liên tưởng.

FINAL_COST: đã sửa xong (B2 locale, E2 Yield guard, H2 fail-closed,
COST_REGISTRY error handling, Espresso/Coconut Juice vào Lock).
132/132 Final Code có tên, 0 formula error.
Còn 2 MISSING COST hợp lệ: Coconut Coffee (chờ giá mua thật
Coconut Milk Powder), Brownie (chờ công thức — thuộc nhóm D.8H).

Range Optimization: PENDING lúc checkpoint này được ghi — sửa 7
ô (C2, E2, G2, H2, I2, J2, K2, O2) trong FINAL_FINISHING_COST,
bỏ full-column reference, chuẩn hóa range 2:1449. Chưa có bằng
chứng thực thi tại thời điểm checkpoint.

Vấn đề chưa rõ nguyên nhân: menu "Kurumi ERP" không hiện cho
Leader dù code onOpen() đã audit sạch (D.8K cũ, không phải D.8
này) — vẫn treo, chưa xác định root cause.
```

---

## Phần G — Việc còn lại (ưu tiên)

```text
1. Chờ Kitchen Bible Cakes/Drinks để xử lý nhóm D.8H (Carrot Cake,
   Brownie, Crafty Cow, 8 món Oat/Coconut Milk).
2. Chờ giá mua thật Coconut Milk Powder (khi có hóa đơn) để đóng
   MISSING COST cho Coconut Coffee.
3. Chờ công thức Brownie để đóng MISSING COST còn lại.
4. GPT hoàn tất Range Optimization, báo kết quả.
5. Vấn đề menu không hiện cho Leader — cần điều tra tiếp (kiểm tra
   quyền Editor đúng email, hay lỗi khác chưa phát hiện).
6. Xa hơn (không gấp): thiết kế Modifier Resolver cho Sales Engine
   tương lai — xử lý việc 1 SKU có nhiều công thức theo lựa chọn
   khách (Nóng/Đá, không hành/tỏi...), tích hợp POS365 thật.
```

**Mục nào thuộc chuyên môn vận hành/bếp của Reality Owner** (theo [[Governance-Protocol]] Mục 5 — Domain Authority): #1 (Kitchen Bible), #2 (giá mua thật), #3 (công thức Brownie) — cần Thanh cung cấp khi có, không phải quyết định IT.
**Mục thuần kỹ thuật IT** (#4, #5, #6) — thuộc phạm vi AI tự xử lý, không cần hỏi Thanh chi tiết.

---

Liên quan: [[D7C-MASTER-CHECKPOINT-2026-08-10-v4]] (track trước, D.7C đóng + mở Stock Dashboard), [[D7C-MASTER-CHECKPOINT-2026-08-10-FINAL]], [[Governance-Protocol]] (Mục 5 — ranh giới hỏi/không hỏi Thanh áp dụng cho Phần G).
