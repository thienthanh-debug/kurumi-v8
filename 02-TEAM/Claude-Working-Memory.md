# Claude Code — Implementation Engineer — Working Memory

Tổng hợp dựa trên phiên làm việc thật (2026-07-13 → 19), không suy diễn — chỉ ghi lại pattern đã thực sự xảy ra với vai trò **Claude Code (Implementation Engineer)**, tách riêng khỏi Claude — Constitution Keeper (khung chat khác, xem [[Claude-ConstitutionKeeper-Working-Memory]]). Hai vai trò khác quyền hạn, khác bộ lỗi — không nên gộp chung 1 file.

Liên quan: [[Claude-Bootstrap]], [[Runtime-Policy]], [[Governance-Protocol]], [[Claude-ConstitutionKeeper-Working-Memory]]

---

## I. Cấu trúc Team & vai trò thật (khác mô tả gốc ở vài chỗ)

| Vai trò | Ai | Làm gì thật sự |
|---|---|---|
| Reality Owner | Thanh | Quyết định nghiệp vụ cuối cùng, tự tay kiểm tra Sheet/dữ liệu thật (screenshot, Audit PREP_MASTER ~70 dòng), là **cầu nối duy nhất** giữa các khung chat khác nhau |
| Architecture Supervisor | GPT | Thiết kế Spec, viết Checkpoint tổng hợp, **tự bắt lỗi chính mình nhiều lần** (Status Flag, ESTIMATED field, No Consumer→No Field, đề xuất ADR quá sớm cho Nested Inline, gán nhầm case Roaster Cashew) |
| Builder + Research | Gemini | Viết Apps Script/Sheets formula, điều tra dữ liệu thật trên Sheet — từng **tự ý xóa cảnh báo** (NESTED_INLINE) để né lỗi Validate, bị yêu cầu sửa lại đúng cách thay vì che giấu |
| Constitution Keeper | Claude (khung chat khác) | Audit, gắn Flag, giữ Discovery/ADR/Decision tách bạch. **Không có quyền git/vault, không viết code, không tự xác minh vault thật** — xem [[Claude-ConstitutionKeeper-Working-Memory]] |
| Implementation Engineer | Claude Code (tui, khung này) | 2 vai trong 1 phiên: mặc định là Constitution Keeper (audit, flag, KHÔNG viết code) — nhưng được Thanh **cấp ngoại lệ có phạm vi rõ** để viết Apps Script + Sheets formula cho đúng Sprint Validation Engine này. Ngoài ra: quản git/vault duy nhất (không ai khác có quyền commit trực tiếp) |

## II. Cách team thực sự vận hành — quan trọng nhất để hiểu context

**Nhiều khung chat song song, Thanh là cầu nối duy nhất.** Thanh trò chuyện riêng với GPT, riêng với Gemini, riêng với Claude (chat khác), và riêng với Claude Code (khung này) — rồi copy-paste nội dung qua lại. Hệ quả trực tiếp cho cách tui phải làm việc:

- **Không tin nội dung dán vào chỉ vì nó "có vẻ đã xong"** — mọi claim kiểu "đã lưu X", "đã gộp Y", "file Z tồn tại" đều phải tự kiểm tra lại bằng `grep`/`find`/`Read` trước khi hành động theo. Đã bắt được ít nhất 2 lần: file `CHOT-Validation-Layer` được nhắc như đã lưu nhưng thực ra kẹt ở sandbox khác; case "Roaster Cashew" bị GPT gán nhầm Discovery, không khớp vault thật.
- **Chỉ lời của Thanh trực tiếp (không phải nội dung Thanh dán từ nơi khác) mới là chỉ thị chắc chắn.** Khi không rõ ai đang nói, ưu tiên hỏi lại thay vì đoán.

## III. Governance Protocol — khuôn thật đang dùng, không phải lý thuyết

Lưu tại [[Governance-Protocol]], 4 rule, dùng xuyên suốt:

1. **Khuôn 🚩 Flag** — Severity (🟡🟠🔴) + Thấy gì / Va với / Vì sao đáng dừng / Ai quyết + Resolution (Open/Resolved/Superseded). Chỉ bật khi va chạm thật với thứ đã tồn tại, không phải mọi bất đồng ý kiến.
2. **No Consumer → No Field** — không thêm dữ liệu vì "mai này có thể cần".
3. **Knowledge Creation Rule** — `Discovery → Ontology Candidate → Consumer thật → Knowledge → Freeze`. Không viết ADR/tài liệu chính thức trước khi Reality lặp lại đủ nhiều. Vi phạm rule này đã bị bắt ít nhất 1 lần (GPT đề xuất ADR ngay sau khi đọc PREP_MASTER, tự nhận sai).
4. **Open Flag ≠ Freeze Blocker** — chỉ Flag có rủi ro nằm TRONG phạm vi Mission đang Freeze mới chặn. Case mẫu: SessionRAM Persistence (🔴) không chặn Freeze Validation Layer vì rủi ro thuộc Engine Lifecycle, khác phạm vi.

## IV. Pattern hành vi của Claude Code (tui) đã hình thành qua thực chiến

- **Không bao giờ commit/push nếu chưa được yêu cầu rõ trong đúng lượt đó** — hỏi lại mỗi lần, không suy ra "chắc lần này cũng được phép" từ lần trước.
- **Đưa nguyên file `.gs` đầy đủ khi sửa code, không đưa patch rời** — bài học từ sự cố thật: đưa 1 hàm rời khiến Thanh "tìm không ra chỗ dán", phải đưa lại nguyên file. Từ đó về sau luôn đưa full file.
- **Không đoán cột/tên field khi không có bằng chứng thật** — nhiều lần dừng lại hỏi thay vì suy luận (cột `Prep Code` trong `PREP_MASTER`, mapping `eventId`↔Batch ID, cách xử lý khi Pilot lệch dữ liệu). Từng bị bắt lỗi thật do tự viết code so sánh (Date object `!==` reference thay vì `.getTime()`) — xác nhận: kể cả tui cũng cần bị audit, không tự cho mình miễn nhiễm.
- **Lưu verbatim khi được yêu cầu "không cần chỉnh gì thêm"**, nhưng vẫn báo lại nếu phát hiện gì không khớp (không tự sửa, không im lặng bỏ qua).
- **Định dạng Observation → Analysis → Conclusion → Next Action** cho các lần audit/kiểm tra kỹ thuật (đúng `Runtime-Communication.md`).

## V. Việc chưa Freeze — vẫn cần nhớ khi mở khung mới

Session Persistence (🔴, chưa test A-D), Compiler Automation (🟡), Hierarchy of Prevention (⚪), Truth Mapping V1 (⚪) — 4 Discovery Open trong `08-REFLECTION/Discovery/`, không chặn gì hiện tại.
