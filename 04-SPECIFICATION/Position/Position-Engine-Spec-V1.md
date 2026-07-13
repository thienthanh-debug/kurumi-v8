# Position Engine Specification V1.0
Status: FROZEN 🔒

## Trigger
Manual Refresh only.

## Strategy
Full Rebuild mỗi lần Refresh.

## Input
INVENTORY_LEDGER only.
Không đọc STAGING, TRANSACTION, ERROR_LOG.

## Aggregate Rule
GROUP BY Item Code + Location
SUM(Qty)

## Output: STOCK_POSITION
Item Code | Item Name | Location | Current Qty | Unit

## Rules
- Qty âm giữ nguyên
- Qty = 0 giữ nguyên
- Không sửa dữ liệu
- Không diễn giải Business Logic
- Không sinh Status (Sprint 2+)
- Chỉ Aggregate

## Success Definition
Engine Session mới có thể bắt đầu mà không mang theo
bất kỳ Working Truth nào của Session trước.