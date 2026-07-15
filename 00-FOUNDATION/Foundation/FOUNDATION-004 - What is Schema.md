##FOUNDATION-004 — What is Schema?
**Status:** DRAFT → READY FOR REVIEW

---

# The Question

**What is Schema?**

---

# Core Definition

> **Schema is the physical representation of Architecture.**

Tiếng Việt.

> **Schema là hình thái vật lý của Architecture.**

Không hơn.

Không kém.

---

# Nature

Schema là nơi Principle bắt đầu chạm Reality.

Đây là lần đầu tiên mọi tư duy được chuyển thành vật chất.

Ví dụ.

Architecture nói

Reality phải được đo.

↓

Schema sinh ra

```
Standard Yield
Reality Yield
High Skill Yield
```

Đó là Schema.

Không phải vì thích có thêm cột.

---

Architecture nói

Raw và Prep là hai bản chất khác nhau.

↓

Schema sinh ra

```
LIST_ITEM

PREP_MASTER
```

---

Architecture nói

Recipe và Inventory không được trộn.

↓

Schema sinh ra

Hai sheet.

---

Schema không phát minh.

Schema chỉ hiện hình.

---

# Nature

Schema không chứa Experience.

Schema cũng không chứa Principle.

Schema chỉ mang dấu vết của chúng.

Giống như hóa thạch.

Nhìn hóa thạch.

Ta biết sinh vật từng tồn tại.

Nhìn Schema.

Ta biết Architecture từng tồn tại.

---

# Validation Test

Một Schema chỉ hợp lệ khi trả lời được bốn câu hỏi.

## 1

Schema này được sinh ra từ Architecture nào?

Nếu không trả lời được.

Schema dư thừa.

---

## 2

Architecture này đang bảo vệ Principle nào?

Nếu không trả lời được.

Schema vô nghĩa.

---

## 3

Principle này được sinh ra từ Experience nào?

Nếu không trả lời được.

Schema chỉ là tưởng tượng.

---

## 4

Reality nào sẽ đi qua Schema này?

Nếu không có Reality.

Schema chết.

---

# What Schema is NOT

Schema không phải

- Google Sheet
- Database
- JSON
- Excel
- SQL
- API Model
- Class

Đó chỉ là implementation.

Schema tồn tại trước implementation.

Implementation chỉ chọn vật liệu để xây Schema.

---

# Example 01

PREP_LOG

Người ngoài nhìn thấy.

```
Date

Prep

Yield

Staff

Remark
```

Kurumi nhìn thấy.

```
Reality
        │
        ▼
Experience
        │
        ▼
Principle
        │
        ▼
Architecture
        │
        ▼
PREP_LOG
```

PREP_LOG không phải bảng.

PREP_LOG là Architecture đã đông cứng.

---

# Example 02

READ Infrastructure

Schema

```
Required Header

Boundary

Object Mapping

Value Preservation
```

Không phải Rule.

Không phải Code.

Đó là hình thái vật lý của một Architecture bảo vệ Principle:

> Infrastructure maps. It does not interpret.

---

# Relationship

```
Reality
      │
      ▼
Experience
      │
      ▼
Principle
      │
      ▼
Architecture
      │
      ▼
Schema
```

Schema là điểm tiếp xúc đầu tiên giữa tư duy và thế giới vật lý.

---

# Learning Note

Phần lớn ngành software bắt đầu bằng Schema.

Kurumi bắt đầu bằng Experience.

Đó là khác biệt.

Schema không phải nơi để thiết kế.

Schema là nơi Architecture kết thúc.

Đồng thời cũng là nơi System bắt đầu.

---

# Rule of Thumb

> **Architecture thinks.**
> 
> **Schema materializes.**

---

## Dẫn chứng thực tế (2026-07-14)

- [[Validation-Decision-Spec-V1]] (Mục 6) — trích nguyên văn "Schema không phát minh, Schema chỉ hiện hình" để quyết định KHÔNG tạo `LOCATION_MASTER` khi chưa có Reality (phân tích luồng kho thật) chứng minh cần — ví dụ cụ thể nhất của Validation Test Mục 4 file này ("Reality nào sẽ đi qua Schema này? Nếu không có Reality, Schema chết").