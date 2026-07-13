### READ ENGINE — FROZEN 🔒

**Trigger:** Manual Refresh only.

**Boundary:**

```
Write Engine → never updates Views.
Read Engine → never writes to Ledger.
```

**Core Flow:**

```
Reality
    ↓
Write Engine → Ledger (Truth)
─────────────────────────────
(User clicks Refresh)
    ↓
Read Engine → Views
```

**Position View Rules:**

```
✓ Qty âm giữ nguyên
✓ Qty = 0 giữ nguyên
✓ Không sửa dữ liệu
✓ Không diễn giải Business Logic
✓ Chỉ Aggregate: SUM(Qty) by Item + Location
```

---

**Principle vào Constitution:**

> Truth trước. Views sau. Decision ở cuối.

> Nhìn xa để không đi sai. Nhưng chỉ Freeze đến đúng nơi mà Reality đã chứng minh.
>
# READ ENGINE SPECIFICATION V1

**Status:** FROZEN 🔒

## Trigger

Manual Refresh.

Read Engine chỉ chạy khi người vận hành chủ động yêu cầu.

Ví dụ:

- Cuối ca
- Cuối ngày
- Trước kiểm kê
- Trước báo cáo Owner
- Khi cần điều tra lỗi
- Khi cần xem Dashboard

---

## Flow

```
Reality↓Write Engine↓Inventory Ledger(Source of Truth)────────────(User clicks Refresh)↓Read Engine↓Operational Views├── Stock Position├── Purchase View├── Prep View├── Waste View├── Dashboard├── Report└── Future Views
```

---

## Core Principle

> **Write Engine creates Truth.**
> 
> **Read Engine creates Views.**

---

## Boundary

Write Engine tuyệt đối không cập nhật bất kỳ Operational View nào.

Read Engine tuyệt đối không ghi xuống Ledger.

---

## Position View

Input

```
INVENTORY_LEDGER
```

Master Data

```
ALL_ITEM
```

Aggregate Key

```
Item Code+Location
```

Formula

```
Current Qty=SUM(Qty)
```

---

## Rules

✓ Qty âm được giữ nguyên.

✓ Qty = 0 được giữ nguyên.

✓ Không sửa dữ liệu.

✓ Không diễn giải Business Logic.

✓ Chỉ Aggregate.

---

## Responsibility

```
Ledger↓Aggregate↓Operational View
```

Không Report.

Không Costing.

Không Forecast.

Không MRP.

---

# Vì sao quyết định này quan trọng

Tui nghĩ đây là một trong những quyết định đẹp nhất của V8 đến hiện tại.

Hầu hết ERP sẽ làm kiểu:

```
Write↓Update Ledger↓Update Stock↓Update Dashboard↓Update Report
```

Tức là **một lần ghi kéo theo cả hệ thống**.

V8 thì khác:

```
Write↓Truth(stop)
```

Khi cần:

```
Truth↓Read↓Views
```

Điều này tạo ra một hệ rất sạch:

- Write chỉ quan tâm ghi sự thật.
- Read chỉ quan tâm trình bày sự thật.
- Decision chỉ dựa trên các View.

Nếu sau này Kurumi có:

- Inventory
- Cost
- Sales
- Finance
- HR
- CRM

thì tất cả đều có thể dùng chung triết lý này:

> **Truth trước. Views sau. Decision ở cuối.**

Đó là một kiến trúc ERP rất bền khi hệ sinh thái mở rộng. Sprint tiếp theo có thể bắt đầu viết **Specification chi tiết của Position Engine** (Refresh → đọc Ledger → Aggregate → cập nhật `STOCK_POSITION`) mà không cần thay đổi bất kỳ quyết định nào đã Freeze hôm nay.