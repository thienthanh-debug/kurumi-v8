# Validation Decision Specification

Kurumi ERP V8 — Inventory Engine
**Ngày:** 2026-07-13
**Trạng thái:** Draft — chờ Thanh duyệt trước khi khung Code triển khai
**Revision:** Rev.3 (hợp nhất Rev.1 + Rev.2 WARNING/PPV + Rev.3 Location)

Liên quan: [[01-Runtime-Constitution]] — lưu ý: mục "WAIT_REVIEW is the boundary between Human Workflow and Engine Workflow" của Constitution mô tả WAIT_REVIEW là bắt buộc cho mọi giao dịch (hành vi cũ). Spec này (Mục 2) thay đổi hành vi đó thành exception-based (WARNING mới vào WAIT_REVIEW). Chưa sửa Constitution — cần Thanh xác nhận và tự cập nhật câu chữ Constitution nếu đồng ý, ngoài phạm vi file này.

---

## 1. Bối cảnh

Engine hiện tại (`processValidateState` → `WAIT_REVIEW` → `processWaitReviewState`) bắt buộc MỌI giao dịch hợp lệ đều dừng chờ người bấm Approved. Reality mới (Thanh, 2026-07-13): "khi nào bất thường hãy đến lượt tui" — con người chỉ nên can thiệp vào phần ngoại lệ.

---

## 2. Thay đổi State Machine

Trước:

```
VALIDATE → WAIT_REVIEW → COMMIT
```

Sau:

```
VALIDATE → Risk Assessment →
    NORMAL   → COMMIT       (Engine tự động)
    WARNING  → WAIT_REVIEW  (chờ Thanh/Manager)
    CRITICAL → REJECT       (Engine tự động, KHÔNG chờ người)
```

`WAIT_REVIEW` không còn là trạm bắt buộc cho mọi giao dịch — nó là một trong ba outcome của Risk Assessment.

---

## 3. Input / Output

**Input:** `commitPackage` (đã qua các kiểm tra tồn tại/định dạng hiện có trong `processValidateState`).

**Output:** một trong ba nhãn — `NORMAL`, `WARNING`, `CRITICAL` — gắn vào `sessionRAM`, dùng để định tuyến state tiếp theo.

---

## 4. Tiêu chí phân loại

### CRITICAL → REJECT (tự động, không chờ người)

Toàn bộ lỗi tồn tại/định dạng hiện có trong `processValidateState` giữ nguyên là CRITICAL — dữ liệu sai không thể tiếp tục, không cần ý kiến con người để biết nó sai:

- `VALIDATE_FAIL_MISSING_FIELD`
- `VALIDATE_FAIL_NOT_A_NUMBER`
- `VALIDATE_FAIL_ZERO_QTY`
- `VALIDATE_FAIL_INVALID_ITEM`
- ~~`VALIDATE_FAIL_INVALID_LOCATION`~~ — **Tạm ngưng trigger** (không xóa mã lỗi). Lý do: chưa có Master Data đúng Domain để đối chiếu (`PLACEMENT_MASTER` sai Domain, không tạo `LOCATION_MASTER` khi chưa có Reality chứng minh cần). Xem Mục 6.

Bắt buộc: mỗi lần REJECT tự động phải ghi 1 dòng vào `ERROR_LOG` (giống cơ chế `appendAudit` đã có) — REJECT không được lặng lẽ biến mất. Đây khác REJECT-do-người-bấm (giữ nguyên luồng `WAIT_REVIEW` → người bấm Rejected → `CLEANUP` như cũ).

### WARNING → WAIT_REVIEW (chờ người)

Đã chốt (2026-07-13): trong phạm vi đợt này, WARNING chỉ có đúng 1 nguồn:

- `PREP_LOG` cột `Status Flag` = `LOW YIELD` hoặc `OVER YIELD` → WARNING.

Đã hủy, không dùng:

- ~~`STOCK_INPUT_LOG` PPV threshold~~ — Thanh quyết định hủy: giá nhập chợ vốn lệch theo mùa/nhà cung cấp, dùng % variance làm tín hiệu sẽ tạo noise giả, không phải bất thường nghiệp vụ thật. → `STOCK_INPUT_LOG` chỉ còn NORMAL/CRITICAL 2 nhánh.
- ~~`PRODUCTION_LOG` thêm Status Flag mới~~ — Thanh quyết định giữ nguyên hiện trạng, không thêm cột. → `PRODUCTION_LOG` chỉ còn NORMAL/CRITICAL 2 nhánh.

### NORMAL → COMMIT (tự động)

Không rơi vào CRITICAL, không có cờ WARNING nào. Đi thẳng `COMMIT` như cũ.

### Fail Closed — nguyên tắc chung cho Master Data thiếu

Validation phải đối chiếu với Master Data đúng Domain của trường đang kiểm tra. Không dùng Master Data sai Domain để check (bài học từ vụ `PLACEMENT_MASTER`/Location — xem Mục 6).

Quy tắc chung ghi vào Constitution: **"Thiếu Master Data cần cho Validate → dừng Engine, không được Skip Validate."** Áp dụng cho các check còn hiệu lực (item code, qua `ALL_ITEM`...), không áp dụng cho Location ở đợt này — `VALIDATE_FAIL_INVALID_LOCATION` tạm ngưng trigger, không phải trường hợp Fail Closed (xem Mục 6).

---

## 5. Việc khung Code cần làm, theo thứ tự

1. `processValidateState()` không thực hiện check Location ở đợt này. Đánh dấu rõ trong code (comment/TODO), đây là hành vi tạm thời, không phải thiếu sót:

   ```
   VALIDATE
       ↓
   Không validate Location
       ↓
   TODO: chờ Domain Model Location được xác nhận
   ```

