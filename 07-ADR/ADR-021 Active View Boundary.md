# ADR-021 — Active View Boundary

Status: Accepted (relayed — xem ghi chú nguồn dưới, mức độ chứng kiến khác ADR-018/019)
Ngày: 2026-07-28
Liên quan: [[ADR-020 Universal Event Lifecycle]], [[ADR-018 Waste Event ID Format]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]]

> **⚠️ Ghi chú đánh số:** nội dung gốc gọi ADR này là "ADR-020" (track riêng của khung chat Waste Engine). Renumber thành ADR-021 để nối tiếp track chính thức của vault.
>
> **⚠️ Ghi chú nguồn (minh bạch, không phải Flag):** cùng mức độ nguồn như [[ADR-020 Universal Event Lifecycle]] — chỉ nhận qua bản tóm tắt GPT relay qua Thanh, không chứng kiến trực tiếp trong khung chat này.

---

## Context

TECH_UNIT_DROPDOWN (V1) dùng `XLOOKUP(Item Code)` để join với `WASTE_LOG` — gây silent corruption khi Item Code trùng (case Stroganoff 2 dòng: `XLOOKUP` luôn trả dòng đầu, dòng thứ 2 bị gán nhầm dữ liệu). Cần 1 nguyên tắc kiến trúc ngăn lỗi loại này tái diễn ở tầng khác.

## Decision

**Nguyên tắc:** Projection không được chứa Business Rule. Business Rule thuộc về 1 lớp riêng: `ACTIVE_WASTE_EVENTS`.

```
Pipeline: WASTE_LOG → Gatekeeper → ACTIVE_WASTE_EVENTS → TECH → Compiler → Ledger

ACTIVE_WASTE_EVENTS = Projection View thuần
  - không nhập tay
  - không Apps Script
  - không sinh ID
  - không Normalize
  - không Compile
  - chỉ Project các Event đã đạt VALID + Event ID <> blank (State 2 — xem [[ADR-020 Universal Event Lifecycle]])
    cho downstream dùng
```

**Insight bổ sung — Join Illusion → Trace Key:** TECH không cần Join `WASTE_LOG` — chỉ cần đọc Projection (`ACTIVE_WASTE_EVENTS`), giữ nguyên quan hệ 1:1 theo dòng (không cần XLOOKUP theo Item Code, loại bỏ hẳn rủi ro join thay vì chỉ vá nó). Event ID chuyển vai trò từ **Join Key** → **Trace Key** (chỉ dùng để Trace/Audit/Ref ID/Parent ID, không dùng để tính toán) — Normalize vẫn dùng `Item Code` để tra Master Data.

## Consequence

- TECH và Compiler trở thành "dumb processor" — khi Business Rule đổi, chỉ sửa `ACTIVE_WASTE_EVENTS`, không đụng TECH/Compiler.
- Thiết kế đủ tổng quát để tái dùng cho `PREP_LOG`/`PRODUCTION_LOG`/`TRANSFER_LOG` sau này mà không cần TECH riêng cho từng module — **chưa kiểm chứng, chỉ là kỳ vọng thiết kế**, không phải Reality Test đã chạy.
