# NOTES

Five packets, nine checks each. Pointers are transcript turns and commit hashes.

## Decisions, and the verification that produced them

### 1. A reference sets the form of an output, never its parameters

The Westbrook sample is the only worked example shipped, and the exercise says of it "not an
exercise" and "nothing to run or submit". Studying its shape is invited, inheriting its answers
is not, and from inside the work the two look alike. An agent given no guidance infers helpfully.

**Passed on:** treating the sample as a template. Fastest start available, and it encodes a
twelve-person design agency's answers, which fit none of these customers.

**Where:** turn 18, mid-session — "What else carries over from the westbrook sample?"

**Wrong:** an owner maps to `BUSINESS_ADMIN`, generalised from the sample's one administrator.

**Evidence:** Acme names its administrators as "Priya and me" and Hypergrowth as "me and maya",
the assistant existing precisely to keep account changes off the CEO's desk. Neither CEO is in
either list.

**Change:** both became `BUSINESS_USER`, mapped by administrative responsibility rather than job
title (`29059cd`). The same reading found two more sample-derived errors: a "(surname pending
roster)" placeholder on a packet with no roster (`85d83cf`), and reimbursements enabled on three
Apex programmes the packet never mentions. None was caught by tooling, so before submission
three agents took the question in sequence (turn 25): one catalogued, one judged each against
"would this still be here if the sample had never existed", one applied only the contamination.
Fifty-nine points, fifty-seven legitimate, one open judgement, one finding: the ledger had
promoted the sample's hedged Slack claim to fact for two customers who never asked about Slack
(`9086da0`).

### 2. The deterministic half is code and customer-agnostic; judgement stays with the session

Forty-three ledger rows in YAML, keyed on what customers say rather than on endpoints, plus nine
scripted checks. Judgement stays with the agent: messy transcripts, conflicting documents, what
Ramp cannot do. Scale, of effort and of reliability, exists only on the mechanical
side. Citations were the tell, hand-built for A and C, then scripted as `cite.py` (`fae09ab`).

**Passed on:** a scripted extractor. It suits packet A's clean roster and fails packet D, which
has only a Slack export and notes that disagree.

**Where:** turn 2, at the very start — "write SKILL.md, run_pipeline.py as a mix of glue code"

**Wrong:** the coverage invariant, that every requirement terminates in a config field or audit
entry, was enforced.

**Evidence:** the check passed on the sample's real outputs while my own fixture cited
`assumptions_made[999]` against an array of one, because nothing resolved a citation against the
document it named.

**Change:** added reference resolution (`ae90065`), which immediately caught two dangling
references I had written myself. A mechanical guarantee is worth what its check is worth.

### 3. Flag forward, in the customer's own words

The audit log names people rather than using pronouns, carries speaker and role on every
citation, and never invents an identifier. The customer's vocabulary outranks house style: the
jargon check first rejected `REQ-1`, which was Apex's own numbering. Each rule became a check,
because I broke every one I only wrote down: care alone left 36 pronoun violations and 17
citations too thin to name a speaker.

**Passed on:** documenting the standards and relying on care.

**Where:** turn 7, early on — "Because this is customer facing, let's never write notes with"

**Wrong:** where a packet gave no email address, the config carried a constructed one at the
customer's apparent domain.

**Evidence:** those addresses appear nowhere in the packet, and a plausible one is worse than a
blank, since someone will send to it.

**Change:** `N/A` in the field and the gap flagged, enforced by check 8 (`20a0360`). The same rule
closed a second gap: packet D's software card had been widened to Cloud computing on the inference
that a subscription budget covers infrastructure, disclosed only in a `translation_notes` field no
customer reads (`29059cd`).

## What the Ramp docs changed

`docs.ramp.com` was blocked by this environment's egress proxy for `curl` and page fetches
alike. Search was the only live channel, so these rest on page titles and quoted excerpts.

- **Entities.** The accounting guide states positively that entities are created in the Ramp UI
  and scoped by `entity_id`, moving `CAP-ENTITY-CREATE` from absence-based UNSUPPORTED to
  evidenced UI_ONLY and validating packet B's `status: requested`.
- **Roles.** *User role deep-dive: IT Admin* supplies semantics the spec does not: `IT_ADMIN`
  grants People and Integrations access while denying spend controls, exactly the "manage users
  but not limits" split Acme and Hypergrowth both asked for.
- **Categories.** *Setting up category and merchant restrictions* confirms Ramp derives its
  category from the MCC plus other signals, so an MCC allow-list is not expressible anywhere in
  the product, UI included. That is the whole of packet E's problem.
- **Naming.** The docs still title the resource *Creating spend limits* while the snapshot path
  is `/developer/v1/funds`. Calling the concept absent was the easiest wrong answer.

## Go-live handoff — Apex Health Partners

- **REQ-3 is not met as written, and Compliance should see it in those words.** Ramp cannot
  check a purchase order while a card is being authorised. Configured instead is the control your
  own document provides for: hard per-transaction caps, same-day reconciliation against NetSuite,
  and suspension on violation. That is detective rather than preventive.
- **There is a $500 gap between your two documents that neither mentions.** Your compliance
  document requires a purchase order above $500, while the discovery call sets the clinic
  per-transaction cap at $1,000. A $700 purchase is approved by the card and still falls inside
  the purchase-order rule. Either accept reconciliation as the control for that band, or lower
  the cap.
- **The high-limit card gate fails closed, but a person is the gate.** Cards above $10,000 a
  month are created and immediately suspended, staying suspended until your office confirms the
  notarised form. Ramp does not verify that the form exists. The Compliance Office does.
- **The vendor block needs one thing from you before it works.** Both trading names, Joe's
  Medical Supply and JMS Distribution, must resolve to merchant records in Ramp, because a name
  that does not resolve is not blocked. The block must also be re-applied to every card programme
  created later.
- **Nothing can be issued until the roster arrives.** Eight open questions stop go-live, and the
  largest is that we have no email address for anyone and no clinic manager is named. Your
  three-week clinic timeline starts when that list does.

## One capability, one question

**Capability: the ledger, owned centrally.** Every packet asked the same forty-odd questions,
and the answers do not vary by customer. Built once with dated evidence per row, it removes that
re-derivation from every deployment after: rows written for Acme answered Apex, and rows added
for Apex answered Vanguard. Runner-up was the audit-log style gate, which travels less well
because it encodes a house voice where the ledger encodes facts.

**Question, for Vanguard Retail Services:** your field force roughly doubles every October and
collapses on 24 December, and the reps live in a spreadsheet rebuilt each year. Should the
seasonal wave become a standing annual motion, with a saved role-to-control mapping and a
re-runnable onboarding flow, rather than rebuilt each season?

## What I'd do next with another day

Reconcile the ledger against the live OpenAPI specification I could not reach, since every
drift row rests on a snapshot and drift ages worst. Then build the check I lack: nothing catches
a silently widened permission on a SUPPORTED capability, which is the failure behind both
examples above. Then the Spanish executive summary Logística Globex asked for. Shipped
knowingly imperfect: packet C's clinic programme permits General merchandise as the nearest
category to "hardware stores", broader than that packet deserves.
