# Constitution — README

## Cấu trúc phân cấp

```
01-GOVERNANCE/Constitution/
├── 00-Kurumi-Constitution.md      ← Meta / OS-level (Mission, Reality, Ontology, Epistemology, Governance)
├── 01-Runtime-Constitution.md     ← Runtime Engine (ERP, Apps Script, Inventory) — kế thừa 00
├── 02-Knowledge-Constitution.md   ← để trống, tạo khi Reality thực sự cần
└── README.md                      ← file này
```

## Nguyên tắc

- **Không merge** hai tầng vào một file — tránh trộn abstraction level (Mixed Abstraction), lỗi đã được ghi nhận và cấm từ Sprint O2.
- **Không để hai Constitution độc lập, mâu thuẫn nhau** — Runtime kế thừa Meta, không cạnh tranh với Meta.
- Khi đọc bất kỳ file `0X-...-Constitution.md` nào, luôn coi `00-Kurumi-Constitution.md` là nền tảng bắt buộc đọc trước.
- Khi có mâu thuẫn giữa hai tầng, tầng Meta (00) thắng — vì nó gần Luật Tối Cao (Reality) hơn.

## Trạng thái hiện tại

- `00-Kurumi-Constitution.md`: Draft Approved, chờ Thanh xác nhận cuối trước khi Freeze.
- `01-Runtime-Constitution.md`: Frozen (giữ nguyên từ 06/07/2026, chỉ thêm dòng kế thừa).
- `02-Knowledge-Constitution.md`: chưa tồn tại — không tạo trước khi có nhu cầu thật.