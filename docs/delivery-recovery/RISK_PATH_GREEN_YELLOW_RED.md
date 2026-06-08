# Risk Path Green Yellow Red

Every Mission Package, Delivery Slice, Work Unit, and PR must declare one risk path.

## Green

Use `green` for sandbox, mock, docs, check-only work, or work with no real data, no secret, and no production impact.

Required action:

- include test or grep evidence;
- include explicit non-goals;
- avoid workflow or business logic changes.

Governance budget:

- 1 Mission Package;
- 1 Delivery Slice;
- at most 3-5 Work Units;
- no new ledger issue;
- AI review + owner self-check.

Examples:

- delivery recovery docs;
- PR template text;
- Issue Form fields that do not remove existing forms.

## Yellow

Use `yellow` for runtime, contract read path, external sandbox API, multi-repository changes, or changes that can affect contributor behavior, PR review, Issue creation, CI configuration, notification routing, or acceptance gates.

Required action:

- include before/after file list;
- run static validation or script tests when available;
- identify notification, CI, PR template, and issue form risk;
- keep rollback simple.

Governance budget:

- human reviewer allowed;
- contract review allowed;
- 1 blocker allowed before escalation or re-slicing.
- test evidence required.

Examples:

- modifying existing Issue Forms;
- editing `.github/copilot-instructions.md`;
- changing PR template required sections;
- touching human-readable gate language.

## Red

Use `red` for production, real user data, provider secret, real billing, customer-visible impact, or changes that can affect business logic, runtime behavior, secrets, permissions, branch protection, route identity, notification delivery code, or required CI gates.

Required action:

- split into a separate PR;
- require explicit owner review;
- include command evidence and rollback notes;
- do not combine with recovery-template cleanup.

Governance budget:

- must use a Risk-Retirement Slice when the path is blocked by architecture, provider, secret, or external dependency risk;
- must declare an unblock condition;
- must declare a decision deadline.
- security / product / release approval required when applicable.

Examples:

- `.github/workflows/feishu-notify.yml` logic changes;
- `issue_comment` workflow behavior changes;
- CI enforcement or branch protection changes;
- `hl-platform` runtime start, smoke, or integration behavior changes.

## Exception Lane

P0 incident, trivial fix, CI failure fix, and security urgent fix may enter through the Exception Lane. Backfill the package/slice context after the urgent action, and keep evidence in GitHub Issues, PRs, or repo files.

## Default

If uncertain, choose `yellow` and name the uncertainty in `ai-output:v1`.
