# ADR-010

## Title

Module ≠ State

## Context

Ban đầu Builder được hiểu là State.

Điều này gây Wrong Abstraction.

## Decision

State

GENERATE
VALIDATE
WAIT_REVIEW
COMMIT

là Runtime.

Builder

Parser

Validator

là Module.

Module có thể gọi nhiều State.

## Consequence

Không dùng Module để thay thế State.