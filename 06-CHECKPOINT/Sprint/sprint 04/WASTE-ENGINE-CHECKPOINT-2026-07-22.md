# WASTE ENGINE — Checkpoint riêng (tách từ CHECKPOINT-2026-07-22.md, cập nhật đến 2026-07-29)

Toàn bộ nội dung Waste Engine tách ra khỏi Checkpoint chính để giữ file gốc gọn. Đây là Mission **chưa build** (`WASTE_LOG` đã tồn tại, `WASTE_COMPILER` chưa có) — không phải Mission chính thức đang mở, chỉ đang điều tra thiết kế trước khi build.

Liên quan: [[CHECKPOINT-2026-07-22]] (Mục II.7, III, V), [[Discovery — Boundary Formula vs Engine]], [[Discovery — Hierarchy of Prevention]], [[Production-Compiler-Execution-Type-Spec-V1]], [[ADR-018 Waste Event ID Format]], [[ADR-019 Pre-Resolver Input Validation Gatekeeper]], [[ADR-020 Universal Event Lifecycle]], [[ADR-021 Active View Boundary]]

---

## 1. Bug lớn đầu tiên (2026-07-22)

**Hiện tượng:** `WASTE_LOG` đang lookup `Unit` trực tiếp từ `ALL_ITEM` (System Unit — đơn vị lưu kho, ví dụ Opera Cake = WHOLE CAKE). Nhưng nhân viên báo Waste theo đơn vị họ quan sát thực tế (1 pcs, 1 slice, 1 bowl...). Nếu ép nhập theo System Unit, dễ sai số nghiêm trọng khi vào Ledger. **Xếp loại: bug lớn** (ảnh hưởng trực tiếp Transaction Truth), không phải bug nhỏ.

**Taxonomy quyết định (đã qua 2 vòng refine, chốt theo Reality Pumpkin Soup):**

- ❌ Không dùng "Deterministic vs Non-deterministic" (dựa trên có cân được hay không) — dễ nhầm lẫn.
- ✅ Dùng **Waste của Business Object** (1 Portion, 1 pcs, 1 Bowl, 1 Whole Cake — đã có Business Rule quy đổi cố định) → Compiler tự quy đổi, **không cần cân lại thành phẩm** (nguyên liệu đã cân từ đầu lúc vào công thức).
- vs **Waste của Bulk Material** (dầu đổ ra sàn, sốt dư trong nồi — không tồn tại Business Rule quy đổi) → bắt nhập trực tiếp theo System Unit (g/ml/kg).

**Đã bác bỏ:** đề xuất thêm cờ `Estimated` — vì có thể vô tình hợp thức hóa việc bỏ SOP (trạm có cân nhưng nhân viên không cân ≠ "không đo được"). Không mở Discovery này trừ khi xác nhận có trạm thật sự không thể đo.

## 2. Discovery — Business Object của Universal Recipe (shared dependency với Production Compiler)

**Câu hỏi gốc:** `UNIVERSAL_RECIPE_DETAIL` normalize theo Business Object nào? Batch/Yield Qty/Portion/Whole Cake/pcs đều chỉ là Projection của Business Object đó, không phải 2 lựa chọn loại trừ nhau (không phải "Batch hay Yield Qty" — câu hỏi nhị phân ban đầu sai khung).

**Trạng thái:** vẫn là *shared dependency* giữa Production Compiler (Mission chính, đã Stable) và Waste Engine — không mở lại Mission Production Compiler để giải quyết.

**Observation (3 case cụ thể, CHƯA FREEZE):**

- Pumpkin Soup: Business Object = 1 Portion → Waste "1 Bowl", không cần biết Batch.
- Oat Pancake Prep: Business Object = 1 Batch → 4 pcs → Waste "1 pcs" = 0.25 Batch.
- Opera Cake: Business Object = 1 Whole Cake → 8 pcs → Waste "1 pcs" = 0.125 Whole.

Đủ mạnh để định hướng, nhưng **chưa đủ để nâng thành Principle** — chỉ 3 case, chưa kiểm chứng ở Drink/Bakery/Sales Consumption (chưa build).

**✅ Đóng phần lớn (2026-07-22, xác nhận bằng dữ liệu thật — `FINAL_PRODUCT_MASTER`, `PREP_MASTER`, `UNIVERSAL_RECIPE_DETAIL`, `PREP_LOG`):**

- `PREP_MASTER`: `Portion Count`/`Standard Portion Size` trống hầu hết mọi dòng — Prep chuẩn hóa theo Yield Qty (gram).
- `FINAL_PRODUCT_MASTER` **đã có sẵn** `Portion UOM`, `Batch UOM`, `Yield Qty` cho mọi Final Product (ví dụ Brownie: Batch UOM=WHOLE CAKE, Yield Qty=8, Portion UOM=pcs).
- **Kết luận:** Business Rule quy đổi Final Product **đã tồn tại sẵn** — không cần xây bảng `WASTE_UNIT_CONVERSION` riêng. Waste Engine tiêu thụ trực tiếp: Prep từ `PREP_MASTER` (Yield Qty), Final từ `FINAL_PRODUCT_MASTER` (Batch UOM/Yield Qty/Portion UOM).

**✅ Đã trả lời — nhưng phát hiện 2 tầng độc lập (2026-07-22, bằng chứng mở rộng 40+ dòng SOUP/BOWL/PASTA/BURGER/SMOOTHIE/SHAKE):** công thức "1 Batch UOM = Yield Qty Portion UOM" **đúng nhưng không đủ**:

- **Tầng 1 — Batch → Yield → Portion UOM:** quy đổi sản xuất (Whole Cake → 8 pcs).
- **Tầng 2 — Portion Size:** số đơn vị nhỏ trong 1 phần bán (Momo: Portion Size=6, Portion UOM=pcs — 1 phần = 6 cái), **độc lập** với Yield Qty. Hầu hết món khác Portion Size=1 nên 2 tầng trông giống nhau — Momo là case duy nhất phơi bày sự tách biệt.

**Phát hiện phụ (nối Discovery cũ, à la carte/Sales Compiler, ~2026-07-20):** nhóm Soup/Bowl/Pasta/Burger/Smoothie/Shake có `Batch UOM = Portion UOM` và `Yield Qty = 1` — xác nhận **không có Batch thật**, nấu 1-1 theo order, không qua `PRODUCTION_COMPILER`. Là cả 1 nhóm lớn, không phải ngoại lệ hiếm.

**⚠️ Correction (cùng phiên):** kết luận *"chỉ SKU có `Batch UOM ≠ Portion UOM` mới cần quy đổi Waste"* đã **rút lại** — dựa trên lỗi đọc nhầm `Portion Size` thành `Yield Qty` (case Momo/Smoothie). Case Momo (`Batch UOM = Portion UOM = pcs`, nhưng `Portion Size = 6`) là phản ví dụ thật, bác bỏ quy tắc đó.

**Bằng chứng thêm (`FINAL_FINISHING_DETAIL`):** sheet này — nơi lẽ ra dùng `Portion Size` nếu có Consumer — **không tham chiếu** field đó. UOM ở đây là đơn vị nguyên liệu thành phần riêng (g/ml/portion/pcs), "portion" khác nghĩa hoàn toàn với `Portion Size` bên `FINAL_PRODUCT_MASTER` (trùng tên, khác khái niệm). Xác nhận: `Portion Size` **chưa có Consumer thật** trong hệ thống đang chạy — cho tới khi Waste Engine dùng nó (xem mục 3).

**Discovery mới, để dành cho Sales Engine (chưa build, không mở Mission bây giờ):** `Portion Size` có Consumer **gốc** là Sales (khách gọi "5 phần Momo" → POS → Sales Compiler dịch sang Inventory), Waste chỉ là Consumer thứ 2 tái dùng cùng Business Rule. Sales Compiler sẽ đối xứng ngược Production Compiler: `Final Product → Business Rule → Inventory` (Sales) vs `Inventory → Business Rule → Final Product` (Production). Ba "ngôn ngữ" song song: Sales Language (phần/miếng/tô), Kitchen Language (batch/prep/yield), Inventory Language (g/ml/pcs/whole cake). **Giữ ở Observation**, chưa đủ Reality để nâng Principle.

**Observation khác (song song, chưa đủ lặp lại để thành Principle):** Yield có dấu hiệu là *Business Knowledge* dùng chung nhiều Mission (Production, Waste — đã xác nhận; Daily Usage/Forecast/Food Cost/Inventory — dự đoán, chưa build), không phải thuộc tính riêng của 1 Compiler.

## 3. Thiết kế dropdown Unit cho WASTE_LOG (Proposal, chưa Freeze)

> Bản spec chi tiết và cập nhật hơn của mục này nằm ở Mục 8 (2026-07-25) — mục này giữ lại làm bối cảnh lịch sử.

**Nguồn suy ra tự động** (không cần bảng nhập tay riêng):

```
Allowed Report Unit =
  System Unit (luôn có)
  + Portion UOM  (nếu Portion Size tồn tại VÀ khác Portion UOM gốc — loại trừ case Smoothie:
                   Portion Size=350=Portion UOM ml, không tạo thêm lựa chọn thừa)
  + "batch"      (nếu Reference Batch Qty tồn tại, từ PREP_MASTER)
```

**Refinement hiển thị:** dropdown không hiện Unit trần (`pcs`/`portion`) — hiện **Business Object** kèm quy đổi trong ngoặc, ví dụ `"2 pcs"` / `"1 Serving (6 pcs)"` / `"1 Batch"`. Nhân viên chọn theo ngôn ngữ nghiệp vụ, không phải đơn vị kỹ thuật. Nguồn dữ liệu sinh dropdown không đổi, chỉ đổi cách hiển thị.