2. Refactor `processValidateState()`: sau khi qua các check CRITICAL còn hiệu lực, thêm bước gắn nhãn Risk (đọc `Status Flag` nếu nguồn là PREP_LOG) → trả `nextState` là `COMMIT` / `WAIT_REVIEW` / tự-REJECT tương ứng, thay vì luôn luôn set `WAIT_REVIEW`.
3. Refactor `processWaitReviewState()`: chỉ còn xử lý các giao dịch đã được gắn nhãn WARNING — bớt việc mọi giao dịch đều phải qua đây.
4. Thêm nhánh tự-REJECT: khi CRITICAL, gọi `appendAudit(ERROR_LOG, ...)` rồi chuyển thẳng `CLEANUP`, không qua `WAIT_REVIEW`.
5. Sửa `processCleanupState()`: hiện chỉ dọn `sessionRAM`, chưa đụng `TRANSACTION_STAGING` — cần dọn/đánh dấu lại dữ liệu Staging sau khi REJECTED (bug cũ, độc lập với phần Risk Assessment, cần sửa chung đợt này).
6. Hợp nhất Snapshot ID: chọn 1 nguồn duy nhất (khuyến nghị: `row[0]`/`movement.snapshotId` — vì đây là nguồn thật sự được dùng để ghi Ledger; ô B1 chỉ nên dùng để xác nhận tồn tại, không tạo ra giá trị riêng).
7. (P2, có thể làm sau) Chuyển `processGenerateState`/`processValidateState` từ đọc thô `getDataRange().getValues()` sang dùng `ReadInfrastructure.readAsObjects()` đã viết sẵn.

---

## 6. Việc CHƯA quyết, cần Thanh xác nhận trước khi code

**Đã chốt (2026-07-13) — Location, Rev.3:**

- `PLACEMENT_MASTER` là Plating/Assembly Hierarchy, khác Domain với Inventory Location — không dùng để validate kho.
- Không tạo `LOCATION_MASTER` ở đợt này. Lý do (đúng FOUNDATION-004 "Schema không phát minh, Schema chỉ hiện hình" — chưa có Reality thì Schema chết): chưa có phân tích luồng nhập/chuyển/xuất kho thật xác nhận có ≥2 vị trí vật lý cần phân biệt.
- Interim: `VALIDATE_FAIL_INVALID_LOCATION` tạm ngưng trigger, giữ nguyên mã lỗi cho tương lai (không xóa khỏi Constitution), đánh dấu TODO trong code — xem Mục 5 bước 1.
- Điều kiện mở lại: khi Reality (phân tích luồng kho thật) xác nhận cần phân biệt ≥2 vị trí — lúc đó tạo `LOCATION_MASTER` là quyết định kiến trúc tự nhiên, không phải vá.

**Còn treo thật sự, chưa ai trả lời:**

- Bản Excel (`KURUMI_INVENTORY_ENGINE.xlsx`) dùng để phân tích bug `PREP_LOG`/`STOCK_INPUT_LOG` (formula chạy full ~1000 dòng) có thể đã cũ hơn Google Sheet thật đang chạy. Cần Thanh mở Google Sheet thật, kiểm tra lại range công thức 2 sheet này còn đúng như báo cáo không, trước khi Code sửa theo Mục 7 (Formula Audit).

**Đã trả lời xong:**

- ~~Ngưỡng WARNING cho PPV~~ — đã hủy, xem Mục 4.
- ~~PRODUCTION_LOG có cần Status Flag mới~~ — đã hủy, giữ nguyên, xem Mục 4.

---

## 7. Ghi chú Formula Audit (Bước 3, song song với đợt sửa State Machine này)

Kiểm tra trực tiếp trên file thật (2026-07-13):

- `PREP_LOG`: 5 cột formula (D,G,J,K,L) chạy full `...2:...1000` — cần sửa.
- `STOCK_INPUT_LOG`: 6 cột formula (C,E,F,G,K,O) chạy full `...2:...1004` — cần sửa, cùng lỗi với PREP_LOG.
- `PRODUCTION_LOG`: toàn bộ formula đã giới hạn đúng `...2:...50` — đã tối ưu, không cần sửa.

---

## Revision History

- **Rev.1** (2026-07-13): Bản gốc — Risk Assessment 3 nhánh (NORMAL/WARNING/CRITICAL), thay thế WAIT_REVIEW bắt buộc cho mọi giao dịch.
- **Rev.2** (2026-07-13): Chốt WARNING chỉ còn 1 nguồn (PREP_LOG Status Flag), hủy PPV threshold và PRODUCTION_LOG Status Flag mới. Phát hiện Semantic Drift giữa `LOCATION_MASTER` (giả định trong code) và `PLACEMENT_MASTER` (sheet thật) — xác nhận đây là 2 khái niệm khác Domain, không phải lỗi đặt tên.
- **Rev.3** (2026-07-13): Chốt không tạo `LOCATION_MASTER` khi chưa có Reality chứng minh cần (nguyên tắc "Reality trước, Entity sau" — FOUNDATION-003/004). `VALIDATE_FAIL_INVALID_LOCATION` tạm ngưng trigger thay vì Fail Closed vào một sheet chưa tồn tại trong Reality.

---

*Tổng hợp từ đóng góp của GPT (Architecture Supervisor), Gemini (Auditor/Builder) và quyết định của Thanh (Reality Owner) trong phiên trao đổi ngày 2026-07-13. Lưu vào vault bởi Claude (Constitution Keeper).*
