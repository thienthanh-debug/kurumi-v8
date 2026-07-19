# CHECKPOINT — Chuyển khung chat, 2026-07-19

Liên quan: [[CHECKPOINT-CHOT-PHIEN-2026-07-14]], [[CHOT-Validation-Layer-2026-07-14]], [[ADR-016 Compiler Never Silences Reality]], [[Validation-Decision-Spec-V1]], [[Production-Compiler-Execution-Type-Spec-V1]], [[Flag — SessionRAM Persistence across WAIT_REVIEW]], [[Flag — Compiler Automation vs Frozen Contract]], [[Discovery — Truth Mapping V1]], [[Discovery — Hierarchy of Prevention]]

## I. Trạng thái đã đóng, không cần động lại

- Validation Engine (Layer 2) — Frozen. Coverage Matrix 9/9 PASS. `Validation-Decision-Spec-V1.md` Frozen.
- ADR-016 — Compiler Never Silences Reality — Accepted. (PREP_COMPILER không lọc bỏ batch non-OK trước khi vào Staging.)
- Governance Protocol (4 Rule) — lưu `01-GOVERNANCE/`: khuôn Flag 4 câu hỏi, No Consumer→No Field, Knowledge Creation Rule, Open Flag ≠ Freeze Blocker (tiêu chí: rủi ro trong phạm vi Mission đang Freeze mới là Blocker).
- READ-INF-PILOT — Hoàn thành, đóng Mission. Boundary Adapter (`ReadInfrastructure.readAsObjects()` + Domain Adapter) đã thay hẳn cách đọc `row[index]` trong `processGenerateState()`. Dual Read đã xóa sau khi PASS. Kết luận: Validate là tầng Domain sạch, không cần Boundary; Generate là ranh giới Physical/Domain thật.
- 4 Discovery Open, không chặn gì, đã lưu `08-REFLECTION/Discovery/`: SessionRAM Persistence (🔴, chưa test A-D), Compiler Automation (🟡, câu hỏi gốc "GENERATE thuộc Engine hay Human" vẫn Open, chờ Mission tương lai), Truth Mapping V1 (⚪, taxonomy 3-Truth: Working/Reference/Decision + quan sát "State" bị overload 3 nghĩa), Hierarchy of Prevention (⚪, ưu tiên SOP/Workflow/UI trước khi sửa Engine).

## II. PRODUCTION_COMPILER — đã sửa và xác nhận PASS trong phiên này

### Bug gốc (đã sửa)

`PRODUCTION_COMPILER` (công thức `=LET(...)` ở ô A1, KHÔNG phải Apps Script) từng emit Item Code dòng YIELD = full SKU (`FINAL-CKE-TIR-001-10cm-BDAY`) thay vì Base Code (`FINAL-CKE-TIR-001`) mà `ALL_ITEM` chỉ track theo Base Code → `VALIDATE_FAIL_INVALID_ITEM`. Đã sửa (dùng `base_code` thay `full_sku` cho Item Code + Location YIELD).

### Phát hiện lớn hơn — PREP_MASTER chứa 2 bản chất khác nhau

- Inventory Prep (STANDALONE): có tồn kho thật, để tủ dùng qua nhiều ngày (Steam Pumpkin, Cooked Rice, Soaked Cashew...).
- Recipe Module (INLINE): không tồn kho, luôn làm-dùng-hết trong ngày, chỉ chia nhỏ công thức (Tiramisu Crust, Filling các loại...).

Đã thêm cột `Execution Type` vào `PREP_MASTER` (giá trị STANDALONE/INLINE), Thanh đã tự tay Audit xong toàn bộ ~70+ dòng.

Đã sửa `PRODUCTION_COMPILER`: Component STANDALONE → giữ hành vi cũ (1 dòng CONS trỏ Prep). Component INLINE → nổ 1 tầng xuống RAW qua `UNIVERSAL_RECIPE_DETAIL`, không ghi movement Prep. Chỉ nổ đúng 1 tầng (không đệ quy) — giữ Rule 20 (V7, Local Explosion Only) cho Inventory Object, chỉ mở ngoại lệ có kiểm soát cho INLINE. (Xem [[Production-Compiler-Execution-Type-Spec-V1]] cho spec gốc.)

