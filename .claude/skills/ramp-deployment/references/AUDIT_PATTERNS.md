# AUDIT_PATTERNS.md — trigger taxonomy and idioms

The engine of Phase 2. Four trigger classes, four arrays, no fifth place to put anything.

> "An empty audit log on a messy packet is a red flag, not an achievement."
> — `candidate/schemas/audit_log_schema.json`, top-level `description`

## Routing

| Class | Array | One-line test |
|---|---|---|
| Judgement | `assumptions_made` | I chose a value the customer did not state |
| Gap | `missing_information_flags` | I needed something the packet does not contain |
| Disagreement | `conflicts` | Two sources — or one source twice — say different things |
| Capability | `unsupported_api_requests` | The ledger verdict for this requirement is not `SUPPORTED` |

**One requirement can fire several classes.** Acme's CEO card fires all four: an assumption
($50,000 is the invented ceiling), a conflict (roster "NO LIMIT" vs the call's "$50k"), a
capability entry (`CAP-UNLIMITED`), and arguably a gap (is $50k the number Marcus expects?).
Do not pick one. Firing once is the most common way an audit log goes thin.

**Every array is required by the schema**, and `additionalProperties: false` applies
everywhere. Empty arrays are legal — see the Westbrook idioms — but an empty array is a
claim you are making, not a default.

---

## Voice: this document is read by the customer

Acme's finance team reads their audit log. Millie's compliance team reads Apex's. It gets
forwarded. Everything below is enforced by `scripts/check_audit_style.py`, which runs as
`--verify` check 5 — these are not style preferences, they are gates.

### Never use a pronoun for a person

| Instead of | Write |
|---|---|
| "his card declines" | "Marcus Webb's card declines" |
| "she will hit declines on office spend" | "Renata Flores will hit declines on office spend" |
| "who is her actual manager?" | "who is Jenny Park's manager?" |
| "they can request it" | "Engineering staff can request it" |

`they`/`them` is covered by the rule. A generic plural is the same vagueness the rule
exists to prevent — the reader still cannot tell who is meant. Restructure the sentence.

**One exception:** a verbatim quote inside a `source` field. The customer's own words stay
as spoken, pronouns and all. Never misquote someone to satisfy a style rule.

### Citations must be verifiable without opening the file

Four things, every time: **the file**, **who said it or where it sits**, **enough context to
carry the meaning**, and **the verbatim quote**.

Rejected by the customer:

```
discovery_call_01.txt — 'Priya and me.' [05:41]
```

A reader cannot tell who "me" is, or why that line supports the assumption it is attached
to. Corrected:

```
discovery_call_01.txt — Diane Marsh (VP Finance), [05:41], answering who should be able to
administer the Ramp instance and change limits: "Priya and me."
```

For a roster row, the locator replaces the speaker:

```
department_roster.csv, row 15 — "Jenny Park,jpark@acme.example,Engineer,Engineering,dkim@acme.example,2022-10-17,500"
```

The checker re-verifies the quoted span against the real packet file, so a citation cannot
drift from its source. A bare timestamp with no speaker fails.

### No internal vocabulary

Never emit: `CAP-…` / `DRIFT-…` row IDs, `req_id`, `REQ-001`, "archetype", "traceability",
"capability ledger", "fan-out" / "fans out".

`proposed_manual_workaround` is copied from the ledger row's **`customer_workaround`**, which
is written for this audience. The `workaround` field is the internal note — it carries row
IDs and jargon and must never reach the audit log.

Plain-language a Ramp role on first use: `AUDITOR` becomes "the Auditor role (read-only
access across the account)".

### `impact_if_wrong` is a consequence in the customer's world

Who can spend what, who sees what, what breaks and when. Not "the config would be
incorrect" — that tells the reader nothing they can act on.

---

## 1. `assumptions_made`

Judgement calls a human could veto.

### Fires on

| Trigger | Typical packet |
|---|---|
| Any value in the config not literally stated in a source | all |
| Headcount → individual people ("about a dozen", "roughly 40 eng") | A, B, D, E |
| Role mapping where customer language has no clean Ramp enum (`CAP-ROLE-MAPPING`) | all |
| Currency normalization, and any FX rate you picked | B |
| MCC → Ramp category translation, once per lossy mapping (`CAP-MCC-ALLOWLIST`) | C, E |
| Group limit fanned out to per-user limits (`CAP-GROUP-LIMIT`) | A, D, E |
| Any rounding — "equivalent, not identical" amounts, cents conversion | B |
| **Every `UI_ONLY` capability you left out of the config** — omitting it *is* an assumption | all |
| Normalizing case-variant or near-duplicate labels (`sales` vs `Sales`) | A |

