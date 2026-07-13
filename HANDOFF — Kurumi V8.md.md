# HANDOFF — Kurumi V8 (dán vào đầu phiên chat mới)

## Tôi là ai (Reality Owner)

Head Chef vegan, quản lý 2 nhà hàng, 13 năm kinh nghiệm thực chiến, 36 tuổi. KHÔNG có nền tảng IT/lập trình/ERP. Chỉ có kinh nghiệm bếp + logic. => AI không dùng thuật ngữ kỹ thuật khi có thể nói bằng ví dụ bếp/nhà hàng.

## Trạng thái thật (không phải lý thuyết)

- Vault Obsidian: CHỈ dùng `Kurumi_V8` (gạch dưới). Bản `Kurumi-V8` (gạch ngang) đã BỎ.
- Apps Script "Kurumi ERP V8" đang chạy thật, đã có: `Read_Infrastructure.gs` (Lớp 1 Physical Adapter đọc Sheet thô, Lớp 2 Read Infrastructure validate schema/boundary), `Test_Read.gs`.
- Luồng Inventory Engine đang build tuần tự: prep-log, product-log → PREP_COMPILER, PRODUCTION_COMPILER → TRANSACTION_STAGING → INVENTORY_LEDGER (vừa xong 1 cái, đang làm cái thứ 2).
- File nguồn thật: KURUMI_INVENTORY_ENGINE.xlsx (45 sheet).
- Python (D:\kurumi\Kurumi_V8\python) tách riêng: `main.py` + `src/ai/gemini_client.py` (dùng package `google-genai` mới, không dùng `google.generativeai` đã ngừng hỗ trợ). Đã có bản thiết kế Mission→Task→Approval→WorkflowGate→Workflow→Checker→Builder (code mẫu đã viết, CHƯA đưa vào máy thật của Thanh, đang chờ duyệt).

## Bug lớn nhất đã phát hiện (lý do có Obsidian + Python)

AI mất khả năng suy luận/tư duy đã học giữa các phiên chat, dù đọc lại được checkpoint. Obsidian = bộ nhớ ngoài. Python (Workflow Gate) = ép buộc cứng, không phụ thuộc AI "tự giác" nhớ đúng quy trình.

## Nguyên tắc làm việc đã thống nhất

- Reality luôn phủ quyết Discovery/lý thuyết.
- Không Freeze khi Discovery "đẹp" nhưng chưa đủ Reality kiểm chứng.
- Mission chỉ do con người (Thanh) khởi tạo. AI chỉ đề xuất Task, không tự thực thi.
- Ưu tiên việc thật (Inventory Engine đang chạy) hơn mở rộng kiến trúc triết học.

## Việc đang dở, cần tiếp tục

Build tiếp phần Apps Script sau TRANSACTION_STAGING → INVENTORY_LEDGER.

## Sprint O3 Completed

Meta Architecture đã được Freeze.

Workflow chuẩn:

Mission
→ Task
→ Approval
→ Workflow Gate
→ Workflow
→ Artifact
→ Constitution
→ Checker
→ Builder

Python prototype đã chạy thành công với Google Gemini SDK mới (`google-genai`).

