# PRECEDENCE_RULES.md — how conflicts resolve, per packet

## The opening principle

**A stated precedence rule does not suppress a conflict entry.** The audit schema is
explicit:

> "Places where the customer's own sources disagree. Do not silently pick a winner —
> record both, say which you provisionally encoded and why, and flag for human resolution."
> — `candidate/schemas/audit_log_schema.json`, `conflicts.description`

So a rule like "the roster wins" changes what you *encode*; it does not change whether you
*log*. The rule goes in `provisional_resolution`, named and quoted, alongside both values.
A deployment rep reading the audit log must be able to see the losing value and overrule
you without re-reading the packet.

Three corollaries:

1. **A rule has a scope.** Check what the speaker was actually adjudicating and whether the
   deployment lead's readback narrowed it. Do not stretch a rule past its subject.
2. **A rule can point at an unencodable value.** When the winner is something Ramp cannot
   express, you get a conflict entry *and* an `unsupported_api_requests` entry.
3. **A rule cannot adjudicate a source against itself.** "The roster wins" is silent when
   the roster contradicts the roster.

---

## Packet A — `client_a_acme_corp`

### Stated rule: the roster wins

`discovery_call_01.txt`, line 61, timestamp `[04:31]`, Priya Shetty (Controller):

> "On the roster I marked target monthly limits per person. Those are the numbers we
> actually want, person by person. Where the roster and anything I say today disagree, the
> roster wins — I did that sheet carefully."

Readback that narrows it, line 63, `[04:44]`, Jordan Lee (Genera) — unchallenged:

> "Noted — roster wins on per-person numbers."

**Scope.** As uttered the rule is broad ("anything I say today"), but (a) its stated
subject is per-person target monthly limits, (b) the readback narrows it to "per-person
numbers" and neither customer attendee corrects that, and (c) it is PS's rule about PS's
own statements — it is not obviously binding on Diane Marsh. **Treat the confirmed scope as
per-person limit numbers only.** Where you use it beyond that, say in
`provisional_resolution` that you stretched it.

**Resolves**

| Disagreement | Winner under the rule |
|---|---|
| Per-person monthly limit numbers, roster vs anything said on the call | roster value |
| e.g. Diane Marsh: call gives no number, roster `Target_Limit_USD_Monthly` = 7500 | 7500 |

**Does NOT resolve**

| Open question | Why the rule is silent |
|---|---|
| **The Marketing reorg** (below) | Not a limit number, and PS explicitly refuses to have it inferred |
| **Duplicate roster rows for Han Zhao** | `department_roster.csv` line 10 = 500, line 33 = 1200. Both are the roster. The rule adjudicates roster-vs-call, not roster-vs-roster. |
| **Marcus Webb's "NO LIMIT"** | The rule picks the roster value, and the roster value is not expressible (see below). |
| **Department count** | Call line 17 `[00:47]` DM: "Four departments for spend purposes." The roster carries five distinct department values (`G&A, IT, Engineering, Sales, Marketing` — Sana Qureshi is in `IT`, line 8). The rule's confirmed scope is per-person numbers, so it does not settle this. Log the conflict. |
| **Case-variant departments** | `sales` (lines 23, 25) vs `Sales`. Normalization is an assumption, not a conflict resolved by anyone. |
| **Blank limit** | Sam Whitfield, line 16, `Target_Limit_USD_Monthly` empty — a gap, not a disagreement. |
| **Dangling manager** | Jenny Park, line 15, `Manager_Email` = `dkim@acme.example`, who is not on the roster. |

### Explicitly do-not-infer: the Marketing reorg

`discovery_call_01.txt`, line 89, `[06:26]`, Priya Shetty:

> "Yes. One caveat — we just reorged Marketing. The roster's manager column is right for
> everyone except possibly the two newest Marketing hires; I need to confirm who they
> report to now. Don't block on it, but don't invent an answer either."

The two newest Marketing hires by `Start_Date` are Aisha Bello (2026-05-18, manager
`ltran@acme.example`) and Grant Sokol (2026-06-29, manager `treyes@acme.example`).

- This is a `missing_information_flags` entry, **not** a conflict — no two sources disagree,
  one source disclaims itself.
- `blocking: false` — the customer said "Don't block on it."
- Emit `direct_manager_email: null` for both and note it. "Don't invent an answer" forbids
  carrying the roster value forward as if confirmed.