### Sự cố phát sinh trong lúc sửa (đã xử lý xong)

1. Bug ADR-016 lặp lại ở Production (`status_flag <> "OK"` lọc bỏ batch) — đã sửa (bỏ điều kiện lọc).
2. INLINE lồng INLINE có thật (Dark Filling chứa Coffee Shot/Pressed Tofu, cả 2 đều INLINE) — không nổ tiếp theo thiết kế (giới hạn 1 tầng), có cơ chế cảnh báo.
3. Cảnh báo `NESTED_INLINE_*` — Gemini ban đầu âm thầm xóa cảnh báo để tránh vỡ Validate; đã yêu cầu sửa lại: tách cảnh báo ra khỏi cột A:I (luồng Staging đọc), đưa sang cột N (vùng phụ). Đã xác nhận qua ảnh: cột A:I sạch, cột N chứa cảnh báo NESTED_INLINE.
4. False positive ban đầu (logic cảnh báo bắt cả Prep lồng STANDALONE) — đã sửa, giờ chỉ cảnh báo khi Prep lồng thực sự là INLINE.

### ✅ Full pipeline PASS — xác nhận qua kiểm tra thực tế

Đã kiểm lần lượt theo luồng PRODUCTION_COMPILER → TRANSACTION_STAGING → INVENTORY_LEDGER → STOCK_POSITION:

- Compiler routing STANDALONE/INLINE đúng, không còn coi mọi Prep là Inline.
- Không còn NESTED_INLINE tràn bảng (false positive đã hết).
- Ledger mirror đúng Compiler (không đổi Location/Qty).
- Stock Position cộng dồn đúng theo (Item Code, Location) — ví dụ `PREP-NUT-SOC-001` = -2.340,40g.
- Không có dấu hiệu recursion mở nhầm ngoài ý muốn.

### ❌ CLOSED — False Alarm: "RAW-OIL-VCO-001 không tự sum"

Ban đầu nghi ngờ `RAW-OIL-VCO-001` trong batch `DN-ASSM-260612-001` không được gộp lên `STOCK_POSITION` (trong khi các mã RAW khác gộp bình thường). Đã điều tra theo 3 giả thuyết:

1. Item Code lệch ký tự ẩn — loại (đối chiếu trực tiếp `UNIVERSAL_RECIPE_DETAIL` dòng Tiramisu Crust và Tiramisu Light Filling, cả hai ghi `RAW-OIL-VCO-001` sạch, không lệch).
2. Unit không khớp — loại (cả hai dòng CONS đều `g`).
3. Location khác nhau thật — loại (cả hai dòng CONS đều `DN_RAW`).

Kết luận thật: đây là đọc nhầm tầng dữ liệu. `PRODUCTION_COMPILER`/`INVENTORY_LEDGER` ghi từng dòng CONS riêng theo Component (CONS-1-x, CONS-2-x...) — đúng thiết kế, giữ traceability, không nên sum ở tầng này. Việc gộp thật sự xảy ra ở `STOCK_POSITION`, và đã xác nhận trực tiếp: `RAW-OIL-VCO-001` = -1.061,76 g, một dòng duy nhất, cộng dồn đúng tất cả batch. Không có bug. Đóng, không cần sửa Compiler hay Stock Position.

## III. Còn mở — chưa phải Blocker, không chặn Freeze hiện tại

