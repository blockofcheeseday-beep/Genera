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
| `references/capabilities.yaml` | **The capability ledger — 43 rows, source of truth for what Ramp can do.** Read it before deciding anything is impossible. |
| `references/CAPABILITY_LEDGER.md` | Same content, readable. Generated — never edit it. |
| `references/AUDIT_PATTERNS.md` | The four trigger classes. The engine of Phase 2. |
| `references/PRECEDENCE_RULES.md` | How conflicts resolve, per packet, with verbatim quotes. |
| `references/CATEGORY_MAP.md` | MCC to Ramp's 43 category codes. Every mapping is lossy; log it. |
| `candidate/schemas/*.json` | The submission contract. `additionalProperties: false` throughout **both** files. |
| `candidate/sample_packet/.../example_output/` | Worked example. Study its idioms before writing anything. |

---

# Phase 1 — Extract

## Read the packet on its own terms first

Before extracting anything, answer three questions about the packet itself. Each one has
changed the shape of a deliverable at least once.

**1. Does any document dictate how it must be answered?** Packet C's compliance file is a
vendor-response instrument: it numbers its requirements `REQ-1`…`REQ-6`, demands each be
answered `ENFORCED BY PLATFORM` / `ENFORCED BY PROCESS` / `NOT MET`, and warns that vague
responses will be returned. A packet that specifies its own response format is telling you
the grading rubric. Adopt its numbering and its vocabulary verbatim in the audit log.

**The customer's vocabulary outranks these instructions.** When a customer's own terms
collide with a house style rule, the customer wins and the rule bends. The jargon check
originally rejected `REQ-1` as internal vocabulary — it was Apex's own mandated numbering.
If a check fires on something the customer requires, fix the check, do not launder the
customer's language.

**2. Who exists, and can they be identified?** Packet A shipped a 32-row roster. Packet C
named six people, one without a surname, and contained **no email address and no email
domain at all**. When identity is missing, do not stall and do not quietly invent:

- **Never invent an email address.** Use a real one only where the packet contains it. Where
  it does not, the value is the literal string `N/A` — not a constructed
  `firstname.lastname@company.example`. A plausible-looking address is indistinguishable
  from a real one to whoever runs the deployment, and inviting it either fails silently or
  reaches a stranger. `--verify` check 8 enforces this: every email domain must appear
  somewhere in the customer's own documents, or the value must be `N/A`.
- **A missing name is declared, not invented or blanked.** Two approved forms, and the choice
  between them is a factual claim about the packet:
  `"(surname pending roster)"` where a roster genuinely is coming, and
  `"(surname not stated)"` where the packet simply never gives one. Substitute the part that
  is missing — `(full name not stated)`, `(first name pending roster)`. Do not write `TBD`,
  `Unknown`, `N/A` or an empty string in a name field: those read as a blank rather than a
  decision, and `N/A` is reserved for addresses. Pair any placeholder with a **blocking** flag
  that names the person. Check 8 enforces the form, the vocabulary, and the pairing.
  A name is descriptive; an address is actionable, which is why they differ — but an invented
  surname still produces a person who does not exist, so neither is guessable.
- Raise a **blocking** flag saying no user may be invited until real addresses arrive, and
  identify each cardholder by name in the limit's `display_name` so an `N/A` address does not
  make the limit ambiguous.

A configuration naming known people with flagged placeholders is useful. An empty `users`
array is not.

**3. What is not in the packet at all?** Locations, shipping addresses, end dates,
headcounts. These become blocking flags, and they are easy to miss precisely because
nothing in the packet mentions them.

## Look at the money before you compose

```
python3 .claude/skills/ramp-deployment/scripts/money_map.py --packet <packet>
```

Lists every monetary figure across every file with its location and context, then collates
them by amount. Two figures from two different documents sitting adjacent in that sorted
list is the signature of a real conflict.

That is how packet C's sharpest finding surfaced: the compliance document requires a
purchase order above **$500**, while the discovery call sets the clinic per-transaction cap
at **$1,000** — so a $700 purchase is approved by the card while sitting inside the
purchase-order rule. Neither document notices. It is only visible side by side.

The script asserts nothing. Judging whether two figures actually collide is yours, and a
real collision becomes a `conflicts` entry.

## Lint the roster, if there is one

If the packet has a roster CSV, run the linter before you trust it:

```
python3 .claude/skills/ramp-deployment/scripts/lint_roster.py <path-to-csv>
```

It deterministically finds duplicate emails with disagreeing values, blank cells,
non-numeric limits, case-variant department names, and dangling manager references. These
become `conflicts` and `missing_information_flags` rows. An LLM reading a 33-row CSV will
skim past all five classes; the script will not.