### Required fields

`assumption` · `source` (file + line or quote) · `impact_if_wrong`. Nothing else is allowed.

`impact_if_wrong` is the field that gets skimped. Write the consequence in the world — who
can spend what, who sees what — not "the config would be incorrect".

### Worked example — UI_ONLY omission (packet A)

`candidate/customer_packets/client_a_acme_corp/discovery_call_01.txt`, line 97, `[07:03]`,
Priya Shetty: "Required over seventy-five dollars. Below that I don't want anyone's time
spent on it. And memo required for anything over five hundred."

```json
{
  "assumption": "Receipt threshold ($75) and memo threshold ($500) are in-app policy settings, not part of this config. Both are omitted from ramp_config.json rather than forced into a field that does not exist.",
  "source": "discovery_call_01.txt line 97 [07:03] PS — 'Required over seventy-five dollars. ... And memo required for anything over five hundred.'",
  "impact_if_wrong": "None to card behaviour. If the deployment owner does not set both in-app during setup, Acme goes live with Ramp's default receipt and memo rules and Priya's reconciliation problem is unchanged."
}
```

Pair it with `CAP-RECEIPT-POLICY` and `CAP-MEMO-POLICY` entries in
`unsupported_api_requests`. This is the omit-and-flag idiom (below).

### Worked example — MCC translation (packet E)

`candidate/customer_packets/client_e_vanguard_retail/mcc_allowlist_matrix.csv`, the
`Field Rep - Installation` row: `Allowed_MCCs` = `5541,5542,7523,5200,5251,5533,5812`.

```json
{
  "assumption": "MCCs 5200 (home supply warehouse), 5251 (hardware stores) and 5533 (auto parts) have no corresponding Ramp category, so 5200/5251 are widened to category 13 'General merchandise' and 5533 is not represented at all.",
  "source": "mcc_allowlist_matrix.csv, row 'Field Rep - Installation', Allowed_MCCs '5541,5542,7523,5200,5251,5533,5812'; note column: 'Hardware and home-supply access is the differentiator vs merchandising. Auto parts for van consumables.'",
  "impact_if_wrong": "Installation reps can transact at department and discount stores the matrix never allowed (category 13 is far wider than hardware), and may be declined buying van consumables at an auto-parts retailer, which the note says is core to the role."
}
```

One entry per lossy mapping, not one per matrix — the customer asked for exactly that:
`onboarding_call_vanguard.txt` line 25, `[01:44]`, AN: "If some rule can't be enforced
exactly as written I need to know which one and what the closest enforceable version is."

---

## 2. `missing_information_flags`

Phrased as the question you would ask the customer. Not a statement.

### Fires on

| Trigger | Typical packet |
|---|---|
| A named person with no email | A (`dkim@acme.example` has no roster row), B (Joaquín, Thiago, Elena) |
| A document referenced but absent from the packet | D ("doc coming, maya has my notes" — the notes did arrive; the PEO export did not) |
| A headcount with no roster | D (82 people), E (271 people, no names at all) |
| An unresolvable manager reference | A (Jenny Park → `dkim@acme.example`, not on the roster) |
| Anything a source says is "coming" | D (PEO export), B (Brazil entity, São Paulo admin team) |
| Explicitly unresolved / parked items | A (Marketing reorg), D (per diem vs actuals, quarterly review owner) |
| An identifier the API needs that the packet cannot supply | C (merchant UUIDs for the two prohibited trade names) |
| A customer decision only they can make | C (does Compliance accept the REQ-3 compensating control?) |

### Required fields

`question` · `blocking` (bool). Optional: `affected_config`. Use `affected_config` —
it is what lets a rep apply the safe 80% of a config and hold the rest.

### When is `blocking` true?

`blocking: true` means **the config should not be applied before this is answered.** Set it
when any of these hold:

1. The section cannot be constructed at all — no roster, no legal entity, no merchant ID.
2. Money could move to someone who should not have it, or at a level nobody approved.
3. A control the customer named as a condition of go-live would be absent.
4. Applying the config would tell one stakeholder that another agreed to something they did
   not.

