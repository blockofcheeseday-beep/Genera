# 02 — Verdicts

Agent 2 of 3. Adjudication of all 59 entries in `01_review.md` (R-01 … R-59).

**The test applied to every entry, and only this test:**

> If the Westbrook sample had never existed, would this still be here, justified by this
> packet's own sources and by verified evidence?

- **LEGITIMATE** — yes: a README-sanctioned idiom, or independently re-derived from the packet.
- **CONTAMINATION** — no: content, a value, a claim or reasoning present *because the sample
  had it*, not because this packet or verified evidence supports it.
- **JUDGEMENT** — cannot be settled on evidence alone.

**Instruction to Agent 3: apply section C only.** Section D (JUDGEMENT) requires a human
decision and must not be applied. Section F ("Observations that are not contamination")
is *not* a change list — it is out of scope for this audit and must not be acted on.

**Result: 1 CONTAMINATION, 1 JUDGEMENT, 57 LEGITIMATE.** A mostly-clean sheet is the honest
outcome here. The three sample-derived errors this build already found and fixed (owner →
`BUSINESS_ADMIN`, `"(surname pending roster)"` on a roster-less packet, a
`reimbursements_enabled` default) are confirmed gone: R-01 finds zero sample literals in
`out/` or `work/`, R-07 shows three distinct packet-true placeholders, R-32/R-35 show the
CEO defaulted *down* in both packets that have one, and R-22 … R-26 show
`reimbursements_enabled` reasoned per programme rather than defaulted (packet B is nine
`true` against one `false` — the opposite shape from a blind inherited default).

---

## A — Summary table

