# ADR-018 — Waste Event ID Format (Human-Readable, Immutable)

Status: Accepted
Ngày: 2026-07-27
Liên quan: [[ADR-017 Snapshot ID Format]], [[ADR-019 Pre-Resolver Input Validation Gatekeeper]], [[WASTE-ENGINE-CHECKPOINT-2026-07-22]]

> **⚠️ Ghi chú đánh số:** nội dung gốc (từ khung chat Waste Engine) gọi ADR này là "ADR-017" — trùng số với [[ADR-017 Snapshot ID Format]] đã Freeze trong vault (2026-07-22, về Snapshot ID của `TRANSACTION_STAGING`, chủ đề hoàn toàn khác). Đây là 2 track đánh số ADR song song chưa từng đồng bộ. Đã renumber thành ADR-018 để không đè lên ADR-017 hiện có — nối tiếp đúng thứ tự trong vault chính thức.

---

## Context

`WASTE_LOG`/`WASTE_COMPILER` cần 1 Event ID ổn định cho mỗi dòng Waste — vừa làm Join Key giữa `WASTE_LOG` và `TECH_UNIT_DROPDOWN`, vừa làm Ref ID/Parent ID cho các Transaction do Resolver sinh ra (1 Waste Event → N Transaction).

Đề xuất ban đầu dùng UUID (`WST-550e8400-e29b-...`) — **mâu thuẫn trực tiếp với [[ADR-017 Snapshot ID Format]] Rule 05** (Human Readable, không dùng UUID ngẫu nhiên). Một tuyên bố "FREEZE hoàn toàn" mô tả UUID sau đó bị xác nhận **không hợp lệ** — không khớp quyết định thật của Thanh.

## Decision

```
Pattern: <Branch Prefix>-WST-<YYMMDD>-<Daily Sequence>
Ví dụ:   DN-WST-260727-014, DN-WST-260727-015

Cơ chế:  Apps Script + LockService/Atomic Counter
         (tránh 2 staff cùng lúc lấy trùng sequence)

Write-once static value — không đổi dù sửa Qty/Reason/sort/insert/delete.
Cấm: =ROW(), =NOW(), ghép chuỗi động, không cập nhật lại ID sau khi đã sinh.

Trigger sinh Event ID: Validation Status = VALID AND Event ID blank
  → generate once, write static, never overwrite
  (điều kiện "VALID" do ADR-019 Gatekeeper định nghĩa)
```

Đạt đủ 6 tiêu chí: Human Readable ✅, Unique ✅, Immutable ✅, Concurrent-safe ✅, Join key ổn định ✅, Ledger trace dễ ✅ — nhất quán với nguyên tắc Human-Readable đã Freeze ở [[ADR-017 Snapshot ID Format]].

## Consequence

- Event ID sinh **sau** Gatekeeper (ADR-019), không sinh cùng lúc với nhập liệu — vì điều kiện trigger phụ thuộc Validation Status.
- Không dùng Event ID để Join dữ liệu tính toán (xem [[ADR-021 Active View Boundary]] — insight "Join Illusion → Trace Key": Event ID chỉ dùng Trace/Audit/Ref ID/Parent ID, không dùng để tính toán).
- `WASTE_COMPILER` giữ **BLOCKED** cho tới khi cơ chế sinh ID này implement xong và test qua case duplicate Item Code + insert/delete row.