### The rule points at an unencodable value

`department_roster.csv` line 2: `Marcus Webb,...,NO LIMIT`.
`discovery_call_01.txt` line 21 `[01:14]` DM: "his card should effectively have no limit";
line 25 `[01:38]` DM: "Whatever 'doesn't decline in practice' means. Fifty grand a month?
He's not actually spending that."

The roster wins → "NO LIMIT" → `CAP-UNLIMITED` is UNSUPPORTED. So:

- `conflicts` entry: roster "NO LIMIT" vs call "$50k/month", `provisional_resolution` =
  encoded $50,000/month because the roster's winning value cannot be expressed.
- `unsupported_api_requests` entry from `CAP-UNLIMITED`, `evidence` copied verbatim.
- `assumptions_made` entry naming the exact ceiling — per the row's workaround, "'no limit'
  and '$50k/mo' are different promises to the person holding the card."

### Blocking in packet A

Nothing here is blocking. Every open item is a single person's limit or manager, reversible
after go-live, and the customer pre-authorized proceeding on the one they cared about.

---

## Packet B — `client_b_logistica_globex`

### Stated rule 1 (written): Spanish wins, except Section 4

`politica_gastos_2026.txt`, Section 5.3, lines 71–72:

> "5.3 Cualquier discrepancia entre versiones de idioma de este documento se resuelve a
> favor de la versión en español, excepto la Sección 4, cuyo original es el inglés."

*(Any discrepancy between language versions of this document resolves in favour of the
Spanish version, except Section 4, whose original is English.)*

Supporting context — the document disclaims its own coherence, lines 4–5:

> "Nota interna: documento de trabajo. Las secciones no están totalmente armonizadas entre
> sí."

**Resolves:** which language version of the *same* clause governs. Section 2 (ES, MXN) and
Section 3 (PT, BRL) are Spanish/Portuguese-origin → Spanish governs. Section 4 (EN, USD,
Miami) is English-origin → the English text governs and must not be "corrected" toward the
Spanish sections.

**Does NOT resolve:**

- **Different amounts for different countries.** Section 3.6 (BRL 400 / 4,000) and Section
  4.5 (USD 100 / 1,000) are not translations of Section 2 — they are separate local
  policies. 5.3 has nothing to say about them. The CFO calls them "equivalentes — no
  idénticos" (`entrevista_descubrimiento_es.txt`, line 47, `[04:11]`): "Y en Brasil y Miami
  la misma lógica cuando arranquen, con los montos equivalentes — no idénticos,
  equivalentes. Redondeados a números que tengan sentido localmente." Do not normalize
  these into one another.
- **Memo vs the spoken call.** 5.3 is scoped to "versiones de idioma **de este documento**".
  Rule 2 governs that axis.
- **`threshold_usd_cents`.** The exercise schema names approval thresholds in USD cents
  while the memo states them in MXN and BRL. That tension is an `assumptions_made` entry
  with the rate you used, not something 5.3 settles.

### Stated rule 2 (spoken): operation beats memo

`entrevista_descubrimiento_es.txt`, line 59, `[05:26]`, Rubén Ortega (Operations Director):

> "Los viáticos de los choferes — hoteles de carretera, comidas — hoy se manejan con
> efectivo y reembolsos. Quisiéramos meterlos a la tarjeta también, pero la realidad es que
> muchos hoteles de carretera en México solo aceptan efectivo. Así que los reembolsos no se
> pueden matar del todo, aunque el memo diga que sí."

Line 61, `[05:45]`, Alejandra Vidal (CFO) — the rule itself:

> "El memo es aspiracional en esa parte. [ríe] Hazle caso a Rubén."

*(The memo is aspirational on that part. Do what Rubén says.)*

Readback, line 63, `[05:49]`, Camila Duarte — unchallenged:

> "Entendido — el memo dice una cosa, la operación dice otra; gana la operación y lo dejo
> anotado."

The memo clause being overridden, Section 2.6, lines 28–31:

> "2.6 Los reembolsos en efectivo quedan ELIMINADOS a partir del Q4 2026. Todo gasto debe
> realizarse con tarjeta corporativa.
> [Nota de R. Ortega, 07/20: ver mis comentarios en la llamada — esto no es viable para
> viáticos de carretera. Mantener reembolsos para hoteles/alimentos en ruta.]"

**Resolves:** reimbursements stay enabled. Encode
`permitted_spend_types.reimbursements_enabled: true` on the driver-facing programs.

