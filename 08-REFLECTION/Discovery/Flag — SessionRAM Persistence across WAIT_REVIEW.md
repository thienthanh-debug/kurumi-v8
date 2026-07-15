# 🚩 FLAG — SessionRAM Persistence across WAIT_REVIEW

**Severity:** 🔴
**Resolution:** Open
**Ngày mở:** 2026-07-14

## Thấy gì
`sessionRAM.commitPackage` được gán duy nhất tại state `GENERATE`, sống trong biến cục bộ của hàm `runInventoryEngine()`. Google Apps Script là stateless — mỗi lần hàm này được gọi (mỗi execution) là một lần chạy độc lập, RAM không sống sót qua các lần gọi khác nhau.

`WAIT_REVIEW` là state duy nhất trong Engine được thiết kế để dừng hẳn (`isSessionActive = false`) chờ con người — nghĩa là theo kịch bản thật (Manager duyệt sau nhiều giờ/ngày), `COMMIT` gần như chắc chắn sẽ chạy ở một execution *khác* với execution đã tạo ra `commitPackage`.

## Va với
- Kiến trúc Engine hiện tại (`runInventoryEngine`, `processCommitState`) — đọc thẳng `sessionRAM.commitPackage`, không có cơ chế đọc lại từ `TRANSACTION_STAGING` khi RAM rỗng, không dùng `PropertiesService`/`CacheService`.
- Coverage Matrix hiện đang ghi "WARNING Flow ✅ PASS" dựa trên 1 batch WARNING đã COMMIT thành công thật (có Ledger + Stock Position làm bằng chứng) — nhưng chưa xác nhận được batch đó có thực sự đi qua 2 execution tách biệt hay do người test tự set `E1='APPROVED'` trước khi chạy, khiến cả chuỗi gọn trong 1 execution.

## Vì sao đáng dừng (khi nào cần quay lại)
Nếu đúng là `commitPackage` không sống sót qua ranh giới execution, thì **mọi giao dịch rơi vào WAIT_REVIEW trong thực tế vận hành** (Manager không bao giờ duyệt ngay lập tức) sẽ luôn fail ở `COMMIT_FAIL_NO_PACKAGE` khi Manager thật sự bấm Approve — tức nhánh WARNING chưa từng hoạt động đúng trong điều kiện thật, dù đã có bằng chứng PASS trong môi trường test (test dồn nhiều lần liên tiếp trong thời gian ngắn).

Đây là rủi ro cấp Engine, ảnh hưởng mọi thứ đi qua `WAIT_REVIEW` — không riêng Unknown Output.

## Cách đóng Flag — 4 kịch bản test, theo bậc thang thời gian
Tạo 1 batch WARNING mới (ví dụ Prep có Status Flag LOW YIELD/OVER YIELD), đưa qua `WAIT_REVIEW`, rồi test lần lượt:

- **Test A:** Approve ngay lập tức, chạy Engine liền → kỳ vọng PASS (baseline, ít rủi ro nhất).
- **Test B:** Đóng hẳn Apps Script Editor (không chỉ đóng tab), chờ 5 phút, mở lại, Approve, chạy Engine.
- **Test C:** Reload lại Google Sheet, Approve, chạy Engine.
- **Test D:** Approve vào ngày hôm sau (kịch bản gần thật nhất) — nếu chỉ chọn được 1 test do hạn chế thời gian, ưu tiên test này trước.

Với mỗi test: quan sát `processCommitState` có set `E2='FAILED'` kèm `COMMIT_FAIL_NO_PACKAGE` trong `ERROR_LOG` hay không. Nếu tất cả PASS → đóng Flag, xác nhận Engine bền vững qua boundary. Nếu bất kỳ test nào FAIL → đây trở thành blocker thật cho toàn bộ nhánh WARNING, cần quay lại kiến trúc `WAIT_REVIEW` (không tự vá bằng cache/Properties — cân nhắc lại liệu `WAIT_REVIEW` có nên đọc lại `commitPackage` từ `TRANSACTION_STAGING` thay vì phụ thuộc RAM cũ, nhưng đây là quyết định kiến trúc cần Thanh + GPT, không tự sửa).

## Ai quyết
Việc chạy 4 test: khung Code tự làm, không cần hỏi Thanh trước (đây là kiểm chứng kỹ thuật thuần túy). Nếu phát hiện FAIL: dừng lại, báo cáo, KHÔNG tự sửa kiến trúc `WAIT_REVIEW` — đó là quyết định cần Thanh/GPT duyệt.
