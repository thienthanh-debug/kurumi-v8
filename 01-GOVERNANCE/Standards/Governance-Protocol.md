# Governance Protocol — Kurumi V8

Lần đầu lưu chính thức: 2026-07-14 (đã dùng thực tế từ đầu Sprint Validation Engine, nay mới đưa vào vault)

---

## 1. Khuôn Flag

Dùng khi phát hiện điều gì đó va chạm với Foundation/Constitution/ADR/Spec/Code/Reality đã có. Không phải mọi ý kiến khác nhau đều thành Flag — chỉ bật khi có va chạm thật với thứ đã tồn tại.

```
🚩 FLAG — [Tên vấn đề]

Severity: 🟡 (không chặn, có thể tiếp tục) / 🟠 (nên dừng review) / 🔴 (không được merge/Freeze phần liên quan)

Thấy gì: mô tả cụ thể, trích nguyên văn nếu có — không diễn giải mơ hồ.

Va với: Foundation / Constitution / ADR / Spec / Code / Reality — chỉ thẳng tài liệu hoặc quyết định cụ thể đang bị đụng.

Vì sao đáng dừng: hậu quả cụ thể nếu bỏ qua — không phải "nghe không ổn", phải chỉ ra chuyện gì thật sự xảy ra.

Ai quyết: Thanh, hay có thể tự sửa không cần hỏi.

Resolution: Open / Resolved / Superseded
```

Buộc mọi phản biện phải chứng minh thay vì chỉ nêu ý kiến — đúng tinh thần RFC Comment / Design Review, tối giản cho AI collaboration.

---

## 2. Rule — No Consumer → No Field

Reference Context (batch context map, lookup object...) chỉ được phép chứa dữ liệu mà ít nhất một consumer hiện tại đang sử dụng. Không thêm field vì "mai này có thể cần" — khi consumer thật xuất hiện, thêm field lúc đó, không refactor interface.

Đo được bằng code: có hàm nào đọc field này không? Không có → field không nên tồn tại.

---

## 3. Rule — Knowledge Creation Rule

Một tài liệu chỉ được sinh ra khi có ít nhất một Reality Consumer. Một khái niệm chỉ được định nghĩa khi Discovery đã xuất hiện từ Reality. Không tạo tài liệu vì dự đoán sẽ hữu ích trong tương lai. Knowledge là kết tinh của Discovery, không phải kế hoạch của tưởng tượng.

Thứ tự đúng: `Discovery → Ontology Candidate → Consumer xuất hiện → Knowledge → Freeze`. Sai: `Knowledge Backlog → đi tìm Reality`.

Khi nghi ngờ có nên viết 1 tài liệu Ontology/Pattern/ADR mới hay không — hỏi: Discovery này đã lặp lại đủ nhiều lần, có consumer thật chưa, hay chỉ là "thấy thiếu nên viết"? Nếu là vế sau — không viết.

---

## 4. Rule — Open Flag ≠ Freeze Blocker

Ba khái niệm khác nhau, không được gộp:

- **Discovery**: ghi nhận Reality chưa được mô hình hiện tại giải thích hết. Không kết luận, không chặn gì.
- **Open Flag**: vấn đề đã xác định, có Severity, chưa Resolved. Một hệ thống sống luôn có Open Flag — đòi "zero Open Flag" mới Freeze nghĩa là không bao giờ Freeze được.
- **Freeze Blocker**: Flag mà phạm vi rủi ro nằm BÊN TRONG Mission đang xin Freeze.

**Tiêu chí phân biệt:** Một Flag là Freeze Blocker khi và chỉ khi phạm vi rủi ro của nó thuộc về chính Mission đang Freeze. Nếu rủi ro thuộc về Mission/Layer khác (kể cả liên quan trực tiếp), Flag đó KHÔNG chặn Freeze — chỉ cần đảm bảo đã ghi lại đầy đủ trong Discovery/Reflection để không mất dấu.

Ví dụ áp dụng (Sprint Validation Engine, 2026-07-14): "SessionRAM Persistence across WAIT_REVIEW" là 🔴 nhưng KHÔNG chặn Freeze Validation Layer, vì rủi ro nằm ở ranh giới Engine Lifecycle (WAIT_REVIEW→COMMIT qua nhiều execution), không phải ở Validation Rule (phạm vi đang Freeze).

Khi mở Freeze Checklist cho bất kỳ Mission nào, phải có bảng Freeze Blocker Matrix liệt kê từng Open Flag hiện có + lý do có/không phải Blocker — không được mặc định "còn Flag = chưa Freeze được" mà không giải thích.

---

## 5. Rule — Domain Authority (hỏi Thanh khi đụng chuyên môn vận hành, không hỏi khi thuần kỹ thuật IT)

Thanh là Head Chef — có chuyên môn vận hành bếp/nhà hàng thật, KHÔNG có chuyên môn IT.

**Chỉ hỏi Thanh khi** quyết định liên quan tới thực tế vận hành hoặc thuộc chuyên môn của Thanh (bếp, nguyên liệu, quy trình, công thức, ý nghĩa nghiệp vụ, số liệu thực tế...).

**Không hỏi Thanh** những gì thuần kỹ thuật IT (hệ thống xử lý bên trong ra sao, cấu trúc code, thuật toán, cách lưu trữ dữ liệu...) — đây không phải chuyên môn của Thanh, Thanh không cần và không muốn bị hỏi.

---

## Nguồn gốc

Mục 1-4 sinh ra từ Discovery thật trong Sprint Validation Engine (2026-07-13 → 14), không phải thiết kế trước — đúng tinh thần Mục 3. Xem [[CHECKPOINT-CHOT-PHIEN-2026-07-14]] và các Discovery trong `08-REFLECTION/Discovery/` ([[Discovery — Truth Mapping V1]], [[Flag — SessionRAM Persistence across WAIT_REVIEW]], [[Flag — Compiler Automation vs Frozen Contract]]) để biết bối cảnh từng rule sinh ra từ va chạm nào.

**Lưu ý (2026-08-10):** một "Mục 5 — IT Decision Authority" từng bị thêm vào tài liệu này dựa trên nội dung checkpoint relay từ Phase D.7C, sau đó một checkpoint khác tự audit và xác nhận rule đó là AI_SELF_PROPOSED — chưa từng có xác nhận trực tiếp của Thanh trong bất kỳ khung chat nào. Đã gỡ khỏi tài liệu theo đúng Mục 4 khuôn Flag (không có thẩm quyền → không đứng trong Governance Protocol).

Mục 5 hiện tại ("Domain Authority") là bản thay thế, nội dung do chính Thanh xác nhận trực tiếp trong chat ngày 2026-08-10 (không phải AI soạn rồi Thanh gật đầu — Thanh nêu tiêu chí, AI chỉ ghi lại nguyên văn): ranh giới hỏi/không hỏi dựa trên chuyên môn thật của Thanh (Head Chef, vận hành bếp) chứ không phải danh sách tiêu chí kỹ thuật (test/an toàn/fail-closed...) như bản cũ.
