# 🚩 Discovery — Boundary Formula vs Engine

**Ngày:** 2026-07-19
**Trạng thái:** Open — chưa Freeze

## Câu hỏi

Đâu là ranh giới tối ưu giữa Google Sheets Formula (`=LET(...)`) và Apps Script Engine cho các Compiler (PREP/PRODUCTION/SALES/WASTE)?

## Reality Test đề xuất

Benchmark Generate với quy mô dữ liệu tăng dần (100, 500, 1000... Event), đo:

- **Performance** — thời gian Generate/recalc/ghi Ledger, trải nghiệm đơ hay không.
- **Maintainability** — độ dài/khả năng bảo trì công thức `LET` lồng sâu so với function Apps Script.

...trước khi quyết định chuyển bất kỳ Compiler nào.

## Nguyên tắc

Không giả định "Apps Script tốt hơn" hay "Formula tốt hơn" — để Reality Test quyết định. Không áp dụng cho toàn bộ Compiler cùng lúc; mỗi Compiler có thể nằm ở boundary khác nhau (ví dụ PREP/PRODUCTION vẫn Formula, SALES đổi Apps Script — hoặc ngược lại, tùy kết quả đo).

## Liên quan

[[ADR-016 Compiler Never Silences Reality]], [[Production-Compiler-Execution-Type-Spec-V1]], [[CHECKPOINT-2026-07-19]]
