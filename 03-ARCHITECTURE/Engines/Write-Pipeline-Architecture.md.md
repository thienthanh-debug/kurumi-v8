# Write Pipeline Architecture
Status: FROZEN

## Pipeline

IDLE → GENERATE → VALIDATE → WAIT_REVIEW → COMMIT → VERIFY → CLEANUP → IDLE

## Session Flow

Session 1: IDLE → GENERATE → VALIDATE → WAIT_REVIEW → STOP
Session 2: WAIT_REVIEW → COMMIT → VERIFY → CLEANUP → IDLE → STOP

## Core Principles

Business Event is Atomic.
Either everything is committed, or nothing is committed.

VERIFY never reconstructs business meaning.
It only confirms physical persistence.

Working Truth ≠ Persistent Truth.
Working Truth = Commit Package in RAM.
Persistent Truth = Ledger.

Nothing is destroyed before success is verified.

## Boundary

Write Engine → never updates Views.
Read Engine → never writes to Ledger.

## Engine Response Contract

SUCCESS: { success: true, data: ... }
FAILURE: { success: false, code: "UPPER_CASE", message: "...", context: {} }