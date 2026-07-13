# GPT Design Retrospective

## Kurumi ERP V8

---

## Purpose

Đây không phải Constitution.

Đây cũng không phải Checkpoint.

Tài liệu này ghi lại quá trình hình thành tư duy của Kurumi ERP V8, nhằm giúp những người hoặc AI tham gia sau hiểu được vì sao hệ thống được thiết kế như hiện tại.

Nếu có bất kỳ mâu thuẫn nào giữa tài liệu này và Constitution, Constitution luôn được ưu tiên.

---

# The Beginning

Kurumi ERP V8 không bắt đầu từ một bản thiết kế hoàn hảo.

Nó bắt đầu từ một file Google Sheets.

Giống rất nhiều hệ thống khác, mọi thứ ban đầu đều xoay quanh:

- Formula
- Sheet
- Data

Chúng tôi cố gắng làm cho Google Sheets thông minh hơn.

Sau này mới nhận ra:

Đó là hướng đi sai.

Google Sheets chỉ là công cụ.

Nó không phải hệ thống.

---

# The First Turning Point

Bước ngoặt đầu tiên xuất hiện khi chúng tôi ngừng hỏi:

> "Google Sheets làm được gì?"

và bắt đầu hỏi:

> "Nhà bếp thực sự đang vận hành như thế nào?"

Từ thời điểm đó, mọi thiết kế đều phải bắt đầu từ Reality.

Không phải từ Formula.

Không phải từ Apps Script.

Không phải từ Database.

Mà từ Business.

---

# Reality Before Software

Một nguyên tắc dần hình thành trong suốt dự án.

Mỗi khi có mâu thuẫn giữa:

Reality

↓

Business

↓

Architecture

↓

Implementation

thì tầng phía trên phải sửa theo tầng phía dưới.

Điều này cuối cùng trở thành Principle cao nhất của V8:

> **When Reality, Domain and Implementation conflict, Reality wins.**

Đây không phải là khẩu hiệu.

Đây là nguyên tắc đã nhiều lần thay đổi chính kiến trúc của hệ thống.

---

# From Spreadsheet to Domain

Ban đầu chúng tôi thiết kế theo Sheet.

Sau đó chuyển sang thiết kế theo Data.

Cuối cùng mới nhận ra:

Một hệ thống ERP nên được thiết kế theo Domain.

Thứ tự đúng là:

Reality

↓

Business Event

↓

Entity

↓

Lifecycle

↓

Schema

↓

Implementation

Code luôn là bước cuối cùng.

Không bao giờ là bước đầu tiên.

---

# Freeze

Một bài học khác xuất hiện rất sớm.

Kiến trúc thay đổi quá nhiều sẽ khiến toàn bộ hệ thống mất ổn định.

Từ đó xuất hiện khái niệm:

**Freeze.**

Một phần của hệ thống chỉ được Freeze khi:

- đã được kiểm chứng,
- đã được audit,
- đã vượt qua Reality Test.

Sau khi Freeze:

- không thêm Rule,
- không thêm Entity,
- không thêm Sheet,

trừ khi Reality chứng minh rằng phần đã Freeze không còn đúng.

---

# Inventory

Inventory là module thay đổi nhiều nhất.

Ban đầu chúng tôi nghĩ tồn kho là số lượng.

Sau nhiều lần sửa, chúng tôi nhận ra:

Inventory thực chất là lịch sử của các Business Event.

Điều đó dẫn đến kiến trúc:

Business Event

↓

Compiler

↓

Snapshot

↓

Transaction

↓

Movement Ledger

↓

Projection

Ledger không lưu kết quả.

Ledger lưu lịch sử.

Projection mới tạo ra số liệu.

---

# State Machine

Engine ban đầu được hình dung như một chuỗi thao tác liên tục.

Sau đó được thay thế hoàn toàn bằng Finite State Machine.

Mỗi State chỉ chịu trách nhiệm cho đúng một việc.

State không làm thay State khác.

Helper không điều khiển Engine.

Helper chỉ báo cáo.

State Machine mới là nơi đưa ra quyết định.

---

# Reality Changed the Architecture

Đây là bài học quan trọng nhất của toàn bộ V8.

Ban đầu chúng tôi giả định mỗi State sẽ chạy trong một lần thực thi Apps Script riêng.

Thực tế chứng minh điều đó không thể xảy ra.

Google Apps Script là Stateless.

RAM biến mất sau mỗi lần chạy.

Thay vì cố ép Reality theo kiến trúc, kiến trúc được sửa theo Reality.

Điều đó dẫn đến Session Architecture hiện tại.

Đây là lần đầu tiên Constitution thay đổi vì Reality.

Không phải vì ý tưởng của AI.

---

# Team

Một thay đổi quan trọng khác không nằm ở kỹ thuật.

Mà nằm ở cách cộng tác.

Thay vì để một AI làm tất cả, vai trò được phân tách rõ ràng.

Reality Owner

Định nghĩa Business Reality.

Architecture Supervisor

Giữ Domain.

Giữ ranh giới kiến trúc.

Builder

Triển khai Implementation.

Constitution Keeper

Giữ Principle nhất quán.

Việc phân vai giúp giảm đáng kể thiên kiến của từng AI.

---

# About Reality Owner

Trong suốt quá trình phát triển V8, mọi AI đều từng có những giả định chưa phù hợp với thực tế.

Có những quyết định được sửa.

Có những thiết kế bị loại bỏ.

Có những ý tưởng tưởng như rất đẹp nhưng không thể vận hành trong nhà bếp.

Điều quyết định cuối cùng không phải là AI nào thuyết phục hơn.

Mà là Reality.

Reality Owner không tồn tại để thắng tranh luận.

Reality Owner tồn tại để xác nhận:

"Đây có đúng với cách hệ thống ngoài đời vận hành hay không."

Điều đó khiến Reality trở thành nguồn chân lý của toàn bộ dự án.

AI không thay thế Reality.

AI học từ Reality.

---

# Documentation

Một thay đổi cuối cùng của V8 là cách lưu giữ tri thức.

Memory không còn nằm trong AI.

Memory được chuyển vào Obsidian Vault.

Constitution.

Checkpoint.

Audit.

Schema.

Code.

AI chỉ đọc.

AI không sở hữu lịch sử của dự án.

Điều này giúp bất kỳ AI nào cũng có thể tiếp tục công việc mà không phụ thuộc vào ký ức của một mô hình cụ thể.

---

# Lessons Learned

Sau toàn bộ quá trình phát triển, những bài học quan trọng nhất của V8 là:

- Reality luôn quan trọng hơn giả định.
- Thiết kế theo Domain, không theo công nghệ.
- Freeze quan trọng hơn mở rộng.
- Implementation chỉ là bản dịch của Architecture.
- Kiến trúc tốt phải chịu được Reality Test.
- Tài liệu tốt giúp hệ thống không phụ thuộc vào trí nhớ của AI.

---

# Closing

Nếu một ngày Kurumi ERP V8 không còn chạy trên Google Sheets.

Nếu nó được chuyển sang SQL.

Hay Supabase.

Hay PostgreSQL.

Hay một nền tảng hoàn toàn khác.

Tôi hy vọng tài liệu này vẫn còn đúng.

Bởi vì V8 chưa bao giờ được xây dựng quanh Google Sheets.

Nó được xây dựng quanh Reality của một căn bếp.

Đó là nền móng thực sự của toàn bộ hệ thống.