| # | one-line description | verdict |
|---|---|---|
| R-01 | Zero Westbrook literals anywhere in `out/` or `work/` | LEGITIMATE |
| R-02 | D's evidence line reuses the sample's "no notifications resource / nearest primitive is POST /webhooks" clause | LEGITIMATE |
| R-03 | Same evidence line in E | LEGITIMATE |
| R-04 | D and E assert the Slack integration "covers the common case of posting card activity to a channel" | **CONTAMINATION** |
| R-05 | A's receipt-threshold assumption reuses the sample's sentence frame around A's own $75/$500 | LEGITIMATE |
| R-06 | Sample's `"Software / SaaS"` spelling deliberately not inherited | LEGITIMATE |
| R-07 | Three distinct name placeholders, each true of its own packet | LEGITIMATE |
| R-08 | Programme `display_name` `"Software"` in A and D | LEGITIMATE |
| R-09 | Three-beat programme-description shape | LEGITIMATE |
| R-10 | No Westbrook identity reaches any packet | LEGITIMATE |
| R-11 | `approval_policies[].source` carries a verbatim quote in all twelve policies | LEGITIMATE |
| R-12 | Tier lists opening `{0, AUTO}` | LEGITIMATE |
| R-13 | Zero-threshold tier with a *person* approver (extension beyond the sample) | LEGITIMATE |
| R-14 | Omit-and-flag dispositions for receipt/memo rules | LEGITIMATE |
| R-15 | Name placeholder paired with a blocking flag | LEGITIMATE |
| R-16 | Group limits state cardinality in `notes` | LEGITIMATE |
| R-17 | Evidence-line shape in `unsupported_api_requests[].evidence` | LEGITIMATE |
| R-18 | `proposed_manual_workaround` names a route rather than refusing | LEGITIMATE |
| R-19 | `conflicts` array sizes (no packet emits `[]`) | LEGITIMATE |
| R-20 | Sample's explicit-`null` habit not reproduced | LEGITIMATE |
| R-21 | `"N/A"` used as a sentinel in address fields | LEGITIMATE |
| R-22 | A: Software `false` / Travel `true` | LEGITIMATE |
| R-23 | B: nine programmes `true`, `Software centralizado` `false`, unexplained | LEGITIMATE |
| R-24 | C: `false` on all four, packet silent, rationale stated | LEGITIMATE |
| R-25 | D: `assumptions_made[9].impact_if_wrong` asserts reimbursements "remain enabled company-wide" | **JUDGEMENT** |
| R-26 | E: `false` on all six with a stated basis | LEGITIMATE |
| R-27 | A: physical-card values stated in the packet | LEGITIMATE |
| R-28 | B: physical inferred on five of ten programmes | LEGITIMATE |
| R-29 | C: physical `true` on two of four while a flag asks about card format | LEGITIMATE |
| R-30 | D: `false` on both, packet silent, flagged | LEGITIMATE |
| R-31 | E: matches the matrix `Card_Type` column | LEGITIMATE |
| R-32 | A: three admin-class roles quoted, 27 users defaulted to BUSINESS_USER | LEGITIMATE |
| R-33 | B: three BUSINESS_ADMIN grants, scope caveat recorded | LEGITIMATE |
| R-34 | C: two admins, one auditor, all quoted | LEGITIMATE |
| R-35 | D: admins quoted, CEO defaulted down with a reason | LEGITIMATE |
| R-36 | E: BUSINESS_ADMIN on an unnamed user record | LEGITIMATE |
| R-37 | Receipt/memo omission and its pairing | LEGITIMATE |
| R-38 | A: department names verbatim from the packet | LEGITIMATE |
| R-39 | B: `Sistemas` promoted to a top-level department | LEGITIMATE |
| R-40 | C: three of six department names constructed | LEGITIMATE |
| R-41 | D: department names verbatim ("Eng, GTM, Ops, Exec") | LEGITIMATE |
| R-42 | E: all three department names constructed | LEGITIMATE |
| R-43 | `base_currency` `"USD"` in all five | LEGITIMATE |
| R-44 | `entities[].status` `"existing"` by default | LEGITIMATE |
| R-45 | `generated_at` midnight-Z convention | LEGITIMATE |
| R-46 | `locations` emitted only by B | LEGITIMATE |
| R-47 | `lock_date` values | LEGITIMATE |
| R-48 | `primary_card_enabled` `true` on all 24 programmes | LEGITIMATE |
| R-49 | Category selections with `translation_notes` | LEGITIMATE |
| R-50 | `assigned_to.group` names that are not departments | LEGITIMATE |
| R-51 | `approval_policies[].applies_to` values | LEGITIMATE |
| R-52 | Per-user limits in A vs group limits elsewhere | LEGITIMATE |
| R-53 | A: 35 of 35 figures trace to packet A | LEGITIMATE |
| R-54 | B: 22 of 26 trace; 4 FX-derived with a stated rate | LEGITIMATE |
| R-55 | C: 13 of 13 trace | LEGITIMATE |
| R-56 | D: 7 of 9 trace; 2 documented arithmetic derivations | LEGITIMATE |
| R-57 | E: 25 of 25 trace to the matrix | LEGITIMATE |
| R-58 | 15 numeric coincidences with Westbrook's five figures | LEGITIMATE |
| R-59 | Packet figures deliberately not configured | LEGITIMATE |

## B — Counts

| verdict | count |
|---|---|
| LEGITIMATE | 57 |
| CONTAMINATION | 1 (R-04) |
| JUDGEMENT | 1 (R-25) |
| **total** | **59** |

---

## C — CONTAMINATION: the change list (Agent 3 applies this section, and only this section)

### R-04 — The Slack integration's *behaviour* is asserted as fact to two customers on evidence that only establishes the integration exists

**Why this fails the test.** The cited evidence is a single source, `openapi_snapshot_2026_08_30`.
The parent has verified what that snapshot actually contains: the string "Slack" appears 12
times, and the only substantive occurrence is a field named `is_integrated_with_slack`,
described as *"whether the business has integrated with slack"* — a **read-only boolean on the
business object**. That establishes that a Ramp Slack integration *exists*. It says nothing
about what the integration does, and in particular nothing about whether it posts card
activity to a channel.

