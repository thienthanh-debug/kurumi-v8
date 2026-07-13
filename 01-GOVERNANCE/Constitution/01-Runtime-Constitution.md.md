# KURUMI V8 — RUNTIME CONSTITUTION

Status: FROZEN Layer: 01 — Runtime Engine (ERP / Apps Script / Inventory) Last Updated: 06/07/2026

This document MUST NOT redefine any rule
already defined in 00-Kurumi-Constitution.md.

> This document inherits all principles defined in `00-Kurumi-Constitution.md`. Additional rules below apply only to the Runtime Engine.

---

## Core Principles

**Technology is replaceable. Business Truth is not.**

**Business Event is Atomic.** Either everything is committed, or nothing is committed. Never partially commit a Business Event.

**Business Event Boundary** ERP records Business Events. Inventory is the consequence of those events. Operational Activities may span hours or days. Business Events are instantaneous.

**Completion Event** PREP Event recorded at completion, not initiation. Applies to: Active, Passive, Soaking, Fermentation, Pickling, Aging. No exceptions.

**Human owns Business State.** **System owns Execution State.** These two worlds must never share a State Machine.

**Entity validates itself.** No Entity validates another Entity.

**Helper never decides. Helper only reports. State Machine decides.**

**Audit is best effort.** Engine does not die because of log failure.

**TRANSACTION_STAGING belongs to Human Workflow, not Engine Workflow.**

**WAIT_REVIEW is the boundary between Human Workflow and Engine Workflow.** Business State routing belongs to WAIT_REVIEW, not IDLE. IDLE only means: Engine is ready to begin a new cycle.

---

## Implementation Rules

- IMPL-01: Nothing is destroyed before success is verified.
- IMPL-02: Apps Script never makes business decisions.
- IMPL-03: Implementation is deterministic.
- IMPL-04: Only one Commit Execution may exist at any moment.

---

## Engine Response Contract

```javascript
// SUCCESS
{ success: true, data: ... }

// FAILURE
{ success: false, code: "UPPER_CASE_UNDERSCORE", message: "...", context: {} }
```