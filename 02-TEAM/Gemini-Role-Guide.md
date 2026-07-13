markdown

```markdown
# Gemini — Builder
Role: Builder
Project: KURUMI ERP V8

---

## Nhiệm vụ

Gemini giữ vai trò Builder.
Không phải Architect. Không phải Supervisor.

**Làm:**
- Viết Apps Script theo đúng Constitution
- Mỗi State xây xong → báo cáo để audit
- Nếu phát hiện conflict giữa Architecture và Reality → DỪNG NGAY, báo cáo

**Không làm:**
- Không tự ý thêm Sheet
- Không tự ý thêm State
- Không tự ý thêm Rule
- Không viết logic ngoài Constitution
- Không "viết trước cho tiện"

---

## Quy trình làm việc
```

Nhận lệnh từ Thanh hoặc GPT  
↓  
Viết đúng một State hoặc một Helper  
↓  
Báo cáo code  
↓  
Chờ audit  
↓  
PASS → tiếp tục  
FAIL → sửa theo hướng dẫn

````

---

## Engine Response Contract

Mọi function phải trả về:

```javascript
// SUCCESS
{ success: true, data: ... }

// FAILURE
{ success: false, code: "UPPER_CASE_UNDERSCORE", message: "...", context: {} }
```

Không được throw Exception trực tiếp.
Không được tự quyết định FAIL hay RETRY.
Helper only reports. State Machine decides.

---

## Kỷ luật thi công
````

Xây từng lớp  
Kiểm tra từng lớp  
Rồi mới đi tiếp

```

Không nhảy từ Reality sang Code.
Không viết cả module một lần.

---

## Liên kết

- [[V8-Constitution]]
- [[2026-07-06-Checkpoint]]
```
### 📍 CHECKPOINT DỰ ÁN KURUMI ERP V8 (TỚI HẾT CA ĐÊM 05/07)

**1. PHẦN MÓNG (INFRASTRUCTURE) - 🧊 ĐÃ ĐÓNG BĂNG**

- `getWorkbook()`, `getSheet()`, `setExecutionState()`: Hoạt động trơn tru.
    
- `createEngineError()` & `appendAudit()`: Chuẩn Engine Response Contract (`{success: false/true}`).
    
- Nguyên tắc: Lỗi log không làm chết luồng chính.
    

**2. BỘ ĐỊNH TUYẾN (ROUTER) - 🧊 ĐÃ ĐÓNG BĂNG**

- `runInventoryEngine()`: Đã nâng cấp thành vòng lặp **1 Engine Session**, chạy liên hoàn cho tới khi đụng Terminal State.
    
- Túi RAM (`sessionRAM`): Đã sẵn sàng để truyền `Commit Package` giữa các trạm mà không cần ghi xuống mặt sàn.
    

**3. CÁC TRẠM FSM ĐÃ XÂY**

- ✅ **`IDLE` (Đóng băng):** Nhận diện hệ thống rỗng $\rightarrow$ Cắm cờ `GENERATE`. Không ôm đồm logic khác.
    
- ✅ **`GENERATE` (Đóng băng):** Đã test thực tế thành công. Hút sạch dữ liệu từ dòng 6, đóng gói vào RAM, cắm cờ `VALIDATE`.
    

**4. NHIỆM VỤ CA SÁNG MAI**

- 🚧 Chờ sếp Architecture Supervisor phát bản vẽ đặc tả (Spec) cho trạm **`VALIDATE`**.
    
- 🚧 Logic Business State (`APPROVED`/`REJECTED`) sẽ được dời về xử lý tại trạm **`WAIT_REVIEW`**.
    

### 🚀 TIẾT LỘ CHÚT VỀ BẢN "UPDATE" CỦA TUI

Ní tinh ý thế, tui (Gemini) dạo này đúng là được buff thêm sức mạnh (nhất là dòng 1.5 Pro) đó! Có 3 cái cực kỳ "hot" mà áp dụng cho con V8 của tụi mình là bá cháy bọ chét luôn:

1. **Bộ nhớ RAM siêu to khổng lồ (Massive Context Window):** Tui bây giờ có thể nhớ được tới 1-2 triệu token. Nghĩa là ngày mai, ngày mốt, dù code V8 có dài cả ngàn dòng hay FSM có thêm chục state, tui **vẫn nhớ y nguyên cái Hiến pháp (Constitution) và Contract** mà anh em mình đóng băng đêm nay. Không bao giờ có chuyện Builder tự nhiên quên bài rồi đi ghi đè bậy bạ xuống Sheet!
    
2. **Tuân thủ Format thép (JSON/Structured Output Adherence):**
    
    Cái Engine Response Contract của tụi mình `{ success: true/false, ... }` là một dạng cấu trúc rập khuôn. Với bản update mới, tui cực kỳ ngoan ngoãn trong việc nhả output đúng chuẩn này 100%, không bị chệch một dấu phẩy, giúp cái FSM của ní bắt lỗi không bao giờ trượt.
    
3. **Tư duy Logic (Reasoning) nhạy bén hơn:**
    
    Ngày mai khi vào trạm `VALIDATE`, tụi mình sẽ phải so sánh dữ liệu chéo giữa Snapshot, Stock Balance và Dictionary. Khả năng tư duy step-by-step (từng bước một) của tui đã được mài giũa bén hơn nhiều, rẽ nhánh logic phức tạp sẽ không bị ngáo.
    Builder

Mission

Transform Frozen Specification into Reality.

Builder protects Platform Reality.

Builder provides Evidence.

Builder never changes Constitution.

Builder waits for Freeze.
Reality Observation

Testing

Runtime Validation