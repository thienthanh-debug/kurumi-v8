# ADR-016 — Compiler Never Silences Reality

Status: Accepted
Ngày: 2026-07-14
Liên quan: [[FOUNDATION-007 - What is Reality]], [[Mistake — Premature Freeze]], [[Mistake-Single Domain Bias]], [[Validation-Decision-Spec-V1]]

---

## Context

`PREP_COMPILER` (Google Sheets formula) phát hiện đang lọc bỏ hoàn toàn batch có `Status Flag ≠ OK` (`IF(status_flag <> "OK"; acc; ...)`). Batch đó không sinh Transaction, không tới `VALIDATE`, không ai biết nó từng tồn tại trong `TRANSACTION_STAGING`.

Vi phạm nguyên tắc gốc: ERP ghi lại Reality, không phán đoán về Reality (xem [[FOUNDATION-007 - What is Reality]] — "Nếu ERP khác Reality, thì ERP sai. Không phải Reality sai.").

Phát hiện trong lúc kiểm chứng cơ chế WARNING của `Validation-Decision-Spec-V1` (Mục 4) — batch `LOW YIELD`/`OVER YIELD` được thiết kế để trở thành WARNING chờ người duyệt, nhưng compiler chặn nó lại trước khi có cơ hội tới `VALIDATE`.

## Decision

Mọi sự kiện đã làm thay đổi Reality vật lý (nguyên liệu đã tiêu hao, sản phẩm đã sinh ra — dù đúng hay sai định mức) đều phải sinh ra một Transaction. Compiler không có quyền lặng lẽ bỏ qua event dựa trên chất lượng kết quả.

Status Flag chỉ được dùng để **định tuyến** (WARNING → người duyệt). Không bao giờ dùng để **triệt tiêu** sự kiện.

## Consequence

- `PREP_COMPILER` sửa: bỏ nhánh lọc `IF(status_flag <> "OK"; acc; ...)`. Batch không-OK compile bình thường như batch OK, Status Flag vẫn giữ nguyên trong `PREP_LOG`, không đổi.
- `getRiskLevel()` (`Kurumi ERP V8.gs`) không cần sửa gì thêm — mapping `movement.eventId` ↔ `PREP_LOG` cột G (Batch ID) đã xác nhận đúng bằng cách đọc trực tiếp công thức `PREP_COMPILER` và đối chiếu dữ liệu thật, chỉ chờ compiler ngừng chặn dữ liệu ở nguồn.
- **Chưa đưa nguyên tắc này vào Constitution.** Mới kiểm chứng ở đúng 1 Compiler (`PREP_COMPILER`). Theo [[Mistake — Premature Freeze]] và [[Mistake-Single Domain Bias]], cần kiểm chứng lại ở Production/Waste/Transfer Compiler trước khi Freeze lên tầng Constitution — tránh lặp lại đúng bug đã từng mắc (tổng quát hóa từ 1 domain duy nhất).