The sample hedged exactly here: *"Ramp's in-app Slack integration **may cover this**
(deployment owner to enable)"*. The ledger's own internal `workaround` field still hedges
("may cover the common case"). The `customer_workaround` field — the one copied verbatim into
packets D and E and read by those customers — dropped the hedge and asserts
"**covers** the common case of posting card activity to a channel". So a tentative claim the
sample raised has been promoted to a statement of fact, and delivered to two customers who
never asked about Slack (D asks to be told about cards over $10k/mo; E asks for a weekly
exceptions report). Neither packet supplies the missing support, and the snapshot does not.

This is the audit's sharpest item because it is the one place where the failure is not a
shared sentence shape but an **unverified claim asserted because the sample raised the
subject**.

**Why the workaround is repaired rather than deleted.** A workaround that names a real route
is more useful to a deployment owner than silence, and the *existence* of the integration is
supported. Only the behavioural claim is unsupported. The fix restores the hedge and states
what the evidence actually shows.

**Fix shape — safe.** All three edits are in-place rewrites of a single string value. **No
array element is added, deleted or reordered anywhere.** This matters: `audit_refs` in
`work/<packet>/traceability.json` are index-based strings (`"unsupported_api_requests[6]"`),
**284 of them across the five packets** (A 54, B 61, C 64, D 57, E 48), and splicing an audit
array would silently shift every later reference while leaving it in range. Nothing here
touches an index.

---

#### C.1 — File 1 of 3

- **File:** `/home/user/Genera/out/client_d_hypergrowth/audit_log.json`
- **JSON path:** `unsupported_api_requests[1].proposed_manual_workaround`
- **Do not change** `unsupported_api_requests[1].requested_feature`, `.reason_unsupported` or
  `.evidence`, and do not change the position of this element in the array.

**Current text (exact, the entire string value):**

```
Ramp has no rule engine for routing spend alerts to a chat channel or to a named person. Ramp's Slack integration, switched on by the deployment owner in the Ramp application, covers the common case of posting card activity to a channel; anything conditional, such as alerting only above a set monthly amount, needs a webhook subscription with the threshold applied by the receiving system.
```

**Replacement text (exact, the entire string value):**

```
Ramp has no rule engine for routing spend alerts to a chat channel or to a named person. Ramp does have a Slack integration, switched on by the deployment owner in the Ramp application, which may cover the simple case of posting card activity to a channel — the API specification records only a read-only is_integrated_with_slack flag on the business object and does not describe what that integration posts, so its scope should be confirmed in the Ramp application before anyone relies on it. Anything conditional, such as alerting only above a set monthly amount, needs a webhook subscription with the threshold applied by the receiving system.
```

#### C.2 — File 2 of 3

- **File:** `/home/user/Genera/out/client_e_vanguard_retail/audit_log.json`
- **JSON path:** `unsupported_api_requests[6].proposed_manual_workaround`
- **Current text:** byte-identical to C.1's current text.
- **Replacement text:** byte-identical to C.1's replacement text.
- **Do not change** any sibling field, and do not change the position of this element in the
  array. Packet E has 48 index-based `audit_refs`.

#### C.3 — File 3 of 3 (the source the other two are copied from)

- **File:** `/home/user/Genera/.claude/skills/ramp-deployment/references/capabilities.yaml`
- **Path:** ledger row `id: CAP-NOTIFICATIONS`, key `customer_workaround` (lines 693–698 as
  the file currently stands).
- **Why this file too:** `customer_workaround` is the string the pipeline copies verbatim into
  packets D and E. If it is not repaired, the next regeneration re-introduces the claim into
  both audit logs.

**Current block (exact, including the `>-` folded-scalar marker and the six-space
continuation indent):**

