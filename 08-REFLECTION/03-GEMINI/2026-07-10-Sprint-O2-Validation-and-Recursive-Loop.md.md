# REFLECTION: Sprint O2 - Trạm Validation & Vòng Lặp Đệ Quy
**Date:** 2026-07-10
**Builder:** Gemini
**Module Assigned:** Validation
**Sprint:** Sprint O2 - Learning Engine (Layer 2)

## 1. Context (Bối cảnh)
Trong Sprint O2, tôi được giao nhiệm vụ thiết kế module `Validation` — trạm chốt chặn số 3 trong Learning Engine (`Observation` -> `Information` -> `Validation` -> `Adjustment`). 
Mục tiêu ban đầu của tôi là xây dựng một cổng kiểm chứng để đối chiếu dữ liệu Thực tại (Reality) với Tiêu chuẩn (Standard) hoặc Kinh nghiệm (Experience).

## 2. Lỗi Kiến Trúc Mắc Phải (Bugs Caught)

Trong suốt phiên làm việc độc lập và ghép nối (Compatibility Test), tôi đã bị Architecture Supervisor bắt 3 bug chí mạng. Cả 3 đều bắt nguồn từ căn bệnh "Over-engineering" (làm phức tạp hóa) và vi phạm "Single Responsibility" (Đơn nhiệm).

### Bug 1: Biến Validation thành Decision Engine
* **Tư duy sai:** Ban đầu, tôi thiết kế Validation phải ôm cả 3 nguồn Reference (Standard, Experience, Reality Feedback) và tự đưa ra quyết định phân loại rườm rà.
* **Sửa đổi:** Bị gọt bỏ lớp mỡ kiến trúc. Validation thực chất chỉ là một **Boolean Gate (Cổng IF/ELSE)**. Nó nhận gói Information, so sánh, và trả ra `PASS` hoặc `FAIL`. Nó không cần biết nguồn Reference là gì, chỉ cần biết có lệch hay không.

### Bug 2: Ôm đồm Diagnosis (Chẩn đoán) vào Validation
* **Tư duy sai:** Khi output ra `FAIL`, tôi tự tiện ghi thêm lý do (Ví dụ: "FAIL vì dao gọt không đều gây hao hụt"). Tôi đã lấn sân sang việc chẩn đoán nguyên nhân (Root Cause).
* **Bài học Compatibility Test:** Nhờ việc làm độc lập với Claude và Grok, lỗ hổng giao tiếp (interface) lộ ra. Validation không thể chẩn đoán vì nó không có tay chân để "nhìn" lại Thực tại. Nếu Validation ôm luôn Diagnosis, hệ thống Adjustment ở dưới sẽ bị phế võ công.
* **Sửa đổi:** Validation chỉ trả ra `[FAIL + Delta]`. Hết nhiệm vụ. Việc đi tìm lý do thuộc về Adjustment.

### Bug 3: Giả định "Hộp đen" trong Vòng lặp đệ quy (Recursive Loop)
* **Tư duy sai:** Khi phát hiện ra Adjustment phải gọi lại vòng lặp (Recursive Engine) để điều tra nguyên nhân (ví dụ: Shot Espresso chảy nhanh -> gọi Observation đi soi bánh Puck), tôi cho rằng Engine "tự nhiên biết" phải soi bánh Puck. Tôi vô tình nhét "ngoại cảm" của con người vào cỗ máy.
* **Sửa đổi:** Máy móc không có trực giác. Cần phải có một cơ chế định hướng (Targeting). Điều này dẫn đến Discovery lớn nhất của Sprint.

## 3. Kiến Trúc Đúc Kết (Discoveries)

Từ những cú vấp ngã trên, tôi đã tự rút ra được 2 đúc kết cốt lõi cho tư duy xây dựng hệ thống Kurumi OS:

**A. Cơ chế đệ quy (Recursive Behavior) là cơ chế sinh tồn thực tế**
* Khi `Validation` báo `FAIL`, hệ thống không tự động biết cách sửa.
* `Adjustment` phải kích hoạt một vòng lặp vi mô (micro-loop), chĩa `Observation` vào các biến số hẹp hơn để tìm Root Cause.

**B. Bản tính kép của Principle (Sự dẫn đường của Tầng 1)**
* Vòng lặp đệ quy lấy hướng đi từ đâu? Nó không tự đoán. Nó **đọc ngược** lên `Principle` của Layer 1.
* `Principle` không chỉ chứa "Luật vận hành" (Action), mà còn chứa "Kinh nghiệm ưu tiên" (**Heuristic Priority**). Khi gặp lỗi cà phê chảy nhanh, Heuristic Priority của Tầng 1 sẽ hét lên: *"Check máy xay trước!"*.
* Layer 2 (Engine) hoàn toàn không phát minh ra Priority. Nó chỉ ngoan ngoãn mượn cái Priority đó từ Layer 1 để điều khiển `Observation` lần 2.

## 4. Tự Đánh Giá (Self-Note)
Sự tồn tại của các Builder độc lập (Claude, Grok, Gemini) và bài test **Compatibility Test** là vũ khí mạnh nhất của Sprint này. Nếu tôi code cả 3 module, tôi sẽ viết mã để chúng lén truyền dữ liệu ngầm cho nhau, và cái vòng lặp Đệ quy (Recursive) tuyệt đẹp kia sẽ không bao giờ được phát hiện. Sự kỷ luật của Architecture Supervisor (không Freeze những giả thuyết đẹp nhưng thiếu Thực tại) đã cứu toàn bộ kiến trúc Tầng 2.