Otherwise `false`. The test is reversibility: a wrong per-person limit is one PATCH after
go-live; a card that should never have transacted is an incident. And an explicit customer
"don't block on it" settles the question — see the Acme example below.

### Worked example — blocking (packet D)

`candidate/customer_packets/client_d_hypergrowth/slack_export_finance.txt`,
`[2026-08-05 16:40]`, rachel.kim: "headcount export is stuck with our PEO, their portal has
been 'undergoing maintenance' since thursday 🙄 you may need to start without a clean
roster. current truth: 82 people, breakdown roughly 40 eng / 22 GTM / 15 ops / 5 exec-ish.
names and emails to follow whenever the portal resurrects"

```json
{
  "question": "Can you send the PEO headcount export (names, emails, department, manager) for all 82 people? Departments, limits and programs are specified; no user can be created without it.",
  "affected_config": "users; all per-user limits",
  "blocking": true
}
```

Trigger 1: the `users` array cannot be built. Note the config is still worth producing —
Rachel explicitly says "you may need to start without a clean roster", and Jordan's reply at
`[2026-08-05 16:44]` promises exactly that shape: "I'll structure everything so the roster
drops in when it arrives, and flag user setup as pending."

### Worked example — non-blocking, because the customer said so (packet A)

`discovery_call_01.txt`, line 89, `[06:26]`, PS: "...I need to confirm who they report to
now. Don't block on it, but don't invent an answer either."

```json
{
  "question": "After the Marketing reorg, who do Aisha Bello and Grant Sokol report to? The roster's manager column is flagged as possibly stale for the two newest Marketing hires.",
  "affected_config": "users[].direct_manager_email for abello@ and gsokol@; manager-tier approvals for both",
  "blocking": false
}
```

`direct_manager_email` is emitted as `null` for both. Carrying the roster value forward
would be inventing an answer; the schema's own field description says "null if unknown — and
if unknown, say so in the audit log."

---

### When a packet has no roster at all

Packet A shipped a 32-row CSV. Packet C named six people, one of them by first name only,
and contained no email address and no email domain anywhere. The convention:

| Situation | What to emit | Flag |
|---|---|---|
| No email domain stated | `firstname.lastname@<company>.example`, with the invention stated in `assumptions_made` | blocking — no user may be invited until real addresses arrive |
| Name part missing | `"(surname pending roster)"`, as the Westbrook sample does | blocking |
| Headcount given, no names ("fourteen clinic managers") | a group limit with the count and its basis in `notes` | blocking |
| Population that varies ("eight to twelve nurses") | plan on the upper figure and say so | blocking |

Name every person the packet does name. A configuration listing known people with flagged
placeholders is useful to a deployment owner; an empty `users` array is not.

## 3. `conflicts`

### Fires on