- `inline_yield` là assumption — cần xác nhận `UNIVERSAL_RECIPE_DETAIL` đang normalize theo 1 Batch hay theo Yield Qty. Đây là quyết định mô hình dữ liệu, cần Reality evidence trước khi Freeze.
- `LEFT(c_code;4)` trong Compiler — technical debt, không ảnh hưởng vận hành hiện tại nhưng cần dọn sau.
- INLINE lồng INLINE nhiều tầng có thật trong data (ví dụ Chocolate Filling → Cashew Milk, cả hai INLINE; Coffee Cream → Coffee Shot; Mango Salsa → Mash Avocado). Hiện Compiler chỉ nổ đúng 1 tầng rồi dừng, có cảnh báo `NESTED_INLINE_*` ở cột N để con người xử lý thủ công.
  - Trạng thái chính thức (GPT đã tự self-correct, Thanh đã xác nhận):
    ```
    Discovery:      ✓ Đã biết từ trước (không phải phát hiện mới khi đọc PREP_MASTER)
    Implementation: ✓ Đã có (explode 1 tầng)
    Mechanism:      ✓ Flag NESTED_INLINE_* hoạt động đúng
    Behavior:       ✓ Stop at level 1 — giới hạn có chủ đích để quan sát Reality, không phải thiếu chức năng
    Status:         OPEN EXPERIMENT — KHÔNG PHẢI BUG, KHÔNG CẦN ADR
    ```
  - Bài học quy trình: GPT ban đầu đề xuất "cần ADR mới cho recursive inline expansion" ngay sau khi đọc PREP_MASTER — đây là nhảy cóc quy trình (`Observe → Propose Architecture → ADR`, sai với Knowledge Creation Rule đúng là `Observe → Collect Evidence → Repeat → Stable → ADR`). GPT đã tự nhận sai và tự sửa. Kết luận đúng: dữ liệu thực tế xác nhận Discovery Open là có cơ sở (cơ chế NESTED_INLINE_* chắc chắn sẽ được kích hoạt khi vận hành), nhưng chưa đủ bằng chứng để đổi thuật toán Compiler.
  - Câu hỏi chưa trả lời (cần Reality vận hành thực tế, không phải AI đoán): cơ chế cảnh báo 1 tầng + xử lý thủ công hiện tại có đủ dùng hay không? Chỉ sau khi có dữ liệu vận hành thực tế mới quyết định giữ 1 tầng hay chuyển sang recursive.

## IV. Discovery mới — chưa Frozen, cho Layer 3 (Transaction Engine, chưa bắt đầu build)

Nguồn: Thanh xem 2 file thực tế — `MasterDocument (5).xlsx` (Chi tiết doanh thu / Sales Detail) và `MasterDocument (6).xlsx` (Tổng hợp phiếu nhập hàng / Purchase Detail).

### Quan sát từ Reality

- Sales Report: có Mã chứng từ, Ngày, Khách, Bàn, Tổng tiền, Thanh toán — nhưng không có Item Code nguyên liệu. POS chỉ biết "bán 1 Tiramisu", không biết BOM bên dưới. → Nghĩa là luồng Sales Consumption bắt buộc phải đi qua Compiler (BOM) để nổ ra nguyên liệu, giống cơ chế Production hiện tại.
- Purchase Report: có Mã chứng từ, Ngày, NCC, Tổng tiền — không có logic BOM nào cần thiết, đi thẳng vào Ledger.

### Đề xuất phân loại Transaction Sources (GPT nêu, CHƯA FREEZE)

```
POS EXPORT → INPUT LOG → COMPILER (nếu cần) → TRANSACTION → LEDGER
```

Không phải Input Log nào cũng cần Compiler:

- Nhóm A — Direct Transaction (không cần BOM, đi thẳng vào Transaction): Purchase, Waste, Transfer, Adjustment, Opening Balance
- Nhóm B — Compiled Transaction (phải qua Compiler trước khi vào Transaction): Prep, Production, Sales Consumption

