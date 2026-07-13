# 2026-07-10 — Sprint O2 — Priority Discovery (Claude Reflection)

Vai trò trong Sprint: Constitution Keeper / Observation Builder

---

## Những lỗi tôi mắc và đã tự sửa trong Sprint này

**1. Dùng từ "xác suất" (probability) sai bản chất.** Khi mô tả cách Adjustment chọn nơi quan sát tiếp theo, tôi dùng ngôn ngữ toán học (probability, xếp hạng khả năng). GPT chỉ ra đúng: cơ chế thực tế là Heuristic Priority — ưu tiên định tính hình thành từ Experience tích lũy, không phải mô hình thống kê. Master Chef không tính 87%, ông chỉ biết "check grinder trước". Bài học: ngôn ngữ kỹ thuật vay mượn từ lĩnh vực khác (thống kê, ML) có thể che lấp bản chất thật của cơ chế đang mô tả, dù ý tưởng cốt lõi đúng.

**2. Đề xuất "hai chế độ Observation" (tức thời vs nền) rồi phải tự rút lại.** Sau khi nghe Thanh mô tả cách vận hành thực tế cho case Food Cost (scan lại kho Experience đã tích lũy, không quan sát mới), tôi vội kết luận có hai cơ chế Observation khác nhau. Thanh chỉ ra chính xác hơn: chỉ có **một trục** — bán kính quét tỉ lệ với độ rộng của vấn đề. Không cần hai cơ chế. Bài học: khi một Reality mới không khớp hoàn toàn với giả thuyết cũ, phản xạ đầu tiên không nên là "thêm một nhánh mới" — nên thử tìm xem có một tham số đơn giản hơn (ở đây là "độ rộng vấn đề") giải thích được sự khác biệt mà không cần phình kiến trúc.

## Điều tôi giữ vững xuyên suốt Sprint

- Từ chối Freeze khi Discovery "quá đẹp" nhưng chưa qua đủ Reality kiểm chứng (đặc biệt ở vòng Root Cause/Diagnosis và Priority).
- Kiên trì phân biệt Backlog vs Bug hiện tại — tránh kéo cả team dừng lại vì thứ chưa tới lượt (case "System").
- Giữ ranh giới vai trò Observation sạch qua nhiều vòng sửa lỗi liên tiếp, dù ranh giới này khó giữ hơn tưởng tượng ban đầu (ngôn ngữ tự nhiên dễ lẫn phán đoán vào mô tả).

## Ghi chú cho bản thân ở Sprint sau

Khi GPT hoặc Builder khác đưa ra một ví dụ minh họa để chứng minh giả thuyết, cần phân biệt rõ: ví dụ đó có phản ánh đúng cơ chế đang được nghiên cứu (Kurumi OS's Learning Engine, vận hành trên dữ liệu nhà hàng thật), hay chỉ là minh họa cách một hệ thống khác (ví dụ: chính AI đang mô tả) vận hành — hai loại bằng chứng này không tương đương và không nên bị đánh đồng khi dùng làm căn cứ Freeze.