| Trigger | Typical packet |
|---|---|
| The same field with two values across two sources | A (roster "NO LIMIT" vs call "$50k"), B (memo 2.6 vs the call) |
| A source contradicting **itself** | A (Han Zhao appears twice in the roster, 500 and 1200) |
| Supersession by time — a later source overriding an earlier one | D (Leo's Slack vs the February notes) |
| A self-correcting author | D (Rachel's "+50% managers" then "correction — eng managers don't need +50%") |
| Two people in one source disagreeing | D (dev "they're ops" vs jj "they're GTM") |
| A hedged figure against a precise one | E ("about one hundred fifty field reps" vs 131 in the matrix) |
| **A threshold in one document straddling a cap in another** | C (purchase order required above $500; clinic per-transaction cap set at $1,000) |

### The straddled-threshold trigger

This one is different from the others: **neither source contradicts itself, and neither
mentions the other.** Each document is internally consistent. The conflict exists only in
the gap between them, and it is invisible unless the figures are laid side by side.

Packet C is the worked case. The compliance document requires a purchase order for any
transaction above $500. The discovery call sets the clinic manager per-transaction cap at
$1,000. A $700 clinic purchase is therefore approved by the card while sitting inside the
purchase-order requirement — a compliance gap of $500 per transaction that nobody wrote down.

Run `scripts/money_map.py --packet <packet>` and read its collated section, where every
figure across the packet is sorted by amount. Adjacent figures from *different files* are
the ones to examine. For each pair ask: does one govern spend that the other permits?

When it is real, encode the figure the business actually needs, then say in
`provisional_resolution` exactly which band is left uncovered and what covers it instead.
Do not quietly adopt the stricter number to make the conflict disappear — that breaks the
customer's operations to tidy a document.

### Required fields

`description` · `source_a` (file + quote) · `source_b` (file + quote) ·
`provisional_resolution`.

### A stated precedence rule does NOT suppress the entry

Say it out loud, because it is the single most common way this array goes empty when it
should not. The schema:

> "Do not silently pick a winner — record both, say which you provisionally encoded and
> why, and flag for human resolution."

The rule — "the roster wins", "Spanish wins except Section 4", "do what Rubén says" — is
*content for* `provisional_resolution`, quoted and attributed. It is never a reason to skip
the entry. `PRECEDENCE_RULES.md` carries the verbatim rule text for each packet.

When nothing resolves it, `provisional_resolution` is literally `"none, blocking"` and a
matching `missing_information_flags` entry carries `blocking: true`.

### Worked example — blocking, recency does not win (packet D)

```json
{
  "description": "Travel approval: the February ops planning meeting records Leo agreeing to a tiered policy (under $2,500 auto-approved by the department manager), while Leo's July Slack message requires his personal approval for all travel at any amount. The later message does not acknowledge the earlier agreement, and the note-taker cannot confirm whether the Q2 trial ended.",
  "source_a": "fragmented_notes_feb2026.md, 'travel (the big one)' — 'PROPOSAL (dev): tiered — travel under $2,500 total trip cost auto-approved by department manager, over $2,500 goes to leo' / 'landed: leo agreed to try the $2,500 threshold for Q2 and revisit end of june'; plus 'NOTE (maya, typing this up in july): i wasn't in this meeting. i can't find the follow-up where the Q2 trial was confirmed or cancelled.'",
  "source_b": "slack_export_finance.txt [2026-07-30 08:55] leo.novak — 'every dollar of travel goes through me. i sign off on all of it. ... ALL travel needs my direct approval until further notice'",
  "provisional_resolution": "none, blocking. Dev raised exactly this incompatibility in-channel ([2026-07-30 09:15] 'is that compatible with what we agreed in the ops planning meeting?') and it was never answered; Finance still describes travel as undesigned ([2026-07-30 11:52] 'travel is its own program, we're still designing it'). Encoding either version would report to one stakeholder that the other agreed to something they did not. approval_policies carries both as desired state with source lines naming each document; nothing is applied via API in any case (CAP-APPROVAL-CHAIN is UI_ONLY)."
}
```

### Worked example — a rule that cannot reach (packet A)

`department_roster.csv` line 10 gives Han Zhao a 500 limit; line 33 repeats the row with
1200. The stated rule "the roster wins" adjudicates roster-vs-call and is silent here.
Provisionally encode the conservative value (500, which also matches every other Staff and
Senior Engineer), say in `provisional_resolution` that you chose the lower value *because*
the conflict is unresolved, `blocking: false`, and ask.

---

## 4. `unsupported_api_requests`

Fires on **any requirement whose ledger verdict is not `SUPPORTED`** — that is
`PARTIAL`, `UI_ONLY`, `UNSUPPORTED` and `DRIFT`, not only the last one. A `PARTIAL` that
goes unmentioned is a false negative; a `SUPPORTED` that appears here is a false positive.
Both are swept in Phase 4, and the exercise grades the second explicitly: "Getting these
right (including NOT listing things the API does support) is graded."

### Required fields, and where each comes from

| Field | Source |
|---|---|
| `requested_feature` | the customer's ask, in their terms — cite the REQ number where the packet numbers them (packet C) |
| `reason_unsupported` | why, in one or two sentences, specific to this customer |
| `evidence` | **copied verbatim from the ledger row's `evidence_line`.** Never composed fresh. |
| `proposed_manual_workaround` | from the ledger row's `workaround` |

`evidence` is the field that makes five audit logs agree with each other instead of each
re-arguing the same point. Copy the string; do not paraphrase, do not trim the date, do not
merge two rows' evidence into one line. If two rows both apply, write two entries.

If `workaround` is `null` in the ledger, the verdict is `SUPPORTED` and the entry should not
exist. If it is null on a non-`SUPPORTED` row, that is a ledger bug — fix the ledger.

### Worked example — packet C, REQ-3

`candidate/customer_packets/client_c_apex_health/security_requirements.doc`, REQ-3:
"Transactions exceeding $500 USD must be declined at authorization unless a valid open
Purchase Order number from the Apex ERP (NetSuite) is associated with the transaction prior
to authorization. ... Vendor response must state clearly which side of that line the
platform falls on."

```json
{
  "requested_feature": "REQ-3 — decline at authorization any transaction over $500 USD without a valid open NetSuite Purchase Order matched before authorization.",
  "reason_unsupported": "Ramp cannot gate an authorization on an external PO match, so REQ-3 as written falls on the detective side of the line the requirement itself draws: NOT MET as a platform control, ENFORCED BY PROCESS via the compensating control the CFO office pre-authorized for review.",
  "evidence": "openapi snapshot 2026_08_30 — no authorization-time hook exists; /purchase-orders is a record API, not a control surface, so a charge cannot be gated on PO match at authorization.",
  "proposed_manual_workaround": "Tightest available compensating control: a hard transaction_amount_limit at the threshold, plus same-day post-transaction PO reconciliation, plus POST /funds/{id}/suspension on violation. Detective rather than preventive — say so plainly, because the difference is the whole point of the requirement."
}
```

Note the two things this entry does beyond the mechanics: it answers in the customer's own
three-way vocabulary (ENFORCED BY PLATFORM / ENFORCED BY PROCESS / NOT MET, per that
document's response instructions), and it names the pre-authorized fallback rather than
inventing one. Pair it with a `blocking: true` gap asking whether Compliance accepts it.

### Do not over-list

Before writing an entry, check the ledger verdict. These look like gaps and are not:

| Customer ask | Verdict | Where it belongs |
|---|---|---|
| Tiered approval chains | `CAP-APPROVAL-CHAIN` UI_ONLY | config as desired state **and** here — real capability, wrong surface |
| Card dies on a fixed date | `CAP-AUTO-EXPIRY` SUPPORTED | config only. Do not list. |
| Read-only compliance access | `CAP-READ-ONLY-AUDITOR` SUPPORTED | config only. `AUDITOR` is a first-class role. |
| "Manage users but not spend limits" | `CAP-IT-ADMIN-SCOPE` SUPPORTED | config only. `IT_ADMIN` is a stock role, not a gap. |
| Local-currency limits | `CAP-LOCAL-CURRENCY` SUPPORTED | config only. |
| Onboard 140 people from a spreadsheet | `CAP-BULK-USERS` PARTIAL | config **and** here — a loop, not a bulk endpoint |

---

## Verdict handling — config, audit log, or both

| Verdict | In `ramp_config.json`? | In `audit_log.json`? |
|---|---|---|
| `SUPPORTED` | yes | only if you inferred a value |
| `PARTIAL` | yes | **always** — `unsupported_api_requests`, naming the caveat |
| `UI_ONLY` | yes **if the schema has a home**; otherwise omit | **always** |
| `UNSUPPORTED` | yes **if the schema has a home**; otherwise omit | **always** |
| `DRIFT` | emit the **schema** shape, not the live API's | **always** — once per packet is enough |

`UNSUPPORTED` and `UI_ONLY` items still belong in the config as desired state wherever the
schema has somewhere to put them. This is not a liberty — the schema invites it in writing:

> `entities` — "Legal entities spend is organized under. NOTE: check what the Ramp API lets
> you do with entities before assuming your pipeline can create them."
>
> `approval_policies` — "Approval chains as desired state. Before assuming your pipeline can
> apply these, check what the Ramp API supports — and record what you find."

So: Brazil's not-yet-existing entity goes in `entities` with `status: "requested"`
(`CAP-ENTITY-CREATE`, UI_ONLY). Acme's three approval tiers go in `approval_policies`
(`CAP-APPROVAL-CHAIN`, UI_ONLY). Where there is **no** home — receipt thresholds, memo
rules, Slack alerts — they live only in the audit log.

`PARTIAL` items get configured **and** flagged. That combination is easy to forget precisely
because the config looks finished.

---

## Idioms from the Westbrook sample

Read `candidate/sample_packet/client_0_sample_westbrook/example_output/audit_log.json` and
`ramp_config.json` before writing anything. Five idioms to copy by name:

1. **Omit-and-flag.** The intake email says "Receipts over $50." There is no receipt field
   in the config schema, so the sample puts nothing in the config and one
   `assumptions_made` entry in the audit log: *"Receipt threshold ($50) is an in-app policy
   setting, not part of this config's card objects."* `impact_if_wrong`: *"None to card
   behavior; the deployment owner sets it during in-app setup instead."* The move is
   deliberate omission plus an explicit record of the omission — never silent omission, and
   never jamming the value into a field that does not mean that.

2. **The "(surname pending roster)" placeholder, paired with a blocking flag.** The sample
   emits `"first_name": "Priti", "last_name": "(surname pending roster)"` with
   `"notes": "Owner. Named in email; full details pending roster."`, and backs it with a
   `blocking: true` gap: *"Full roster (names, emails, who the finance contractor is and
   what access they need) — email says it's coming before the call."* Placeholder text goes
   in a human-readable field, is obviously not a real value, names what would replace it,
   and is never left to stand on its own — the blocking flag is what makes it honest.

3. **The group-limit fan-out note.** The Studio limit is emitted once as
   `"assigned_to": {"group": "Studio"}` with
   `"notes": "One per Studio member (9 people) once the roster arrives."` The note is what
   distinguishes nine per-person limits from one shared pot — `CAP-GROUP-LIMIT` says those
   are different products and customer phrasing rarely distinguishes them. Ask, and record
   which one you meant.

4. **The evidence line format.** `"docs.ramp.com API reference, checked 2026-08-24 — no
   notifications resource; nearest primitive is POST /webhooks (transaction events)."` —
   *source, date checked, em dash, what was found, nearest primitive.* Ledger
   `evidence_line` strings are written in this shape, which is why they can be copied
   straight in. The schema demands "what you checked, not what you guessed".

5. **`"conflicts": []` is legitimate.** Westbrook's packet is one email from one author, so
   nothing disagrees with anything. The sample leaves the array empty rather than
   manufacturing tension. The corollary is the harder half: on packets A–E, which are built
   to disagree with themselves, an empty `conflicts` array means you did not read carefully
   enough.

Also worth copying: the sample's `unsupported_api_requests` proposes a *route to the
outcome*, not an apology — "Ramp's in-app Slack integration may cover this (deployment owner
to enable); otherwise a webhook consumer that posts to #spend."

---

## Before you finish — Phase 2 checklist

- [ ] Every requirement in `work/<packet>/requirements.json` has fired at least one class,
      or is in the config with nothing to flag. Nothing dropped silently.
- [ ] Every quote is copied from the file, not reconstructed. Phase 4 substring-matches all
      of them against the source.
- [ ] Every `unsupported_api_requests[].evidence` is byte-identical to a ledger
      `evidence_line`, and every `proposed_manual_workaround` comes from that row's
      `workaround`.
- [ ] Nothing in `unsupported_api_requests` has a `SUPPORTED` verdict (false-positive sweep).
- [ ] Every `PARTIAL` / `UI_ONLY` / `UNSUPPORTED` / `DRIFT` item you configured is also
      flagged (false-negative sweep).
- [ ] Every `UI_ONLY` capability omitted from the config has an `assumptions_made` entry
      saying it was omitted and who has to set it.
- [ ] Every stated precedence rule appears inside a `provisional_resolution`, quoted — and
      the conflict entry still exists.
- [ ] Every conflict names both values. A reader can overrule you without reopening the packet.
- [ ] Every `blocking: true` survives the four tests above; every `blocking: false` is
      reversible with one PATCH after go-live.
- [ ] Every `missing_information_flags[].question` is a question, addressed to the customer.
- [ ] Every `impact_if_wrong` describes a consequence in the world, not "the config would be
      wrong".
- [ ] Every lossy MCC mapping has its own entry, not one entry for the whole matrix.
- [ ] Every non-obvious role mapping is recorded, including what the person can consequently
      see or do (`CAP-ROLE-MAPPING`); every `GUEST_USER` assignment carries the six-month
      auto-deactivation note (`CAP-GUEST-EXPIRY-DEFAULT`).
- [ ] `conflicts: []` only if you can defend it out loud.
- [ ] The file validates: four required arrays, `additionalProperties: false` everywhere,
      no extra keys.
