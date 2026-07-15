# DISCOVERY — Truth Mapping V1 (Draft)

**Ngày:** 2026-07-14
**Trạng thái:** Draft — chưa kết luận, chỉ phân loại Reality
**Liên quan:** Validation-Decision-Spec-V1, ADR-016

## Mục tiêu
Không tạo taxonomy. Không tạo nhóm mới. Chỉ trả lời: Artifact này hiện đang đóng vai trò gì trong Engine?

Bối cảnh: 3-Truth Model (Working / Reference / Decision Truth) đã giải quyết được nhiều quyết định kiến trúc trong Sprint này (Status Flag không vào commitPackage, ALL_ITEM chỉ lookup không copy, batchContextMap chỉ giữ field có consumer, Allow Unknown Output lookup runtime). Discovery này kiểm tra xem model đó có giải thích được toàn bộ Artifact đang tồn tại trong Engine hay không, trước khi quyết có viết Ontology chính thức (`What is Truth`) hay không.

## Bảng Mapping

| Artifact | Vai trò hiện tại | Candidate Truth | Evidence / Ghi chú |
|---|---|---|---|
| PREP_MASTER | Reference khi Validate | Reference | `Allow Unknown Output`, Lookup runtime |
| ALL_ITEM | Reference khi Validate | Reference | Validate Item Code |
| PREP_LOG | Reference | Reference | Status Flag, Expected Output |
| UNIVERSAL_RECIPE_DETAIL | Reference | Reference | PREP_COMPILER đọc |
| TRANSACTION_STAGING | Snapshot của Transaction | Working | Generate → Validate → Commit |
| commitPackage | Working object trong RAM | Working | SessionRAM, sinh ra từ Snapshot |
| batchContextMap | Lookup cache | Working *(tạm)* | Runtime cache của Reference Truth — copy/index/cache từ PREP_LOG, không sinh tri thức mới. Khác `commitPackage` (sinh từ Snapshot) và `effectiveQty` (kết quả Resolution). Chưa rõ cache có nên xem là Working Truth hay chỉ là Representation của Reference Truth — chưa kết luận. |
| effectiveQty | Runtime value | Working | resolveEffectiveQty(), là kết quả Resolution, không phải copy thuần túy |
| Risk Level | Kết quả đánh giá | Decision | NORMAL / WARNING / CRITICAL — Decision Result thật |
| Business State | Quyết định nghiệp vụ | Decision | APPROVED / REJECTED |
| WAIT_REVIEW | Điểm chờ quyết định | Machine State *(tạm)* | Sửa lại từ "Decision" — WAIT_REVIEW không phải kết quả đánh giá, mà là vị trí Engine đang đứng (giống VALIDATE/COMMIT/VERIFY), chỉ khác là có thêm tương tác con người. Gần Execution State hơn Decision. Cần thêm Reality để xác nhận. |
| INVENTORY_LEDGER | ? | ? | Append-only Business History — không khớp Working/Reference/Decision |
| STOCK_POSITION | ? | ? | Derived State |
| ERROR_LOG | ? | ? | Append-only Engine History — gần giống Ledger về bản chất (ghi lại quá khứ), nhưng Ledger là Business Truth (tồn kho) còn ERROR_LOG là System Truth (Engine đã làm gì) |
| Execution State | ? | ? | GENERATE → VALIDATE → COMMIT... — không phải kết quả đánh giá, chỉ nói Engine đang đứng ở đâu (Machine Lifecycle) |

## Phát hiện 1 — Có thể tồn tại 2 chiều phân loại, không phải thiếu nhóm

Không gán được `INVENTORY_LEDGER`/`ERROR_LOG` vào 3-Truth Model không phải vì model thiếu nhóm, mà vì đang cố dùng 1 taxonomy để giải thích 2 chiều khác nhau:

- **Chiều 1 — Theo chức năng:** Reference / Working / Decision
- **Chiều 2 — Theo thời gian:** Runtime / Historical

| Artifact | Function | Time |
|---|---|---|
| PREP_MASTER | Reference | Runtime |
| commitPackage | Working | Runtime |
| Risk Level | Decision | Runtime |
| INVENTORY_LEDGER | ? | Historical |
| ERROR_LOG | ? | Historical |

**Không kết luận** có 2 taxonomy thật hay không — chỉ ghi nhận: một số Artifact không phân loại được bằng mô hình 3-Truth hiện tại, có khả năng tồn tại chiều phân loại thứ hai (Function vs Time), nhưng chưa đủ Reality để kết luận.

## Phát hiện 2 — Từ "State" đang bị overload cho ít nhất 3 khái niệm khác nhau

- **Execution State** (`GENERATE`, `VALIDATE`, `COMMIT`...) — vị trí trong Machine Lifecycle, không phải kết quả đánh giá.
- **Business State** (`APPROVED`, `REJECTED`) — kết quả quyết định của con người.
- **Risk Level** (`NORMAL`, `WARNING`, `CRITICAL`) — thực chất là Classification, không phải State, nhưng từ trước tới giờ vẫn bị gọi chung nhóm "State".

**Observation (không kết luận, không đổi tên, không tạo taxonomy mới):** Một số thuật ngữ đang được dùng cho nhiều khái niệm khác nhau (ví dụ "State"). Điều này có thể là nguyên nhân khiến việc phân loại Artifact trở nên mơ hồ — không phải do 3-Truth Model thiếu nhóm, mà do chính công cụ mô tả (từ ngữ) đã mơ hồ từ trước. Chưa đủ Reality để đổi tên hay tạo taxonomy mới.

## Kết luận Discovery
Dừng đúng ở đây — không mở taxonomy mới, không viết Ontology `What is Truth` ngay. Đây là điểm dừng theo đúng Knowledge Creation Rule: Discovery chỉ ghi nhận Reality chưa được mô hình hiện tại giải thích hết, chưa phải lúc kết tinh thành Knowledge chính thức. Sẽ quay lại khi có thêm Reality (ví dụ: Production/Waste/Transfer Compiler cũng cần phân loại Artifact tương tự — nếu 2 chiều phân loại hoặc 3 nghĩa của "State" tiếp tục xuất hiện, lúc đó mới đủ điều kiện viết Ontology chính thức).