## 4. Discovery mới nhất (2026-07-22) — Waste Log là Multi-Domain Reader

**Quan sát của Thanh:** Waste không chỉ là `Item / Qty / Unit / Reason` đơn giản — nó đứng ở giao điểm nhiều domain, mỗi domain có "ngôn ngữ" riêng:

| Nguồn Waste | Đọc từ Sheet | Ngôn ngữ |
|---|---|---|
| RAW | `LIST_ITEM` | kg, ml (không Sales, không Portion) |
| PREP | `PREP_MASTER` | batch, g (Business Language của bếp) |
| FINAL | `FINAL_PRODUCT_MASTER` | portion, pcs, whole cake, slice (ngôn ngữ Sales) |

**Nguyên nhân:** Waste Log không đặc biệt — nó là **màn hình dùng chung** cho toàn ERP, phải phục vụ Kho + Prep + Production + Sales thành phẩm, nên phải hiểu ngôn ngữ của từng domain.

**Kiến trúc đề xuất (Proposal, chưa Freeze):** không hard-code `IF Item Type = RAW/PREP/FINAL` trong logic Waste Engine. Thay vào đó:

```
User chọn Source
    ↓
RAW    → đọc LIST_ITEM
PREP   → đọc PREP_MASTER
FINAL  → đọc FINAL_PRODUCT_MASTER
```

Mỗi sheet tự mang theo ngôn ngữ của chính nó — Waste Engine không sở hữu ngôn ngữ, chỉ là **Consumer** đọc ngôn ngữ do từng Master Sheet định nghĩa.

**Hệ quả tốt (chưa kiểm chứng, chỉ là kỳ vọng thiết kế):** nếu sau này có `SEMI_PRODUCT_MASTER` hoặc `PACKAGING_MASTER`, Waste Engine gần như không cần sửa logic — chỉ cần thêm 1 dòng ánh xạ `Domain → Master Sheet → Business Language`, dropdown tự mở rộng.

**Trạng thái:** Proposal kiến trúc, chưa Freeze, chưa build. Đáng chú ý vì nhất quán với nguyên tắc đã Freeze ở nơi khác (mỗi domain tự chịu trách nhiệm định nghĩa dữ liệu của mình — giống cách `PREP_MASTER` tự có `Execution Type` thay vì Compiler tự đoán).

## 5. Consumption Resolver — thay thế Type A/B/C (2026-07-25, refinement lớn)

**Thay đổi so với bản trước:** không còn phân loại theo "loại Final Product" (Type A Inventory Final / Type B Cook-to-order / Type C Prep) — phân loại đó đúng nhưng ở sai mức độ chi tiết. Đúng hơn: **resolve theo từng component**, không theo cả món.

**Nguyên lý:** SELL và WASTE đứng cùng phía "Consumption/OUT" của Inventory (đối lập "Birth/IN" = PREP_LOG/PRODUCTION_LOG/STOCK_INPUT). Cả 2 dùng chung 1 **Consumption Resolver**, chỉ khác `Event Type` (SALE vs WASTE) khi ghi vào `TRANSACTION_STAGING`.

```
SELL / WASTE
     │
     ▼
Business Object Resolver
     │
     ├── Inventory Object tồn tại trực tiếp? (FINAL đã Production thành Whole Cake, v.v.)
     │        YES → Consume Object → STOP
     │
     └── NO → Read Final BOM (FINAL_ASSEMBLY_DETAIL / FINAL_FINISHING_DETAIL)
              For each Component:
                ├── Component đã là Inventory Object tồn tại (PREP STANDALONE/SEMI đã log)
                │        → Consume component đó → STOP (không nổ tiếp, tránh double-consumption)
                └── Component là RAW hoặc PREP INLINE (chưa từng có tồn kho riêng)
                         → Consume RAW / tiếp tục nổ theo Execution Type đã Freeze
```

**Cơ chế "đã là Inventory Object hay chưa" — nguyên lý chung, không phải field riêng của PREP:** câu hỏi thật không phải "PREP có Execution Type gì" — mà là **Item Code này đã từng có Ledger ghi YIELD (tức có Compiler nào sinh ra tồn kho cho nó) hay chưa**, bất kể tầng nào (RAW/PREP/SEMI/FINAL, hay tầng tương lai như Frozen Product/Central Kitchen/Commissary — chưa tồn tại nhưng Resolver không cần sửa gì khi chúng xuất hiện). `Execution Type` (STANDALONE/INLINE) trong `PREP_MASTER` chỉ là **cách hiện tại đang implement câu hỏi đó cho riêng tầng PREP** — không phải bản thân nguyên lý. SEMI không có field Execution Type nhưng vẫn là điểm dừng hợp lệ, vì `SEM-MOM-FRO-001` có Ledger thật từ Production.

**Principle (2026-07-25):** *"Consumption không bao giờ đi xuống thấp hơn Inventory Reality — nếu Object đã tồn tại trong Inventory, Consume Object, không explode tiếp."* Đây là lý do không bao giờ double-count, và là abstraction đủ cao để mở rộng sang tầng mới (Frozen Product, Central Kitchen, Workshop, Commissary...) mà không cần sửa Resolver — chỉ cần tầng mới đó ghi Ledger thật khi sinh ra.

**✅ Đóng câu hỏi Semi Product (Momo) đang treo:** không cần quyết định riêng "dừng ở Semi hay xuống RAW" — Resolver tự trả lời bằng đúng 1 nguyên lý chung: `SEM-MOM-FRO-001` (Frozen Momo) là Inventory Object có tồn kho thật (đã qua Production, nhập kho) → Resolver dừng ở đó, consume `-6 pcs SEM-MOM-FRO-001`, không nổ tiếp xuống công thức làm Momo.

**Ví dụ đối chiếu 3 case đã bàn, giờ thống nhất 1 luồng:**

- **Opera Cake** (Whole Cake tồn kho thật) → dừng ngay ở bước đầu, không đọc BOM nào cả — Production Compiler đã consume RAW từ lúc sinh ra Whole Cake.
- **Burger** (không tồn kho ở cấp Final) → đọc `FINAL_FINISHING_DETAIL`, từng component: BBQ Sauce (PREP STANDALONE, đã log) → dừng, consume PREP; Lettuce/Tomato (RAW) → consume RAW trực tiếp.
- **Momo** → đọc `FINAL_FINISHING_DETAIL`, Frozen Momo (SEMI đã log) → dừng, consume SEMI; Spice Mayo/Soy Sauce → theo đúng Execution Type của từng cái.

**⚠️ Phụ thuộc thật (nối [[Discovery — Hierarchy of Prevention]], đang Open ở Checkpoint chính):** độ chính xác của Resolver phụ thuộc `PREP_LOG` được ghi đầy đủ cho mọi PREP STANDALONE. Nếu 1 PREP đánh dấu STANDALONE nhưng SOP ghi log chưa tuân thủ (case Đậu hũ ép — `PREP-PRO-PTO-001`), Resolver dừng đúng logic nhưng dừng ở tồn kho sai/thiếu — không phải lỗi Resolver, là lỗi Reality chưa khớp giả định.

**Kết luận:** SELL_COMPILER và WASTE_COMPILER không sở hữu 2 logic explode riêng — chỉ khác lý do Business Event (`Event Type = SALE` vs `WASTE`), dùng chung 1 Resolver.

**⚠️ Refinement (nguồn chưa xác minh — xem ghi chú cuối đoạn):** có đề xuất dùng `Assembly Cost > 0` (từ `FINAL_COST`) làm signal để Resolver quyết định STOP ở FINAL hay explode xuống `FINAL_FINISHING_DETAIL`. **Tín hiệu này chỉ nên dùng làm audit cross-check, không phải signal quyết định chính** — vì nó phản ánh Cost Model (recipe có khai báo Assembly hay không, tức "declared"), không phải Reality thật (tồn kho có thật hay không, tức "observed"). Nếu 1 Final Code có Assembly Cost > 0 nhưng chưa từng chạy qua `PRODUCTION_COMPILER` thật, Resolver dùng Assembly Cost sẽ tưởng nhầm có tồn kho — đúng loại Reality gap đã gặp ở Đậu hũ ép (SOP khai báo nhưng chưa từng log thật), chỉ khác tầng.

**Signal đúng cho Resolver:** tra trực tiếp `STOCK_POSITION`/`INVENTORY_LEDGER` — Item Code đã từng có dòng YIELD thật chưa, không tra Cost Model. `Assembly Cost > 0` vẫn có giá trị làm cảnh báo audit: nếu có Assembly Cost nhưng chưa từng xuất hiện Ledger, đó là dấu hiệu đáng chú ý (recipe khai báo nhưng chưa từng sản xuất thật), không phải điều kiện STOP/EXPLODE.

**Điểm hội tụ đáng ghi nhận:** `Assembly Cost > 0` khớp đúng với `Batch UOM ≠ Portion UOM` (Type A cũ) đã xác nhận độc lập trước đó qua `FINAL_PRODUCT_MASTER` — 2 nguồn dữ liệu khác nhau cùng chỉ về 1 phân loại, tăng độ tin cậy của việc phân biệt "sản phẩm được tạo trước" vs "resolve lúc bán", dù cơ chế quyết định cuối vẫn nên là Ledger thật.

> **Ghi chú nguồn (đã xác nhận với Thanh):** đoạn Refinement này là việc thật do 1 phiên Claude Code làm — **trước khi phiên chat hiện tại tham gia team**, nên không có trong ký ức của phiên này. Không phải nhầm lẫn/misattribution.

## 6. Đối chiếu file thật (`System_Kit`, 65 sheet + `KURUMI_COST_ENGINE`, 28 sheet) — 2026-07-25

**`WORKSHOP_*` (9 sheet, hệ V7) — làm rõ, không phải "thụt lùi":** `WORKSHOP_EXPLODE_L2` đã có nested PREP explosion thật (gặp PREP → đọc `UNIVERSAL_RECIPE_DETAIL`, scale theo Yield/Portion, nếu component bên trong lại là PREP thì tiếp tục nổ). `WORKSHOP_TERMINAL_FILTER` dừng bằng graph check ("còn recipe phía dưới không"). Đây là **Explosion Engine** đã có sẵn — prior art đáng tham khảo. Nhưng **chưa đủ bằng chứng nói V8 thụt lùi** — có thể Workshop giải bài toán khác (planned production), Production Compiler V8 cố ý giữ transaction reality khác. Cần phân biệt "algorithm tái dùng được" ≠ "business semantics tái dùng được".

**Materialization Boundary — chính là câu hỏi Ledger-based signal đã đề xuất ở Mục 5, không phải câu hỏi mới:** Workshop's Terminal Filter chỉ hỏi "còn recipe không" (thiếu chiều "đã materialize thành inventory thật chưa"). Consumption Resolver V8 cần thêm đúng 1 chiều: nếu Object đã có Ledger thật → STOP, dù vẫn còn recipe phía dưới. Đây trùng khớp hoàn toàn với đề xuất "tra `STOCK_POSITION`/`INVENTORY_LEDGER`" ở Mục 5 — 2 lần đề xuất độc lập hội tụ, tăng độ tin cậy.

**⚠️ Cảnh báo scope, không nhét nguyên field Recovery/Waste của `PREP_MASTER` vào Waste Resolver:** quét formula toàn bộ 65 sheet xác nhận **không có Compiler nào tham chiếu** `Recovery`/`Waste %`/`Waste Tracking`/`Recovery Source`/`Recovery Target` — declared nhưng chưa có Consumer thật (giống case `Portion Size` trước đây). Nhưng 2 domain khác nhau, không đồng nhất: `Recovery Before Waste` của PREP_MASTER nói về **production transformation loss** (RAW → Process → Usable/Recoverable/Waste). `WASTE_LOG` nói về phạm vi rộng hơn (Storage loss, Spoiled, Expired, Burnt, Service waste, Process failure...). Nhét thẳng Recovery vào Waste Resolver chung sẽ biến Waste Engine thành Production Yield Engine lần 2 — cần Mission riêng nếu muốn xử lý Recovery.

## 7. Consumption Resolver — Architecture khép kín, sẵn sàng handoff (2026-07-25)

**Reframe quan trọng:** Execution Type chỉ là field hiện có cho PREP, không phải bản thân khái niệm kiến trúc. Lõi thuật toán nên hiểu theo **Materialized vs Non-materialized**, không hard-code "STANDALONE = terminal":

```
RAW                → MATERIALIZED     → consume, STOP
SEMI               → MATERIALIZED     → consume, STOP  (⚠️ giả định, xem nuance dưới)
PREP / STANDALONE  → MATERIALIZED     → consume, STOP
PREP / INLINE      → NON-MATERIALIZED → explode, RECURSE
```

**Công thức Scaling đã khóa, xác nhận bằng Reality (`FINAL_FINISHING_DETAIL`, Veggi Noodle Sauce dùng 164ml trong món "Veggi Noodle"):**

```
Scale = Required Usable Qty / Standard Usable Yield (child)
        (KHÔNG dùng Reference Batch Qty — đó là input trước loss, không phải usable output parent cần)
Expanded Consumption = child QTY_GROSS × Scale
```

Case thật: Veggi Noodle cần 164ml Sauce → `Scale = 164/1600 = 0.1025` → nhân vào từng dòng recipe Sauce (Water 800×0.1025, Soy Sauce 400×0.1025...). Verify tự nhất quán: tổng `QTY_GROSS` của recipe (≈1646) khớp `Reference Batch Qty` (1640) — xác nhận `QTY_GROSS` viết theo Input Basis, `Standard Usable Yield` là Output Basis, 2 basis khác nhau và công thức trên xử lý đúng.

**6 case thật đã test, đủ đa dạng để đóng kiến trúc:**

- Veggi Noodle Sauce (INLINE, mixed RAW + Syrup PREP/STANDALONE bên trong) → explode, dừng đúng tại Syrup.
- Mushroom Stroganoff Sauce (STANDALONE) → consume trực tiếp, STOP, không nổ Cashew Cream Cheese/onion/mushroom bên trong.
- Pumpkin Cream Soup Base (STANDALONE) → consume, STOP.
- "No Beef" Burger (Final, mixed RAW + PREP STANDALONE + PREP cần check) → Resolver đánh giá từng child độc lập, không gộp cả món theo 1 hướng.
- Momo Dumplings (Frozen Momo = SEMI đã log) → dừng ở SEMI, không nổ tiếp xuống công thức làm Momo.
- Opera Cake (Whole Cake tồn kho thật) → dừng ngay ở bước đầu, không đọc BOM nào — Production Compiler đã consume RAW từ lúc sinh ra Whole Cake.

**⚠️ Nuance chưa test — 🟡 pending Reality verification, không phải đã xác nhận:** "SEMI luôn Materialized/terminal" hiện có cơ sở business rule hợp lý (SEMI được Workshop sản xuất → transfer về branch → tồn tại như inventory object) — nhưng **chưa có 1 SEMI cụ thể được trace end-to-end** qua `SEMI_PRODUCT_MASTER → PRODUCTION_LOG → PRODUCTION_COMPILER → INVENTORY_LEDGER (YIELD) → TRANSFER → STOCK_POSITION tại branch → SELL/WASTE consume` để xác nhận thật. Khác các nhánh khác trong Resolver (case Pancake Batter/Base đã hỏi Reality trực tiếp và có câu trả lời cụ thể).

**Bước xác minh đề xuất, chưa làm:** chọn 1 SEMI thật (ví dụ `SEM-MOM-FRO-001` Frozen Momo) trace xuyên suốt chuỗi trên. Nếu có YIELD và tồn kho thật tại branch → nâng 🟡 thành ✅. Không chặn build Resolver ngay bây giờ — chỉ ghi lại để không tự nâng độ tin cậy vượt quá bằng chứng đang có (đúng loại lỗi vừa bị bắt ở chính GPT lượt trước, không lặp lại — xem [[GPT (khung chat này) — 2026-07-23]]).

**⚠️ Phụ thuộc thật (nối [[Discovery — Hierarchy of Prevention]], đang Open ở Checkpoint chính):** độ chính xác của Resolver phụ thuộc `PREP_LOG` được ghi đầy đủ cho mọi PREP STANDALONE. Nếu 1 PREP đánh dấu STANDALONE nhưng SOP ghi log chưa tuân thủ (case Đậu hũ ép), Resolver dừng đúng logic nhưng dừng ở tồn kho sai/thiếu — không phải lỗi Resolver, là lỗi Reality chưa khớp giả định.

**Kết nối Discovery khác:** traversal đệ quy không giới hạn tầng (INLINE→INLINE→PREP) là ví dụ cụ thể nhất cho [[Discovery — Boundary Formula vs Engine]] ([[CHECKPOINT-2026-07-22]] Mục II.6) — đáng chạy Benchmark Reality Test đó trước khi quyết viết Resolver bằng Formula hay Apps Script.

**Cảnh báo kỹ thuật khi build:** không vá `PREP_COMPILER` hiện tại (formula L1) bằng cách thêm IF — bản chất thuật toán đổi từ "explode 1 tầng" sang "traversal đồ thị đệ quy", vá sẽ vỡ lại khi gặp INLINE→INLINE→PREP. Build Resolver riêng từ đầu theo traversal, rồi mới gắn vào cả SELL_COMPILER lẫn WASTE_COMPILER — không viết 2 logic riêng.

**Kết luận:** SELL_COMPILER và WASTE_COMPILER không sở hữu 2 logic explode riêng — chỉ khác lý do Business Event (`Event Type = SALE` vs `WASTE`), dùng chung 1 Resolver.

**✅ Decision cuối (2026-07-25, Reality xác nhận) — đóng câu hỏi Tiramisu/Finishing:** Cost thật của Finishing trên Materialized FINAL rất thấp (Tiramisu: 15-25g dâu tây, 1-2g bột cacao, 1 hạt coffee bean) — không đáng để bắt operator phân biệt "đã Finishing/chưa Finishing" mỗi lần Waste. Chi phí thao tác thêm (thêm 1 trạng thái phải nhập cho mỗi Waste event) lớn hơn giá trị accuracy thu được. **Trade-off có chủ đích: Accuracy đủ dùng > Complexity không đáng giá.**

**Rule cuối cho Materialized FINAL:**

```
FINAL
├─ Có trong FINAL_ASSEMBLY_DETAIL → MATERIALIZED
│    → DIRECT Base Inventory → STOP
│    → IGNORE Supplemental Finishing (dù Waste xảy ra trước hay sau plating)
│
└─ Không có trong FINAL_ASSEMBLY_DETAIL → NON-MATERIALIZED
     → Read FINAL_FINISHING_DETAIL → EXPLODE → RECURSE
```

