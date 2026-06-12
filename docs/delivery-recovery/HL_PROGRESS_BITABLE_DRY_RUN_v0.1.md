# HL Progress Bitable Dry-Run Projection v0.1

Date: 2026-06-12

Status: P2_DRY_RUN_ONLY

Implementation:

- `scripts/project-hl-progress-bitable.py`
- `scripts/test-hl-progress-bitable-projection.py`
- `scripts/fixtures/hl-progress-export.json`

## Position

This is the P2 dry-run projection for Feishu Bitable.

It maps `hl-progress-export:v0.1` JSON into a Bitable-shaped row preview, field mapping, and dry-run projection ledger.

It does not call Feishu APIs, write Bitable rows, write GitHub, create tasks, update dashboards, or change any source-of-truth state.

## Projection Notice

Projection only. GitHub remains SSOT. Bitable edits are notes until captured in GitHub. External Bitable write requires a separate projection gate.

## Boundary

- GitHub -> Bitable is one-way by default.
- Bitable is not a fact source.
- The dry-run ledger is an audit preview, not proof of external sync.
- Actual Bitable write requires a separate Founder / Gate projection SSOT with exact table, fields, credentials boundary, rollback, and exclusions.
- This P2 dry-run does not authorize GitHub writeback.
- This P2 dry-run does not use secrets.

## Command

JSON dry-run ledger:

```bash
python3 scripts/project-hl-progress-bitable.py \
  --input scripts/fixtures/hl-progress-export.json \
  --generated-at 2026-06-12T01:00:00Z \
  --format json
```

Markdown Founder / operator packet:

```bash
python3 scripts/project-hl-progress-bitable.py \
  --input scripts/fixtures/hl-progress-export.json \
  --generated-at 2026-06-12T01:00:00Z \
  --format markdown
```

Write a local artifact only when explicitly requested:

```bash
python3 scripts/project-hl-progress-bitable.py \
  --input /tmp/hl-progress-export.json \
  --format json \
  --output /tmp/hl-progress-bitable-dry-run.json
```

## Field Mapping

| Bitable Field | Source Field | Type | Semantics |
|---------------|--------------|------|-----------|
| Task ID | `task_id` | text | projection_only |
| Repo | `repo` | text | projection_only |
| Owner | `owner` | text | projection_only |
| Status | `status` | single_select | projection_only |
| Risk Path | `risk_path` | single_select | projection_only |
| Evidence State | `evidence_state` | single_select | projection_only |
| Next Gate | `next_gate` | text | projection_only |
| Next Action | `next_action` | text | projection_only |
| Blocker | `blocker` | text | projection_only |
| Founder Decision Required | `founder_decision_required` | checkbox | projection_only |
| GitHub Link | `github_link` | url | projection_only |
| Last Synced | `last_synced` | datetime | projection_only |
| Warnings | `warnings` | text | projection_only |

## Dry-Run Ledger

Each projected row emits a ledger entry:

```json
{
  "task_id": "HLPROG-P1-WU1",
  "github_link": "https://github.com/huanlongAI/hl-dispatch/issues/301",
  "operation": "dry_run_upsert_preview",
  "external_write": false,
  "result": "skipped_external_write",
  "warnings": []
}
```

Rows without a GitHub link carry `missing_github_link_for_projection` and remain invalid for governance decisions.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-bitable-projection.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
git diff --check
```

## Gate For Real Bitable Write

Before any real Feishu Bitable write, open a separate GitHub SSOT gate that names:

- Bitable app / table target without exposing credentials.
- Exact fields and row identity key.
- Write command and dry-run artifact hash.
- Rollback / delete / restore approach.
- Proof that GitHub remains SSOT and Bitable edits cannot write back to GitHub.
- Explicit exclusions for production, secrets, route / mode / permission changes, branch protection, and GitHub writeback.
