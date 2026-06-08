# Action Projection Exporter v0.1

`action-projection:v0.1` is a read-only Delivery Recovery helper. It turns GitHub issue facts into a local JSON projection for action review.

It is not a fact source, task platform, Feishu sender, Bitable writer, Project sync, or ledger replacement.

## Boundary

- GitHub Issue / PR / repo file remains the fact source.
- Bitable / Project / Feishu may consume projection output, but they do not become evidence.
- The exporter does not write GitHub comments, labels, issues, Feishu messages, Bitable rows, or Project fields.
- The exporter omits issues without a concrete `next_action` or an explicit decision / blocker / acceptance signal.
- Legacy issues with missing structured fields are exported with `unknown` and `warnings`; missing fields are not inferred.

## Command

Offline input:

```bash
gh issue list --state open --limit 100 --json number,title,url,state,labels,assignees,updatedAt,body > /tmp/hl-dispatch-issues.json
python3 scripts/export-action-projection.py --input /tmp/hl-dispatch-issues.json
```

Live read-only input:

```bash
python3 scripts/export-action-projection.py --state open --limit 100
```

Write a local artifact only when explicitly requested:

```bash
python3 scripts/export-action-projection.py \
  --input /tmp/hl-dispatch-issues.json \
  --output /tmp/hl-dispatch-action-projection.json
```

## Output

```json
{
  "schema": "action-projection:v0.1",
  "source": "github",
  "generated_at": "2026-06-08T00:00:00Z",
  "counts": {
    "total_input": 1,
    "exported": 1,
    "omitted_no_action": 0
  },
  "items": []
}
```

Each item includes issue number, title, URL, projection class, package / slice / risk / work-unit IDs, DRI, risk path, next action, expected evidence, labels, assignees, updated time, fact source, and warnings.

## Projection Classes

- `action`: explicit concrete `next_action`.
- `decision`: decision label or decision request signal.
- `blocker`: blocker label, blocker wording, or structured blocker field.
- `acceptance`: acceptance-ready signal.

## E Dual Audit Summary

E1 delivery / evidence audit and E2 automation / safety audit passed with conditions before implementation.

Conditions applied:

- Include `counts.total_input`, `counts.exported`, and `counts.omitted_no_action`.
- Add per-item `warnings` for missing structured fields.
- Use stdout by default; write a file only with `--output`.
- Keep tests offline and deterministic.
- Use read-only `gh issue list` live mode without shell interpolation.