Không cần `Process Stage` làm trigger (đã xét và loại — mô tả bối cảnh vận hành, không mô tả trạng thái món, dễ false positive: "Service" bao gồm cả chưa decor lẫn đã plating xong). Không cần field `Finishing Applied?` mới. Không cần nhánh supplemental finishing riêng.

**Lưu ý phạm vi:** Finishing không biến mất khỏi ERP — `FINAL_FINISHING_DETAIL` vẫn dùng cho recipe/cost, và Sales Consumption (khi build) vẫn có thể consume Finishing theo chuẩn bán hàng thật. Quyết định này **chỉ áp dụng cho Waste** của Materialized FINAL — chấp nhận variance nhỏ để bảo vệ operator workflow, không ảnh hưởng Cost Engine hay Sales Engine tương lai.

**Bước tiếp theo trước khi code thật:** test thêm bằng chính 6 case ở Mục này để verify traversal dừng đúng boundary và scale đúng, sau đó mới viết Resolver.

## 8. Unit Dropdown Engine — spec chi tiết (2026-07-25)

**Input tối giản `WASTE_LOG` đã khóa (7 field nghiệp vụ, Item Code là derived từ Item):**

```
Date | Item | Item Code (auto) | Waste Qty | Unit (dynamic dropdown) | Reason | Staff | Branch
```

Giữ nguyên tên cột thật đã có (`Reason`, không đổi tên). Các cột còn lại của `WASTE_LOG` 12 cột (`Process Stage`, `Evidence`, `Investigation Flag`, `Loss Type`) giữ nguyên cho mục đích điều tra, **không** tham gia Reader/Resolver ở phase đầu.

**Flow nhập liệu:** `Date → Item → Item Code (auto) → Unit dropdown (mở sau khi có Item Code) → Waste Qty → Reason → Staff → Branch`.

**Quy tắc Unit theo Domain (bản đầu):**

| Domain | Nguồn | Allowed Report Unit |
|---|---|---|
| RAW | `ALL_ITEM` | chỉ System Unit |
| PREP STANDALONE | `PREP_MASTER` | System Unit + "1 Batch (X)" nếu có Business Rule — **X = Standard Usable Yield, KHÔNG phải Reference Batch Qty** (đúng công thức Mục 7; ví dụ Mushroom Stroganoff Sauce: Batch = 2300g, không phải 2410g input) |
| PREP INLINE | `PREP_MASTER` | 🟡 xem correction dưới — không cấm tuyệt đối |
| SEMI | `SEMI_PRODUCT_MASTER` | System Unit; chỉ thêm business conversion khi Master có rule thật, không tự bịa |
| FINAL | `FINAL_PRODUCT_MASTER` | 2 tầng: Batch/Portion UOM + Portion Size (nếu khác 1) |

**Hiển thị:** Business Language kèm quy đổi trong ngoặc (`"1 Serving (6 pcs)"`), không hiện Unit trần khi dễ nhầm. Quy tắc chống duplicate: chỉ thêm 1 lựa chọn khi nó mang ý nghĩa khác — không tạo `"1 Serving (1 pcs)"` hay `"1 Batch (1000g)"` nếu Portion Size/Batch trùng với System Unit đã có (case Smoothie, case Veggi Noodle Portion Size=1).

**✅ Reality Verified (2026-07-25) — PREP INLINE selectable trong Waste, không bị ẩn theo Execution Type:** Xác nhận bằng case thật — Tomato Salsa, Mango Salsa, Mashed Avocado: chuẩn bị vật lý trước service, dùng dần trong ngày, không carry-over, hết shelf-life cuối ngày thì phần dư → Waste thật. **Nguyên lý chốt:** *"Non-materialized trong Inventory ≠ không tồn tại vật lý trong Kitchen."* INLINE chỉ nói nó không có vòng đời inventory độc lập qua PREP_LOG/Ledger — không nói staff không thể nhìn thấy, cân, hoặc waste nó.

**Bảng Domain đã cập nhật (PREP STANDALONE và INLINE giờ cùng hàng về Allowed Unit):**

| Domain | Allowed Unit |
|---|---|
| RAW | System Unit |
| PREP STANDALONE | System Unit + Batch nếu Business Rule có ý nghĩa |
| PREP INLINE | System Unit + Batch nếu Business Rule có ý nghĩa (giống STANDALONE về mặt UI) |
| SEMI | System Unit + conversion đã được Master định nghĩa |
| FINAL | Portion/pcs/Batch UOM + Portion Size theo Business Rule |

**Hệ quả cho Resolver (không cần nhánh mới, dùng đúng Consumption Resolver đã có ở Mục 5/7):** khi staff báo trực tiếp "Mango Salsa, Waste Qty = 200g", **không thể** trừ thẳng `-200g Mango Salsa` khỏi Ledger vì INLINE không có inventory balance. Resolver nhận Business Object 200g → normalize theo Standard Usable Yield → explode recipe → trừ đúng các Inventory Object nằm dưới (giống hệt cách Veggi Noodle Sauce được explode khi là component của Final, chỉ khác điểm vào là trực tiếp từ WASTE_LOG thay vì qua Final BOM).

**Còn treo (UX, không phải Architecture — không chặn build):** PREP INLINE có nên mặc định hiện thêm "1 Batch" ngoài System Unit hay chỉ hiện khi staff thực tế nhận diện theo batch? Cùng câu hỏi UX đã ghi cho PREP STANDALONE ở trên — gộp chung, quyết 1 lần.

**Ma trận ví dụ đã thống nhất:**

| Object | Domain | Dropdown |
|---|---|---|
| Coconut Milk | RAW | `g` |
| Fermented Cashew Cream Cheese | PREP STANDALONE | `g`, `1 Batch (1000g)` nếu cần |
| Veggi Noodle Sauce | PREP INLINE | ✅ `g`/`ml` (System Unit), `1 Batch` nếu cần — selectable, không ẩn |
| Frozen Momo | SEMI | `pcs` |
| Momo Dumplings | FINAL (Portion Size=6) | `pcs`, `1 Serving (6 pcs)` |
| Opera Cake | FINAL (Batch≠Portion) | `WHOLE CAKE`, `pcs` |
| Veggi Noodle | FINAL (Portion Size=1) | `plate` (không duplicate) |

**✅ Đã đóng (2026-07-25) — `Batch` có Consumer thật, expose ngay từ build đầu, không cần đợi thêm Reality Test:** Case thật — Roasted Veggie cháy nguyên mẻ, không Recovery được. Ép staff cân lại từng gram khi cả mẻ đã cháy vừa thừa thao tác vừa đi ngược Business Rule đã có. `Batch` phục vụ đúng sự cố loại này (whole-batch loss), không phải thao tác thường xuyên — nhưng khi xảy ra thì bắt buộc cần, không thể thay bằng System Unit.

**Quyết định cuối cho PREP (STANDALONE và INLINE giống nhau):** expose cả `System Unit` + `"1 Batch (Standard Usable Yield)"` khi Master có Business Rule batch/yield hợp lệ — dùng đúng `Standard Usable Yield` làm giá trị hiển thị (nhất quán với công thức Scaling đã khóa ở Mục 7, không dùng `Reference Batch Qty`). Ví dụ Roasted Veggie: `g` / `1 Batch (1580g)`. Compiler normalize cả 2 lựa chọn về cùng 1 quantity trước khi vào Resolver — staff mất 300g chọn "300g", cháy nguyên mẻ chọn "1 Batch", không có nhánh xử lý riêng.

**Điểm ngữ nghĩa quan trọng:** `Batch` là Business Report Unit cho exceptional whole-batch loss — không phải System Unit, và không phải dấu hiệu Materialization (không liên quan gì tới việc PREP có tồn kho Ledger hay không, chỉ là 1 lựa chọn hiển thị trong Waste Log).

**Build đầu (đã chốt, sẵn sàng handoff):**

```
RAW    → System Unit
PREP   → System Unit + "1 Batch (Standard Usable Yield)" nếu Master có rule
SEMI   → System Unit + conversion đã có thật (không tự bịa thêm)
FINAL  → Business Unit theo Final Master + Portion Size khi > 1 + Batch/Portion conversion khi có thật
```

**⚠️ Cập nhật độ chính xác trạng thái (2026-07-25, sau smoke-test thật của Gemini + review của GPT):** Gemini test case `Mushroom Stroganoff Sauce` (PREP) và tuyên bố *"Freeze toàn bộ Unit Engine"* — **overclaim, đã bị GPT bắt lại**. Bằng chứng thật chỉ xác nhận đúng **domain PREP**:

- ✅ **Unit Normalizer PREP — PASS:** `Waste Qty=1 + "1 Batch"` → đúng `2300g` (Standard Usable Yield), **không lấy** `2410g` (Reference Batch Qty) — tuân đúng công thức đã Freeze ở Mục 7.
- ✅ **Unit Dropdown PREP — PASS:** hiển thị `g | 1 Batch` đúng business language.
- ✅ **Operator/Technical Separation — PASS:** `WASTE_LOG` chỉ giữ tầng operator-facing (`Reason | Process Stage | Staff | Branch`); tầng tính toán (`Conversion Basis | Normalized Qty | Normalized UOM`) tách sang sheet riêng `TECH_UNIT_DROPDOWN` — đúng nguyên tắc Protect Operator, không trộn 2 tầng.
- 🟡 **RAW, SEMI, FINAL — chưa test, KHÔNG được coi là Frozen theo suy diễn từ case PREP.**

**Smoke-test còn thiếu trước khi Freeze toàn Unit Engine (3 case, không cần test hàng loạt):**