```yaml
    customer_workaround: >-
      Ramp has no rule engine for routing spend alerts to a chat channel or to a named
      person. Ramp's Slack integration, switched on by the deployment owner in the Ramp
      application, covers the common case of posting card activity to a channel; anything
      conditional, such as alerting only above a set monthly amount, needs a webhook
      subscription with the threshold applied by the receiving system.
```

**Replacement block (exact — keep the `>-` marker, the four-space key indent and the
six-space continuation indent; a folded scalar joins these lines with single spaces, which
reproduces the replacement text in C.1 exactly):**

```yaml
    customer_workaround: >-
      Ramp has no rule engine for routing spend alerts to a chat channel or to a named
      person. Ramp does have a Slack integration, switched on by the deployment owner in
      the Ramp application, which may cover the simple case of posting card activity to a
      channel — the API specification records only a read-only is_integrated_with_slack
      flag on the business object and does not describe what that integration posts, so
      its scope should be confirmed in the Ramp application before anyone relies on it.
      Anything conditional, such as alerting only above a set monthly amount, needs a
      webhook subscription with the threshold applied by the receiving system.
```

**Also in the same ledger row — add the second evidence source that the repaired wording now
relies on.** The row currently cites one source and says nothing about `is_integrated_with_slack`,
which is why the claim went uncontrolled. Append one entry to the **end** of the existing
`evidence:` list in `CAP-NOTIFICATIONS` (append only — do not reorder or renumber; nothing
indexes into this list, `audit_refs` point only at `audit_log.json` arrays):

```yaml
      - source: openapi_snapshot_2026_08_30
        checked_on: 2026-08-30
        note: >-
          The only substantive Slack reference in the specification is a read-only
          is_integrated_with_slack boolean on the business object ("whether the business has
          integrated with slack"). It establishes that a Slack integration exists; it does
          not describe what the integration posts, so any claim about its behaviour must
          stay hedged.
```

**Do not change** the row's `evidence_line`, `api_mechanism`, `verdict`, `workaround`
(the internal field — it is already correctly hedged) or `seen_in`.

**Evidence justifying all three edits, in one place:**
1. `candidate/2026_08_30_Ramp_OpenAPI_Schema.json` — "Slack" appears 12 times; the only
   substantive occurrence is the field `is_integrated_with_slack`, described as "whether the
   business has integrated with slack", read-only on the business object. Nothing describes
   the integration's behaviour. (Verified by the parent.)
2. `.claude/skills/ramp-deployment/references/capabilities.yaml`, `CAP-NOTIFICATIONS.evidence`
   — one source only, `openapi_snapshot_2026_08_30`. No other evidence is cited for the claim.
3. `candidate/sample_packet/client_0_sample_westbrook/example_output/audit_log.json` —
   `unsupported_api_requests[0].proposed_manual_workaround`: "Ramp's in-app Slack integration
   **may cover this** (deployment owner to enable)". The sample was hedged; the packets are not.
4. `candidate/customer_packets/client_d_hypergrowth/slack_export_finance.txt` and
   `candidate/customer_packets/client_e_vanguard_retail/onboarding_call_vanguard.txt` — neither
   customer asks for chat-channel alerts, so neither packet supplies independent support for
   the behavioural claim.