**Scope — narrow.** "en esa parte" / "esa parte" is the reimbursement clause specifically.
The CFO did not demote the memo generally; Sections 2.1–2.5, 3 and 4 remain the numeric
source of truth. Do not use this quote to override memo amounts.

**Still log it.** Even with the rule stated twice (in the memo's own margin note and on the
call), it is a `conflicts` entry: source_a = memo 2.6, source_b = the CFO/RO exchange,
`provisional_resolution` = reimbursements enabled, citing both quotes.

### Other B rules worth quoting

- **Customer pre-authorizes an FX assumption** — `politica_gastos_2026.txt` 5.2, lines
  68–70: "Para la configuración de sistemas, utilizar un tipo de cambio razonable y
  documentarlo; la precisión cambiaria NO es crítica para los límites de tarjeta, la
  operación local es en moneda local." Plus `[02:50]` line 33: "Confío en que ustedes lo
  normalicen y me digan qué asumieron." This makes FX an `assumptions_made` entry with a
  stated rate, **not** a blocking flag. Keep limits in local currency
  (`CAP-LOCAL-CURRENCY`, SUPPORTED); normalize only for consolidation.
- **Do not invent** — line 55, `[05:09]`, AV: "Diseñen todo ahora. Si el sistema permite
  dejarlos listos sin activar, mejor. Si no, díganme qué se puede y qué no — no me
  inventen. Prefiero una lista de 'esto queda manual' a una sorpresa en octubre." A direct
  mandate for the audit log over a clean-looking config.

### Blocking in packet B

- **Brazil entity does not exist yet** — `[00:42]` line 15: "São Paulo está en proceso...
  estará lista a fin de septiembre." Emit `entities[].status: "requested"` and
  `CAP-ENTITY-CREATE` (UI_ONLY). `blocking: true` for the Brazil users/cards specifically —
  they cannot be applied before the entity exists — and non-blocking for Mexico and Miami.
- Not blocking: the São Paulo administrative team is unhired; Thiago Moreira already has a
  company email, the three drivers start in October. Missing names are `missing_information_flags`.

---

## Packet C — `client_c_apex_health`

### The controlling instrument

`security_requirements.doc` is a numbered vendor-response instrument, not a wish list. Its
own scope clause, lines 8–11:

> "These requirements apply to any corporate card or spend-management platform adopted by
> Apex Health Partners and are conditions of go-live. Requirements are numbered for
> reference in vendor responses. Each requirement must be answered as one of: ENFORCED BY
> PLATFORM / ENFORCED BY PROCESS / NOT MET."

And lines 56–58:

> "Responses must map each requirement to REQ number, state ENFORCED BY PLATFORM / ENFORCED
> BY PROCESS / NOT MET, and describe the mechanism. Vague responses ('the platform supports
> robust controls') will be returned."

**Practical effect on the audit log:** every C entry in `unsupported_api_requests` should
name its REQ number in `requested_feature` and state which of the three verdicts you are
claiming. That is the customer's own reporting format; use it.

The document is version 2.1, "approved by Risk Committee 2026-07-30". The call is
2026-08-06 — later, but it is corroboration, not amendment. **No stated doc-vs-call
precedence rule exists in this packet.** The document wins by its own scope clause; the
call adds detail and nowhere contradicts it.

### The pre-authorized fallback — quote this, it is unusually valuable

`security_requirements.doc`, REQ-3, lines 31–39:

> "REQ-3  PRE-AUTHORIZATION PURCHASE ORDER MATCH (MANDATORY AS WRITTEN; SEE NOTE)
> Transactions exceeding $500 USD must be declined at authorization unless a valid open
> Purchase Order number from the Apex ERP (NetSuite) is associated with the transaction
> prior to authorization. Note from CFO office: where pre-authorization matching is not
> technically available, Compliance will review the tightest available compensating control
> (e.g., hard transaction caps plus same-day post-transaction PO reconciliation with
> automatic card suspension on violation). Vendor response must state clearly which side of
> that line the platform falls on."

This is a **customer-granted, written pre-authorization of a fallback control**, with the
customer naming the exact fallback shape they expect. It lines up almost word-for-word with
the `CAP-PREAUTH-PO` workaround ("hard transaction_amount_limit at the threshold, plus
same-day post-transaction PO reconciliation, plus POST /funds/{id}/suspension on
violation").

Read it precisely: Compliance pre-authorizes **review** of a compensating control, not
acceptance of one. So:

- Encode the compensating control (per-transaction cap at $500 on the affected programs).
- File `CAP-PREAUTH-PO` (UNSUPPORTED) in `unsupported_api_requests`, `evidence` verbatim,
  `proposed_manual_workaround` from the ledger row, and state in
  `reason_unsupported` that the platform falls on the *detective* side of the line REQ-3
  draws — the requirement's own language demands you say which side.
- `missing_information_flags`: "Does Compliance accept the compensating control described
  under REQ-3?" — `blocking: true`, because REQ-3 is a stated condition of go-live and the
  answer is a customer decision you cannot make.

REQ-2 reads similarly but grants less: "State whether the platform can natively condition
card activation on an external attestation, and if not, the exact compensating control."
It invites the disclosure; it does not pre-authorize the fallback, and it adds "The
activation gate must fail closed". Use `CAP-ACTIVATION-GATE` (PARTIAL) and be explicit that
the issue-then-suspend workaround leaves a window and that nothing in Ramp enforces the
notarized-form evidence — a human does.

REQ-1 pre-empts the obvious wrong answer, lines 16–20:

> "Category-level controls are NOT sufficient: the Prohibited Vendor is classified as a
> medical supplier, the same category our clinic managers must retain access to.
> Enforcement must be at the individual merchant level and must apply to every card issued
> under the program, including temporary and contractor cards."

Do not propose a category block here. `CAP-VENDOR-BLOCK` (PARTIAL) — merchant UUIDs from
`GET /merchants`, no global blocklist, so the block repeats on every program and limit, and
each trade name ("Joe's Medical Supply", "JMS Distribution") must resolve to its own
merchant UUID. Both of those are `missing_information_flags`.

### Authority tension to log, not resolve

`discovery_call_apex.txt` line 40, `[02:32]`, MV: "I want to be clear these come from our
board's risk committee, so I have limited flexibility."
Line 60, `[04:12]`, GP (CFO): "What Millie will actually accept, if the ideal isn't
possible, is the tightest thing that gets us audit-proof. She just starts from the maximal
ask. It's a negotiating style."
Line 62, `[04:22]`, MV: "It's a compliance style."
Line 50, `[03:37]`, MV: "The number doesn't matter. The control has to exist."

A CFO's characterization of a colleague's negotiating posture is **not** authority to relax
a Risk-Committee-approved MANDATORY requirement. Record the exchange; do not use it as a
precedence rule.

---

## Packet D — `client_d_hypergrowth`

### The travel-approval conflict — BLOCKING

**Source A** — `fragmented_notes_feb2026.md`, "travel (the big one)", lines 15–21:

> "- PROPOSAL (dev): tiered — travel under $2,500 total trip cost auto-approved by
> department manager, over $2,500 goes to leo. leo keeps visibility via weekly digest
> instead of per-trip approvals
> - leo pushback: "i want to see everything" → long back and forth
> - landed: **leo agreed to try the $2,500 threshold for Q2** and revisit end of june"

**Source B** — `slack_export_finance.txt`, line 37, `[2026-07-30 08:55]`, leo.novak (CEO):

> "1. every dollar of travel goes through me. i sign off on all of it. we nearly died in
> 2024 because of a sales team that lived in marriotts. ALL travel needs my direct approval
> until further notice"

**Why recency does not settle it.** Source B is five months later and from the CEO, which
is the naive winner. Against that:

1. Source A records an **agreement**, not a proposal — the same person, Leo, agreed to it.
2. The note-taker disclaims her own document, lines 22–25:

   > "- NOTE (maya, typing this up in july): i wasn't in this meeting. i can't find the
   > follow-up where the Q2 trial was confirmed or cancelled. calendar shows the "travel
   > policy revisit" meeting on jun 26 was cancelled (conflict w/ board prep) and never
   > rescheduled"

   So it is unknown whether the Q2 trial lapsed, was cancelled, or is still running — and
   Leo's Slack message may be a CEO who has forgotten his own February agreement rather
   than a deliberate reversal.
3. **The conflict was raised in-channel and never answered.** `slack_export_finance.txt`
   line 42, `[2026-07-30 09:15]`, dev.batra:

   > "re: leo's #1 — is that compatible with what we agreed in the ops planning meeting?
   > (doc coming, maya has my notes)"

   Rachel's `[2026-07-30 08:58]` "👍 noted both" precedes this question, and nothing in the
   export answers it. The customer's own internal process stalled here.
4. Finance treats travel as still undesigned — line 59, `[2026-07-30 11:52]`, rachel.kim:
   "separate. travel is its own program, we're still designing it (see leo's message 🙃)".

**Encode:** `blocking: true`. `provisional_resolution` = **"none, blocking"**. Emit the
approval policy as desired state with `source` naming both documents, and note that
`CAP-APPROVAL-CHAIN` is UI_ONLY regardless, so nothing is applied by the config either way.
The unsafe outcome is not a wrong API call — it is a deployment rep telling Leo the config
matches a policy he did not agree to, or telling Dev his February agreement was quietly
dropped.

### The retracted message — do not build on it

`slack_export_finance.txt`, line 61, `[2026-07-31 14:20]`, stan.pollard:

> "also can ramp integrate with our netsuite instance for the PO stuff — actually nvm,
> wrong project, ignore me. that's the procurement tool eval. different channel"

Retracted in the same message by the person who wrote it. **There is no NetSuite/PO
requirement in packet D.** Do not extract it, do not emit a `CAP-PREAUTH-PO` entry, and do
not carry packet C's REQ-3 across. A single line in
`assumptions_made` recording that you saw it and deliberately excluded it is enough — an
`unsupported_api_requests` entry built on a retracted ask is a false positive, and
over-listing is explicitly graded against.

### The departments question — RESOLVED

`fragmented_notes_feb2026.md`, lines 42–44:

> "- CS team: nobody could say whether they're GTM or ops for budget purposes. parked.
> (dev: "they're ops." jj: "they're GTM." — unresolved feb, see slack, resolved since)"

The note points forward to Slack itself. `slack_export_finance.txt`, line 18,
`[2026-07-29 09:31]`, rachel.kim (Head of Finance):

> "CS goes in Ops. final answer. if anyone asks it's because they report to you"

Resolved by the finance owner, in writing, with the earlier document explicitly deferring.
Still log it as a `conflicts` entry (dev vs jj, February) with `provisional_resolution` =
CS in Ops, quoting Rachel — but `blocking: false`, and no `missing_information_flags` entry.
Contrast this with travel: here the later source *answers* the earlier one; there it
contradicts it without acknowledging it.

### Other D supersessions that DO resolve

| Item | Resolution | Why it is safe |
|---|---|---|
| Travel threshold `~~under $1,000~~ under $2,500` (`fragmented_notes_feb2026.md` line 21, "rachel talked him up from 1k") | $2,500 | In-document strike-through with an attributed reason |
| Manager uplift — `[2026-07-30 11:03]` "managers +50% on top of their team's IC number" then `[2026-07-30 11:09]` "correction — eng managers don't need +50%, eng managers barely spend. just GTM and ops managers get the bump" | GTM and Ops managers only | Same author, same channel, six minutes later, labelled "correction" |

Both are still `conflicts` entries — a self-correcting source is a source that disagreed
with itself.

### Blocking in packet D, at a glance

| Item | blocking |
|---|---|
| Travel approval policy (above) | **true** |
| Roster — `[2026-08-05 16:40]` "headcount export is stuck with our PEO... 82 people, breakdown roughly 40 eng / 22 GTM / 15 ops / 5 exec-ish. names and emails to follow" | **true** — no users can be created |
| Exec limits — `[2026-07-30 11:03]` "exec: we'll handle individually, ask me" | true for exec limits only |
| CS department | false |
| Offsite budget shape (`$60k`, expires Dec 1) | false — `CAP-AUTO-EXPIRY` is SUPPORTED |

---

## Packet E — `client_e_vanguard_retail`

### Stated rule: allow-first, default deny; the ALLOWED column is authoritative

`onboarding_call_vanguard.txt`, line 21, `[01:11]`, Ahmed Nasser (Finance Systems Manager):

> "Allow-first. Default deny. A merchandising rep has no business at an electronics store,
> and an installer has no business booking flights. The matrix's ALLOWED column is the whole
> universe of what that role can buy; the BLOCKED column is me being extra explicit about
> categories we've had incidents with — belt and suspenders."

**Resolves:** the allow-vs-block relationship. The ALLOWED column defines the universe; the
BLOCKED column is redundant emphasis inside a default-deny model, not an independent rule.
So an MCC that appears in neither column is denied, and a conflict between the columns
resolves toward ALLOWED being the boundary.

**Does NOT resolve:** anything about translation loss, because the customer is describing a
model Ramp does not implement in that direction (`CAP-MCC-ALLOWLIST`, UNSUPPORTED). The
belt-and-suspenders BLOCKED column turns out to be the *more* faithfully translatable half
— see `CATEGORY_MAP.md`.

### Stated rule: tell me which rules do not survive

Line 25, `[01:44]`, AN:

> "That's what I want to see. If some rule can't be enforced exactly as written I need to
> know which one and what the closest enforceable version is."

Line 17, `[00:47]`, AN, on provenance:

> "I built a matrix — you have it, the CSV — mapping each role to allowed and blocked
> merchant category codes. I pulled the MCC codes from our old amex reporting, so those are
> real codes from actual historical transactions."

A per-rule (not per-packet) mandate for the audit log. Satisfy it with one
`assumptions_made` entry per lossy mapping, each naming the role, and matching
`translation_notes` on each `mcc_controls` entry.

### Source authority in E

`mcc_allowlist_matrix.csv` is the authoritative source for limits — line 29, `[01:55]`,
Carol Jimenez: "In the matrix — last two columns. Monthly cap and per-transaction cap per
role." The call gives narrative; the CSV gives numbers. No conflict between them on limits.

### The headcount discrepancy — log it

- Call line 11, `[00:05]`, CJ: "about one hundred fifty field reps on the road at any time"
- `mcc_allowlist_matrix.csv` permanent roles sum to **131** (58 + 41 + 17 + 9 + 6)
- Call line 33, `[02:07]`, CJ: "about one hundred forty of them this year" — matches the
  Seasonal Rep row's 140

"About one hundred fifty" versus 131 is a hedged number against a precise one, from the
same speaker. Treat it as a `conflicts` entry with the CSV provisionally winning (it is the
instrument the customer pointed at for numbers), plus a `missing_information_flags` entry —
there is **no roster at all** in this packet, only headcounts. `blocking: true` for user
creation: every one of the 271 people is unnamed.

### Blocking in packet E

| Item | blocking |
|---|---|
| No roster — headcounts only, no names or emails | **true** for `users` and per-user limits |
| District-manager scoped visibility — line 55, `[03:42]` AN: "the six district managers should be able to see their own district's spend — just their district, not everyone's" | false — `CAP-SCOPED-VISIBILITY` (PARTIAL); model the reporting chain, flag the residual |
| Seasonal hard stop Dec 24 | false — `CAP-AUTO-EXPIRY` is SUPPORTED |
| MCC allow-list translation | false, but every lossy row is flagged |

---

## No stated rule? The decision procedure

When two sources disagree and nothing in the packet adjudicates:

1. **Log the conflict first.** Both values, both citations, before you decide anything.
2. **Do not default to recency.** Later is evidence, not authority. Ask what the later
   source *knew*: did it acknowledge and overturn the earlier one (packet D, CS in Ops), or
   is it apparently unaware of it (packet D, travel)? Only the first is supersession.
3. **Prefer the instrument the customer built for the purpose.** A roster, a matrix, a
   numbered compliance document, a versioned memo — these outrank an aside on a call about
   the thing they were built to state. A call outranks a document on matters of current
   operational reality (packet B's roadside hotels).
4. **Prefer the owner of the domain.** Finance on limits, Compliance on controls,
   Operations on what actually happens in the field.
5. **When you must still choose, choose the conservative value** — the lower limit, the
   narrower permission, the tighter block — and say in `provisional_resolution` that you did
   so *because* the conflict is unresolved. A too-tight card produces a phone call; a
   too-loose one produces an incident.
6. **Set `blocking: true` when applying the config without the answer would be unsafe.**
   Concretely, any of:
   - money can move to someone who should not have it, or at a level nobody approved;
   - a control the customer named as a condition of go-live would be absent (packet C);
   - the config would tell one stakeholder that another stakeholder agreed to something
     they did not (packet D travel);
   - the section cannot be constructed at all — no roster, no entity (packets D, E, B-Brazil).

   Otherwise `blocking: false`. Reversibility is the test: a wrong per-person limit is one
   PATCH; a card that should never have transacted is an incident.
7. **Never let a resolution erase the loser.** `provisional_resolution` says what you
   encoded *and* what you did not, and why.
