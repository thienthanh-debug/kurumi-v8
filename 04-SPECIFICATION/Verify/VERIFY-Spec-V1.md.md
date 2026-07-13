# VERIFY Specification V1.0
Status: FROZEN 🔒

## Mission
VERIFY xác nhận Physical Write Integrity.
Không diễn giải Business. Không Validate lại.

## Constitution
VERIFY never reconstructs business meaning.
It only confirms physical persistence.

## Input
sessionRAM.expectedLedgerRows
sessionRAM.lastCommitResult

## Verification Logic
Rows Written = Rows Expected → SUCCESS
Rows Written ≠ Rows Expected → FAILED

## Boundary
- Không đọc Snapshot
- Không rebuild Commit Package
- Không chạy Business Logic
- Chỉ đếm rows