**What is NOT changed by this fix, and why.** The `evidence` string in both entries
("no notifications resource; nearest primitive is POST /webhooks (transaction events), which
delivers events but does not evaluate threshold or routing rules") stays exactly as it is. It
is a true claim, independently verifiable in the snapshot — `/developer/v1/webhooks` exists
with GET and POST, alongside `/webhooks/{id}`, `/webhooks/{id}/verify` and
`/webhooks/mock-webhook-event`, and there is no notifications configuration resource. See
R-02/R-03.

---

## D — JUDGEMENT (do not apply; a human decides)

### R-25 — Packet D tells the customer that "reimbursements remain enabled company-wide"

- **File:** `/home/user/Genera/out/client_d_hypergrowth/audit_log.json`
- **JSON path:** `assumptions_made[9].impact_if_wrong`
- **Current text:** `"None to card behaviour. Reimbursements remain enabled company-wide so
  invoice reimbursement is unaffected."`

**The facts.** Both of packet D's spend programmes carry
`permitted_spend_types.reimbursements_enabled: false`. `candidate/schemas/ramp_config_schema.json`
has no company-wide reimbursement field at all — `permitted_spend_types` is per programme,
with `additionalProperties: false` and both booleans required. Packet D never states that
reimbursements remain on; its three reimbursement mentions are the contractors' invoice route,
an unresolved per-diem question, and jj wanting to stop fronting money. The nearest thing to a
source for this sentence is packet **A**'s `conflicts[3]`, where the same phrase *is* earned
(`discovery_call_01.txt` [06:48]: "Keep reimbursements on for edge cases").

**Why it cannot be settled on evidence alone.** Two readings are both available and the
evidence does not choose between them:

- **Option 1 — leave it.** Read as a statement of *scope* ("nothing in this configuration
  switches reimbursements off company-wide"), the sentence is true: the two programme flags
  govern only those two programmes, and the QA contractors are excluded from the
  configuration entirely, so their invoice route is untouched. On this reading it is clumsy
  phrasing, not a false claim, and the audit's remit — Westbrook contamination — does not
  reach it, since the phrase's ancestry is packet A, not the sample.
- **Option 2 — rewrite the sentence in place** to say only what packet D supports:
  `"None to card behaviour. The contractors receive no cards in this configuration, so their
  invoice reimbursement runs outside it entirely."`
  This is a single-string in-place rewrite — no array splice, no index shift (packet D has 57
  index-based `audit_refs`).

**What the human needs to decide:** whether an audit-log sentence that asserts a positive
state for a setting this document does not contain is acceptable as scope-language, or whether
it should be narrowed to what packet D actually supports. Two considerations for that call:
the claim is customer-facing, and the phrase travelled from a packet where it was quoted to
one where it is not — which is the same failure mode as R-04 even though its ancestry is not
Westbrook. Option 2 is true under **both** readings, so it is the safe choice if the decision
is close.

---

## E — LEGITIMATE (one line each)

**Dimension 1 — literal content**

- **R-01** — Negative result: zero sample literals in `out/` or `work/`; the only occurrences
  are in skill files that cite the sample as a model. Nothing to inherit.
- **R-02** — The shared clause states a claim the parent verified true against
  `candidate/2026_08_30_Ramp_OpenAPI_Schema.json` (webhooks exist; no notifications resource);
  `candidate/README.md` explicitly tells the reader to cite date and source in the sample's shape.
- **R-03** — Same claim, same verification; and E's own request (a scheduled weekly exceptions
  report) is genuinely notification-class, so the entry belongs in E on E's own facts.
- **R-05** — The figures are packet A's own and verified (`discovery_call_01.txt` [07:03]:
  "Required over seventy-five dollars… memo required for anything over five hundred"), and the
  underlying claim — receipt thresholds are an in-app setting with nowhere in this schema to
  live — is true. A reused sentence frame around correct, packet-specific facts is exactly the
  README-sanctioned idiom, not contamination.
- **R-06** — The sample's `"Software / SaaS"` spelling was deliberately *rejected* in favour of
  the API vocabulary, with the reason recorded in the ledger. Evidence of independence.
- **R-07** — Three distinct placeholders, each asserting something true of its own packet
  (C has no roster; D's roster is genuinely promised; E's controller is unnamed). The sample's
  string appears nowhere.
- **R-08** — "Software" is the customers' own word in both packets ("a dedicated software
  card", "NOT let random ICs buy software"); a common English noun is not an inheritable literal.
- **R-09** — Every clause of A's description traces to A's own quotes ([02:31], [03:02]); a
  three-beat description shape is a writing convention, not a claim.
