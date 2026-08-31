# NOTES

Five packets, each passing nine checks. What follows is what I decided, what I got wrong,
and how I found out. Commit hashes are the session pointers — the repository history is
the transcript.

## The audit log is the deliverable; the config is downstream of it

The exercise says the audit log is half the deliverable. I treated that as an ordering
constraint rather than a sentiment: Phase 2 writes `audit_log.json` **before** Phase 3
writes the config (`3203145`). Composing first and documenting afterwards produces an
audit log that rationalises a config already written. Flagging first forces the config to
be the consequence of the flags.

The alternative I passed on was the obvious one — compose, then annotate. It is faster and
it reads the same. It is also how a confidently wrong config gets a confident audit log.

## Verdicts derived from an OpenAPI snapshot are weaker evidence than they look

I built the capability ledger in two deliberate passes so the difference between them
would be visible. Pass 1 (`ab1f6db`) took every verdict from the 2026-08-30 snapshot
alone, and I asserted in code that no row cited anything else. Pass 2 (`86be791`) checked
the same rows against live documentation.

Every correction ran the same direction: the snapshot-only pass **over-claimed that Ramp
could not do things it can**. Absence of an endpoint is not evidence of absence of a
capability — it is evidence about an API surface. That distinction is the single most
useful thing I learned here, and `git diff ab1f6db 86be791` is the record of it.

I rejected keeping the ledger as prose. Machine-readable rows let the false-positive and
false-negative sweeps run as mechanical checks rather than as my own judgement about my
own work.

## The unit of the ledger is a customer request, not an endpoint

Forty-three rows, keyed on things customers say — "the card must decline for this vendor",
"I never want to see a decline" — not on API paths. This is what made packets cheaper as
the set went on: the same rows fired across all five. Keying on endpoints would have
produced a reference nobody consults while reading a transcript.

## Enforcement beats intention

Every rule that mattered ended up as a check in `run_pipeline.py --verify`, because the
rules I merely wrote down are the rules I personally broke. The pronoun rule, the
no-invented-identifier rule, and the name-placeholder rule were each violated by text I
wrote *after* writing the rule. Nine checks now gate every packet; a fully green run is
also the only thing that writes `deliverables/`.

# Verification delta

**The ledger told Vanguard's district managers they could not be served.** Pass 1 marked
`CAP-SCOPED-VISIBILITY` UNSUPPORTED, reasoning from `GET /roles` being read-only: no
custom roles, therefore no scoping. Ramp's *User roles overview* says visibility follows
the **management chain**, not department labels — and that chain is settable through the
API via `direct_manager_id`. Verdict corrected to PARTIAL (`86be791`). Packet E asks for
exactly this: six district managers seeing only their own district. Uncorrected, I would
have reported a supported requirement as impossible, in the packet where it matters most.

**My coverage invariant was hollow.** The pipeline's central promise is that every
extracted requirement terminates in a config field or an audit entry. Testing it against
the Westbrook sample's real outputs, the check passed while my fixture cited
`assumptions_made[999]` against an array with one entry (`ae90065`). Nothing resolved
citations against the document. "Everything lands somewhere" means nothing if the
somewhere need not exist. I added a resolution check, which immediately caught two more
dangling references I had written myself.

Three others, briefly: the category vocabulary is 43 codes, not the 44 I had inherited and
repeated in four places (`15e188f`); a `.title()` normaliser turned `IT` into `It`,
orphaning a user from the department the same config creates — both valid strings, so
schema validation passed (`9549f2f`); and both CEOs held administrative rights nobody
granted, in Hypergrowth's case against an explicit statement that the CEO should *not* be
making account changes (`29059cd`).

# What the Ramp documentation changed

`docs.ramp.com` and `ramp.com` were blocked by this environment's egress proxy for both
`curl` and page fetches. WebSearch was the only live channel, so what follows rests on
page titles and quoted excerpts, not full pages — worth stating plainly rather than
implying deeper reading.

- **Entities** — the accounting guide states it positively: *"Entities are created in the
  Ramp UI, and objects are scoped to an `entity_id` when fetching via the API."* This moved
  `CAP-ENTITY-CREATE` from an absence-based UNSUPPORTED to an evidenced UI_ONLY, and
  validated packet B's `status: requested`.
