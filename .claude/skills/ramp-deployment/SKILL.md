---
name: ramp-deployment
description: Turn a raw customer packet (call transcripts, rosters, Slack exports, policy memos) into a desired-state ramp_config.json plus an audit_log.json that records every assumption, gap, conflict, and unsupported request. Use when asked to run a customer packet, produce a Ramp deployment config, or build the two graded JSON outputs.
---

# Ramp deployment: packet to config

You are doing a deployment rep's first pass. A customer's messy reality goes in; a
concrete Ramp configuration and an honest audit trail come out.

**The audit log is half the deliverable.** A deployment rep trusts the config exactly as
far as the audit log is honest. A confidently wrong config is the worst possible outcome —
worse than an incomplete one. When in doubt, flag it.

## Run it

```
python3 run_pipeline.py --packet client_a_acme_corp     # Phase 0: setup + runbook
python3 run_pipeline.py --packet client_a_acme_corp --verify   # Phase 4: all checks
```

Phase 0 and Phase 4 are mechanical and scripted. **Phases 1-3 are yours** — the judgement
work is the job, and it does not automate.

## The one invariant

> Every requirement extracted in Phase 1 must terminate in a config field, an audit entry,
> or both. Nothing is dropped silently.

Phase 4 fails the run on any orphan. This is what makes "flag-forward" mechanically true
rather than aspirational.

## Files you will use

| Path | What it is |
|---|---|
| `references/capabilities.yaml` | **The capability ledger — 42 rows, source of truth for what Ramp can do.** Read it before deciding anything is impossible. |
| `references/CAPABILITY_LEDGER.md` | Same content, readable. Generated — never edit it. |
| `references/AUDIT_PATTERNS.md` | The four trigger classes. The engine of Phase 2. |
| `references/PRECEDENCE_RULES.md` | How conflicts resolve, per packet, with verbatim quotes. |
| `references/CATEGORY_MAP.md` | MCC to Ramp's 44 categories. Every mapping is lossy; log it. |
| `candidate/schemas/*.json` | The submission contract. `additionalProperties: false` throughout **both** files. |
| `candidate/sample_packet/.../example_output/` | Worked example. Study its idioms before writing anything. |

---

# Phase 1 — Extract

Read **every** file in the packet. Not a skim: the dirt is in the details, and packets are
deliberately built so the important things sit in asides.

Write `work/<packet>/requirements.json`:

```json
{"packet": "client_a_acme_corp",
 "requirements": [
   {"req_id": "REQ-001",
    "claim": "CEO's card should effectively have no limit",
    "source_file": "discovery_call_01.txt",
    "source_quote": "I never want to see a decline",
    "archetype_id": "CAP-UNLIMITED",
    "confidence": "high"}]}
```

**Capture every quote verbatim, at extraction time.** Copy it out of the file as you read.
Reconstructing a quote later from memory is exactly how citations get hallucinated, and
Phase 4 checks every one of them against the file with a substring match. The audit schema
wants "file + line/quote"; this is where you earn it.

Tag each requirement with the closest ledger `archetype_id`, or `null` if nothing fits.
A `null` is a signal, not a failure — it means the ledger may need a new row. Say so.

If the packet has a roster CSV, run the linter before you trust it:

```
python3 .claude/skills/ramp-deployment/scripts/lint_roster.py <path-to-csv>
```

It deterministically finds duplicate emails with disagreeing values, blank cells,
non-numeric limits, case-variant department names, and dangling manager references. These
become `conflicts` and `missing_information_flags` rows. An LLM reading a 33-row CSV will
skim past all five classes; the script will not.

---

# Phase 2 — Flag

**Write the audit log before the config exists.** This ordering is deliberate: if you
compose first, the audit log becomes a rationalization of what you already built. Flagging
first makes composition downstream of the flags.

Write `out/<packet>/audit_log.json`. Four trigger classes, each feeding one array — the
full taxonomy with worked examples is in `references/AUDIT_PATTERNS.md`. In brief:

| Array | Fires on |
|---|---|
| `assumptions_made` | any value not literally stated; inference from headcount; role mapping; currency normalization; MCC translation; group fan-out; rounding; every `UI_ONLY` capability you omitted |
| `missing_information_flags` | named person without an email; a document referenced but absent; headcount with no roster; unresolvable manager; anything a source says is "coming" |
| `conflicts` | same field, two values; a source contradicting itself; supersession by time |
| `unsupported_api_requests` | any requirement whose ledger verdict is not `SUPPORTED` |

Three rules that matter more than the rest:

1. **A stated precedence rule does not suppress a conflict.** The schema is explicit: "Do
   not silently pick a winner — record both, say which you provisionally encoded and why."
   The rule goes in `provisional_resolution`. The conflict still gets logged.
2. **Copy `evidence` verbatim from the ledger row's `evidence_line`.** Never compose it
   fresh. That is how several audit logs stay consistent with each other instead of each
   re-arguing the same point. `proposed_manual_workaround` comes from the row's `workaround`.
3. **Do not list things the API supports.** Getting `unsupported_api_requests` right
   *including not over-listing* is explicitly graded. Check the ledger verdict before you
   claim anything is impossible — several verdicts that look like gaps are `UI_ONLY`
   (real capability, wrong surface) or `PARTIAL` (possible with a caveat).

> "An empty audit log on a messy packet is a red flag, not an achievement."

---

# Phase 3 — Compose

Write `out/<packet>/ramp_config.json`, walking the eight sections in schema order:
`entities, departments, locations, users, spend_programs, limits, approval_policies,
mcc_controls`.

