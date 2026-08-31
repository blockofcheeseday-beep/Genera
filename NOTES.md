# NOTES

Five packets, nine checks each. Pointers are turn numbers from this session's transcript and
commit hashes from this repository.

## Decisions

### 1. The audit log is written before the config, not after it

Phase 2 emits `audit_log.json` before Phase 3 emits `ramp_config.json` (`3203145`).
Composing first and documenting after produces an audit log that rationalises a config
already written; flagging first makes the config the consequence of the flags.

**Passed on:** compose, then annotate. Faster, and the output reads identically — which is
the problem. It is how a confidently wrong config acquires a confident audit log.

**Where:** turn 2, at the very start — "write SKILL.md, run_pipeline.py as a mix of glue code"

### 2. Judgement stays with the session; only the deterministic parts are code

`run_pipeline.py` inventories the packet and runs nine checks. Reading a messy transcript,
resolving a conflict and deciding what Ramp cannot do stay with the agent, guided by
`SKILL.md`.

**Passed on:** a scripted extractor. It would have worked on packet A's clean roster and
failed on packet D, which has no documents at all — a Slack export and second-hand notes
that disagree.

**Where:** turn 2, at the very start — "such that a fresh Claude Code or Codex session can run any packet end-to-end"

### 3. The capability ledger is keyed on customer requests, not endpoints

Forty-three rows keyed on what customers say — "the card must decline for this vendor" —
each with a verdict, dated evidence and a workaround. Each packet was cheaper than the last
because the same rows fired across all five.

**Passed on:** an endpoint-keyed API reference. Accurate, and nobody opens it mid-transcript.

**Where:** turn 1, at the very start — "focusing on the capability ledger"

### 4. Every rule that mattered became a check, because I broke the ones I only wrote down

The pronoun rule, the no-invented-identifier rule and the name-placeholder rule were each
violated by text I wrote *after* writing the rule. Nine checks now gate every packet, and
only a fully green run writes `deliverables/`.

**Passed on:** documenting the standards and relying on care. Measured on the first audit
log, care produced 36 pronoun violations and 17 unattributed citations.

**Where:** turn 7, early on — "Because this is customer facing, let's never write notes with"

## Verification delta

### The ledger told Vanguard's district managers they could not be served

**Believed:** `CAP-SCOPED-VISIBILITY` was UNSUPPORTED, reasoned from `GET /roles` being
read-only — no custom roles, therefore no scoping.

**Evidence:** *User roles overview* states visibility follows the management chain, not
department labels, and that chain is settable via `direct_manager_id`.

**Change:** corrected to PARTIAL (`86be791`). Packet E asks precisely this — six district
managers seeing only their own district — so uncorrected I would have called a supported
requirement impossible in the packet where it matters most. Every correction in that pass ran
one way: the snapshot-only reading over-claimed what Ramp cannot do.

### The coverage invariant was hollow

**Believed:** the central promise — every requirement terminates in a config field or an
audit entry — was enforced.

**Evidence:** against the Westbrook sample's real outputs, the check passed while my fixture
cited `assumptions_made[999]` against an array holding one entry. Nothing resolved citations
against the document.

**Change:** added a reference-resolution check (`ae90065`), which immediately caught two
further dangling references I had written myself.

### Both CEOs held administrative rights nobody granted

**Believed:** an owner maps to `BUSINESS_ADMIN`, generalised from the Westbrook sample.

**Evidence:** Acme's administrators were named as "Priya and me"; Hypergrowth's as "me and
maya", the stated reason for the assistant being to keep account changes away from the CEO.
Neither CEO was in either list.

**Change:** both became `BUSINESS_USER`, and the ledger row now maps by administrative
responsibility rather than job title (`29059cd`). Found by re-reading A and C against a rule
derived from D — three more surfaced the same way, including a `.title()` normaliser that
turned `IT` into `It`, orphaning a user from the department the same config creates.

