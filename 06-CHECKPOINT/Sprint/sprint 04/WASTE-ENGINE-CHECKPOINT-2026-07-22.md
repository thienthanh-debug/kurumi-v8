# WASTE ENGINE — Checkpoint riêng (tách từ CHECKPOINT-2026-07-22.md, cập nhật đến 2026-07-25)

Toàn bộ nội dung Waste Engine tách ra khỏi Checkpoint chính để giữ file gốc gọn. Đây là Mission **chưa build** (`WASTE_LOG` đã tồn tại, `WASTE_COMPILER` chưa có) — không phải Mission chính thức đang mở, chỉ đang điều tra thiết kế trước khi build.

Liên quan: [[CHECKPOINT-2026-07-22]] (Mục II.7, III, V), [[Discovery — Boundary Formula vs Engine]], [[Discovery — Hierarchy of Prevention]], [[Production-Compiler-Execution-Type-Spec-V1]]

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

## Câu hỏi còn treo

1. `inline_yield`/Business Object — về mặt "field nào Compiler đọc cho từng loại" đã rõ hướng (Mục 2), nhưng chưa build thật để kiểm chứng.
2. Dropdown "User chọn Source" — có cần validate chéo (ví dụ chọn "PREP" nhưng gõ mã Item lại là mã RAW) hay tin tưởng người dùng chọn đúng?
3. ✅ **Đã đóng** — Semi Product (Momo) không cần quyết riêng: Consumption Resolver (Mục 5) tự quyết dừng ở Semi Product bằng nguyên lý chung dựa trên "đã có Ledger YIELD hay chưa", không cần quyết định riêng cho từng case.
4. **Mới:** Consumption Resolver dùng chung cho SELL và WASTE — khi Sales Engine build (chưa mở Mission), nên tái dùng đúng Resolver này, không viết lại logic explode riêng cho SELL_COMPILER.
5. Waste Engine vẫn chưa phải Mission chính thức đang mở — quyết định mở khi nào vẫn thuộc về Thanh (xem [[CHECKPOINT-2026-07-22]] Mục III).