| Test | Expected |
|---|---|
| Coconut Milk (RAW) | chỉ `g` |
| 1 SEMI thật | System Unit + conversion chỉ nếu `SEMI_PRODUCT_MASTER` có định nghĩa |
| Opera/Tiramisu (FINAL) | Portion/Whole Cake/Batch đúng theo Final Master |

**Trạng thái chính xác:** Unit Dropdown Engine **KHÔNG** ở trạng thái "Frozen toàn bộ, sẵn sàng implement" như từng ghi trước đó trong Checkpoint — chỉ **domain PREP đã Verified bằng test thật**. 3 domain còn lại (RAW/SEMI/FINAL) đúng về mặt spec/thiết kế nhưng chưa qua Reality Test cụ thể. Chưa nhảy sang Supplemental Finishing Loss (Mục 7) cho tới khi 3 smoke-test này xong — ưu tiên đóng nốt Unit Engine trước.

## 8.5 Normalizer — Contract D/E cho Virtual Unit (2026-07-26)

**Nguyên tắc:** `"1 Serving"`/`"1 Batch"` không phải data mới trong Master — là **derived semantic**, suy ra từ field đã có sẵn (`System Unit`, `Portion Size`, `Portion UOM`, `Standard Usable Yield`). Single Source of Truth không nghĩa là mọi giá trị hiển thị phải là field riêng — nghĩa là mọi giá trị suy ra phải có nguồn và rule xác định duy nhất.

**⚠️ Sửa 1 heuristic sai đã từng dùng:** không dùng `"Batch UOM blank → tạo 1 Serving"` — blank không phải bằng chứng có quan hệ Serving, chỉ là thiếu dữ liệu.

**Contract D/E đã khóa (`Unit 1 = System Unit` luôn cố định, `Unit 2` suy theo domain):**

```
PREP:
  IF Standard Usable Yield > 0 AND System Unit valid
  → Unit 2 = "1 Batch", Basis = Standard Usable Yield

FINAL — relationship A (Batch-based, ví dụ Opera):
  IF System Unit = Batch UOM AND Portion UOM valid
     AND Portion UOM ≠ System Unit AND Yield Qty > 0
  → Unit 2 = Portion UOM, Basis = 1/Yield Qty

FINAL — relationship B (Portion-based, ví dụ Momo):
  IF System Unit = Portion UOM AND Portion Size > 0 AND Portion Size ≠ 1
  → Unit 2 = "1 Serving", Basis = Portion Size

RAW / SEMI:
  Unit 2 = blank, Basis = 1
```

**✅ Fail-closed khi Ambiguous — không được âm thầm chọn 1 quan hệ:** nếu 1 FINAL thỏa cả relationship A và B cùng lúc (hoặc nhiều quan hệ hợp lệ khác), **không** tự chọn — trả `AMBIGUOUS_CONVERSION`. Đúng tinh thần "Compiler Never Silences Reality" ([[ADR-016 Compiler Never Silences Reality]]) áp dụng cho tầng Normalizer.

```
0 relationship hợp lệ → Unit 2 blank
1 relationship hợp lệ → dùng relationship đó
>1 relationship hợp lệ → AMBIGUOUS_CONVERSION (không đoán)
```

Nếu sau này thực tế cần 3-4 cách báo Waste cho 1 item, kiến trúc đúng là 1 bảng Unit Conversion Registry nhiều dòng, không nhét thêm Unit 3/Unit 4 vào TECH — **chưa cần build bây giờ**.

**Invariant cuối, đây mới là thứ cần Freeze:** *"Conversion Basis luôn mang nghĩa: Qty System Unit / 1 Alternate Unit."* Giữ đúng invariant này thì Normalizer không cần biết RAW/PREP/FINAL hay Opera/Momo là gì — chỉ làm:

```
Selected = Unit 1 → Normalized Qty = Waste Qty
Selected = Unit 2 → Normalized Qty = Waste Qty × Basis
Normalized UOM = Unit 1 (luôn luôn — Virtual Unit KHÔNG BAO GIỜ xuống Ledger)
```

**Verify nhanh 2 case đã biết, không phá gì đã Freeze:**

- Momo: `System Unit=pcs=Portion UOM`, `Portion Size=6>1` → relationship B đúng → `"1 Serving"=6pcs`. Khớp Mục 8.
- Opera: `System Unit=WHOLE CAKE=Batch UOM`, `Portion UOM=pcs≠System Unit`, `Yield=8` → relationship A đúng → `Unit 2=pcs, Basis=1/8`. Khớp Mục 8.

**Kế hoạch build:** viết C/D/E trước (logic Normalizer), giới hạn range `2:500` để test nhanh, test bằng Opera + Momo + Stroganoff + 1 RAW + 1 FINAL cấu hình lỗi (để test nhánh Ambiguous/blank) — **chưa đụng phần H** (render/output) cho tới khi C/D/E test xong.

**✅ TECH V2 — Normalizer trưởng thành thành Strategy-based (2026-07-28/29, relay qua Thanh):** Sau khi [[ADR-021 Active View Boundary]] Freeze, Normalizer được thiết kế lại thành hàm thuần túy `Normalize(EventID, ItemCode, Qty, SelectedUnit) → 7 output` (Domain/Source Unit/Target Unit/Master Basis/Applied Basis/Normalized Qty/Normalized UOM), tách rõ 3 lớp: Contract → Acceptance Test → Implementation.

**Phân biệt quan trọng:** `Master Conversion Basis` (hệ số từ Master Data) ≠ `Applied Conversion Basis` (hệ số Resolver thực sự dùng sau khi đối chiếu Selected Unit) — với case Stroganoff Qty=0.5, `Applied Basis` vẫn là `2300` (không phải `1150`), công thức `Normalized Qty = Waste Qty × Applied Basis` mới ra `1150`. Không nhầm hệ số quy đổi với kết quả tính.

**⚠️ Correction quan trọng — Domain ≠ Strategy:** thiết kế ban đầu route Strategy theo Domain (`IF Domain=PREP → LINEAR`, `IF Domain=FINAL → ...`) đã bị bác bỏ bằng phản ví dụ: RAW (Milk 1L→1000ml) cũng LINEAR giống PREP; FINAL có thể là DISCRETE (Whole Cake→pcs) hoặc IDENTITY (Sauce g→g) tùy sản phẩm cụ thể. Domain không dự đoán được Strategy.

**Kiến trúc đúng — 4 bước độc lập, Strategy route theo Conversion Context, không theo Domain:**

```
1. Resolve Metadata           — Domain, Target Unit, Yield, Serving Size (Domain chỉ dùng để chọn bảng Master)
2. Resolve Conversion Context — Source Unit + Target Unit + Master Metadata
3. Select Strategy            — IDENTITY (Selected=Target) / LINEAR (Batch→g, Serving→pcs) / DISCRETE (Whole Cake→pcs, dành cho tương lai)
4. Execute Strategy           — Qty × Applied Basis (theo đúng Strategy đã chọn)
```

Lợi ích: khi có đơn vị mới (Pack/Tray/Bottle/Slice/Cup...), chỉ cần thêm vào bước Resolve Context, không sửa cây quyết định theo Domain — đúng Open/Closed Principle.

**Ranh giới Input/Output giữ nguyên theo [[ADR-021 Active View Boundary]]:** TECH không tự HSTACK Input — Input đến từ `ACTIVE_WASTE_EVENTS` (1 spill duy nhất, cột A:D, read-only). Normalizer chỉ bắt đầu từ cột E trở đi (Output). TECH V1 chỉ dùng làm nguồn dữ liệu tham khảo (hằng số, Master table nào dùng ở đâu) — **không** mang theo cấu trúc công thức/thuật toán cũ sang V2.

**Trạng thái:** Contract + Acceptance Test đã Frozen, kiến trúc Strategy-based đã APPROVE ~90% (chờ áp đúng Resolve Context thay vì Domain-routing trước khi gọi `sheets_executor`).

**⚠️ Regression phát hiện khi build `ITEM_METADATA` (TECH V2) — không phải "bug mới trong spec", mà là đánh mất lời giải đã Frozen ở trên (2026-07-29):**

Khi Implementation build `ITEM_METADATA` (schema: `Item Code | Domain | Target Unit | Master Basis` — chỉ 1 cặp Target/Basis mỗi Item Code), test Opera (`1 pcs → 0.125 WHOLE_CAKE`) FAIL, và được mô tả như *"phát hiện bug trong spec"*. **Thực ra không phải bug mới** — đây chính xác là bài toán Relationship A đã giải ở trên:

```
FINAL relationship A (Opera): System Unit=WHOLE CAKE=Batch UOM, Portion UOM=pcs≠System Unit, Yield=8
→ Unit 2 = pcs, Basis = 1/8
```

`ITEM_METADATA` với chỉ 1 cặp `Target Unit + Master Basis` tĩnh/item **không đủ khả năng biểu diễn** quan hệ 2 tầng mà Opera cần (WHOLE_CAKE khi chọn theo Batch, pcs khi chọn theo Portion) — nên dữ liệu bị trộn sai (`Target Unit=pcs, Master Basis=Whole Cake` — text lẫn vào cột số).

**Hướng sửa đúng — không để Implementation tự dò lại từ đầu:** đừng bắt Gemini tự suy ra rule mapping mới từ việc đọc cột `FINAL_PRODUCT_MASTER` — trỏ thẳng về Relationship A/B đã Frozen ở trên. `ITEM_METADATA`/bước `Resolve Conversion Context` cần giữ được khả năng biểu diễn **2 quan hệ** cho FINAL loại Batch-based (không chỉ 1 cặp Target/Basis tĩnh) — ví dụ: lưu riêng cả `Batch UOM` lẫn `Portion UOM + Yield Qty`, để bước Resolve Context chọn đúng cặp theo Selected Unit, đúng cách đã thiết kế.