Consult the ledger per requirement. What a verdict means for where the requirement lands:

| Verdict | In the config? | In the audit log? |
|---|---|---|
| `SUPPORTED` | yes | only if you inferred a value |
| `PARTIAL` | yes | **always** — `unsupported_api_requests`, naming the caveat |
| `UI_ONLY` | yes if the schema has a home; otherwise omit | **always** |
| `UNSUPPORTED` | yes if the schema has a home; otherwise omit | **always** |
| `DRIFT` | emit the **schema** shape, not the live API's | **always** — once per packet is enough |

`UNSUPPORTED` and `UI_ONLY` items still belong in the config as desired state wherever the
schema has somewhere to put them — the schema descriptions for `entities` and
`approval_policies` explicitly invite exactly this. Where there is no home (receipt
thresholds, memo rules), they live only in the audit log. That omit-and-flag move is the
idiom the Westbrook sample demonstrates with its $50 receipt rule.

Then write `work/<packet>/traceability.json`, linking every requirement to where it landed:

```json
{"packet": "client_a_acme_corp",
 "entries": [
   {"req_id": "REQ-001", "archetype_id": "CAP-UNLIMITED", "disposition": "both",
    "config_paths": ["limits[3]"], "audit_refs": ["assumptions_made[2]"]}]}
```

This file is how Phase 4 proves the coverage invariant and runs both graded sweeps. It
lives in `work/` because both output schemas set `additionalProperties: false`, so there is
nowhere in `out/` to carry the linkage.

## Idioms worth copying from the sample

Read `candidate/sample_packet/.../example_output/ramp_config.json` before composing. It is
short and every line of it is a decision:

- `approval_policies[].source` carries the **verbatim quote** the policy came from
  (`"intake_email.txt — 'Anything over $1,000 needs Priti's approval.'"`). Use it; it is
  where a reviewer looks when sources conflict.
- A tier list starts at `{"threshold_usd_cents": 0, "approver": "AUTO"}` — the auto-approve
  floor is an explicit tier, not an absence.
- A group limit says the fan-out in `notes`: *"One per Studio member (9 people) once the
  roster arrives."* Never leave a group limit's cardinality implicit.
- An unknown surname is encoded `"(surname pending roster)"` and paired with a **blocking**
  missing-information flag, rather than invented or left blank.
- `mcc_controls[].applies_to` is a limit or spend-program `display_name` — it must match one
  you actually emitted.

## Schema traps

These will bite. The validator catches none of them.

- **`limits[].assigned_to`** — the description says exactly one of `user_email` or `group`
  must be set, but there is **no `oneOf`**, so nothing enforces it. `--verify` checks it.
- **`threshold_usd_cents` is USD by field name.** A packet quoting approval thresholds in
  MXN or BRL creates a real tension. That needs an audit entry, not a silent conversion.
- **Six roles, no `BUSINESS_OWNER`.** Map owners to `BUSINESS_ADMIN` and log the mapping.
- **No `allowed_mcc_codes` mechanism** — the enum has `blocked_mcc_codes` but allow-listing
  exists only at category granularity. See `CATEGORY_MAP.md`.
- **Categories are name strings here, integer codes in the API.** `allowed_categories` is
  `array<string>` in this schema and the sample writes `"Software / SaaS"` — but the live API
  takes integer codes (`40`) on `allowed_category_codes`. Emit the **name**; record the code
  in `translation_notes` so the mapping survives into deployment. Getting this backwards
  validates cleanly and is wrong.
- **Seven intervals, no `TERTIARY`.** The live API has eight.
- **`permitted_spend_types` takes exactly two booleans** and forbids anything else.
- `out/` contains **only** the two JSON files. Intermediates go in `work/`.

---

# Phase 4 — Verify

```
python3 run_pipeline.py --packet <packet> --verify
```

Six checks, in order: outputs parse; both files validate against the shipped schemas; every
quote matches its source file; the coverage invariant plus both graded sweeps; the
`assigned_to` exactly-one rule; ledger freshness.

The two sweeps are the ones the exercise grades explicitly, in **both** directions:

- **False-positive sweep** — nothing sits in `unsupported_api_requests` that the ledger
  marks `SUPPORTED`. Claiming Ramp cannot do something it can is a failure mode, and it is
  the one candidates miss.
- **False-negative sweep** — nothing is configured as if fully supported when the ledger
  says `UNSUPPORTED`, `UI_ONLY`, or `PARTIAL` and the audit log says nothing about it.

Fix what it reports and run it again. Green is the bar.

---

# Working notes

**If the ledger is wrong, fix the ledger.** When a packet reveals a capability question no
row answers, add the row to `references/capabilities.yaml`, regenerate with
`scripts/gen_ledger.py`, and commit that separately. The ledger is the reusable asset here —
it is what makes the next packet cheaper, including one nobody has seen. A `null`
`archetype_id` in Phase 1 is the signal.

**Evidence beats absence.** "This endpoint isn't in the OpenAPI snapshot" is weak evidence
that Ramp cannot do something — it may be a UI capability, or a renamed path. Three ledger
verdicts were corrected on exactly this point. Where a claim is load-bearing, corroborate it
against the live docs before the audit log asserts it, and cite what you checked and when.

**Script budget.** If a check cannot be written in about 40 lines, it becomes an instruction
here instead of a script. The deliverable is instructions plus small scripts; anything that
smells like infrastructure is out of scope.

**Time discipline.** Packets A, C and D are the core. If you are running over, cut E, then
B. Never cut the audit logs.
