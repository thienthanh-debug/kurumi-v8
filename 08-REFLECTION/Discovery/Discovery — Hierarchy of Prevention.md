# DISCOVERY — Hierarchy of Prevention

**Ngày:** 2026-07-14
**Trạng thái:** Draft — Observation + Open Question, chưa kết luận
**Liên quan:** Discovery — Compiler Automation, ADR-016

## Observation
Một bug không đồng nghĩa với việc Engine phải thay đổi. Cùng một bug có thể được loại bỏ ở nhiều tầng khác nhau, và nên giải quyết ở tầng cao nhất có thể trước khi rơi xuống tầng thấp hơn:

```
Reality
    │
    ▼
Operation (SOP / Workflow)
    │
    ▼
System (Sheets / UI)
    │
    ▼
Engine (Code)
```

Nguyên tắc tạm đặt tên **Hierarchy of Prevention**: khi gặp bug, hỏi theo thứ tự — Có giải bằng SOP không? → Có giải bằng Workflow không? → Có giải bằng UI không? → Mới sửa Engine. Nếu tầng trên giải quyết được, không cần đụng tầng dưới (không thêm `if`/exception vào Engine nếu SOP/Workflow đã đủ).

## Evidence
- **Bug Roaster Cashew** (2026-07-14): `PREP_LOG` bị sửa/xóa sau khi đã Generate Snapshot nhưng trước khi Commit — dữ liệu Ledger không khớp Reality hiện tại của Prep Log. Bug này CÓ THỂ giải ở nhiều tầng: thêm validation vào Engine (yếu nhất — code ngày càng nhiều exception), khóa `PREP_LOG` tại thời điểm Generate (System), hoặc SOP (Staff nhập → Leader kiểm tra → Generate → Copy → Commit).
- Quy trình nhập liệu hiện tại (Staff nhập Prep Log → Compiler tự sinh → copy/paste vào Staging → bấm nút) đã tự nhiên làm giảm mạnh xác suất xảy ra bug này — không phải nhờ Engine thông minh hơn, mà nhờ khung thời gian con người có thể can thiệp sai đã bị thu hẹp bởi chính cách thao tác.
- Dự kiến: khi chuyển sang App (Staff nhập → Generate → Commit, gọn hơn), cùng một Engine có thể không cần thay đổi gì — bug tự giảm tiếp nhờ đổi tầng Operation/System, không phải sửa Engine.

## Open Question
Có bao nhiêu bug trong V8 thật sự cần sửa Engine, và bao nhiêu bug nên được giải quyết ở tầng Operation hoặc System?

## Trạng thái
Chưa đủ Reality để nâng thành Principle chính thức — mới có 1 case cụ thể (Roaster Cashew) làm evidence. Theo Knowledge Creation Rule (01-GOVERNANCE/Governance-Protocol), cần Discovery này lặp lại/được xác nhận qua nhiều bug khác trước khi kết tinh thành Knowledge/Principle. Không mở Mission, không sửa code, không viết Governance mới tại thời điểm này.

## Liên kết
Câu hỏi "khóa PREP_LOG tại thời điểm Generate" và "auto-clear PREP_LOG sau 24-48h" (2 hướng kỹ thuật cụ thể nêu ra cùng lúc với Discovery này) đã được gộp vào Discovery — Compiler Automation, không tách file riêng — cùng vùng câu hỏi (GENERATE thuộc Engine hay Human, khi nào Snapshot được tạo).