**Trạng thái hiện tại — đang BLOCKED đúng chỗ, chưa nên nối B/D/E vào TECH:** `RAW`/`PREP` Contract cơ bản PASS (sau khi sửa Domain enum, Master Basis blank). `FINAL` Contract FAIL — cần chốt lại mapping cho từng profile sản phẩm (Batch-based như Opera, Portion-based như Momo, gram-based như Date Truffle) trước khi viết tiếp Strategy/Execution. Đã yêu cầu đúng: dừng, báo cáo cấu trúc cột thật của `FINAL_PRODUCT_MASTER` (Portion Qty/UOM, Yield Qty/UOM, Batch Qty/UOM, Inventory Unit) cho 3 nhóm sản phẩm khác nhau trước khi tự chọn mapping.

**✅ `UNIT_DICTIONARY` — Master Data mới xuất hiện, 3 tầng rõ ràng (2026-07-29):**

```
Unit Code (định danh bản ghi) → Canonical Unit (enum nghiệp vụ, VD: G/BATCH/PCS/WHOLE_CAKE) → Display Unit (nhãn hiển thị)
```

Lookup chuyển từ VLOOKUP sang XLOOKUP (không phụ thuộc vị trí cột, thêm cột không gãy công thức). `WHOLE_CAKE` đã tách khỏi `PCS` — khớp đúng Acceptance Test đã Freeze ở trên.

**🟡 Chưa chốt dứt điểm, chấp nhận tạm cho phạm vi Waste:** `plate`/`bowl` ban đầu map thẳng thành `PCS` — sai, vì đây là **Container** (vật chứa), không phải đơn vị đếm. Tinh chỉnh tiếp: tách `PORTION` (business/serving concept) khỏi `CONTAINER` (plate/bowl vật lý) — vì 1 Portion có thể phục vụ trong nhiều loại container khác nhau. Chấp nhận tạm thời cho phạm vi Waste hiện tại; cần xét lại nghiêm túc nếu `UNIT_DICTIONARY` mở rộng thành Master dùng chung toàn ERP (không chỉ riêng TECH_UNIT_DROPDOWN).

**✅ Strategy quay lại Diagnostic Output** (từng bị rớt 1 vòng, đã khôi phục) — không phục vụ tính toán, phục vụ Explainability: nhìn cột Strategy là biết Router đã định tuyến đúng Domain/Context hay chưa khi debug.

**✅ Header đổi tên khớp Contract đã thống nhất:** `Unit 1/Unit 2` → `Source Unit/Target Unit`; `Conversion Basis/Final Conversion Basis` → `Master Basis/Applied Basis` (khớp đúng thuật ngữ đã Freeze ở phần đầu Mục 8.5).

**✅ Tuyên bố đóng băng thiết kế, chuyển trọng tâm sang verification (2026-07-29):** Từ đây không thêm cột nếu chưa có ADR mới, không đổi tên cột vì sở thích, không sửa `UNIT_DICTIONARY` nếu không ảnh hưởng Contract. Trọng tâm chuyển sang: hoàn thiện công thức Normalizer → chạy toàn bộ Acceptance Test → kiểm thử edge case (UNKNOWN/IDENTITY/LINEAR/DISCRETE) → chỉ sửa kiến trúc nếu có test FAIL, không tự tinh chỉnh thêm.

## Bug Queue — giao Gemini xử lý, KHÔNG chặn Resolver Architecture

