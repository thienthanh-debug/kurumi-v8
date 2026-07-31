# ADR-019 — Pre-Resolver Input Validation (Gatekeeper)

Status: Accepted — FROZEN (2026-07-27), xác nhận bằng 11/11 test case thật
Ngày: 2026-07-27
Liên quan: [[ADR-018 Waste Event ID Format]], [[ADR-020 Universal Event Lifecycle]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]]

> **⚠️ Ghi chú đánh số:** nội dung gốc gọi ADR này là "ADR-018" (đúng số trong track riêng của khung chat Waste Engine). Renumber thành ADR-019 để nối tiếp [[ADR-018 Waste Event ID Format]] trong track chính thức của vault, tránh trùng số.

---

## Context

`NO_VALID_TRANSACTIONS` regression (V6, 2026-07-27): `WASTE_COMPILER` trả về rỗng cho **toàn bộ** log, không chỉ dòng lỗi. Root cause trace được: 1 dòng `Waste Qty` để trống (case "Passion Mango") khiến công thức `("" / portion_size) * child_qty` lỗi `#VALUE!`, lỗi này lan ra ngoài `REDUCE`, bị `IFERROR` cuối cùng nuốt silent, trả `NO_VALID_TRANSACTIONS` cho tất cả — không cô lập đúng dòng lỗi.

Kết luận: validation phải chặn ở **cửa vào** (`WASTE_LOG`), trước khi bất kỳ dòng nào đi vào Normalizer/Resolver — không để 1 dòng lỗi kéo sập cả Engine.

## Decision

**3 trạng thái, không phải nhị phân:**

```
Row Activated? = có ít nhất Item Code hoặc bất kỳ business input nào
  NO  → EMPTY (không phải lỗi — dòng trống chưa dùng tới, không spam ERROR_LOG)
  YES → kiểm 7 field bắt buộc:
          Date        — phải là date hợp lệ, không chỉ "không blank"
          Item Code   — không blank
          Waste Qty   — numeric VÀ > 0 (không chỉ "không blank")
          Unit        — không blank
          Reason      — không blank
          Staff       — không blank
          Branch      — không blank
        Thiếu bất kỳ field nào → INVALID_INPUT
        Đủ hết → VALID
```

**Behavior:**

```
EMPTY         → ignored
INVALID_INPUT → blocked trước Normalizer/Resolver
VALID         → eligible cho Event ID (ADR-018)
```

Range: `2:500`. **Fail-isolated per row** — 1 row lỗi không được kéo sập cả `REDUCE`/Engine thành `NO_VALID_TRANSACTIONS` cho tất cả.

**Gatekeeper chỉ làm đúng 2 việc:** xác định VALID/EMPTY/INVALID_INPUT, và chỉ cho row VALID đi xuống Normalizer/Resolver — không explode, không normalize, không tạo transaction. Apps Script sinh Event ID (ADR-018) sau đó **chỉ nhìn row VALID + Event ID blank**, không tự kiểm lại business rule lần 2 (tránh 2 bản validation logic khác nhau — DRY).

## Consequence

- Test đã qua: `Qty=0`, `Qty=text`, `Branch=spaces`, `Qty blank` đều bị chặn đúng; Opera/Momo/Stroganoff (case hợp lệ) vẫn PASS. 11/11 test case.
- **Nuance đã chốt, không chặn Freeze:** `ISNUMBER(date)` mới là structural validation (đúng định dạng ngày), chưa phải business-date validation (ví dụ chưa chặn ngày tương lai/quá khứ bất thường) — ghi lại để biết còn 1 lớp kiểm tra sâu hơn có thể cần sau này, không phải thiếu sót cần sửa ngay.
- `WASTE_COMPILER` giữ **BLOCKED** cho tới khi cả ADR-018 (Event ID) và Gatekeeper này implement xong, test qua case duplicate Item Code + insert/delete row.
