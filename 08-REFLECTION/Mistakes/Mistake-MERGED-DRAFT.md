Dưới đây là kết quả phân tích, tổng hợp và làm gọn 10 ghi chú "Mistake" trong dự án của bạn. Nội dung được viết lại một cách đơn giản, dễ hiểu, không lạm dụng thuật ngữ kỹ thuật phức tạp và bám sát chính xác các tài liệu ADR đi kèm.

---

### PHẦN 1: CÁC GHI CHÚ TRÙNG HOẶC TƯƠNG ĐỒNG NHAU (ĐÃ GỘP)

#### Nhóm 1: Vội vã đóng băng lý thuyết khi chưa thử thách ở nhiều lĩnh vực khác nhau
* **Các file gộp lại**: 
  1. `Mistake — Premature Freeze.md`
  2. `Mistake-Single Domain Bias.md.md`
* **Bài học rút ra**: 
  Khi một công thức hay giả thuyết hoạt động tốt trên một hoặc hai lĩnh vực có cùng tính chất (ví dụ: Yield và Espresso — đều là các kỹ năng thực hành lặp đi lặp lại), chúng ta thường có xu hướng muốn khóa (Freeze) và áp dụng cố định công thức đó ngay. Điều này rất dễ dẫn đến sai lệch. 
  Để đảm bảo công thức thực sự đúng, bắt buộc phải thử nghiệm nó trên các lĩnh vực có tính chất hoàn toàn khác biệt (ví dụ: Food Cost — lĩnh vực tổng hợp nhiều biến số phức tạp). Nếu chưa thử thách giả thuyết qua nhiều lĩnh vực khác nhau để cố gắng tìm ra điểm chưa hoàn thiện, tuyệt đối không được vội vàng đóng băng lý thuyết.

#### Nhóm 2: Rò rỉ ranh giới giữa các bộ phận và tự làm phình to hệ thống
* **Các file gộp lại**: 
  1. `Mistake — Boundary Leak.md.md`
  2. `Mistake — Ontology Explosion.md.md`
* **Bài học rút ra**: 
  Mỗi bộ phận (Module) chỉ được phép làm đúng một nhiệm vụ duy nhất của mình (Single Responsibility). Việc một bộ phận tự ý lấn sân sang việc của bộ phận kế tiếp (ví dụ: bộ phận Đánh giá lại đi làm luôn việc Chẩn đoán; hoặc bộ phận Mô tả khách quan lại tự tiện chèn thêm các tính từ phán xét như "lệch", "tốt", "xấu") là sai lầm. 
  Đồng thời, không được tự vẽ thêm các quy trình/khái niệm mới song song nếu các quy trình cốt lõi sẵn có đã đủ khả năng giải quyết vấn đề. Sự rò rỉ ranh giới này thường chỉ lộ ra khi ghép nối các bộ phận được viết độc lập lại với nhau. Nếu thấy bất kỳ dấu hiệu lấn sân nào, cần dừng lại và kiểm tra ngay lập tức để giữ ranh giới sạch sẽ.

---

### PHẦN 2: CÁC GHI CHÚ RIÊNG BIỆT (ĐÃ VIẾT LẠI CHO DỄ HIỂU)

#### 3. Phân biệt rõ ràng giữa "Trạng thái" và "Bộ phận chức năng" (Module vs State)
* **File liên quan**: `Mistake  Module vs State  Resolved.md.md` (kèm `ADR-010`)
* **Bài học rút ra**: 
  Đừng nhầm lẫn giữa hai khái niệm này để tránh thiết kế sai hệ thống:
  * **Trạng thái (State)**: Là các bước trong chu kỳ chạy của dữ liệu (bao gồm: Tạo mới -> Kiểm tra -> Chờ duyệt -> Xác nhận).
  * **Bộ phận chức năng (Module)**: Là các công cụ thực thi (như Bộ phân tích - Parser, Bộ kiểm tra - Validator). 
  Một Bộ phận chức năng có thể được gọi ra để xử lý ở nhiều Trạng thái khác nhau. Do đó, không được phép dùng tên Bộ phận chức năng để thay thế hay gọi tên cho Trạng thái.

