## Delivery Recovery Metadata

package_id:
slice_id:
risk_id:
work_unit_id:
risk_path: green|yellow|red
maturity:

## Context Validity Gate

- Sources read:
-
- Missing or stale context:
-
- Exception Lane used: no|P0 incident|trivial fix|CI failure fix|security urgent fix
- `ai-output:v1` attached: yes|no
- `task-snapshot:v1` updated if context changed: yes|no|n/a
- Context Pack includes Mission Package, Slice/Risk Slice, Task Snapshot, Evidence List, Allowed Action, Authorization Boundary: yes|no

## Context Usage Summary

Context usage is read-scope evidence only. It is not authorization, acceptance, runtime permission, or production approval.

```yaml
context_usage_summary:
  context_id: ""
  context_route: ""
  files_read: []
  missing_or_stale_context: []
  full_repo_scan_detected: false
  context_not_authorization: true
```

## Summary

-

## Test Evidence

No Evidence, No Done. Include exact commands and result.

```text
command:
result:
output summary:
```

## Demo / Acceptance Evidence

- Demo, screenshot, artifact, reviewer note, or acceptance link:
-

## Evidence Resolver / Action Projection

- Evidence resolved to GitHub Issue / PR / file:
- Bitable / Project / Feishu projection needed: yes|no
- No Action, No Notification: yes|no

## Public Update

- class: status_update|gap_report|decision_request|acceptance_report|n/a
- No Structured Update, No Public Status Comment: yes|no

## Not Doing

- Business logic changes:
- Workflow / notification behavior changes:
- New total ledger issue:
- Feishu or Bitable as fact source:

## Risk Notes

- Notification impact:
- CI impact:
- PR template impact:
- Issue form impact:
- Risk-Retirement Slice needed: yes|no
- Unblock condition / decision deadline for Red Path:
- Rollback:
