# CHECKPOINT — Constitution Keeper (khung chat này) — 2026-07-13

Liên quan: [[Sprint O4 Ready]] (checkpoint cùng ngày, khung Code)

## Đối chiếu với báo cáo khung Code (đã đọc toàn bộ Obsidian vault)

Không mâu thuẫn. Cả hai khung cùng chỉ vào một điểm: **bước thật tiếp theo là xây `WAIT_REVIEW`** trong Write Engine (`TRANSACTION_STAGING` → `INVENTORY_LEDGER`). Infrastructure (5 helper), Generate, Validate đã chạy thật và pass.

## Quyết định đã chốt trong phiên này (sẵn sàng để khung Code triển khai)

1. **Không tách nhiều file Google Sheets.** Lý do: 45 tab gộp 1 file vốn là để né `IMPORTRANGE` (chậm, phức tạp quyền, formula liên file) — đã từng bị V7 né vì lý do này. Giữ 1 file, tách theo **module** bên trong: CORE / MASTER DATA / WORKSPACE / ENGINE / LEDGER / READ MODEL / LOG.
    
2. **Submit Flow — exception-based, không phải duyệt-mọi-giao-dịch.** Thanh xác nhận: _"khi nào bất thường hãy đến lượt tui"_.
    
    ```
    Staff nhập → Submit → Validation
                             │
                 ┌───────────┴───────────┐
              Hợp lệ                 Bất thường
                 │                       │
            Engine tự COMMIT      WAIT_REVIEW → Thanh duyệt
                 │                       │
                 └───────────┬───────────┘
                         Ledger → Reset Workspace
    ```
    
    → Đây cũng là câu trả lời cho câu hỏi cũ "Submit là lệnh chờ duyệt hay khai báo sự thật": với giao dịch hợp lệ, Submit gần với khai báo sự thật; chỉ khi bất thường mới thành lệnh chờ duyệt. **Lưu ý xung đột:** `01-Runtime-Constitution.md` (Frozen 06/07) đang ghi WAIT_REVIEW là ranh giới bắt buộc cho **mọi** giao dịch — cần sửa lại khi ghi vào vault chính thức, không để 2 bản mô tả song song.
    
3. **Data Taxonomy (trục ngang, trực giao với Operational Pipeline):** Master Data / Configuration / Reference Data / **Security** (giữ tách riêng — KHÔNG gộp chung "Observability", vì `SYSTEM_MASTER` (tài khoản/phân quyền) là Security thật, khác bản chất với `ERROR_LOG`/`AUDIT_LOG` (Observability)).
    
4. **Workspace phải thiết kế theo Reality thật của 1 ca làm việc**, không theo dung lượng tối đa giả định. Kèm giới hạn formula range, dropdown, conditional formatting theo đúng số dòng thật (không quét cả cột / cả 1000 dòng).
    

## Phát hiện Reality đã verify bằng code thật (không phải suy đoán)

- **`EVENT_REGISTRY` chưa được xếp vào bất kỳ nhóm Taxonomy nào** trong ma trận Gemini đưa ra — cần bổ sung.
- **`PREP_LOG` CHƯA được tối ưu như GPT tưởng.** Kiểm tra trực tiếp file: 5 cột công thức (`D`, `G`, `J`, `K`, `L`) đều là ArrayFormula chạy full `...2:...1000`, không giới hạn theo Reality (~50-60 dòng/ngày). Bước 3 (Formula Audit) của Sprint O4 là việc thật cần làm, chưa xong.
- **Nguyên nhân ~15 giây mở file trên mobile CHƯA được kiểm chứng rõ**: chưa có phép so sánh với bản file đã rút gọn (chỉ giữ Workspace) để biết đây là chi phí cố định của Google Sheets hay do tổng khối lượng file. Việc trước mắt (giới hạn formula/dòng) vẫn nên làm vì có lợi bất kể kết quả, nhưng câu hỏi "có cần tách file không" vẫn để mở.

## Khớp với gap mà khung Code phát hiện

Khung Code xác nhận `01-Reality_and_Domain.md` và `00-Mission.md` vẫn còn nguyên câu hỏi chưa trả lời từ đầu dự án: **Workspace là gì? Ledger là gì? Event là gì? History là gì? Review là gì? Lifetime từng Object?** — phiên chat này đã _trả lời một phần_ qua thực hành (ví dụ Workspace = dữ liệu 24h theo Reality ca làm, Ledger = vĩnh viễn/append-only), nhưng **chưa viết chính thức vào file vault** — vẫn là việc tồn đọng.

## Việc tiếp theo đề xuất

Viết đặc tả `WAIT_REVIEW` theo hướng exception-based đã chốt ở mục 2 (quy tắc nào tính là "bất thường" để đẩy qua Review, còn lại Engine tự Commit) — đưa thẳng cho khung Code triển khai, không cần bàn kiến trúc lại.