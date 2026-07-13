# CLEANUP Specification V1.0
Status: FROZEN 🔒

## Mission
CLEANUP kết thúc một Engine Session một cách sạch sẽ.
Chỉ quản lý Session Lifecycle. Không quản lý Business.

## Constitution
- CLEANUP never changes business data.
- CLEANUP only releases temporary working resources.
- An Engine Session is complete only after temporary resources are released.
- Temporary resources shall be released before an Engine Session declares itself IDLE.

## Session Release Order
1. Release Working Truth (= null)
2. Reset Execution State → IDLE
3. Return Engine Response
4. Engine Session Ends

Không đảo thứ tự. Không dùng delete.

## Working Truth cần Release
sessionRAM.commitPackage = null
sessionRAM.lastCommitResult = null
sessionRAM.expectedLedgerRows = null

## Success Definition
Engine Session mới có thể bắt đầu mà không mang theo
bất kỳ Working Truth nào của Session trước.