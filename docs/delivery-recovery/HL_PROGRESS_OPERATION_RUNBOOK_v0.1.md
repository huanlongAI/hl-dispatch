# HL Progress Operation Runbook v0.1

Date: 2026-06-12

Status: GREEN_READ_ONLY_OPERATION

This runbook turns the merged P1 / P2 / P3 artifacts into repeatable read-only operations.

It does not authorize Feishu write, Bitable write, GitHub writeback, route / mode / permission changes, branch protection changes, production work, secrets, deployment, release, provider, payment, billing, refund, settlement, or real user data access.

## No External Writes

These commands are safe only because they read GitHub and write stdout by default:

- do not write Feishu
- do not write Bitable
- do not write GitHub
- do not change route / mode / permission
- do not treat projection as evidence

Local artifact output with `--output` is allowed only when the operator explicitly names the local path. External writeback still requires a separate Founder / Gate SSOT.

## Daily Read-Only Scan

Purpose: build the current active-work read model from GitHub Issues / PRs and surface missing fields as warnings.

Command:

```bash
python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state open --limit 100 --format json
```

Expected output:

- `schema: hl-progress-export:v0.1`
- `items[]` using `hl-progress-work-item:v0.1`
- `warnings[]` for missing owner, risk, evidence, next action, or source links

Stop if:

- GitHub CLI cannot read issues / PRs.
- A row has no GitHub source link and the result would be used for governance.
- The operator wants to write Feishu, Bitable, dashboard, Project, or GitHub.

## Weekly Founder Packet

Purpose: generate a human-readable packet for active work, blockers, decision-required items, review waits, accepted evidence, and warnings.

Command:

```bash
python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state open --limit 100 --format markdown
```

Rules:

- Every line must retain a GitHub source link or warning.
- Founder decisions still happen in GitHub SSOT, not in the packet.
- The packet is a projection, not acceptance evidence.

## Bitable Dry-Run Projection

Purpose: preview how P1 JSON would map into Feishu Bitable rows without writing Feishu.

Command:

```bash
python3 scripts/project-hl-progress-bitable.py --input <hl-progress-export.json> --format json
```

Output must include:

- field mapping for Task ID, Repo, Owner, Status, Risk Path, Evidence State, Next Gate, Next Action, Blocker, Founder Decision Required, GitHub Link, Last Synced, and Warnings
- dry-run ledger entries with `external_write: false`
- projection notice that GitHub remains SSOT

## Gate Stop Rules

Stop and request a separate Founder / Gate SSOT before any of the following:

- real Feishu or Bitable write
- GitHub comment, label, issue, PR, Project, workflow, file, branch, release, or setting write
- any action that would close, accept, reject, archive, or unblock work
- any use of dashboard, Feishu, Bitable, report, PM draft, CI green, or Gate readback as final evidence
- any work involving production, secrets, provider, payment, billing, refund, settlement, release, deployment, or real user data

## Verification Commands

Run these before reporting the operation healthy:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-exporter.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-bitable-projection.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-hl-progress-writeback-proposal.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test-action-projection-exporter.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_context_engineering_templates.py
bash scripts/check-agent-governance-d10.sh
git diff --check
```

The Context Engineering Template Gate also runs as an observer-only GitHub Actions workflow on pull requests, pushes to `main`, manual dispatch, and weekdays at 10:30 CST. It does not create GitHub issues, send Feishu messages, update Project, write Bitable, or grant authorization.

`scripts/check-agent-governance-d10.sh` is a local wrapper for the canonical sibling `sentinel-shared/scripts/precheck-agent-governance.sh`; it does not redefine D-10 rules.

CI D-10 remains owned by the existing `Consistency Sentinel` reusable workflow. The Context Engineering Template Gate intentionally does not checkout `sentinel-shared`; it only checks local task / output templates.

Optional live read-only smoke:

```bash
python3 scripts/export-hl-progress.py --repo huanlongAI/hl-dispatch --state open --limit 5 --format json
```

## Reporting Format

Use this concise report shape:

```text
hl-progress read-only scan
- source: GitHub
- generated_at: <timestamp>
- items: <count>
- warnings: <count>
- blockers: <count or n/a>
- founder_decision_required: <count or n/a>
- external_writes: none
- verification: <commands + pass/fail>
```

If verification was not run, state the gap. Do not report DONE without fresh command output.
