### Infrastructure Contract Pattern — FROZEN

```
Infrastructure
        ↓
Boundary
        ↓
Contract
        ↓
Validation
        ↓
Return Contract
```

**Template name:** `INFRASTRUCTURE SPECIFICATION TEMPLATE`

Read Infrastructure là implementation đầu tiên. Không phải định nghĩa của template.

---

### Hệ quả

Write Engine và Read Engine đều đã tuân theo pattern này mà không ai nhận ra. Discovery hôm nay chỉ là đặt tên cho thứ đã tồn tại.

Sau này Import, Export, Sync, API Engine đều dùng cùng một khuôn — không cần nghĩ lại từ đầu.
Discovery lớn nhất của Sprint.

```
Boundary↓Contract↓Validation↓Return Contract
```

Đây là Universal Pattern.