0. 🟡 **[TIẾN TRIỂN LỚN, CHƯA FREEZE] `WASTE_COMPILER` — Hotfix V2 đã sửa đúng 2 bug critical, còn 2 câu hỏi trước khi Freeze (2026-07-26, qua nhiều vòng audit thật):**

   **✅ Đã PASS, xác nhận bằng output thật (không phải lời Gemini báo):**
   - `PREP-SAU-STR-001, 1 Batch → -2300g`, `0.5 Batch → -1150g` — Normalizer PASS.
   - Zero-row guard: các dòng `Qty=0` đã biến mất khỏi output, không chảy xuống Staging/Ledger. PASS.
   - **Momo (Bug A đã sửa):** `FIN-SNA-MOM-001, Waste 6 pcs` → đúng Scale Factor 1 (6 pcs ÷ 6 pcs/serving = 1) → `SEM-MOM-FRO-001 -6pcs, Spice Mayo -20g, Soy Sauce -10ml, Black Sesame -1g, Cilantro Washed -1g`. Bug ×6 cũ (do dùng Normalized Qty làm BOM multiplier trực tiếp, sai với Business Scale Factor) đã hết.
   - **Opera routing (Bug B đã sửa):** `FINAL-CKE-OPE-001` giờ ra **đúng 1 dòng terminal**, không còn explode crust/filling/ganache. Xác nhận qua **2 event độc lập** (DN-WST-007: -1; WS-WST-011: -8) — cùng hành vi nhất quán, không phải trùng hợp 1 lần. `FINAL_ASSEMBLY_DETAIL` presence giờ đúng vai trò Materialization Signal (DIRECT+STOP), không còn bị hiểu nhầm thành BOM để explode.

   **🔴 Opera Canonical UOM — vẫn FAIL qua 2 vòng sửa, chẩn đoán vị trí bug đã thay đổi (2026-07-26):**
   - **Vòng 1:** Authoritative data xác nhận `FINAL-CKE-OPE-001` — System Unit = **WHOLE CAKE**, Stock Position Unit = **WHOLE CAKE**, Yield = 8 pcs/Whole Cake. Output `-1 pcs`/`-8 pcs` sai thật, phải là `-0.125`/`-1 WHOLE CAKE`. Yêu cầu sửa: DIRECT terminal contract phải dùng Normalized Qty/UOM, không phải Report Qty/Unit — áp dụng chung, không đặc cách riêng Opera.
   - **Vòng 2 (sau khi `WASTE_COMPILER` đã sửa để đọc từ `TECH_UNIT_DROPDOWN`):** Output **vẫn không đổi** — `DN-WST-260722-007` và `WS-WST-260722-011` vẫn ra `-1 pcs`/`-8 pcs`. Vì `WASTE_COMPILER` giờ đã đọc đúng cột Normalizer (xác nhận qua code), bug **không còn ở `WASTE_COMPILER`** — chẩn đoán mới: **tầng Normalizer/`TECH_UNIT_DROPDOWN` chưa từng tính phép quy đổi Portion→Batch cho domain FINAL** (có vẻ chỉ build/test cho PREP Batch→Yield). Việc cần làm: Claude Code kiểm tra `TECH_UNIT_DROPDOWN`, không sửa lại `WASTE_COMPILER` nữa.

   **Test lại sau khi sửa đúng chỗ (Normalizer, không phải Compiler):**
   ```
   Event 007: Opera 1 pcs → FINAL-CKE-OPE-001 | -0.125 | WHOLE CAKE
   Event 011: Opera 8 pcs → FINAL-CKE-OPE-001 | -1     | WHOLE CAKE
   ```
   Momo không cần test lại — đã PASS Scale Factor/Explosion.

   **Còn lại sau khi Opera PASS:** đúng 1 gate kiến trúc lớn cuối — Deep Recursion INLINE→INLINE→Terminal, chưa có bằng chứng thật. Sau đó mới đủ điều kiện Freeze Consumption Resolver hoàn toàn.

   **✅ Event ID Immutable Risk — đã ghi nhận minh bạch, không còn ẩn:** GPT xác nhận `ROW()`-based ID sẽ lệch khi Insert/Delete — chấp nhận là Technical Debt có chủ đích, đánh dấu rõ `[TEMPORARY_ID_PENDING_SNAPSHOT]` để không ai nhầm là ID bất biến thật. Chưa giải quyết triệt để (cần Snapshot Script hoặc UUID tĩnh), nhưng rủi ro giờ được document rõ, không âm thầm vi phạm Rule Immutable như trước.

   **🔴 Bug 5 (UOM terminal phải là System Unit) — xác nhận CÒN, qua output thật:** `PREP-BAS-OCP-001` khi là **base_code gốc** (waste trực tiếp, event `DN-WST-260722-003`) → đúng `-1, g`. Nhưng cùng mã đó khi đạt được **qua explosion** (làm ingredient của Final khác, event `HA-WST-260722-004-CONS-1`) → sai `-1, portion` — giữ nguyên UOM từ dòng recipe, không tra lại System Unit từ `ALL_ITEM`. Bug chỉ xảy ra ở nhánh explosion, không phải nhánh base_code gốc.

   **✅ Bug 4 (Domain qua ALL_ITEM, không prefix) — xác nhận đã sửa qua đọc code:** `VLOOKUP` thay `LEFT(code,4)`.

   **Trạng thái:** Không Freeze toàn Resolver. Đừng để Gemini tự tuyên bố "implemented" — chỉ audit qua output thật.

   **🔴 Regression phát hiện ở vòng sau (2026-07-26) — STOP đúng lúc, không vá tạm:** Sau khi sửa Location/UOM lookup, Opera **quay lại sai** (`-8 pcs` thay vì `-1 WHOLE CAKE`) — tệ hơn vòng trước vì đây là regression, không phải bug cũ còn sót. **Root cause đã trace:** code hard-code vị trí cột (`INDEX(raw_log;r;14)` lấy Qty, **bỏ quên cột 15 UOM**), làm đứt cặp Qty-UOM ngay từ `initial_bom`, rồi bù lại bằng cách VLOOKUP System Unit ở **cuối** cho mọi dòng kể cả DIRECT terminal — vi phạm đúng nguyên tắc "không tính lại UOM ở cuối cho node DIRECT". Lệnh đúng khi phát hiện: **STOP, không vá bằng exception (không chia `/8` riêng cho Opera)** — bắt trace nguyên nhân gốc trước.

   **Refinement quan trọng trước khi cho sửa tiếp:**
   - Không hard-code vị trí cột (`14`/`15`) — chính kiểu lookup này gây lệch dữ liệu. Phải resolve theo header/mapping cố định (`Normalized Qty | Normalized UOM | Conversion Basis`), và đảm bảo dòng `TECH_UNIT_DROPDOWN` join đúng theo cùng Waste Event, không chỉ dựa row number (dễ lệch nếu có sort/filter khác nhau giữa 2 sheet).
   - **Không nhầm Canonical UOM với Scale Factor/Conversion Basis** — 2 khái niệm khác nhau. Momo không cần "Canonical UOM = serving-equivalent" (dễ gây nhầm lẫn) — chỉ cần Normalizer cung cấp đủ dữ liệu (`6 pcs / Portion Size 6`) để Resolver tự tính BOM multiplier = 1, không đổi UOM thành "serving".

   **Contract cuối, khóa trước khi cho Implementation sửa:**

   ```
   DIRECT terminal (RAW/SEMI/PREP STANDALONE báo trực tiếp/Materialized FINAL)
     → giữ NGUYÊN Atomic Pair [Normalized Qty, Normalized UOM] từ Normalizer
     → KHÔNG VLOOKUP lại UOM ở bước cuối cho các node này
   EXPLODED child (từ INLINE hoặc Non-materialized FINAL)
     → Qty tính từ BOM Scale Factor (dùng Conversion Basis riêng, không phải Canonical UOM)
     → UOM lấy System Unit của chính child đó từ ALL_ITEM
   ```

   **4 Gate bắt buộc (không sửa exception riêng cho từng món):**

   ```
   Opera 1 pcs        → -0.125 WHOLE CAKE  (DIRECT, giữ Atomic Pair)
   Opera 8 pcs        → -1     WHOLE CAKE  (DIRECT, giữ Atomic Pair)
   Stroganoff 1 Batch → -2300  g            (DIRECT, giữ Atomic Pair — gate mới thêm, xác nhận PREP không bị đụng khi sửa FINAL)
   Momo 6 pcs         → BOM multiplier=1 → Frozen Momo -6pcs, Spice Mayo -20g... (EXPLODE, không đổi UOM thành serving)
   ```

   Nếu cả 4 gate PASS đồng thời, mới chứng minh ranh giới Normalizer→Resolver thật sự sạch.

   **🔴 V5 — review code chi tiết, 6 bug mới, CHƯA sẵn sàng dán vào production A1 (2026-07-26):** Formula V5 đã sửa đúng hướng Atomic Pair + Direct Terminal Contract (kiến trúc ✅), nhưng review dòng-theo-dòng phát hiện 6 lỗi implementation, 2 trong đó nguy hiểm nhất vì thuộc loại "chạy đẹp, ra số, nhưng sai âm thầm":

   - 🔴 **PREP_MASTER mapping tự mâu thuẫn:** khai báo range `B2:M1000` (12 cột) nhưng comment ghi *"M=Exec Type(12)"* trong khi Execution Type thật nằm ở cột `AG` (đã xác nhận từ trước) — range B:M không thể với tới AG. Nếu không sửa, mọi lookup Execution Type trả `UNKNOWN`, khiến toàn bộ PREP bị route sai (STANDALONE/INLINE lẫn lộn).
   - 🔴 **Atomic Pair join theo vị trí dòng, không phải key — nguy hiểm nhất:** `norm_qtys`/`norm_uoms` lấy qua `FILTER` song song theo giả định "dòng N của `WASTE_LOG` = dòng N của `TECH_UNIT_DROPDOWN`". Nếu 2 sheet lệch dòng vì bất kỳ lý do gì (sort, filter, thiếu dòng), **Normalized Pair của Event A sẽ gắn nhầm vào Event B** — sai âm thầm, sheet vẫn chạy ra số bình thường. Cần join bằng key thật (Source Row hoặc Event ID), không dựa vị trí.
   - 🔴 **`FILTER()` không tìm thấy trả `#N/A` trực tiếp**, không chắc được `ISNA()` bắt sạch xuyên suốt chuỗi LET/MAP — nên bọc `IFERROR` trả về sentinel rõ ràng (`"NOT_FOUND"`) thay vì tin vào lan truyền lỗi ngầm định.
   - 🔴 **Event ID dùng nguyên tên chi nhánh** (`"Da Nang"`) thay vì prefix đã chuẩn hóa (`DN`) — vỡ convention `DN-WST-...` đã dùng xuyên suốt, và làm sai luôn Location (`"Da Nang_FREEZER"` thay vì `"DN_FREEZER"`). Cần `SWITCH` chuẩn hóa branch ngay từ đầu ingestion.
   - 🟠 **Transaction sequence dùng row toàn bảng** (`SEQUENCE(ROWS(valid_bom))`) thay vì đếm riêng theo từng Event — vỡ contract `-CONS-1, -CONS-2...` tính từ đầu mỗi Event, không phải toàn cục.
   - 🟠 **Cột Qty trong `UNIVERSAL_RECIPE_DETAIL`/`FINAL_FINISHING_DETAIL` cần đối chiếu lại header thật** — V5 dùng vị trí cột khác bản trước, chưa xác nhận đúng.

   **Điểm đã đúng, giữ lại:** khái niệm Atomic Pair, Direct Terminal Contract, Bounded Traversal, Fail-closed validation (bắt được `ERR_*`, PREP INLINE sót, FINAL non-materialized sót, domain UNKNOWN) — đều đúng hướng, chỉ implementation còn lỗi.

   > **⚠️ Cần Thanh xác nhận (Claude Code):** Bug Staff/Branch lệch cột (`raw_log` cột 9/10) mà tui tìm ra ở phiên bản formula trước đó — **vẫn không thấy nhắc tới trong V5 review lẫn trace V6 dưới đây**, dù trace V6 rất chi tiết (đọc thẳng công thức `TECH_UNIT_DROPDOWN`). Có thể đã bị cấu trúc lại tự nhiên khi đổi sang Atomic Pair, hoặc vẫn còn ẩn vì chưa ai kiểm cụ thể field Staff/Branch trong output. Cần dán nguyên văn formula mới nhất để tui đối chiếu trực tiếp, không suy đoán thêm.

   **🔴 V6 — REGRESSION NGHIÊM TRỌNG, 100% output failed (2026-07-27):** `WASTE_COMPILER!A1` giờ trả `NO_VALID_TRANSACTIONS` — **mọi dòng** bị Fail-Closed từ chối, kể cả Stroganoff/Momo từng PASS ở vòng trước. Tệ hơn mọi vòng debug trước đó.

   **⚠️ Dấu hiệu đáng lo nhất — nghi đảo ngược đúng fix đã yêu cầu ở V5 review:** Gemini tự báo đã *"đổi sang positional row mapping trực tiếp từ `TECH_UNIT_DROPDOWN`, thay vì `XLOOKUP` với fake row keys"*. Đây rất có thể là **quay lại chính rủi ro đã bị cấm** ở review V5 (Atomic Pair join theo vị trí dòng, không phải key thật — flagged là bug nguy hiểm nhất vì sai âm thầm). Nghi vấn: key trước đó có bao giờ hoạt động đúng không, hay từ đầu đã "fake" — nếu vậy, lỗ hổng gốc (thiếu join key thật giữa `WASTE_LOG` và `TECH_UNIT_DROPDOWN`) **chưa từng được giải quyết** qua tất cả các vòng trước, chỉ đổi cách né tránh.

   **✅ Trace hoàn tất, 3 câu hỏi đã trả lời bằng bằng chứng cụ thể (2026-07-27):**

   1. **Normalizer 100% chính xác**, verify đủ 4 dòng thật (Opera, Momo, Stroganoff×2) — khớp đúng Contract D/E (Mục 8.5).
   2. **Fake Key xác nhận bằng chứng cụ thể:** `TECH_UNIT_DROPDOWN` cột A chỉ là `=ARRAYFORMULA(WASTE_LOG!C2:C500)` — copy thẳng Item Code, **không unique**. Bằng chứng: dòng 10 và 11 cùng là `PREP-SAU-STR-001` (Stroganoff, khác Qty) — `XLOOKUP` luôn dừng ở dòng 10 (`2300g`), bỏ qua dòng 11. Silent corruption xác nhận có thật, không còn là giả thuyết.
   3. **Trace `validation_check` tìm ra nguyên nhân thật của `NO_VALID_TRANSACTIONS`:** dòng 13-14 (`Passion Mango`) có `Waste Qty` **để trống**. Công thức tính `("" / portion_size) * child_qty` → lỗi `#VALUE!` → sập toàn bộ `REDUCE` bên ngoài → bị `IFERROR` cuối cùng nuốt silent → trả `NO_VALID_TRANSACTIONS` cho **toàn bộ**, không chỉ riêng dòng lỗi.

   **Kết quả — 4 ADR mới, đã Freeze, giải quyết gọn cả 3 câu hỏi trên:**

   - [[ADR-018 Waste Event ID Format]] — Human-Readable Immutable Event ID (`<Branch Prefix>-WST-<YYMMDD>-<Sequence>`, Apps Script + LockService). Thanh đã bác bỏ đề xuất UUID (mâu thuẫn [[ADR-017 Snapshot ID Format]] Rule 05) — 1 lần tuyên bố "FREEZE" mô tả UUID trước đó bị xác nhận không hợp lệ.
   - [[ADR-019 Pre-Resolver Input Validation Gatekeeper]] — 3 trạng thái EMPTY/VALID/INVALID_INPUT, Fail-isolated per row (giải quyết đúng nguyên nhân V6: 1 dòng lỗi không được sập cả Engine). FROZEN, 11/11 test case.
   - [[ADR-020 Universal Event Lifecycle]] — DRAFT → VALIDATED → IDENTIFIED, chỉ tiêu thụ Event ở State 2.
   - [[ADR-021 Active View Boundary]] — `ACTIVE_WASTE_EVENTS` là Projection thuần, giải quyết đúng Fake Key: TECH đọc Projection 1:1, không Join `WASTE_LOG` nữa — Event ID chuyển vai trò Join Key → **Trace Key**.

   > ⚠️ Ghi chú đánh số: nội dung gốc gọi 4 ADR này là "017/018/019/020" — trùng số với [[ADR-017 Snapshot ID Format]] đã có trong vault (chủ đề khác hoàn toàn: Snapshot ID của Transaction Staging). Đã renumber thành 018-021, xem ghi chú trong từng file ADR. ADR-020/021 chỉ nhận qua bản tóm tắt GPT relay qua Thanh (không chứng kiến trực tiếp như 018/019) — đã ghi rõ mức độ nguồn trong từng file.

   **Không viết lại `WASTE_COMPILER` cho tới khi 2 Anchor xong:** (1) cơ chế sinh Event ID (ADR-018) implement thật, (2) Pre-validation (ADR-019) chặn đúng ở cửa vào, không để lỗi 1 dòng sập cả Engine. Sau đó mới nối lại `WASTE_LOG → Gatekeeper → ACTIVE_WASTE_EVENTS → TECH → Resolver → WASTE_COMPILER`. Bước tiếp theo đã làm: ADR-019 (Gatekeeper) FROZEN trước, vì điều kiện trigger sinh Event ID trong ADR-018 phụ thuộc logic Gatekeeper — verify bằng chính case Passion Mango (`Waste Qty` trống), xác nhận chỉ loại đúng dòng đó, không sập cả bảng.