- **R-10** — No Westbrook name, address or entity reaches any packet; `"N/A"` is used rather
  than a constructed address, with the reason stated in four packets.

**Dimension 2 — structural idioms**

- **R-11** — `source` is optional in the schema; filling it with a verbatim quote is the idiom
  `SKILL.md:321` names, and the packets extend it with speaker, role and timestamp.
- **R-12** — The schema itself defines `threshold_usd_cents: 0` as the auto-approve tier, and
  each AUTO band is backed by a packet quote.
- **R-13** — An extension *beyond* the sample (the sample's only zero-threshold tier is AUTO),
  so it cannot be inherited; each instance records in `source` that the encoding is broader
  than the request, and is paired with an `unsupported_api_requests` entry.
- **R-14** — The dispositions differ per packet and track each packet's own facts; the schema
  has no receipt or memo field, so recording the rule somewhere in the audit log is the only
  honest option.
- **R-15** — Placeholder-plus-blocking-flag is a correct pattern on its own merits: an
  incomplete identity that cannot be provisioned must be visible as a blocker.
- **R-16** — `candidate/README.md` names group limits as an idiom to study, and every count
  traces to its own packet (A [04:05], B [01:18], C [00:08], D [2026-08-05 16:40], E's
  `Headcount` column).
- **R-17** — `candidate/README.md`: "cite the date and source you checked in your audit-log
  `evidence` fields (the sample packet shows the shape)". The sample's own source name and date
  appear nowhere in `out/`.
- **R-18** — `AUDIT_PATTERNS.md:469` prescribes proposing a route rather than refusing; the
  twelve repeated strings are one archetype each, correctly reused. The single defective string
  is handled at R-04.
- **R-19** — Sizes track how much each packet disagrees with itself (B's memo says of itself
  that its sections are not harmonised); `conflicts: []` was never treated as a target to hit.
- **R-20** — The sample's explicit-`null` habit was *not* reproduced; both forms validate.
  Evidence of independence.
- **R-21** — Cannot be sample-inherited: the sample carries real addresses and `null`. `"N/A"`
  in `email` is a documented house rule with a stated reason in four packets. (C's use of
  `"N/A"` in `direct_manager_email` is a separate, non-contamination inconsistency — see F.2.)

**Dimension 3 — reasoning inheritance**

- **R-22** — Both values are quoted: "Nobody buys software on a personal card, period" [02:31]
  and "Keep reimbursements on for edge cases" [06:48].
- **R-23** — Nine `true` against one `false` is the opposite shape from an inherited default: a
  blind sample echo would have set all ten `false`. The exception is supported by B's own
  sources — [03:45] "una sola tarjeta virtual para todo el software, la maneja sistemas",
  §2.5 "tarjeta única virtual", §3.4 "A filial brasileira NÃO deve contratar software por conta
  própria" — and that reasoning is already stated in
  `spend_programs[4].description`. The audit log's silence about the exception is a
  documentation gap, not an unearned value (see F.1).
- **R-24** — `assumptions_made[12]` states the rule and the reason explicitly, and records that
  an earlier draft enabling reimbursements by inference was withdrawn — the corrected pattern
  working.
- **R-26** — Quoted from `onboarding_call_vanguard.txt` [00:27] and the matrix's per-diem note,
  with `impact_if_wrong` naming the risk and a date to confirm by.
- **R-27** — Both values stated in the packet ("a dedicated software card — virtual"; "physical
  for everyone in Sales anyway").
- **R-28** — Cannot be sample-inherited: five programmes are set `true` where the sample is
  `false`. Physical cards for road drivers and commercial staff are a plain reading of the
  packet's operations. Unstated, but not inherited (see F.3).
- **R-29** — The two `true` values trace to `discovery_call_apex.txt` [03:30] — Bruno's card and
  the regional directors' named in answer to which *physical* cards could exceed $10,000 — which
  are exactly the Facilities and Regional Travel programmes. No contradiction with
  `missing_information_flags[11]`: the field is `issue_physical_card_if_needed` ("may be issued
  if needed"), while the flag asks the different and still-open question of *which cardholders*
  and *what shipping addresses*.
- **R-30** — Silence answered with the conservative value (no plastic nobody asked for) and the
  gap recorded in `missing_information_flags[9]`, which names card format as never discussed.
  The field is required-shaped in practice and `false` withholds rather than grants.
- **R-31** — Every value matches the matrix `Card_Type` column and is corroborated at [02:49].
- **R-32** — The defaulted 26 are BUSINESS_USER, the *least*-privileged role; the sample's
  failure mode was over-granting, and `assumptions_made[1]` records the CEO grant being withdrawn.
- **R-33** — Two grants quoted at [04:37]; the third carries an explicit caveat that the grant
  is company-wide where the request was Miami-scoped.
- **R-34** — All three admin-class roles quoted ([05:51], [05:58], REQ-5); no sample counterpart
  exists for an auditor. (The nurses' GUEST_USER statement without nurse user records is a
  separate internal inconsistency — see F.4.)
- **R-35** — The corrected pattern, verbatim: admins quoted from Slack, and the CEO defaulted
  *down* with the reason in `users[0].notes`.
- **R-36** — The role is stated, not inferred: `onboarding_call_vanguard.txt` [03:42] answers
  "Who administers?" with "Me and our controller." Only the *identity* is missing, and that is
  carried by a blocking `missing_information_flags[1]` plus `users[2].notes`. This is the
  opposite of the fixed error, which inferred a role from a job title.
- **R-37** — See R-14; the substance is recorded in every packet, in the section that fits that
  packet's facts.
- **R-38** — Four names verbatim from [00:47], the fifth from the roster, with an assumption and
  a conflict entry.
- **R-39** — Cannot be sample-inherited: the sample's idiom is to create exactly the departments
  the source names, so an *extra* department is a departure from it, not an echo. It is a
  modelling choice with a real anchor (the software card is held by Sistemas and is separate for
  spend purposes) that contradicts the packet's three-area statement — a genuine defect, but
  outside this audit's remit (see F.5).
- **R-40** — No sample counterpart exists (Westbrook's names are lifted from its email), so
  nothing was inherited; the constructed labels are groupings of the packet's own words.
- **R-41** — Verbatim, abbreviations included: "keep it simple: Eng, GTM, Ops, Exec. that's it."
- **R-42** — No sample counterpart; `HQ` is literal, the other two are the packet's own job-title
  vocabulary.
- **R-43** — `base_currency` is a required field with no packet statement in four of five; B, the
  one packet that speaks, supports USD consolidation (§5.1, [02:50]) while entity currencies stay
  local.
- **R-44** — `status` is required with a two-value enum, and `"existing"` is the only correct
  value for a company already operating; B, the one packet that speaks, correctly marks Brazil
  `"requested"`.
- **R-45** — Midnight-Z is a formatting convention, not a claim; every date is the build's own,
  and a config generated on the 31st citing a snapshot checked on the 30th is coherent.
- **R-46** — `locations` is optional; only B's packet states geography with entity structure, and
  B's `assumptions_made[6]` explains the binding. C and E raise their geography as blocking flags.
- **R-47** — Every lock date is quoted ("stops existing on dec 1"; "must stop working December
  24th"), and C's absence is explained in `limits[5].notes` with a blocking flag.
- **R-48** — Required by the schema, and every programme in every packet exists because the
  packet asked for cards; no packet describes a reimbursement-only programme.
- **R-49** — Each selection carries `translation_notes` naming the Ramp category and what is
  lost, with exclusions stated and repeated as questions; D records a withdrawn widening.
- **R-50** — The schema explicitly permits a cohort ("a department name or a named cohort, e.g.
  'Field Reps'"), and membership is stated in `notes` in every case.
- **R-51** — `applies_to` is a free string in the schema; A/C/D/E use the described forms and D's
  over-broad scope is flagged `PROVISIONAL` with a conflict. (B's entity-scoped values are a
  separate, non-contamination deviation — see F.6.)
- **R-52** — A is the only packet with a roster supplying per-person targets, and the packet says
  the roster wins ([04:31]).

**Dimension 4 — value provenance**

- **R-53** — 35 of 35 trace to packet A by amount and currency; the one interpretive figure
  carries an assumption, a conflict, an unsupported entry and a blocking flag.
- **R-54** — 22 of 26 trace unconverted; the four FX-derived thresholds state their rate, state
  that no rate provider was used, and ask the customer to accept them in a blocking flag.
- **R-55** — 13 of 13 trace, including five spelled-out forms.
- **R-56** — 7 of 9 trace; the two exceptions are exact arithmetic from a stated rule
  ("managers +50% on top of their team's IC number"), with the derivation in `notes`.
- **R-57** — 25 of 25 trace to the matrix columns; the one non-matrix figure is quoted at [03:33].
- **R-58** — All 15 coincidences with Westbrook's five figures have an independent quote in their
  own packet, including the sample's most distinctive value ($800), which appears once and comes
  from a roster cell. Numeric overlap is therefore not evidence of inheritance anywhere in this
  build.
- **R-59** — Figures deliberately left out of the configs are each carried in the audit log with
  a reason; nothing was configured because a number was available.

---

## F — Observations that are **not** contamination (out of scope; not a change list)

Recorded so the reader can see what was examined and set aside, and because a human may want
them on a separate list. **None of these is a verdict, and Agent 3 must not act on any of
them.** Each fails the test in the same way: it has no sample counterpart, or the sample's
value is the opposite, so it cannot be unearned inheritance from Westbrook. Every one is an
in-place text or value change if it is ever pursued — none needs an array splice.

1. **R-23 — packet B's audit log is silent on its one `reimbursements_enabled: false`.**
   `assumptions_made[10]` says flatly "Reimbursements remain enabled." while
   `spend_programs[4]` disables them. The value is defensible; the sentence is unqualified.
2. **R-21 — packet C writes the string `"N/A"` into `direct_manager_email` for five users**
   where the schema says "null if unknown"; A, B, D and E all use `null`. C also assigns three
   limits to `assigned_to.user_email: "N/A"`.
3. **R-28 — packet B sets `issue_physical_card_if_needed: true` on five programmes** whose card
   format the packet never states, with no `assumptions_made` entry and no traceability coverage.
4. **R-34 — packet C's `assumptions_made[5]` assigns traveling nurses the Guest User role**, but
   no `users[]` record in C carries `GUEST_USER` and no nurse user record exists.
5. **R-39 — packet B's `departments[3] = "Sistemas"`** contradicts [01:18], which places sistemas
   inside Administración, and `requirements.json` REQ-007, which records three areas. No entry
   explains it.
6. **R-51 — packet B's three entity-scoped `applies_to` values** are none of the schema's
   described forms (department, spend program, or "all"), with no entry explaining the departure.

---

## G — Note on fix safety, for whoever applies anything from this file

`work/<packet>/traceability.json` stores `audit_refs` as index-based strings such as
`"unsupported_api_requests[6]"` — **284 across the five packets: A 54, B 61, C 64, D 57,
E 48.** Deleting, inserting or reordering an element in any `audit_log.json` array silently
shifts every later reference while leaving it in range, so the references stay valid-looking
and point at the wrong entry. **Every change proposed in this file is an in-place rewrite of a
single string value, plus one append to the end of a YAML list that nothing indexes into.** No
proposed change moves an index. Any future fix that would require a splice should be raised as
JUDGEMENT rather than applied.
