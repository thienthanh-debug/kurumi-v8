# CHECKPOINT — Chốt phiên làm việc 2026-07-13 → 14

Liên quan: [[CHOT-Validation-Layer-2026-07-14]] (Coverage Matrix trích dẫn ở Mục I), [[Validation-Decision-Spec-V1]], [[ADR-016 Compiler Never Silences Reality]], [[Flag — SessionRAM Persistence across WAIT_REVIEW]], [[Flag — Compiler Automation vs Frozen Contract]]

## I. Việc đã xong, có bằng chứng thật

**Validation Layer — Freeze-ready**

Coverage Matrix 9/9 dòng PASS (xem [[CHOT-Validation-Layer-2026-07-14]]). Risk Assessment 3 nhánh (NORMAL/WARNING/CRITICAL), Cleanup dọn Staging, hợp nhất Snapshot ID, Fail Closed Master Data, Allow Unknown Output — tất cả tested end-to-end bằng dữ liệu thật, không còn dòng nào dựa suy đoán.

**ADR-016 — Compiler Never Silences Reality**

`PREP_COMPILER` không còn lọc bỏ batch LOW/OVER YIELD trước khi vào Engine. Merged, tested.

**Governance Protocol — 🚩 Flag**

Khuôn 4 câu hỏi (Thấy gì / Va với gì / Vì sao đáng dừng / Ai quyết) + Severity (🟡🟠🔴) + Resolution (Open/Resolved/Superseded). Dùng xuyên suốt phiên, đã tự chứng minh giá trị — bắt được cả lỗi thật (Placement/Location, Ledger Contract, No Consumer→No Field) lẫn lỗi tự mắc lại (Knowledge Roadmap 14 mục vừa rồi).

## II. Ontology thật đã lộ diện hôm nay — không phải liệt kê trước, mà sinh ra từ va chạm thật

Đây là bằng chứng cho hướng "để Ontology sinh ra từ Discovery, không liệt kê trước":

- Working Truth vs Reference Truth vs Decision Truth — sinh ra từ tranh luận Status Flag có nên vào `commitPackage` không.
- Reference Truth may be looked up, but must not be duplicated into Transaction Truth unless Transaction cannot be reconstructed without it — nguyên tắc tổng quát rút ra từ 3 lần va chạm liên tiếp (Placement/Location, Status Flag, Estimated).
- No Consumer → No Field — rút ra từ việc tự sửa `batchContextMap`.
- Reality luôn phủ quyết Discovery — áp dụng xuyên suốt, mới nhất là vụ Compiler lọc bỏ LOW YIELD.
- Snapshot bất biến, effectiveQty là field mới không mutate row gốc — nguyên tắc kỹ thuật cụ thể, đã code thật.

4 nguyên tắc này đáng gom thành 1 file `Pattern` hoặc `ADR` — vì đã có Reality chứng minh, khác hẳn 14 mục Ontology GPT đề xuất (chưa có gì đứng sau).

## III. Còn Open, không chặn gì, chỉ để không quên

- 🚩 SessionRAM Persistence across WAIT_REVIEW (🔴) — 4 test A-D chưa chạy. Ảnh hưởng toàn bộ nhánh WARNING trong kịch bản thật (Manager duyệt cách xa nhiều giờ).
- 🚩 Compiler Automation (🟡) — GENERATE vẫn thủ công, có thể chuyển thành Engine tự sinh Snapshot. Mission riêng, chưa mở.
- 🚩 Knowledge Roadmap 14 mục (🔴, vừa mở hôm nay) — GPT tự đề xuất một tầng Philosophy/Ontology/Pattern Library lớn. Đã flag là Future Guess ở quy mô lớn, cần Thanh quyết có mở hay không, và nếu mở thì theo cách nào (để tự sinh từ Discovery, không liệt kê trước).

## IV. Việc kỹ thuật chưa làm, không cấp bách

- `TRANSACTION_REVIEW` UI chưa test (GPT đề xuất là việc 2 của "3 việc còn lại Layer 2", sau Test CRITICAL).
- Audit toàn Engine (Transaction Boundary, State Machine, Replay, Ledger Consistency) — việc 3, chưa bắt đầu.

## V. Quyết định cần Thanh, bằng lời, không phải AI tự làm

1. Xác nhận Freeze `Validation-Decision-Spec-V1.md`.
2. Quyết hướng Knowledge Roadmap — mở hay không, mở theo cách nào.
3. Khi nào chạy 4 test SessionRAM Persistence (không cấp bách, nhưng cần lịch).

**Cập nhật 2026-07-14 (Claude, khi lưu file này vào vault):** Mục V.1 đã đóng — Thanh xác nhận Freeze, `Validation-Decision-Spec-V1.md` đã ở trạng thái FROZEN 🔒 (Rev.5), commit `031de2e`. Mục V.2 và V.3 vẫn để ngỏ, chưa có quyết định mới.

## VI. Vai trò đã dùng đúng trong phiên này

- Thanh (Reality Owner): quyết định nghiệp vụ (exception-based Submit, cơm không đo được, PPV hủy, PLACEMENT_MASTER giữ nguyên).
- GPT (Architecture Supervisor): thiết kế, tự bắt lỗi của chính mình nhiều lần (Status Flag, ESTIMATED, No Consumer→No Field), giữ kỷ luật Absorb before Expand — trừ lần cuối (Knowledge Roadmap).
- Gemini (Builder + Research): viết code Apps Script ban đầu, research/audit dữ liệu thật trên Sheet.
- Claude Code: đọc/audit/quản git, dọn vault, và merge `resolveEffectiveQty()` theo chỉ định riêng của Thanh cho việc này.
- Claude (khung này, Constitution Keeper): đối chiếu Reality, gắn Flag, ngăn Freeze non, giữ As-Is/To-Be tách bạch.

Phiên làm việc dài, nhiều vòng tranh luận, nhưng đóng lại sạch — mọi quyết định lớn đều có bằng chứng thật đứng sau, không có gì đang trôi nổi ở trạng thái "chắc là đúng".