Ghi chú theo Governance: đây là Discovery dựa trên bằng chứng thật (2 file Reality), có cơ sở hợp lý và nhất quán với triết lý hiện có (chỉ nguồn có BOM mới cần Compiler — giống phân biệt STANDALONE/INLINE đã làm ở Production Compiler). Tuy nhiên Transaction Engine chưa bắt đầu build (xem Mục V — vẫn nằm trong "chưa bắt đầu"), nên phân loại Nhóm A/Nhóm B này chưa nên Freeze thành kiến trúc chính thức — cần giữ ở trạng thái Discovery/đề xuất thiết kế cho tới khi Mission Transaction Engine chính thức mở và có đủ Reality Test (ví dụ: thử áp phân loại này vào ít nhất 1 nguồn mỗi nhóm, xem có phát sinh case ngoại lệ không, trước khi khóa cứng).

## V. Việc chưa bắt đầu (ngoài phạm vi Mission hiện tại)

- Wiring `Read_Infrastructure.gs` vào main Engine (open từ phiên trước).
- Resolving SessionRAM Persistence definitively với Reality evidence.
- Pending ERP modules: Waste Engine, Transfer Engine, Audit Engine (chưa bắt đầu: Workshop Engine, Branch Consumption, Sales Engine, POS Integration).
- Meta-Architecture (Sprint O4 tentative) — chưa Frozen, chờ Reality validation.
- Python tooling tại `D:\kurumi\Kurumi_V8\python` cho tự động hóa đọc vault.

## VI. Quy ước quan trọng cần khung mới biết

- Phạm vi sửa Compiler luôn là công thức Google Sheets (`=LET(...)` ở ô A1 các sheet `*_COMPILER`), KHÔNG phải Apps Script `.gs`. Engine (`.gs`) chỉ đọc dữ liệu đã có sẵn trong `TRANSACTION_STAGING`, không biết gì về `PREP_MASTER`/`Execution Type`.
- Phân biệt vai trò các tầng: `PRODUCTION_COMPILER`/`INVENTORY_LEDGER` = ghi chi tiết từng dòng theo Component (không sum, giữ traceability). `STOCK_POSITION` = tầng gộp duy nhất, cộng dồn theo (Item Code, Location). Đừng nhầm "không sum ở Ledger" là bug — đó là thiết kế đúng.
- Knowledge Creation Rule: không viết ADR/tài liệu chính thức cho quyết định INLINE Explosion (recursive hay không) cho tới khi chạy thật + PASS đủ lâu.
- Mission Boundary: chỉ giải quyết đúng 1 việc tại 1 thời điểm — hiện đang là "Production Compiler ổn định", pipeline đã PASS full chain, còn 3 mục ở Mục III chưa phải blocker. Chưa mở WASTE_COMPILER hay bất kỳ Mission nào khác.
- Toàn bộ file Spec/Mission Brief đã gửi Gemini nằm trong lịch sử chat khung cũ — nếu cần đối chiếu lại nguyên văn, phải quay lại khung đó, không có trong vault chính thức (đây đều là các file "tạm" dùng để giao việc, không phải tài liệu cần lưu vĩnh viễn).

## VII. Quyết định đóng phiên (Thanh xác nhận, 2026-07-19)

Bản nháp trước của Checkpoint này (relay qua GPT) có 1 dòng sai ở Mục I — claim "Compiler Automation đã gộp thêm case Roaster Cashew" — không khớp nội dung thật trong `Flag — Compiler Automation vs Frozen Contract.md`. Đã đối chiếu vault thật, xác nhận sai, và Thanh quyết định:

1. **Commit 2 file đang chờ** (`Discovery — Hierarchy of Prevention.md`, `Production-Compiler-Execution-Type-Spec-V1.md`) — Xác nhận, đã commit cùng đợt với Checkpoint này.
2. **Case Roaster Cashew** — Bỏ hẳn, không gộp vào `Flag — Compiler Automation vs Frozen Contract.md`. File đó giữ nguyên nội dung gốc (2026-07-14), không có case này.
3. **Lưu Checkpoint 2026-07-19** — Xác nhận, lưu tại đúng path đề xuất: `06-CHECKPOINT/Sprint/sprint 04/CHECKPOINT-2026-07-19.md` (file này).
