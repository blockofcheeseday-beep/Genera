# Genera Take-Home — Ramp Deployment Pipeline

Turns one customer packet (raw transcripts, rosters, Slack exports, policy memos) into
two JSON files: a desired-state `ramp_config.json` and an `audit_log.json` that says
what was assumed, what is missing, what conflicts, and what Ramp cannot actually do.

The exercise spec is `candidate/README.md` and it is the source of truth for direction.

## Layout

```
.claude/skills/ramp-deployment/
  references/
    capabilities.yaml       SOURCE OF TRUTH — the capability ledger
    CAPABILITY_LEDGER.md    generated from the yaml, committed so it reads without running
  scripts/
    gen_ledger.py           regenerates the markdown; --check fails on staleness
candidate/                  exercise material, committed so the repo stays runnable
work/                       intermediates (requirements.json) — not graded
out/                        ONLY the two graded JSONs per packet
session/                    session export
```

## The capability ledger

The ledger is the part that makes this reusable. Its unit is *a thing customers ask for*
("the card must decline for this vendor"), not an endpoint — so a row written for one
packet answers the same question in the next one, including packets nobody has seen.

Each row carries a verdict (SUPPORTED / PARTIAL / UI_ONLY / UNSUPPORTED / DRIFT), the
endpoints and fields that implement it, dated evidence, and — for anything not fully
supported — a workaround. `evidence_line` is copied verbatim into audit-log evidence
fields, which is how several audit logs stay consistent with each other instead of each
re-arguing the same point.

Regenerate and check the markdown:

```
python3 .claude/skills/ramp-deployment/scripts/gen_ledger.py
python3 .claude/skills/ramp-deployment/scripts/gen_ledger.py --check
```

## Validating outputs

```
python3 candidate/tools/validate.py out/<packet>/ramp_config.json out/<packet>/audit_log.json
```