---

## Then extract

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

Build citations with the tool rather than by hand:

```
python3 .claude/skills/ramp-deployment/scripts/cite.py --packet <packet> --speakers
python3 .claude/skills/ramp-deployment/scripts/cite.py --packet <packet> --quote "..." --context "..."
```

It locates the quote, derives the speaker, role and timestamp from the file, and emits a
citation that satisfies the Phase 4 gate. Run `--speakers` first on an unfamiliar packet to
check the parse before building thirty citations on it. Hand-written citations are how
attribution goes wrong.

`source_quote` must be a **contiguous span** — no `...` elision, no stitching two sentences
together. The check is a substring match after whitespace and unicode-punctuation
normalization, so an elided quote fails even when it is honest. If the useful material spans
a gap, either quote the shorter contiguous piece or split it into two requirements. (Prose in
`NOTES.md` and the reference docs may elide freely; this rule is only about
`requirements.json`.)

Tag each requirement with the closest ledger `archetype_id`, or `null` if nothing fits.
A `null` is a signal, not a failure — it means the ledger may need a new row. Say so. A
*cluster* of nulls means the ledger does not yet cover this customer's kind of problem;
stop and add rows before composing, or the audit log will be thin in exactly the places
that matter.


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
   re-arguing the same point. `proposed_manual_workaround` is copied from the row's
   **`customer_workaround`** — never from `workaround`, which is the internal note and
   carries row IDs and jargon the customer must not see.
3. **Do not list things the API supports.** Getting `unsupported_api_requests` right
   *including not over-listing* is explicitly graded. Check the ledger verdict before you
   claim anything is impossible — several verdicts that look like gaps are `UI_ONLY`
   (real capability, wrong surface) or `PARTIAL` (possible with a caveat).

> "An empty audit log on a messy packet is a red flag, not an achievement."

## Write it for the customer

**The audit log is a customer-facing document.** For Acme it is read by their finance team,
and it will be forwarded internally. It is not a working note. Three rules, all enforced by
`--verify` check 5:

1. **Never use a pronoun for a person — name them.** Not *"his card declines"* but *"Marcus
   Webb's card declines"*. This covers `they`/`them` too: a generic plural is exactly the
   vagueness the rule exists to prevent. Rewrite the sentence rather than reaching for a
   pronoun. The one exception is a verbatim quote inside a `source` field — never misquote a
   customer to satisfy a style rule.

2. **A citation must be verifiable without opening the file.** Name the file, attribute the
   line, and quote it. A bare quote plus a timestamp is not enough: `discovery_call_01.txt —
   'Priya and me.' [05:41]` leaves the reader unable to tell who "me" is or why the line
   supports the point. Give the speaker, the role, and enough surrounding context that the
   quote carries its meaning:

   ```
   discovery_call_01.txt — Diane Marsh (VP Finance), [05:41], naming who should administer
   the Ramp instance: "Priya and me."

   department_roster.csv, row 15 — "Jenny Park,jpark@acme.example,Engineer,Engineering,
   dkim@acme.example,2022-10-17,500"
   ```

   Check 5 re-verifies the quoted span against the named packet file, so a citation cannot
   drift from its source any more than a Phase 1 quote can.

3. **No internal vocabulary.** No ledger row IDs (`CAP-…`, `DRIFT-…`), no `req_id`, no
   "archetype", no "fan-out". Say "one card per person", not "fans out to N funds". Plain-
   language a Ramp role name on first use — `AUDITOR` becomes "the Auditor role (read-only
   access across the account)".

Write `impact_if_wrong` as a consequence in the customer's world — who can spend what, who
sees what, what breaks and when — never as a statement about the configuration file.

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

**Never widen a permission by inference.** Narrowing on a judgement call is recoverable — a
decline gets reported and fixed. Widening is not: a category, vendor or limit nobody asked
for grants spend the customer never authorised, and nothing surfaces it. Packet D's software
programme was drafted with Ramp's Cloud computing category added on the reasoning that a
company with 340 vendors probably runs infrastructure. Nothing in the packet mentioned
infrastructure. It was withdrawn, the narrower mapping kept, and the question asked instead.

The corollary: when you narrow, say so where the customer will see it. A note buried in the
config's `translation_notes` is not a flag — the audit log is what gets read. Any inference
that changes what a card will accept or refuse belongs in `assumptions_made` with its
consequence spelled out, and usually in `missing_information_flags` as a question.

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

## When the customer demands an answer to every requirement

