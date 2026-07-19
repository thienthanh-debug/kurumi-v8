# Spec — PRODUCTION_COMPILER đọc Execution Type (PREP_MASTER)

**Ngày:** 2026-07-17
**Trạng thái:** Draft — chờ Gemini xác nhận cấu trúc `UNIVERSAL_RECIPE_DETAIL`/`actual_multiplier` trước khi code (chưa chạy thật)
**Người triển khai:** Gemini (Builder) — spec này không giao cho Claude Code, khác lệ thường của Sprint Validation Engine

Liên quan: [[ADR-016 Compiler Never Silences Reality]] (cùng chủ đề sửa lỗi routing trong Compiler, khác lỗi cụ thể — ADR-016 là filter bỏ sót batch non-OK, spec này là route sai Item Code có tồn kho vs không tồn kho)

---

## Bối cảnh

`PREP_MASTER` đã Audit xong toàn bộ (~70+ dòng), cột `Execution Type` đã điền đủ 2 giá trị: `STANDALONE` (có tồn kho thật, có PREP_LOG) hoặc `INLINE` (Recipe Module, không tồn kho, luôn làm-dùng-hết trong ngày).

`FINAL_ASSEMBLY_DETAIL` hiện tại coi mọi Component đều là PREP có tồn kho — sai với các dòng INLINE (ví dụ Tiramisu Crust/Filling), gây `VALIDATE_FAIL_INVALID_ITEM` hoặc Ledger âm giả nếu chỉ đổi Item Code mà không đổi logic explode.

## Nguyên tắc route (thay thế logic cũ)

Với mỗi Component trong `FINAL_ASSEMBLY_DETAIL` (cột `Component Code`):

```
Tra PREP_MASTER theo Component Code -> lấy Execution Type

Nếu Execution Type rỗng/không tìm thấy:
  → FAIL CLOSED. Dừng compile, báo lỗi rõ Component Code nào thiếu phân loại.
  Không tự đoán STANDALONE hay INLINE.

Nếu STANDALONE:
  → Giữ nguyên hành vi cũ: 1 dòng CONS, Item Code = Component Code (Prep Code thật),
    Qty = định lượng gốc x actual_multiplier. Dừng lại đây (đúng Rule 20 — Local Explosion).

Nếu INLINE:
  → KHÔNG tạo dòng CONS cho Component Code này.
  → Tra UNIVERSAL_RECIPE_DETAIL theo Component Code (cột base_code, giống cách
    PREP_LOG đang tra công thức PREP hiện tại) -> lấy danh sách RAW ingredients
    + định lượng của recipe đó.
  → Tạo dòng CONS cho TỪNG RAW ingredient đó, Qty = định lượng RAW x (Qty gốc
    của Component trong FINAL_ASSEMBLY_DETAIL) x actual_multiplier.
  → CHỈ nổ đúng 1 tầng (INLINE -> RAW). Nếu trong UNIVERSAL_RECIPE_DETAIL của
    Component INLINE này lại xuất hiện 1 Prep khác (STANDALONE hoặc INLINE) thay vì
    thẳng RAW -> FAIL CLOSED, báo lỗi "INLINE lồng nhau chưa được hỗ trợ", không tự
    đệ quy thêm. (Chưa có Reality xác nhận cần nhiều hơn 1 tầng — xem ghi chú cuối.)
```

## Điểm cần Gemini xác nhận trước khi code (không đoán)

1. `UNIVERSAL_RECIPE_DETAIL` dùng chung công thức cho cả STANDALONE và INLINE Prep, tra theo cột base_code (index 2, giống code `PRODUCTION_COMPILER` cũ đang dùng cho nhánh `is_final = FALSE`). Xác nhận cấu trúc cột này đủ để tra RAW ingredient cho Component INLINE — nếu công thức của 1 Component INLINE nào đó lại trỏ sang Prep khác thay vì RAW thuần, đó là dấu hiệu FAIL CLOSED ở trên, không phải lỗi code.
2. Item Code của dòng YIELD (đã sửa ở lần trước — dùng base_code, không dùng full_sku) không đổi gì thêm trong lần sửa này — giữ nguyên.

## Việc CHƯA làm trong spec này

- Không viết ADR chính thức ngay — đợi chạy thật + PASS trước, đúng kỷ luật "Reality trước Governance" đã giữ suốt Sprint.
- Không hỗ trợ INLINE lồng nhau (INLINE trong INLINE) — chưa có bằng chứng cần, chỉ FAIL CLOSED nếu gặp.
- Không đổi gì ở `PRODUCTION_LOG`, `TRANSACTION_STAGING`, hay Apps Script Engine (`processValidateState` không cần sửa gì thêm — Item Code đưa vào Validate vẫn luôn là mã đã tồn tại trong `ALL_ITEM`, dù là Base Code của FINAL/STANDALONE hay RAW code, không có gì mới ở tầng Engine).

## Test xác nhận sau khi sửa

Chạy lại batch Tiramisu (đã dùng làm case gốc). Kỳ vọng:

- Dòng YIELD: Item Code = `FINAL-CKE-TIR-001` (giữ nguyên như đã sửa).
- Dòng CONS: KHÔNG còn `PREP-CRS-TIR-001`/`PREP-FIL-TDR-001`/`PREP-FIL-TLG-001` — thay bằng các RAW ingredient thật (bột hạnh nhân, cacao, dừa...) lấy trực tiếp từ `UNIVERSAL_RECIPE_DETAIL` của 3 Component đó, đã nhân đúng hệ số.
- `ERROR_LOG`: không có `VALIDATE_FAIL_INVALID_ITEM` cho batch này nữa.
- `STOCK_POSITION`: `PREP-CRS-TIR-001` và tương tự không còn xuất hiện (hoặc nếu còn dữ liệu cũ âm từ trước, đó là lịch sử cần dọn riêng, không phải lỗi của lần sửa này).

---

## Ghi chú lưu trữ (Claude, 2026-07-17)

Spec này chưa được Claude Code xác minh kỹ thuật — khác với `PREP_COMPILER` (ADR-016), Claude chưa từng thấy code thật của `PRODUCTION_COMPILER`, nên không đối chiếu được các giả định (`actual_multiplier`, cấu trúc `UNIVERSAL_RECIPE_DETAIL`...) với công thức thật. Lưu nguyên văn theo yêu cầu, chờ Gemini code + Reality Test trước khi cập nhật trạng thái.
