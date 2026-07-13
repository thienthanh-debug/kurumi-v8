# Read Engine Architecture
Status: FROZEN

## Core Principles

Write Engine creates Truth.
Read Engine creates Views.
Read Engine exists to support Decision.

Truth trước. Views sau. Decision ở cuối.

Nhìn xa để không đi sai.
Nhưng chỉ Freeze đến đúng nơi mà Reality đã chứng minh.

## Flow

Material Flow (Reality)
↓
Write Engine → Ledger (Truth)
─────────────────────────────
(User clicks Refresh)
↓
Read Engine → Views

## Trigger

Manual Refresh only.
Read Engine chỉ chạy khi người vận hành chủ động yêu cầu.

## Position Engine V1

Input: INVENTORY_LEDGER only
Strategy: Full Rebuild
Aggregate: GROUP BY Item Code + Location → SUM(Qty)
Output: STOCK_POSITION

Rules:
- Qty âm giữ nguyên
- Qty = 0 giữ nguyên
- Không diễn giải Business Logic
- Chỉ Aggregate