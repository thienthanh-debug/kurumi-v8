# ADR-020 — Universal Event Lifecycle

Status: Accepted (relayed — xem ghi chú nguồn dưới, mức độ chứng kiến khác ADR-018/019)
Ngày: 2026-07-28
Liên quan: [[ADR-018 Waste Event ID Format]], [[ADR-019 Pre-Resolver Input Validation Gatekeeper]], [[ADR-021 Active View Boundary]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]]

> **⚠️ Ghi chú đánh số:** nội dung gốc gọi ADR này là "ADR-019" (đúng số trong track riêng của khung chat Waste Engine — đây chính là ADR-019 mà GPT hỏi Claude Code không có bản ghi, ở lượt trước). Renumber thành ADR-020 để nối tiếp track chính thức của vault.
>
> **⚠️ Ghi chú nguồn (minh bạch, không phải Flag):** ADR-020/021 khác ADR-018/019 ở chỗ — ADR-018/019 được chứng kiến trực tiếp quá trình Thanh trao đổi/approve/reject ngay trong khung chat Waste Engine. ADR-020/021 chỉ nhận qua bản tóm tắt GPT tự đóng gói "FROZEN" rồi Thanh relay sang — tin tưởng Thanh đã duyệt ở khung chat khác (đúng vai trò cầu nối), nhưng ghi rõ mức độ nguồn khác nhau, không lẫn lộn.

---

## Context

Sau khi ADR-018 (Event ID) và ADR-019 (Gatekeeper) Freeze, cần 1 mô hình chung mô tả vòng đời của 1 Waste Event — để Normalizer/Compiler/Resolver/Ledger biết chính xác chúng đang tiêu thụ Event ở trạng thái nào, không tự ý diễn giải.

## Decision

```
State 0 — DRAFT       = EMPTY hoặc INVALID_INPUT (không có Event)
State 1 — VALIDATED   = VALID + Event ID blank (đã hợp lệ, chưa có Identity)
State 2 — IDENTIFIED  = VALID + Event ID (Historical Fact, Lifecycle kết thúc tại đây)
```

Normalizer/Compiler/Resolver/Ledger **không làm thay đổi Lifecycle** — chỉ tiêu thụ Event ở State 2 (IDENTIFIED).

## Consequence

- State 0→1 là trách nhiệm của ADR-019 (Gatekeeper). State 1→2 là trách nhiệm của ADR-018 (Apps Script sinh Event ID). Không tầng nào khác được phép thay đổi Lifecycle State của 1 Event.
- Đặt nền cho [[ADR-021 Active View Boundary]] — Projection (`ACTIVE_WASTE_EVENTS`) chỉ project Event ở State 2.
