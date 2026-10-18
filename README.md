# x4-autofix

**Policy-gated autofix and recovery loops for agent fleets.**

Detect failures, propose repairs, and (when authorized by Level 0–3 policy) apply them. Integrates with x4-fleet and x4-evidence.

## Autonomy Levels

| Level | Name | Allowed |
|-------|------|---------|
| 0 | Observe | Detect + report only |
| 1 | Assist | Open PR with proposed fix |
| 2 | Governed Autopilot | Apply trivial fixes (lint, pin, bump) inside hard limits |
| 3 | Never | Secrets, deletes, force-push, financial |

## Quick Start

```bash
pip install -e ".[dev]"
python -m x4_autofix.detect --repo dhe-cruzer69/x4-beast
```

## License

Apache-2.0

## APEX Architecture Map

> Status: architecture documentation; implementation and deployment claims require independent verification.

```mermaid
flowchart TB
  Patch[Proposed patch] --> Parse[Parse patch metadata]
  Parse --> Paths{All paths allowlisted?}
  Paths -->|no| RejectPath[Reject without write]
  Paths -->|yes| Scan[Scan for prohibited operations]
  Scan -->|unsafe| RejectRisk[Reject and explain]
  Scan -->|clean| DryRun[Generate dry-run diff]
  DryRun --> Review{Explicit apply approval?}
  Review -->|no| Preview[Return preview only]
  Review -->|yes| Snapshot[Capture pre-change hashes]
  Snapshot --> Write[Apply atomically where supported]
  Write --> Verify[Run targeted verification]
  Verify -->|pass| Receipt[Write patch receipt]
  Verify -->|fail| Rollback[Restore from snapshot]
  Rollback --> RollbackCheck{Restore verified?}
  RollbackCheck -->|yes| Failed[Return failure + rollback receipt]
  RollbackCheck -->|no| Escalate[Stop; human recovery required]
```
**Evidence note:** Atomicity and rollback are filesystem-dependent. Verify backups, path handling, and failure-injection tests before enabling write mode.

