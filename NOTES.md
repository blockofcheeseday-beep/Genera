# NOTES.md — what I decided, and how I checked it

Anchors are commit hashes; `git log` is the session timeline. Packets A, C and D are complete,
each 9/9 green under `run_pipeline.py --verify`.

## Decisions

### 1. Instructions plus small scripts — the judgement was never automated
Python does Phase 0 (inventory, scaffold, runbook) and Phase 4 (nine checks); reading messy
documents and deciding what Ramp cannot do stay with the agent.
**Passed on:** a scripted extractor parsing transcripts into requirements. Packet D settled it:
a Slack export and second-hand notes that disagree have no structure to parse, and an extractor
good enough for D would be the whole exercise.
**Where:** `8567351`; phase structure at `3203145`.

### 2. The capability ledger came before any packet, keyed on customer asks
43 rows, each a thing customers ask for ("the card must decline for this vendor"), not an
endpoint — verdict, dated evidence, workaround, and an `evidence_line` copied verbatim into
audit logs, which is why three of them agree.
**Passed on:** answering can/can't per packet as it arose — faster to the first deliverable,
and it degrades: the same question gets a different answer in C than in A, and nothing carries
to a packet nobody has seen yet.
**Where:** `ab1f6db` → `86be791` → `acddd09` — the first hour, before any output existed.

### 3. The audit log is written before the config, and coverage is enforced
Every requirement must terminate in a config field, an audit entry, or both; `--verify`
fails the run on any orphan.
**Passed on:** compose first, document after — the natural order, and it turns the audit log
into a rationalization, flagging only where the config was already awkward. A second pass made
the audit log customer-facing and gated its prose (`check_audit_style.py`) after a packet A review
rejected an unresolvable pronoun and an unusable citation.
**Where:** `3203145`, hardened at `ae90065`; the style gate at `9ee2b59` and `1a27bb8`.

## Verification delta

### A capability I marked UNSUPPORTED that Ramp actually supports
**Believed:** scoped visibility — "a manager sees only their own slice of spend" — was
impossible: `/roles` is GET-only in the snapshot and the role enum has no scoping dimension.
**Evidence:** support.ramp.com "User roles overview", checked 2026-08-30 — visibility follows
the *management chain*, not department labels, and manager permissions are scoped to their
team. That is reachable from the API via `direct_manager_id` / `is_manager`.
**Change:** UNSUPPORTED → PARTIAL, workaround inverted — model the reporting chain first,
escalating to Custom Roles only where scoping follows neither reporting lines nor a role.
This is the false-negative the brief grades, and my first pass had it. Two more verdicts moved
on the same pass (`86be791`): absence from a snapshot is weak evidence, and I had been reading
it as strong.

### My own normalizer orphaned a user from a department the same file created
**Believed:** normalizing roster departments with `.title()` was harmless tidying.
**Evidence:** `IT` became `It` while `departments[]` still said `IT` — both valid strings, so
schema validation passed and the config was silently wrong.
**Change:** added `check_cross_refs` (`run_pipeline.py:158`) — every department, program,
limit and manager name must resolve to something the config emits.

### The coverage invariant was hollow
**Believed:** the coverage check enforced the invariant the pipeline is built on.
**Evidence:** a probe — a traceability reference to `assumptions_made[999]`, which does not
exist — passed cleanly.
**Change:** dangling references now fail (`ae90065`). A check that cannot fail is worse than
none, because the green run gets quoted.

## What the Ramp docs changed

- **The resource is `/funds`, not `/limits`** — yet docs.ramp.com still titles the page
  "Creating spend limits" (`/developer-api/v1/api/limits`), and *both* `limits:*` and `funds:*`
  OAuth scopes exist. Logged as drift, output shape unchanged. The likeliest place to produce a
  wrong "the API cannot do this" claim.
- **Approval chains are UI-only, not unsupported** — support.ramp.com "Set up your spend
  approval policies" describes a workflow builder with layered conditions. Ramp does this and
  the API cannot reach it, which changed every audit log's framing from "cannot" to "not via
  the API".
- **Restrictions replace, they do not merge** — spend limits reference: "the entire set of new
  spending restrictions must be passed". Absent from the snapshot; every edit is
  read-modify-write. It became a handoff bullet.
- **Categories are integer codes in the API, name strings in the schema** — emit the name,
  record the code in `translation_notes`; backwards validates cleanly and is wrong. And
  **production writes are disabled**: sandbox is a separate environment with its own base URL,
  so go-live is not a script pointed at production.

**Access constraint:** docs.ramp.com is blocked by org egress for curl and WebFetch here, so
WebSearch was the only live channel — these citations are page titles and snippets.

## Go-live handoff — Apex Health Partners

To Dana Whitfield, Controller (co-administrator with Gordon Pryce), before clinic go-live.

- **Nobody can be invited until we have real email addresses.** Your documents contain none,
  so every person is recorded as N/A — and the fourteen clinic managers are not named at all.
  That, not the configuration, is what puts the three-week clinic date at risk.
- **REQ-3 is not met as written, and no configuration change makes it met.** Ramp has no hook
  that runs while a card authorizes, so nothing can check NetSuite before a transaction is
  approved. The compensating control is same-day reconciliation, which your own compliance
  document provides for — please get Millie's sign-off in writing before go-live.
- **A gap sits between two of your own numbers.** Purchase orders are required above $500,
  but clinic managers have a $1,000 per-transaction cap — a $700 purchase is approved by the
  card while still inside the purchase-order rule. Decide which one moves.
- **Approval routing must be built in the Ramp app** — auto-approve within limits, manager
  approval over $500, compliance escalations to Gordon. Ramp supports all of it but the API
  cannot create it, so book an administrator session before go-live, not during.
- **Two things that bite quietly later.** The block on Joe's Medical Supply / JMS Distribution
  must be set on every spend program — there is no company-wide blocklist — and holds only if
  both trading names resolve to merchant records, which we need confirmed. And editing
  restrictions later *replaces* the whole set rather than merging, so a partial edit silently
  drops that block.

## One capability, one question

**Capability:** the ask-keyed capability ledger and the two sweeps enforcing it — nothing
claimed impossible that the ledger says is supported, nothing silently configured as supported
when it is not. Built once per partner product, cited by every audit log, re-verified when the
docs move. It made the third packet cheap and is the only asset here that pays off on a
customer nobody has seen. Runner-up: `money_map.py`, which found the $500/$1,000 straddle —
narrower, and it prompts rather than concludes.

**Question, for Apex Health Partners:** you asked for purchase-order enforcement at
authorization, which no card platform can do. Would a monthly exception report — spend above
$500 with no matching order — satisfy Compliance? If so that is a reporting build rather than
a controls build, which changes the scope.

## What I'd do next with another day

1. **Fix the over-capture I shipped.** "Any new vendor needs approval" is not amount-shaped,
   but `tiers[]` is keyed only on amount, so it becomes a zero-threshold tier catching *all*
   spend on that target. Flagged honestly, still a mismatch, twice now.
2. **Packet B, then E.** `money_map.py` already found 2,000 MXN as both a per-transaction
   ceiling and an auto-approve threshold, and `threshold_usd_cents` is USD by field name — an
   MXN policy is a tension, not a conversion.
3. **Date-stamp the ledger against live docs.** Freshness today means the markdown matches the
   YAML, not that the YAML matches Ramp.
