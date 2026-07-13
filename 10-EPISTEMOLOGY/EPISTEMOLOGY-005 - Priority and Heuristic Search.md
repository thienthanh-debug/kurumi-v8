# EPISTEMOLOGY-005 — Priority and Heuristic Search

Status: ✅ Frozen (đã kiểm chứng bằng case biên — xem mục 5) Sprint: O2 Liên quan: [[EPISTEMOLOGY-004 - What is Adjustment]], [[FOUNDATION-002 - What is Principle]]

---

## 1. Câu hỏi kiến trúc

Khi Adjustment cần gọi lại Engine (Observation → Information) để tìm nguyên nhân FAIL, nó phải nhìn vào đâu trước? Có hàng chục khả năng (dao, cà rốt, người, cân, SOP, supplier...) — Master Chef không kiểm tra hết, ông nhìn đúng một chỗ. Cơ chế nào đứng sau việc "nhìn đúng chỗ" đó?

## 2. Câu trả lời: Priority không phải thực thể được sinh ra

**Priority không phải một Node, Module, hay dữ liệu được lưu trữ riêng.** Nó là **hệ quả tự nhiên** khi Principle đủ dày — một hành vi đọc (read behavior), không phải một thực thể mới trong Ontology.

```
Reality
   ↓
Experience
   ↓
Principle
   ↓
Priority (heuristic — hệ quả tự nhiên, không phải node riêng)
   ↓
Adjustment đọc ngược Principle
   ↓
Targeted Observation (thu hẹp)
```

Layer 2 không sinh Priority. Layer 2 chỉ **dùng** Priority để dẫn hướng Observation tiếp theo.

## 3. Vì sao không dùng từ "Probability" / "Xác suất"

Ban đầu có đề xuất mô tả cơ chế này bằng "xác suất" (kiểu 83.7%). Đây là **thuật ngữ sai bản chất, đã bị sửa.**

- Master Chef không nói "Grinder = 87%". Ông chỉ nói "Check grinder trước."
- Không ai trong thực tế vận hành tính phần trăm — họ **ưu tiên** dựa trên Experience tích lũy.
- Priority = **Heuristic Priority** (ưu tiên định tính, hình thành từ tích lũy), không phải mô hình thống kê/Bayesian.

Ví dụ tương tự trong các lĩnh vực khác: bếp trưởng nhìn món và biết nhìn nước sốt trước; bác sĩ hỏi tiền sử trước; lập trình viên thấy lỗi mở log trước — không ai tính con số, tất cả đều ưu tiên theo Experience đã tích lũy.

## 4. Discovery: Principle có hai chức năng

Sprint O1 hiểu Principle là "luật vận hành hệ thống" (điều khiển Action). Sprint O2 làm lộ ra thêm một chức năng chưa từng được nhìn thấy:

```
Principle
     │
     ├── Điều khiển Action (đã biết từ Sprint O1)
     │
     └── Điều hướng Learning — tức cung cấp Priority cho Adjustment (phát hiện ở Sprint O2)
```

**Đây không phải Principle mới.** Đây là một chức năng mới được phát hiện của Principle đã có sẵn.

> ⚠️ Ghi chú mở (chưa chốt cứng): chưa rõ đây là _một thuộc tính, hai biểu hiện_ hay _hai thuộc tính khác nhau, tình cờ cùng nguồn gốc Experience_. Sự phân biệt này không quan trọng ở tầng triết học, nhưng có thể ảnh hưởng cách Grok/Gemini thiết kế lưu trữ và truy vấn Principle khi implement. Cần quyết định khi build thật.

## 5. Kiểm chứng bằng case biên (Reality phủ quyết Discovery)

Theo nguyên tắc "Reality luôn có quyền phủ quyết Discovery", giả thuyết trên được test bằng case cố tình khác xa domain gốc (cà rốt, espresso — đều là kỹ năng tay chân lặp lại):

**Case test: Food Cost tăng lần đầu tiên, chưa từng có tiền lệ (Principle rỗng/mỏng).**

Kết quả test (theo kinh nghiệm vận hành thực tế của Reality Owner — Thanh):

> Khi FAIL loại này lần đầu xảy ra, không "quan sát mới" ngay tại thời điểm đó — mà **scan lại một kho Experience đã tích lũy liên tục từ trước** (nhân viên mới, làm ẩu, không dùng cân, tỷ lệ khách bỏ món, phản hồi kênh, thông tin từ leader...). Những quan sát này đã và đang diễn ra hàng ngày, độc lập với việc FAIL có xảy ra hay không.

### Kết luận rút ra từ case test

Không cần tách thành "hai chế độ Observation" (tức thời vs nền) như giả thuyết trung gian từng đề xuất — giả thuyết đó đã bị rút lại vì không cần thiết.

**Cách giải thích đúng và gọn hơn — một trục duy nhất: bán kính quét (scope radius) tỉ lệ với độ rộng của vấn đề:**

|Đặc điểm|Vấn đề hẹp (vd: Yield cà rốt)|Vấn đề rộng (vd: Food Cost)|
|---|---|---|
|Khoảng cách nguyên nhân — triệu chứng|Gần, gần như tức thời (cùng một đối tượng: con dao, củ cà rốt)|Xa, trải dài theo thời gian (nhiều luồng Reality khác nhau)|
|Bán kính quét của Adjustment|Nhỏ — điều chỉnh ngay trên chính Reality đang diễn ra|Lớn — cần tổng hợp nhiều nguồn Experience đã tích lũy|
|Priority hoạt động thế nào|Đọc Principle hẹp, quen thuộc|Đọc Principle từ nhiều nguồn Experience rải rác|
|Khi Principle rỗng (chưa từng có tiền lệ)|Hiếm khi xảy ra vì vấn đề hẹp thường đã có Experience|Không có cơ sở ưu tiên rõ ràng → quan sát rộng hoặc escalate cho con người quyết định hướng nhìn|

**Đây vẫn là một cơ chế Priority duy nhất** (đọc ngược Principle) — không cần thêm khái niệm, không cần thêm Node. Bán kính quét chỉ là thuộc tính của chính vấn đề đang FAIL, không phải một cơ chế riêng của Layer 2. Điều này làm giả thuyết gọn hơn, không phình ra.

### Trường hợp Principle hoàn toàn rỗng

Khi hoàn toàn chưa có Experience nào liên quan (lần đầu tuyệt đối), Adjustment không có cơ sở ưu tiên → rơi vào một trong hai nhánh, không cần quy tắc đặc biệt nào thêm vì đây là hệ quả tự nhiên của việc "đọc trên tập rỗng":

- (a) Quan sát rộng — kiểm tra đồng thời nhiều khả năng
- (b) Escalate cho con người (Reality Owner) quyết định hướng nhìn

## 6. Backlog

- Nếu khi implement, việc "truy vấn Experience nền đã tích lũy" và "quan sát mới tức thời" cần cấu trúc lưu trữ khác nhau về mặt kỹ thuật, cần quay lại xem xét có nên tách thành hai luồng riêng hay không — dù về mặt kiến trúc/triết học Sprint O2 đã kết luận là một cơ chế duy nhất.