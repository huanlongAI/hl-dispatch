# HL Progress Exporter v0.1

Date: 2026-06-12

Status: P1_READ_ONLY_TOOLING

Implementation:

- `scripts/export-hl-progress.py`
- `scripts/test-hl-progress-exporter.py`
- `scripts/fixtures/hl-progress-input.json`

## Position

`hl-progress-export:v0.1` is the P1 read-only exporter for the `hl-progress` governance loop.

It normalizes GitHub Issues, PRs, and repository file references into `hl-progress-work-item:v0.1`, then emits either JSON or a Markdown Founder packet.

It is not a Feishu writer, Bitable writer, GitHub writeback tool, task platform, dashboard authority, or completion evidence source.

## Boundary

- GitHub Issues, PRs, and repository files remain the fact source.
- The exporter does not write GitHub comments, labels, issues, PRs, files, Projects, Feishu messages, Bitable rows, dashboards, or reports.
- Missing fields are emitted as `unknown` or `n/a` plus `warnings`.
- The exporter does not infer owner, status, risk, evidence, or next action from AI judgment.
- `done` is not emitted unless the source explicitly carries `evidence_state: accepted`.
- Local files are included only through explicit `--file-ref`.
- Local artifacts are written only when `--output` is provided.

## Offline Command

```bash
python3 scripts/export-hl-progress.py \
  --input scripts/fixtures/hl-progress-input.json \
  --generated-at 2026-06-12T00:00:00Z \
  --format json
```

Markdown Founder packet:

```bash
python3 scripts/export-hl-progress.py \
  --input scripts/fixtures/hl-progress-input.json \
  --generated-at 2026-06-12T00:00:00Z \
  --format markdown
```

## Live Read-Only Smoke

```bash
python3 scripts/export-hl-progress.py --state open --limit 5 --format json
python3 scripts/export-hl-progress.py --state open --limit 5 --format markdown
```

Live mode shells out only to:

```text
gh repo view --json nameWithOwner --jq .nameWithOwner
gh issue list --state <state> --limit <limit> --json number,title,url,state,labels,assignees,updatedAt,body
gh pr list --state <state> --limit <limit> --json number,title,url,state,labels,assignees,updatedAt,body,isDraft,reviewDecision,author,mergedAt
```

## Offline Input Shape

```json
{
  "repo": "huanlongAI/hl-dispatch",
  "issues": [],
  "pull_requests": [],
  "files": [
    {
      "path": "docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md",
      "url": "https://github.com/huanlongAI/hl-dispatch/blob/main/docs/delivery-recovery/HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md",
      "content": "..."
    }
  ]
}
```

## Output Shape

```json
{
  "schema": "hl-progress-export:v0.1",
  "source": "github",
  "repo": "huanlongAI/hl-dispatch",
  "generated_at": "2026-06-12T00:00:00Z",
  "counts": {
    "issues": 1,
    "pull_requests": 0,
    "repo_files": 0,
    "items": 1,
    "warnings": 4
  },
  "items": []
}
```

Each item uses the `hl-progress-work-item:v0.1` schema from `HL_PROGRESS_GOVERNANCE_LOOP_v0.1.md`.

## Field Mapping

| Work item field | Source |
|-----------------|--------|
| `task_id` | `### task_id`, `### work_unit_id`, issue number, PR number, or file path. |
| `source.repo` | Offline `repo` field, `--repo`, or `gh repo view`. |
| `source.issue_url` | GitHub issue URL. |
| `source.pr_urls` | GitHub PR URL. |
| `source.file_refs` | GitHub blob URL or explicit repo file path. |
| `owner.github` | `### owner_github`, `### DRI`, assignee, or PR author. |
| `owner.role` | `### owner_role` / `### role`; otherwise `unknown`. |
| `status` | Explicit `### status`, decision signal, blocker signal, or PR review state. |
| `risk_path` | `### risk_path` or `risk:<green/yellow/red>` label. |
| `evidence_state` | Explicit `### evidence_state`. |
| `next_gate` | `### next_gate`, Founder decision signal, or PR review. |
| `next_action` | Explicit `### next_action`; otherwise `n/a` plus warning. |
| `blocker` | `### blocker`, `### current_blocker`, `### blocked_by`, or blocker label. |
| `founder_decision_required` | `decision-request`, `action:decision_required`, `[Decision]`, or explicit decision field. |
| `projection.source_hash` | SHA-256 over source kind, repo, and raw source record. |
| `warnings` | Missing fields, invalid done/evidence state, or missing source links. |

## Verification

```bash
python3 scripts/test-hl-progress-exporter.py
python3 scripts/test-action-projection-exporter.py
git diff --check
```

Live read-only smoke check:

```bash
python3 scripts/export-hl-progress.py --state open --limit 5 --format json
```

The live smoke output is a projection artifact only. It must not be used as acceptance evidence unless the underlying GitHub source link is reviewed.