#### 4. Phân loại tài liệu theo Vai trò, không theo Ngôn ngữ định dạng (Role vs Language)
* **File liên quan**: `Mistake  Role vs Language  Resolved.md.md` (kèm `ADR-011`)
* **Bài học rút ra**: 
  Các tài liệu sản phẩm (Artifact) trong hệ thống phải được phân loại dựa trên **Vai trò** (nhiệm vụ) của chúng trong quy trình làm việc. Định dạng file hay ngôn ngữ viết ra tài liệu đó (như Python, Markdown, Google Sheet, JSON...) chỉ là cách thức lưu trữ/hiển thị thông tin, không phải là cơ sở để phân loại tài liệu.

#### 5. Quy trình một chiều: Tài liệu quyết định Bộ quy tắc kiểm tra (Serialization vs Artifact)
* **File liên quan**: `Mistake  Serialization vs Artifact  Resolved.md.md` (kèm `ADR-012`)
* **Bài học rút ra**: 
  Để đảm bảo tính nhất quán, hệ thống phải tuân thủ nghiêm ngặt quy trình một chiều: 
  $$\text{Quy trình (Workflow)} \rightarrow \text{Tài liệu (Artifact)} \rightarrow \text{Bộ quy tắc (Constitution)} \rightarrow \text{Bộ kiểm duyệt (Checker)}$$
  Bộ dựng tài liệu (Builder) tuyệt đối không được tự ý lựa chọn Bộ quy tắc kiểm tra. Bộ quy tắc này phải được quyết định hoàn toàn dựa trên loại Tài liệu được sinh ra.

#### 6. Cổng phê duyệt là chốt chặn độc lập và tuyệt đối (Gate is Truth)
* **File liên quan**: `Mistake  Gate is Truth  Resolved.md.md` (kèm `ADR-014`)
* **Bài học rút ra**: 
  Cổng phê duyệt (Workflow Gate) là một chốt chặn hoàn toàn độc lập, không thuộc về AI và cũng không thuộc về Bộ dựng (Builder). Cổng này đứng chắn ngay trước Quy trình (Workflow). Nếu Cổng phê duyệt đánh giá là Thất bại (FAIL), toàn bộ quy trình phía sau tuyệt đối không được phép chạy.

#### 7. Tránh thiết kế quá phức tạp so với nhu cầu thực tế (Over Engineering)
* **File liên quan**: `Mistake — Over Engineering.md.md`
* **Bài học rút ra**: 
  Đừng thiết kế những hệ thống phụ trợ cồng kềnh khi thực tế người vận hành chỉ cần một quyết định đơn giản. Bộ kiểm tra (Validation) thực chất chỉ cần hoạt động như một công cụ so sánh Có/Không (Đúng hay Sai). Nếu phát hiện sai, chỉ cần giữ lại những lý do và dấu vết tối thiểu để bộ phận sửa đổi biết đường sửa. Nếu bạn thấy một chức năng đơn giản đang đòi hỏi cả một hệ thống con phức tạp để chạy, đó là dấu hiệu của việc làm quá mức cần thiết.

#### 8. Tránh lạm dụng các mô hình toán học hoặc cơ chế rườm rà (Wrong Abstraction)
* **File liên quan**: `Mistake — Wrong Abstraction.md.md`
* **Bài học rút ra**: 
  Đừng cố vay mượn các mô hình phức tạp (như tính toán "Xác suất %") hoặc tự vẽ ra các cơ chế riêng biệt (như chia thành "nhiều chế độ quan sát") khi thực tế con người chỉ hành động dựa trên kinh nghiệm ưu tiên đơn giản và một trục phạm vi quan sát rõ ràng. Khi xuất hiện một khái niệm mới có vẻ cần đến một mô hình toán học riêng, hãy luôn ưu tiên tìm phương án đơn giản nhất dựa trên những dữ liệu nền tảng sẵn có trước khi chấp nhận sự phức tạp mới.