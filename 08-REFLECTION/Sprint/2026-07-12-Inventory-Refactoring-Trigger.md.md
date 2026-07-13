# REFLECTION — Inventory Refactoring Trigger
**Ngày:** 2026-07-12
**Status:** DRAFT (Chưa Freeze)
**Triggered by:** Reality (Staff feedback: "Inventory quá nặng để nhập liệu trên điện thoại")

## 1. Reality lên tiếng
Hệ thống đúng về mặt kỹ thuật, nhưng không đúng với người sử dụng. Việc staff thấy nhập liệu nặng nề là tín hiệu báo động: Kiến trúc hiện tại đang trộn lẫn quá nhiều trách nhiệm (Responsibility) vào cùng một Workspace.

## 2. Discovery 01 — Workspace ≠ Data Store
PREP_LOG không phải là kho lưu dữ liệu (Data Store). Nó là *Workspace* (Bàn làm việc). Nhiệm vụ của nó là giúp Human thao tác nhanh nhất. Sau khi việc xong, Workspace có thể được dọn dẹp. Thứ duy nhất cần giữ lại vĩnh viễn là Business Event đã được tạo ra.

## 3. Discovery 02 — "Lifetime" trở thành chiều thiết kế mới
Không phải Object nào cũng có tuổi thọ giống nhau:
* **Workspace:** Sống trong 24 giờ (1 ca/1 ngày làm việc).
* **Review/Transaction:** Sống đến khi được duyệt/commit.
* **Ledger:** Sống vĩnh viễn (Lịch sử).
* **Stock Position:** Chỉ phản ánh khoảnh khắc hiện tại (Realtime).
=> Kiến trúc phải xuất phát từ vòng đời dữ liệu, không chỉ từ chức năng.

## 4. Discovery 03 — Inventory = Cảm biến học tập (Learning Sensor)
Inventory không tồn tại chỉ để đếm xem còn bao nhiêu hàng. Nó tồn tại để giúp Leader nhìn thấy Thực tại: Yield thay đổi, Waste tăng, Shelf Life giảm... Lịch sử (History) không phải đích đến, nó là nguyên liệu để học hỏi, điều tra nguyên nhân và điều chỉnh vận hành.

## 5. Kết luận & Quyết định hành động
* **Chưa chốt Solution:** Khoan quyết định việc tách sheet hay viết code dọn rác.
* **Quyết định mở Project Alpha:** Mở dự án *Inventory Refactoring Project Alpha* để định nghĩa lại hoàn toàn cách Human Workspace và System Engine tương tác.
* **Bài học tối cao:** "Reality is the final authority". Mọi thay đổi kiến trúc phải xuất phát từ những điều Reality đang diễn ra, không phải từ trí tưởng tượng của AI.