## What the Ramp docs changed

`docs.ramp.com` was blocked by this environment's egress proxy for both `curl` and page
fetches. Search was the only live channel, so these rest on page titles and quoted excerpts,
not full pages.

- **Entities** — the accounting guide states positively that entities are created in the Ramp
  UI and scoped by `entity_id` when fetched. Moved `CAP-ENTITY-CREATE` from absence-based
  UNSUPPORTED to evidenced UI_ONLY, validating packet B's `status: requested`.
- **Roles** — *User role deep-dive: IT Admin* supplies semantics the spec does not:
  `IT_ADMIN` grants People and Integrations access while denying spend controls — exactly the
  "manage users but not limits" split Acme and Hypergrowth both asked for.
- **Categories** — *Setting up category and merchant restrictions* confirms Ramp derives its
  category from the MCC plus other signals, so an MCC allow-list is not expressible anywhere
  in the product, UI included. That is the whole of packet E's problem.
- **Naming** — the docs still title the resource *Creating spend limits* while the snapshot
  path is `/developer/v1/funds`. Claiming the concept absent would have been the easiest
  wrong answer in the set.

## Go-live handoff — Apex Health Partners

- **REQ-3 is not met as written, and Compliance should see it in those words.** Ramp cannot
  check a purchase order while a card is being authorised. What is configured instead is the
  control your own document provides for: hard per-transaction caps, same-day reconciliation
  against NetSuite, suspension on violation. That is detective, not preventive.
- **There is a $500 gap between your two documents that neither mentions.** Your compliance
  document requires a purchase order above $500; the discovery call sets the clinic
  per-transaction cap at $1,000. A $700 clinic purchase is approved by the card and falls
  inside the purchase-order rule. Accept reconciliation as the control for that band, or
  lower the cap.
- **The high-limit card gate fails closed, but a person is the gate.** Cards above $10,000 a
  month are created and immediately suspended, and stay suspended until your office confirms
  the notarised form. Ramp does not verify the form exists; the Compliance Office does.
- **The vendor block needs one thing from you before it works.** Both trading names, Joe's
  Medical Supply and JMS Distribution, must resolve to merchant records in Ramp. A name that
  does not resolve is not blocked. The block must also be re-applied to every card programme
  created later.
- **Nothing can be issued until the roster arrives.** Eight questions are open that stop
  go-live; the largest is that we have no email address for anyone and no clinic manager is
  named. Your three-week clinic timeline starts when that list does.

## One capability, one question

**Capability: the ledger, owned centrally.** Every packet asked the same forty-odd questions
— can Ramp block a vendor, expire a card, scope a manager's view, allow-list an MCC — and the
answers do not vary by customer. Built once with dated evidence per row, it costs days and
removes that re-derivation from every deployment after. Rows written for Acme answered Apex;
rows added for Apex answered Vanguard. Runner-up was the audit-log style gate, which travels
less well: it encodes one house voice, the ledger encodes facts.

**Question, for Vanguard Retail Services:** your field force roughly doubles every October
and collapses on 24 December, and the reps live in a spreadsheet rebuilt each year. Should
the seasonal wave become a standing annual motion — a saved role-to-control mapping and a
re-runnable onboarding flow — rather than a configuration rebuilt each season?

## What I'd do next with another day

Reconcile the ledger against the live OpenAPI specification, which I could not reach; every
drift row rests on a point-in-time snapshot, and drift ages worst. Then build the check I do
not have: nothing catches a *silently widened* permission on a SUPPORTED capability, which is
how Cloud computing reached Hypergrowth's software card and how both CEOs got administrative
rights — all caught by reading, not tooling. Then the Spanish executive summary Logística
Globex asked for, which the JSON cannot satisfy. Shipped knowingly imperfect: packet C's
clinic programme permits General merchandise as the nearest category to "hardware stores",
broader than that packet's compliance posture deserves.
