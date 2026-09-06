---
flagId: FLAG-D20A-D20B-001
status: RESOLVED
issuedBy: Claude (Constitution Keeper)
participants: [GPT (Architecture Supervisor), Grok (Strategic Radar), Reality Owner]
relatedTracks: [D.20A, D.20B, D.19A]
dateRange: 2026-09 (single session)
---

# FLAG-D20A-D20B-001 — D.20A Closure Gate / D.20B Entry Gate

## Bối cảnh

D.20A (Web App Phase 1 audit, do GPT thực hiện, READ-ONLY) kết luận Phase 1 khả thi nhưng có các giả định chưa kiểm chứng được trình bày ở cùng mức độ tin cậy với kiến trúc đã freeze. Constitution Keeper ban FLAG để buộc tách "đã freeze" khỏi "chờ Reality Test" trước khi cho D.20B build.

## Trạng thái ban đầu (issued)

```text
D.20A_closed: false
D20B_build_authorized: false
D20B_verify_only_authorized: true
```

### 4 Blockers ban đầu

1. Verify deployment mode và email identity bằng tài khoản thật DN/HA
2. Chốt mapping API Response ↔ Engine Response Contract
3. Radar-search toàn bộ nguồn trước khi tuyên bố SALES_REVIEW contract chưa tồn tại
4. Giữ D.19A tách biệt và khóa Sales Part A

### Thứ tự bắt buộc D.20B

1. Reality-test identity trước
2. Làm rõ response-contract mapping
3. Rà lại toàn bộ nguồn về Sales Review
4. Chỉ khi 1-3 PASS mới thiết kế role/branch và command contract
5. Không sửa code/Sheet/D.19A trong giai đoạn verify

---

## Step 1 — Identity Reality Test: PASSED

**Harness:** Project throwaway riêng biệt (`15rWRkvgryqp4vD8B0gzv52u8ShVJF84DW53jwlONGu6-aYrYc-WaqEXd`), không liên kết Kurumi V8, được Constitution Keeper cấp `TEST-HARNESS-AUTHORIZATION-001` — chỉ trả email, không đọc Sheet/Engine.

**Kết quả:**

| Mode | DN | HA | Kết luận |
|---|---|---|---|
| Execute as user accessing | `nhannguyen250202@gmail.com` ✅ ổn định qua nhiều lần reload | `thanhtam110298@gmail.com` ✅ ổn định | **Dùng làm phương án chính** |
| Execute as me | `{"email":""}` ❌ | `{"email":""}` ❌ | Loại bỏ |

**Phương án dự phòng ghi nhận:** Google OAuth ID token — backend verify token rồi mới map role/branch; tuyệt đối không nhận branch/role từ phía client.

**Harness:** đã retire hoàn tất sau khi PASS — 2 deployment lưu trữ/ngừng hoạt động, project chuyển vào Trash, Kurumi V8 không bị chạm.

---

## Step 2 — API Response ↔ Engine Response Contract Mapping: PASSED

**Envelope 6 trường** (additive-compatible với Engine Contract đã freeze `{success, code, message, context}`):

```json
{
  "success": false,
  "code": "STABLE_API_CODE",
  "message": "User-safe message",
  "data": null,
  "context": {},
  "requestId": "request-id"
}
```

15 quy tắc mapping (ưu tiên top-to-bottom, fail-closed ở rule cuối) — full table lưu tại `D20B_STEP2_RESPONSE_CONTRACT_MAPPING_DRAFT.md`. Điểm mấu chốt đã qua 1 vòng sửa:

- Legacy bug bắt được: `CRITICAL_REJECTED` từng trả `success:true` ở wrapper cũ → API normalizer ép về `success:false, BUSINESS_VALIDATION_FAILED` theo semantic precedence, không tin `success` boolean cũ.
- Sửa quan trọng (Rule 5 vs 14):
  - `WAIT_REVIEW`/`REQUIRES_REVIEW` (nghiệp vụ bình thường, WARNING theo taxonomy Sprint O4) → `success:true, code:"REVIEW_REQUIRED"` — vì lệnh đã được tiếp nhận, hệ thống ở trạng thái hợp lệ, chỉ chờ Leader duyệt. UI hiển thị trung tính "Đã ghi nhận, chờ Leader duyệt", không phải lỗi đỏ.
  - `STAGING_BUSY_PENDING_REVIEW` (bằng chứng `attempted:false` trong `RecursiveResolverCore.gs`) → `success:false, RESOURCE_BUSY` — thao tác chưa hề xảy ra.
  - `*_UNEXPECTED_WAIT_REVIEW` → `success:false, INTERNAL_ERROR` — vi phạm invariant, không phải review nghiệp vụ bình thường.
  - Tiêu chí thống nhất: `success:true` = command được tiếp nhận, hệ thống ở trạng thái hợp lệ/nhất quán — không có nghĩa lifecycle đã FINALIZED.