- **Roles** — *User roles overview* and *User role deep-dive: IT Admin* supply semantics the
  spec does not. `IT_ADMIN` grants People and Integrations access while explicitly denying
  spend controls, which is precisely the "manage users but not limits" split Acme and
  Hypergrowth both asked for. The enum value alone tells you nothing.
- **Approvals** — *Set up your spend approval policies* documents a workflow builder inside
  the application. The chain is real; only the API surface is missing. UI_ONLY, not
  unsupported.
- **Categories** — *Setting up category and merchant restrictions* confirms Ramp derives its
  own category from the MCC plus other signals. An MCC allow-list is therefore not
  expressible anywhere in the product, UI included — which is the whole of packet E's
  problem.
- **Naming** — the docs still title the resource *Creating spend limits* while the snapshot
  path is `/developer/v1/funds`, with both `limits:*` and `funds:*` scopes defined. The
  concept exists under a different path; claiming otherwise would have been the easiest
  wrong answer in the set.

# Go-live handoff — Apex Health Partners

For the deployment owner, before go-live:

- **REQ-3 is not met as written and Compliance has to see that in those words.** Ramp cannot
  check a purchase order while a card is being authorised — no platform does this at
  authorisation time. What is configured instead is the control your own document provides
  for: hard per-transaction caps, same-day reconciliation against NetSuite, and card
  suspension on violation. That is detective, not preventive, and your document reserves
  the right to *review* such a control rather than accept it in advance.
- **There is a $500 gap between your two documents that neither mentions.** The compliance
  document requires a purchase order above $500; the discovery call sets the clinic
  per-transaction cap at $1,000. A $700 clinic purchase is approved by the card and falls
  inside the purchase-order rule. Configured at $1,000 so clinics can operate — Compliance
  needs to accept reconciliation as the control for that band, or lower the cap.
- **REQ-2 fails closed, but a person is the gate.** High-limit cards are created and
  immediately suspended, and stay suspended until your office confirms the notarised form.
  A card left alone never transacts. Ramp does not verify the form exists; the Compliance
  Office does.
- **REQ-1 needs one thing from you before it works.** Both trading names — Joe's Medical
  Supply and JMS Distribution — must resolve to merchant records in Ramp. Any name that does
  not resolve is not blocked. The block also has to be re-applied to every programme created
  later, because Ramp has no company-wide blocklist.
- **Nothing can be issued until the roster arrives.** Eight blocking questions are open, and
  the largest is that this packet contains no email address for anyone and no clinic manager
  is named. The three-week clinic go-live starts when that list does.

# One capability, one question

**Capability: the ledger itself.** Every packet asked the same forty-odd questions — can
Ramp block a vendor, expire a card, scope a manager's view, allow-list an MCC — and the
answers do not vary by customer. Genera should own that ledger centrally, with dated
evidence per row and a regeneration step, so no deployment re-derives it and no two
customers get different answers to the same question. Its value compounds: the rows written
for Acme answered Apex, and rows added for Apex answered Vanguard.

**Question, for Vanguard Retail Services:** the seasonal wave is not a one-off. The field
force roughly doubles every October and collapses on 24 December, and the reps live in a
spreadsheet that is rebuilt each year. Should this become a standing annual motion — a
saved role-to-control mapping plus a re-runnable onboarding flow — rather than a
configuration rebuilt from scratch each season? The date does not move, and neither does
the shape of the work.

# With another day

Reconcile the ledger against the live OpenAPI specification at
`docs.ramp.com/openapi/developer-api.json`, which I could not reach; my drift rows rest on
a point-in-time snapshot. Write the Spanish executive summary Logística Globex asked for —
their board reads Spanish and the two JSON files cannot satisfy that. Build the reverse
check I do not have: today nothing catches a *silently widened* permission on a SUPPORTED
capability, which is how Cloud computing reached Hypergrowth's software card and how both
CEOs got administrative rights. And put the six district assignments into packet E, since
the reporting-chain mechanism that answers their hardest requirement cannot be built
without them.
