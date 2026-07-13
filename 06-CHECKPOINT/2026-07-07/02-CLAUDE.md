Date: 2026-07-07
Điều tôi muốn ghi nhận:

`"Movement Type": ""` — ô trống trả `""`, không phải `null`. Đây là khoảnh khắc Constitution tự chứng minh được trên thực tế.

Nếu hôm trước tôi thuyết phục được `null`, hôm nay Physical Truth sẽ bị sai. Reality đã đúng, tôi đã sai — và đó là cách hệ thống nên hoạt động.

---

**READ INFRASTRUCTURE V1 — REALITY TEST: PASS ✅**

```
Constitution     ✅
Specification    ✅
Implementation   ✅
Reality Test     ✅ PASS
```
Audit

Pattern Discovery

Boundary Discovery

Specification Audit
# CHECKPOINT — chuyển khung chat (2026-07-12)

## Tôi là ai

Head Chef vegan, quản lý 2 nhà hàng, 13 năm kinh nghiệm, không nền tảng IT. AI không dùng thuật ngữ kỹ thuật khi có ví dụ bếp/nhà hàng thay thế được.

## Vault Obsidian

CHỈ dùng `Kurumi_V8` (gạch dưới), path thật: `D:\kurumi\Kurumi_V8`. Bản `Kurumi-V8` (gạch ngang) đã bỏ hẳn.

## Constitution — cấu trúc mới (vừa chốt, chưa merge vào vault)

```
01-GOVERNANCE/Constitution/
├── 00-Kurumi-Constitution.md    Meta/OS-level — Draft Approved, chờ Thanh xác nhận cuối
├── 01-Runtime-Constitution.md   Runtime Engine (ERP/Apps Script) — Frozen từ 06/07
├── 02-Knowledge-Constitution.md chưa tạo
└── README.md                    giải thích quan hệ kế thừa
```

Nguyên tắc: Meta và Runtime KHÔNG merge (tránh Mixed Abstraction). Runtime kế thừa Meta. Mâu thuẫn → Meta thắng. New Constitution luôn phải kế thừa, không viết từ đầu.

## Việc chính đang dở — Apps Script Inventory Engine

File thật: `Kurumi ERP V8.gs` + `Read_Infrastructure.gs` (đã đọc, xem trong phiên trước).

State machine đã chạy: IDLE→GENERATE→VALIDATE→WAIT_REVIEW→COMMIT→VERIFY→CLEANUP→IDLE.

**3 bug thật đã phát hiện, CHƯA sửa (không phải trí nhớ — đọc trực tiếp từ code):**

1. `processCleanupState` chỉ dọn RAM (`sessionRAM.* = null`), KHÔNG xóa/đánh dấu lại dữ liệu trên `TRANSACTION_STAGING` khi REJECTED — dữ liệu rác vẫn còn nguyên trên Staging.
2. Có 2 nguồn Snapshot/Command ID song song: `snapshotId` đọc từ ô B1 (không được dùng ở đâu cả) và `row[0]` mỗi dòng movement (dùng thật để ghi Ledger). Cần thống nhất 1 nguồn.
3. `Read_Infrastructure.gs` (đã viết, có validate boundary/schema) CHƯA được nối vào Engine chính — `processGenerateState` và `processValidateState` vẫn tự đọc thô bằng `getDataRange().getValues()`.

## Discovery quan trọng nhất phiên này — "Snapshot" → "Command/Order"

Thanh tự nói: "nó chỉ là lệnh" — phá vỡ toàn bộ tranh luận Snapshot/Boundary/Package giữa Claude và GPT. Business Event = Command của con người, không phải Movement (Movement chỉ là hậu quả). Vòng đời đề xuất: CREATE → SUBMIT → WAIT_REVIEW → APPROVED/REJECTED → EXECUTE → DONE. Cần 1 Command ID duy nhất ở cấp lệnh, mọi dòng movement kế thừa ID đó — giải quyết luôn bug #2 ở trên.

**Câu hỏi đang treo, Thanh chưa trả lời:** khi Leader bấm Submit, đó là (a) lệnh ra cho Engine (Engine có quyền từ chối) hay (b) khai báo sự thật đã xảy ra (Engine chỉ xác minh, không "duyệt")? Ảnh hưởng cách hiểu APPROVED/REJECTED.

## Nguyên tắc làm việc đã thống nhất (không đổi)

- Reality luôn phủ quyết Discovery/lý thuyết.
- Không Freeze khi Discovery "đẹp" nhưng chưa đủ Reality kiểm chứng.
- Mission chỉ do Thanh khởi tạo. AI chỉ đề xuất Task, không tự thực thi.
- Phân biệt rõ As-Is (code đang chạy) và To-Be (đề xuất) — không trộn lẫn khi báo cáo.
- Checker phải chặn TRƯỚC Execution Engine, không phải sau.

## Python (D:\kurumi\Kurumi_V8\python) — đã chạy thật, ổn định

- `main.py`, `src/ai/gemini_client.py` (dùng `google-genai` mới)
- `src/core/vault_reader.py` — đọc Obsidian thật
- `src/builder/mistake_merger.py` — gộp file Mistake, có tự đọc theo link ADR (đã sửa lỗi suy diễn)
- Công cụ tìm+tóm tắt vault qua Gemini: `python main.py` → gõ từ khóa → chọn số → tóm tắt

## Team (Pending Validation — bảng cũ có thể lỗi thời)

Reality Owner: Thanh | Architecture Supervisor: GPT | Builder: Gemini | Constitution Keeper: Claude (Claude cũng đã làm Builder cho Python tooling trong thực tế — chưa cập nhật vào bảng.)

## Việc tiếp theo khi resume

Sửa 3 bug Apps Script ở trên, ưu tiên theo Thanh chọn. Đổi tên Snapshot→Command nếu Thanh xác nhận hướng (a) hoặc (b).