Context allowlist (public): `operation, eventId, itemCode, branch, status, reviewRequired, retryable`. Cấm tuyệt đối lộ ra ngoài: sheetName, spreadsheetId, row/range/a1/formula, stack trace, internal checkpoint/staging coordinates, file/function names, raw Engine code. Server log riêng `{requestId, engineCode, sanitized diagnostics}`.

---

## Step 3 — Radar Search (SALES_REVIEW contract): PASSED — PARTIAL

Lần 1: NOT_FOUND nhưng bị reclassify thành INCONCLUSIVE — Radar chỉ quét được Drive snapshot cũ, không mount được vault local `D:\kurumi\Kurumi_V8`. Bằng chứng: không tìm thấy ADR-016 dù ADR-016 đã confirmed tồn tại (Sprint O4, PREP_COMPILER bug fix).

Lần 2 (sau khi mount đủ 11/11 folder, xác nhận có ADR-016): PARTIAL, no source gap.

Kết luận:

- Không có holotype "SALES_REVIEW" command contract sẵn có.
- Có đủ building blocks để KHÔNG thiết kế từ số 0:
  - Status lifecycle `IMPORTED→READY/REQUIRES_REVIEW/REJECTED→RESOLVED` (`resolveSaleConsumption_()`)
  - `WAIT_REVIEW` pattern + `Approved By/Approved Time` (ADR-022, Validation-Decision-Spec-V1, Runtime Constitution)
  - `ADR-013 Approval Scope`, `ADR-014 Workflow Gate` — ngắn, chưa đề cập Sales, nhưng là khuôn tổng quát nên tái dùng.

Ràng buộc cho Step 4: GPT phải trình bày rõ phần nào tái dùng nguyên ADR-014/building blocks, phần nào thực sự mới — cấm trình bày như thiết kế từ số 0.

---

## D.19A — vẫn LOCKED

Tách biệt hoàn toàn khỏi D.20A/D.20B trong suốt quá trình. Sales Part A import vẫn khóa, không được chạm bởi bất kỳ track nào ở trên.

---

## Trạng thái đóng FLAG

```text
D.20A: CLOSED / PASS
D.20B Steps 1-3: PASSED (evidence-based)
D.20B Step 4: IN_PROGRESS — GPT đang audit ADR-014 + building blocks,
  phân tách reuse / extend / new trước khi trình command contract
D.19A: still LOCKED
D20B_build_authorized: TRUE (scoped to role/branch design + command
  contract per newConstraint_forStep4)
```

## Nguyên tắc rút ra cho các FLAG tương lai

Một audit READ-ONLY do một AI tự thực hiện không được đóng track chỉ bằng tuyên bố của chính AI đó — cần Reality Test độc lập (harness, Radar search trên nguồn đầy đủ) trước khi coi kết luận là Reality đã validate. Việc Radar lần đầu quét nhầm nguồn cũ (thiếu ADR-016) là bằng chứng cụ thể cho thấy quy trình xác minh nguồn trước khi tin kết luận "NOT_FOUND" là cần thiết, không phải thủ tục thừa.

Ghi bởi Claude (Constitution Keeper), tổng hợp từ phiên làm việc trực tiếp với Reality Owner, GPT, và Grok.

---

Liên quan: [[Governance-Protocol]] (Mục 1 — Khuôn Flag; nguyên tắc rút ra ở trên mở rộng khuôn này cho trường hợp nhiều AI/audit chéo), [[Flag — SessionRAM Persistence across WAIT_REVIEW]], [[Flag — Compiler Automation vs Frozen Contract]] (2 Flag đơn giản hơn, theo khuôn cũ, lưu tại `08-REFLECTION/Discovery/` — FLAG này dùng định dạng có ID/frontmatter riêng vì phạm vi đa-AI/nhiều bước audit, không thay thế quy ước cũ).