A numbered requirements document expects a verdict on each item — including the ones Ramp
handles perfectly. Those have nowhere obvious to go: the audit log has no "works fine"
array, and filing a `SUPPORTED` capability under `unsupported_api_requests` trips the
false-positive sweep, correctly.

Put them in `assumptions_made`, stating the verdict in the first sentence and then the
encoding decision and any operational gap. Packet C's REQ-4 and REQ-5 are the worked
examples: both are `ENFORCED BY PLATFORM`, and both still carry a real caveat — no
assignment end dates exist anywhere in the packet, and only one member of the Compliance
Office is named. The verdict is a win; the gap is still worth the customer's attention.

Check before shipping that **every** numbered requirement appears somewhere with an
explicit verdict. A requirement the customer numbered and you did not answer reads as an
evasion.

## Idioms worth copying from the sample

Read `candidate/sample_packet/.../example_output/ramp_config.json` before composing. It is
short and every line of it is a decision:

- `approval_policies[].source` carries the **verbatim quote** the policy came from
  (`"intake_email.txt — 'Anything over 1,000 dollars needs Priti's approval.'"` — the sample
  quotes the figure with a dollar sign; written without one here because a literal `$1` in
  this file gets eaten by skill argument substitution). Use it; it is
  where a reviewer looks when sources conflict.
- A tier list starts at `{"threshold_usd_cents": 0, "approver": "AUTO"}` — the auto-approve
  floor is an explicit tier, not an absence.
- A group limit says the fan-out in `notes`: *"One per Studio member (9 people) once the
  roster arrives."* Never leave a group limit's cardinality implicit.
- An unknown surname is encoded `"(surname pending roster)"` and paired with a **blocking**
  missing-information flag, rather than invented or left blank.
- `mcc_controls[].applies_to` is a limit or spend-program `display_name` — it must match one
  you actually emitted.
- **A group limit must state its cardinality in `notes`** — how many people, and whether the
  number is stated or assumed. "One per clinic manager (14 assumed, one per clinic; none are
  named in the packet)" tells a reviewer the exposure and the uncertainty in one line.
- **A rule that is not amount-shaped still has to go in `tiers[]`, which is keyed only on
  amount.** "Any new vendor needs approval regardless of amount" and "anything Compliance
  flags comes to me" both encode as a zero-threshold tier — which then catches *all* spend on
  that target, not just the intended subset. Encode it, say so in the policy's `source`
  field, and log the over-capture. This has now recurred in two packets; expect it again.

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
- **Optional fields are omitted, not nulled.** `affected_config` is optional on a
  missing-information flag, but its type is `string` — emitting `null` fails validation.
  Only `direct_manager_email` is explicitly nullable.
- **Names must point at something you emitted.** A user's `department`, an
  `mcc_controls[].applies_to`, a `limits[].spend_program`, a `direct_manager_email` — all
  are free strings to the schema, so a typo or a stray case-normalization validates
  cleanly and is wrong. Normalizing roster departments with `.title()` turns `IT` into
  `It`, which silently orphans that user from the department you created. `--verify`
  check 6 catches this class; it exists because that exact bug got through packet A.
- `out/` contains **only** the two JSON files. Intermediates go in `work/` — the rendered
  `view.html` included.

---

# Phase 4 — Verify

```
python3 run_pipeline.py --packet <packet> --verify
```

Nine checks, in order: outputs parse; both files validate against the shipped schemas;
every Phase 1 quote matches its source file; the coverage invariant plus both graded sweeps;
audit-log style (pronouns, citation quality, jargon, blocking order, dated evidence); the
`assigned_to` exactly-one rule; config cross-references; no invented identifiers;
ledger freshness.

The two sweeps are the ones the exercise grades explicitly, in **both** directions:

- **False-positive sweep** — nothing sits in `unsupported_api_requests` that the ledger
  marks `SUPPORTED`. Claiming Ramp cannot do something it can is a failure mode, and it is
  the one candidates miss.
- **False-negative sweep** — nothing is configured as if fully supported when the ledger
  says `UNSUPPORTED`, `UI_ONLY`, or `PARTIAL` and the audit log says nothing about it.

Fix what it reports and run it again. Green is the bar.

A fully green run also writes the customer-facing copies:

```
deliverables/Acme_Corp/Acme_Corp_Ramp_Config.json
deliverables/Acme_Corp/Acme_Corp_Audit_Log.json
```

`out/` keeps the canonical `ramp_config.json` / `audit_log.json` the exercise spec asks for,
so grading tooling still finds them. `deliverables/` carries the customer's name for anything
sent onward. Packaging runs **only** when every check passes — a skipped check blocks it too,
because a skip means the check did not actually happen and these copies are what a customer
receives.

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
