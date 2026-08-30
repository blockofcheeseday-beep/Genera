# Genera Take-Home — Ramp Deployment Pipeline

Turns one customer packet (raw transcripts, rosters, Slack exports, policy memos) into
two JSON files: a desired-state `ramp_config.json` and an `audit_log.json` that says
what was assumed, what is missing, what conflicts, and what Ramp cannot actually do.

The exercise spec is `candidate/README.md` and it is the source of truth for direction.

## Running a packet

```
python3 run_pipeline.py --list                          # what packets exist
python3 run_pipeline.py --packet client_a_acme_corp     # Phase 0: setup + printed runbook
#   ... the agent does Phases 1-3, guided by SKILL.md ...
python3 run_pipeline.py --packet client_a_acme_corp --verify    # Phase 4: all checks
```

`run_pipeline.py` is glue, not an engine. It does the deterministic parts — inventorying the
packet, scaffolding `work/` and `out/`, and running every check — and prints a runbook telling
a fresh session what to do in between. The judgement work (reading messy transcripts,
resolving conflicts, deciding what Ramp genuinely cannot do) is done by the Claude session
following `.claude/skills/ramp-deployment/SKILL.md`. That split is deliberate: the parts that
should be reproducible are code, and the parts that need judgement are instructions.

### The four phases

| Phase | Who | Output |
|---|---|---|
| 0 Setup | script | `work/<packet>/packet_manifest.json` + printed runbook |
| 1 Extract | agent | `work/<packet>/requirements.json` — every claim with a verbatim quote |
| 2 Flag | agent | `out/<packet>/audit_log.json` — written *before* the config exists |
| 3 Compose | agent | `out/<packet>/ramp_config.json` + `work/<packet>/traceability.json` |
| 4 Verify | script | pass/fail table; non-zero exit on any failure |

Phase 2 runs before Phase 3 on purpose. Compose first and the audit log becomes a
rationalization of what you already built.

**The coverage invariant:** every requirement extracted in Phase 1 must terminate in a config
field, an audit entry, or both. Phase 4 fails the run on any orphan — which is what makes
"flag-forward" mechanically enforced rather than aspirational.

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

## Verification

`--verify` runs seven checks: outputs parse, both files validate against the shipped
schemas, every quote substring-matches its source file, the coverage invariant plus both
graded sweeps, the `assigned_to` exactly-one rule the schema describes but does not
enforce, config cross-references (every department, program, limit and manager name points
at something the config actually emits), and ledger freshness.

The two sweeps check the failure modes the exercise grades in both directions:

- **false positive** — nothing claimed impossible that the ledger says is `SUPPORTED`
- **false negative** — nothing silently configured as fully supported when the ledger says
  `UNSUPPORTED`, `UI_ONLY` or `PARTIAL` and the audit log is silent about it

## Validating outputs

```
python3 candidate/tools/validate.py out/<packet>/ramp_config.json out/<packet>/audit_log.json
```