1. 🟡 **Location mapping — ✅ cập nhật một phần, còn 1 câu chưa test:** Mapping đã đổi đúng hướng `Branch + Base Location` (không còn `Branch + Domain`), dùng `all_item_registry` để resolve — nhưng các ví dụ đã thấy (RAW→DN_RAW, PREP→DN_PREP...) **tình cờ** Base Location trùng Domain, chưa chứng minh được fix vật lý thật. **Test cần làm:** tìm 1 item có Domain=SEMI nhưng Base Location=FREEZER (khác Domain), xem có ra đúng `DN_FREEZER` hay vẫn `DN_SEMI`.
2. **`FINAL_COST` cột "Final Product Name" lệch 89/92 dòng (97%)** — số tiền (Assembly/Finishing/Total Cost) **đúng theo Item Code** (đã verify: tổng 12 dòng nguyên liệu thật của Kind Bowl = khớp chính xác 35.255,24đ hiển thị trong `FINAL_COST`). Chỉ cột Tên bị tra sai/lệch hàng — nghi công thức VLOOKUP/INDEX sai reference trong chính sheet `FINAL_COST`. Không ảnh hưởng Compiler (join theo Code), nhưng đánh lừa người đọc báo cáo (`COST_AUDIT`, quản lý xem giá vốn).
3. **`FIN-APP-DIP-001` (Dips Plate) — lỗi `#VALUE!` thật:** `Assembly Cost=0`, `Finishing Cost=#VALUE!`, `Total Cost=#VALUE!`, `SERVING_YIELD=0`, `Status=#VALUE!`. Bug riêng biệt với bug #1 — công thức tính bị lỗi thật, không phải lệch tên.
4. **`PREP-BAS-OCP-001` (Oat Coconut Pancake Base) — gắn sai `Execution Type`:** đang là INLINE, phải là **STANDALONE** (xác nhận Reality: có PREP_LOG, giữ tồn, carry-over qua ngày). Sửa trong `PREP_MASTER`. Đây là data bug độc lập với Compiler gap (Mục 7) — cả 2 cần sửa cùng lúc: data (Execution Type) + code (Compiler chưa tra Execution Type khi explode).

## Câu hỏi còn treo

1. `inline_yield`/Business Object — về mặt "field nào Compiler đọc cho từng loại" đã rõ hướng (Mục 2), nhưng chưa build thật để kiểm chứng.
2. Dropdown "User chọn Source" — có cần validate chéo (ví dụ chọn "PREP" nhưng gõ mã Item lại là mã RAW) hay tin tưởng người dùng chọn đúng?
3. **Đã đóng một phần** — Nested Scaling (Veggi Noodle Sauce) đã khóa công thức Scaling bằng Reality thật (Mục 7). "SEMI luôn Materialized/terminal" (case Momo) **vẫn là 🟡 pending Reality verification**, chưa trace end-to-end 1 SEMI thật — không tự nhận đã đóng hoàn toàn (xem Mục 7).
4. Consumption Resolver dùng chung cho SELL và WASTE — khi Sales Engine build (chưa mở Mission), nên tái dùng đúng Resolver này, không viết lại logic explode riêng cho SELL_COMPILER.
5. Waste Engine vẫn chưa phải Mission chính thức đang mở — quyết định mở khi nào vẫn thuộc về Thanh (xem [[CHECKPOINT-2026-07-22]] Mục III).
6. ✅ **Đã đóng (2026-07-25)** — Trigger "Finishing đã xảy ra chưa" cho Materialized FINAL: quyết định IGNORE Supplemental Finishing cho Waste (trade-off Accuracy đủ dùng > Complexity), không cần `Process Stage` hay field mới. Xem Decision cuối ở Mục 7.
7. Smoke-test còn thiếu cho Unit Dropdown Engine (Mục 8) — RAW (Coconut Milk), SEMI (1 case thật), FINAL (Opera/Tiramisu). Chỉ PREP đã Verified bằng test thật, 3 domain còn lại chưa được coi là Frozen.
8. `WASTE_COMPILER` giữ **BLOCKED** — 2 Anchor phải xong trước khi mở lại: [[ADR-018 Waste Event ID Format]] (implement thật, chưa chỉ là thiết kế) và [[ADR-019 Pre-Resolver Input Validation Gatekeeper]] (đã FROZEN, 11/11 test, nhưng chưa nối vào `WASTE_COMPILER` thật). Còn 1 gate Deep Recursion INLINE→INLINE→Terminal chưa có bằng chứng thật.
9. V5/V6 review code (Bug Queue mục 0) — root cause `NO_VALID_TRANSACTIONS` đã trace xong (Fake Key + Waste Qty blank không được cô lập lỗi), giải quyết bằng 4 ADR mới (018-021). Chưa test lại toàn bộ pipeline sau khi implement.
10. Location mapping (Bug Queue mục 1) — đã đổi đúng hướng `Branch + Base Location`, nhưng còn 1 test chưa làm: item có Domain≠Base Location (ví dụ SEMI nhưng ở FREEZER) để chứng minh không còn tình cờ trùng Domain.
11. **Cần Thanh xác nhận:** bug Staff/Branch lệch cột tui tìm ra ở phiên bản formula trước — vẫn không thấy nhắc tới trong cả V5 lẫn trace V6 (dù trace V6 đọc thẳng công thức `TECH_UNIT_DROPDOWN` rất chi tiết). Cần dán nguyên văn formula mới nhất để đối chiếu trực tiếp, không suy đoán thêm.
12. Contract D/E cho Normalizer (Mục 8.5 — Unit 2, Ambiguous Fail-closed) mới chỉ là thiết kế đã khóa trên giấy — kế hoạch build/test (Opera + Momo + Stroganoff + 1 RAW + 1 FINAL lỗi) chưa chạy thật.
13. Cả 4 ADR mới (018-021) mới dừng ở thiết kế/Freeze trên giấy — chưa có bằng chứng `WASTE_COMPILER` thật đã chạy qua pipeline `WASTE_LOG → Gatekeeper → ACTIVE_WASTE_EVENTS → TECH → Resolver → Compiler` đầy đủ.
14. TECH V2 Strategy-based Normalizer (Mục 8.5) — `RAW`/`PREP` Contract PASS, nhưng **`FINAL` Contract đang FAIL** (`ITEM_METADATA` chỉ lưu 1 cặp Target/Basis, không đủ biểu diễn quan hệ 2 tầng của Opera). Đang chờ báo cáo cấu trúc cột thật `FINAL_PRODUCT_MASTER` cho 3 nhóm sản phẩm (Batch-based/Portion-based/gram-based) trước khi tự chọn mapping.
15. **Mới:** `UNIT_DICTIONARY` — phân biệt `PORTION` (business/serving concept) vs `CONTAINER` (plate/bowl vật lý) mới chỉ chấp nhận tạm cho phạm vi Waste, chưa chốt dứt điểm — cần xét lại nếu `UNIT_DICTIONARY` mở rộng thành Master dùng chung toàn ERP. Thiết kế Waste Engine tuyên bố đóng băng (2026-07-29) — trọng tâm chuyển sang chạy Acceptance Test thật.
