# 01 — Reviewer's evidence log: points of contact with the Westbrook sample

Agent 1 of 3. **This document gathers evidence only.** Nothing here is a finding, a
severity, or a recommendation. Entries are numbered R-01 … R-72 and are cited by number
in the final message. Judgement belongs to Agent 2.

## What was read

- `candidate/sample_packet/client_0_sample_westbrook/intake_email.txt` (full, the sample's only source)
- `candidate/sample_packet/client_0_sample_westbrook/example_output/ramp_config.json` (full, repeatedly)
- `candidate/sample_packet/client_0_sample_westbrook/example_output/audit_log.json` (full, repeatedly)
- `out/<packet>/ramp_config.json` and `out/<packet>/audit_log.json` for all five packets (full)
- `work/<packet>/requirements.json` (all 180 requirements, all five packets) and `work/<packet>/traceability.json`
- All ten source documents under `candidate/customer_packets/` (full)
- `candidate/README.md`; `candidate/schemas/ramp_config_schema.json`
- `.claude/skills/ramp-deployment/SKILL.md` and `references/*.md` — read only to locate where
  the sample is cited as a model, since that is the transmission path

## Tools run (read-only)

- `python3 .claude/skills/ramp-deployment/scripts/money_map.py --packet <p> --json` for all five packets
- A scratch script cross-joining every `limit_amount_cents` / `transaction_amount_limit_cents` /
  `threshold_usd_cents` in each config against that packet's money_map output (dimension 4)
- A scratch script diffing every config path against `work/<packet>/traceability.json`
  `config_paths` coverage (dimension 3)

`run_pipeline.py --verify` was **not** run. Nothing outside this file was written.

## The sample, for reference

Westbrook is one 12-person design agency, one intake email, one author (Nora Bailey), two
departments (Studio / Ops), two named users, one spend program, two limits, one approval
policy, one MCC control, one assumption, one missing-info flag, **zero conflicts**, one
unsupported request (Slack alerts). Every figure in it: $50, $800, $1,000, $2,000, $5,000.

---

# Dimension 1 — Literal content

## R-01 — Confirmation of the parent's negative greps, plus extensions

- **packet:** all five
- **JSON path:** whole of `out/`, whole of `work/`
- **what is there:** `grep -ril` over `out/` and `work/` for `westbrook`, `priti`, `nora`,
  `bailey`, `studio` returns **zero files**. `grep -rn` for `2026-08-24`, `Software / SaaS`,
  and `surname pending` returns **zero lines**. I extended the set: `westbrookdesign`,
  `#spend`, `design agency`, `12-person`, `finance contractor`, `project materials`,
  `client meals` — all zero in `out/` and `work/`.
- **the sample counterpart:** the strings themselves.
- **evidence:** the only occurrences anywhere in the repo are inside
  `.claude/skills/ramp-deployment/SKILL.md` (lines 43, 283, 315–321, 354) and
  `references/AUDIT_PATTERNS.md` (lines 23, 242, 247, 429–469),
  `references/CAPABILITY_LEDGER.md` (lines 298, 722, 1186), `references/CATEGORY_MAP.md`
  (lines 283–284), where the sample is cited *as a model to study*.
- **stated basis:** `candidate/README.md` — "Read it to see the output shapes and audit-log
  idioms (group limits, empty sections when a packet genuinely has none, evidence lines that
  cite what was checked and when)."

## R-02 — Sample's unsupported-request evidence sentence appears near-verbatim in packet D

- **packet:** client_d_hypergrowth
- **JSON path:** `out/client_d_hypergrowth/audit_log.json → unsupported_api_requests[1].evidence`
- **what is there:** `"Ramp Developer API specification (snapshot dated 2026-08-30) — no
  notifications resource; nearest primitive is POST /webhooks (transaction events), which
  delivers events but does not evaluate threshold or routing rules."`
- **the sample counterpart:** `"docs.ramp.com API reference, checked 2026-08-24 — no
  notifications resource; nearest primitive is POST /webhooks (transaction events)."`
  The clause `no notifications resource; nearest primitive is POST /webhooks (transaction
  events)` is identical word for word; only the source name, the date, and a trailing
  qualifier differ.
- **evidence:** packet D's request is `slack_export_finance.txt` — Leo Novak, 2026-07-30
  08:55: `"nobody gets a card with more than $10k/mo without me knowing"`. Packet D never
  mentions Slack alerts, a channel, or notifications as a product request; the Slack export
  is the *medium* of the packet, not a feature request in it.
- **stated basis:** none given for the wording. The entry's own
  `reason_unsupported` says "This is a request to be informed rather than a spending rule,
  and Ramp has no notification configuration surface."

## R-03 — The same evidence sentence again in packet E

- **packet:** client_e_vanguard_retail
- **JSON path:** `out/client_e_vanguard_retail/audit_log.json → unsupported_api_requests[6].evidence`
- **what is there:** the identical string to R-02, character for character.
- **the sample counterpart:** as R-02.
- **evidence:** packet E's request is `onboarding_call_vanguard.txt` — Carol Jimenez,
  [03:21]: `"District managers review a weekly exceptions report instead of approving in
  advance."` A weekly report to six named managers; no channel, no alert, no threshold.
- **stated basis:** the entry's `reason_unsupported` — "Ramp has no configurable report
  scheduler or notification rule surface".

## R-04 — Sample's Slack-integration workaround prose reused in D and E

- **packet:** client_d_hypergrowth and client_e_vanguard_retail
- **JSON path:** `out/client_d_hypergrowth/audit_log.json → unsupported_api_requests[1].proposed_manual_workaround`;
  `out/client_e_vanguard_retail/audit_log.json → unsupported_api_requests[6].proposed_manual_workaround`
- **what is there:** both carry the identical text: `"Ramp has no rule engine for routing
  spend alerts to a chat channel or to a named person. Ramp's Slack integration, switched on
  by the deployment owner in the Ramp application, covers the common case of posting card
  activity to a channel; anything conditional, such as alerting only above a set monthly
  amount, needs a webhook subscription with the threshold applied by the receiving system."`
- **the sample counterpart:** `"Ramp's in-app Slack integration may cover this (deployment
  owner to enable); otherwise a webhook consumer that posts to #spend."` Same two-move
  structure (in-app Slack integration → else webhook consumer), same actor phrasing
  ("deployment owner to enable" / "switched on by the deployment owner").
- **evidence:** neither packet asks for a chat channel. Packet D: `"nobody gets a card with
  more than $10k/mo without me knowing"`. Packet E: `"District managers review a weekly
  exceptions report"`. The phrase "posting card activity to a channel" has no referent in
  either packet. Westbrook's does: `intake_email.txt` — `"we'd love it if every transaction
  posted an alert into our #spend Slack channel automatically"`.
- **stated basis:** none given.

## R-05 — Sample's receipt-threshold assumption prose reproduced in packet A

- **packet:** client_a_acme_corp
- **JSON path:** `out/client_a_acme_corp/audit_log.json → assumptions_made[5]` and `assumptions_made[6]`
- **what is there:** `"The $75 receipt threshold is an in-application policy setting and is
  deliberately left out of this configuration, because there is nowhere in the configuration
  to record it."` `impact_if_wrong`: `"No effect on card behaviour. If the deployment owner
  does not set the threshold in the Ramp application during setup, receipts are not required
  at all…"` The memo entry (`assumptions_made[6]`) repeats the shape verbatim: "…for the
  same reason as the receipt threshold."
- **the sample counterpart:** `"Receipt threshold ($50) is an in-app policy setting, not part
  of this config's card objects."` `impact_if_wrong`: `"None to card behavior; the deployment
  owner sets it during in-app setup instead."`
- **evidence:** packet A states its own thresholds — `discovery_call_01.txt` [07:03], Priya
  Shetty: `"Required over seventy-five dollars… And memo required for anything over five
  hundred."` The figures are A's own; the sentence frame and the impact clause are the
  sample's.
- **stated basis:** `.claude/skills/ramp-deployment/SKILL.md:283` — "…idiom the Westbrook
  sample demonstrates with its $50 receipt rule."

## R-06 — Sample's category spelling was *not* inherited

- **packet:** all five
- **JSON path:** e.g. `out/client_a_acme_corp/ramp_config.json → spend_programs[0].spending_restrictions.allowed_categories[0]`
- **what is there:** every packet writes `"SaaS / Software"` (A, B, D). Zero occurrences of
  `"Software / SaaS"` anywhere in `out/`.
- **the sample counterpart:** `"allowed_categories": ["Software / SaaS"]` (sample config,
  `spend_programs[0]` and `mcc_controls[0].values`).
- **evidence:** `references/CAPABILITY_LEDGER.md:722` — "the canonical spelling is 'SaaS /
  Software'; the Westbrook sample config writes 'Software / SaaS', which validates because
  the exercise schema takes free strings but does not match the API vocabulary."
- **stated basis:** as quoted above — a deliberate departure from the sample.

## R-07 — Name-placeholder wording: sample string absent, three variants present

- **packet:** C, D, E (A and B have none)
- **JSON path:**
  - `out/client_c_apex_health/ramp_config.json → users[5].last_name` = `"(surname not stated)"`
  - `out/client_d_hypergrowth/ramp_config.json → users[5].last_name` = `"(full name pending roster)"`
  - `out/client_e_vanguard_retail/ramp_config.json → users[2].first_name` = `"(first name not stated)"`, `users[2].last_name` = `"(surname not stated)"`
- **what is there:** three distinct placeholder strings, all in the sample's parenthetical
  lower-case register.
- **the sample counterpart:** `"first_name": "Priti", "last_name": "(surname pending roster)"`.
- **evidence:** C — `discovery_call_apex.txt` [00:32]: `"And our facilities lead, Bruno, who
  handles repairs and contractors."` C's packet contains no roster and no promise of one.
  D — `slack_export_finance.txt` line 4 lists `"jj (Sales lead)"`, and [2026-08-05 16:40]
  Rachel Kim: `"names and emails to follow whenever the portal resurrects"` — a roster is
  genuinely pending. E — `onboarding_call_vanguard.txt` [03:42]: `"Me and our controller."`
  The controller is never named; a spreadsheet is promised ([02:55]).
- **stated basis:** C `assumptions_made[3]`: "…rather than a guessed name. This packet
  contains no roster, so the surname is not pending a document — it is simply absent."
  D `assumptions_made[3]`: "…the only name this packet contains for that person."
  E: no assumptions entry naming the placeholder; `missing_information_flags[1]` asks
  "Who is the controller named as the second administrator?"
  `references/AUDIT_PATTERNS.md:242,247` prescribes: "Pick the placeholder that is true of
  this packet. Westbrook and Hypergrowth both have a [roster coming]."

## R-08 — Spend-program display name "Software"

- **packet:** A, D (B uses `"Software centralizado"`)
- **JSON path:** `out/client_a_acme_corp/ramp_config.json → spend_programs[0].display_name`;
  `out/client_d_hypergrowth/ramp_config.json → spend_programs[0].display_name`
- **what is there:** `"Software"` in both.
- **the sample counterpart:** `"display_name": "Software"`.
- **evidence:** A — `discovery_call_01.txt` [02:31]: `"We want a dedicated software card —
  virtual — that lives with IT."` D — `slack_export_finance.txt` [2026-07-29 10:02]:
  `"whatever we set up needs to NOT let random ICs buy software"`. Neither packet names the
  programme; the name is chosen.
- **stated basis:** none given in either config or audit log.

## R-09 — Program-description sentence shape

- **packet:** A (closest), B, D
- **JSON path:** `out/client_a_acme_corp/ramp_config.json → spend_programs[0].description`
- **what is there:** `"All software and SaaS subscriptions on one virtual card held by IT.
  No software on personal cards. New vendors require Diane Marsh's approval regardless of
  amount — see approval_policies and audit log."`
- **the sample counterpart:** `"All software subscriptions, single virtual card held by
  Nora. New-vendor purchases follow the approval policy."` Same three-beat shape:
  *scope → single virtual card held by X → new-vendor approval pointer*.
- **evidence:** A's own quotes support each clause ([02:31], [03:02]). B
  `spend_programs[4].description` follows the same beats in Spanish-named form; D
  `spend_programs[0].description` follows the first two beats.
- **stated basis:** none given.

## R-10 — No customer-identifying literal from Westbrook reaches any packet

- **packet:** all five
- **JSON path:** `users[].email`, `users[].first_name`, `users[].last_name`, `entities[].name`
- **what is there:** A uses `@acme.example` and `kevin@orourketalent.example`, all traceable
  to `department_roster.csv`. B, C, D, E carry `"N/A"` for every address (5, 6, 6, 3 users
  respectively). No name in `out/` matches any name in the sample.
- **the sample counterpart:** `nora@westbrookdesign.example`, `priti@westbrookdesign.example`.
- **evidence:** verified by direct comparison of every `users[]` record against the sample's
  two records.
- **stated basis:** B `assumptions_made[2]`, C `assumptions_made[2]`, D `assumptions_made[2]`,
  E `assumptions_made[10]` — each states that no address appears in the packet and that
  `"N/A"` is recorded "rather than constructed".

---

# Dimension 2 — Structural idioms

## R-11 — `approval_policies[].source` carrying a verbatim quote

- **packet:** all five, every policy
- **JSON path:** `approval_policies[*].source` — A: [0], [1]; B: [0], [1], [2], [3];
  C: [0], [1], [2]; D: [0], [1]; E: [0]. Twelve policies, twelve `source` fields, none absent.
- **what is there:** every one carries `<filename> — <speaker (role)>, [<timestamp>]: "<quote>"`,
  several with an added translation or encoding note.
- **the sample counterpart:** `"source": "intake_email.txt — 'Anything over $1,000 needs
  Priti's approval.'"` — filename, em dash, single-quoted verbatim quote. The packets extend
  it with speaker, role, timestamp and double quotes.
- **evidence:** `source` is an *optional* field in `candidate/schemas/ramp_config_schema.json`
  (`approval_policies.items.required` is `["name","applies_to","tiers"]`). Its universal
  presence is a choice.
- **stated basis:** `SKILL.md:321` names this as an idiom to copy from the sample.

## R-12 — Tier list opening `{"threshold_usd_cents": 0, "approver": "AUTO"}`

- **packet:** A, B, C, D, E — seven of twelve policies
- **JSON path:**
  - A `approval_policies[0].tiers[0]` (Default spend approval)
  - B `approval_policies[0].tiers[0]`, `[1].tiers[0]`, `[2].tiers[0]`
  - C `approval_policies[0].tiers[0]` (single AUTO tier only), `[1].tiers[0]`
  - D `approval_policies[1].tiers[0]` (February proposal)
  - E `approval_policies[0].tiers[0]`
- **the sample counterpart:** `"tiers": [{"threshold_usd_cents": 0, "approver": "AUTO"}, {"threshold_usd_cents": 100000, "approver": "Priti (owner, priti@westbrookdesign.example)"}]`
- **evidence:** each is backed by a packet statement of an auto-approve band — A
  `"Anything under five hundred dollars, people should just be able to spend"` [01:56];
  B `"Hasta dos mil pesos, automático"` [04:11]; C `"Clinic managers' spend auto-approves
  within their limits"` [05:27]; E `"normal manager approvals over five hundred dollars"`
  [03:33] (the AUTO band is the implied complement); D's is inside a policy explicitly
  labelled "not encoded as active".
- **stated basis:** schema description of `threshold_usd_cents` — "0 = auto-approve tier".

## R-13 — Zero-threshold tier used for a rule that has no amount (extension beyond the sample)

- **packet:** A, B, C, D — five policies
- **JSON path:** A `approval_policies[1].tiers[0]` (`approver: "Diane Marsh (VP Finance, dmarsh@acme.example)"`);
  B `approval_policies[3].tiers[0]` (CFO); C `approval_policies[2].tiers[0]` (Gordon Pryce);
  D `approval_policies[0].tiers[0]` (Leo Novak)
- **what is there:** a first tier at threshold 0 whose approver is a **person, not AUTO** —
  used to express "regardless of amount" / "all travel" / "anything Millie's team flags".
- **the sample counterpart:** none. The sample's only zero-threshold tier is `AUTO`.
- **evidence:** each is accompanied in the same `source` string by a statement that the
  encoding is broader than the request, e.g. A: "…this catches ALL software spend, not just
  new vendors — see audit log."
- **stated basis:** as quoted; and in each packet's `unsupported_api_requests` (A[1], B[2],
  C[6], D[0]).

## R-14 — Omit-and-flag (rule absent from config, present in `assumptions_made`)

- **packet:** A, C, D, E (B: nothing to omit)
- **JSON path / disposition:**

  | packet | rule in packet | in config? | `assumptions_made` entry? | `missing_information_flags` entry? | `unsupported_api_requests` entry? |
  |---|---|---|---|---|---|
  | A | receipts > $75, memo > $500 | no | **yes** — `[5]`, `[6]` | no | yes — `[4]`, `[5]` |
  | C | REQ-6 receipts on every transaction | no | **no** | `[12]` asks about reimbursement, not receipts | yes — `[3]` |
  | D | none stated | no | **yes** — `[12]` ("No receipt or memo policy is configured, because the packet never mentions either") | `[8]` | no |
  | E | none stated | no | no | `[6]` | no |
  | B | none stated | no | no | `[9]` | no |

- **the sample counterpart:** the sample pairs the omission with an `assumptions_made` entry
  and nothing else: `assumptions_made[0]` = "Receipt threshold ($50) is an in-app policy
  setting, not part of this config's card objects." The sample has **no**
  `unsupported_api_requests` entry for the receipt rule.
- **evidence:** C's packet states the requirement twice and marks it mandatory —
  `security_requirements.doc` REQ-6: `"Receipts are required for every transaction regardless
  of amount."`; `discovery_call_apex.txt` [05:27]: `"receipts on everything. Every
  transaction, every amount."`
- **stated basis:** C `unsupported_api_requests[3].reason_unsupported`: "ENFORCED BY
  PLATFORM, configured outside this document… It is listed here so it is not lost between
  this document and go-live."

## R-15 — Name placeholders in `first_name` / `last_name`

- **packet:** C, D, E — see R-07 for strings.
- **JSON path:** C `users[5]`; D `users[5]`; E `users[2]` (both name fields).
- **the sample counterpart:** `users[0].last_name = "(surname pending roster)"`.
- **evidence / stated basis:** as R-07. Recorded here as a structural idiom because the
  placeholder is paired with a blocking `missing_information_flags` entry in C (`[2]`) and
  D (`[6]`), and with a blocking flag in E (`[1]`) — the sample's pairing (`assumptions`
  placeholder + `missing_information_flags[0]`, blocking true) is reproduced in all three.

## R-16 — Group limits stating cardinality in `notes`

- **packet:** all five — 22 limits
- **JSON path:** every `limits[*]` whose `assigned_to.group` is set:
  - A `limits[30]` — `"One per traveller (11 people: all of Sales, plus Marcus Webb, Diane Marsh and Tom Reyes)…"`
  - B `limits[0]`–`[9]` — `"One per Mexican driver. Operations has roughly forty people with spend and none are named in the packet, so the count is not yet known."` etc.
  - C `limits[0]`, `[4]`, `[5]` — `"One per clinic manager (14 assumed, one per clinic; none are named in the packet)."`
  - D `limits[0]`–`[2]` — `"One per engineering individual contributor (roughly 40; no roster available)."` (D `limits[3]`, `[4]` are group limits with **no** count: "No manager is named anywhere in this packet".)
  - E `limits[0]`–`[5]` — `"One per field rep - merchandising (58 people per the matrix)."`
- **the sample counterpart:** `"notes": "One per Studio member (9 people) once the roster arrives."`
- **evidence:** counts trace to the packets — A [04:05]; B [01:18] "unas cuarenta personas
  con gasto", "unas doce personas"; C [00:08] "Fourteen clinics"; D [2026-08-05 16:40]
  "roughly 40 eng / 22 GTM / 15 ops"; E `mcc_allowlist_matrix.csv` `Headcount` column.
- **stated basis:** `candidate/README.md` names "group limits" as one of the sample idioms
  to study.

## R-17 — Evidence-line shape in `unsupported_api_requests[].evidence`

- **packet:** all five — 50 entries total (A 11, B 11, C 11, D 7, E 10)
- **JSON path:** `unsupported_api_requests[*].evidence`
- **what is there:** every one follows *source, date-qualifier — finding[; nearest primitive
  is X]*. Two source forms recur: `"Ramp Developer API specification (snapshot dated
  2026-08-30) — …"` (50 occurrences across the five files) and `"support.ramp.com '<page>',
  checked 2026-08-30 — …"` (15 occurrences). One entry per packet carries the
  "nearest … primitive" clause: `"is_shareable with /funds/{id}/members is the nearest
  shared-pool primitive"` (A[3], B[5], C[4], D[2], E[2]).
- **the sample counterpart:** `"docs.ramp.com API reference, checked 2026-08-24 — no
  notifications resource; nearest primitive is POST /webhooks (transaction events)."`
- **evidence:** the sample's own source name (`docs.ramp.com API reference`) does not appear
  in `out/`; the date `2026-08-24` does not appear in `out/`.
- **stated basis:** `candidate/README.md` — "cite the date and source you checked in your
  audit-log `evidence` fields (the sample packet shows the shape)."

## R-18 — `proposed_manual_workaround` naming a route rather than refusing

- **packet:** all five, all 50 entries
- **JSON path:** `unsupported_api_requests[*].proposed_manual_workaround`
- **what is there:** none of the 50 is a bare refusal; each names an in-app path, a
  compensating control, or a person who must act. **Twelve** distinct workaround strings are
  byte-identical across two or more packets, accounting for 39 of the 50 entries:
  approval-chain A[0] B[1] C[6] D[0] E[7]; group-limit A[3] B[5] C[4] D[2] E[2];
  physical-card A[8] B[7] C[5] D[4] E[4]; program-immutability A[9] B[9] C[9] D[5] E[8];
  role-mapping A[10] B[10] C[10] D[6] E[9]; bulk-user B[8] C[7] D[3] E[3];
  reporting-line visibility A[6] B[3] E[5]; new-vendor approval A[1] B[2];
  receipt policy A[4] C[3]; guest deactivation A[7] C[8]; merchant block B[6] C[0];
  Slack/notifications D[1] E[6] — see R-04.
- **the sample counterpart:** `"Ramp's in-app Slack integration may cover this (deployment
  owner to enable); otherwise a webhook consumer that posts to #spend."`
- **evidence:** `references/AUDIT_PATTERNS.md:469` — "Also worth copying: the sample's
  `unsupported_api_requests` proposes a *route to the [outcome]*…"
- **stated basis:** as quoted.

## R-19 — `conflicts` array sizes

- **packet:** all five
- **JSON path:** `audit_log.json → conflicts`
- **what is there:** A 5, B 3, C 3, D 5, E **1**. No packet emits `conflicts: []`.
- **the sample counterpart:** `"conflicts": []`.
- **evidence, packet by packet, for how messy the packet is:**
  - **E — 1 conflict.** The single conflict is the 150-vs-131 headcount. Not recorded as
    conflicts: the matrix's `Card_Type` column says `Virtual` for Trainer while the same row
    permits MCC 7011 (lodging) and 3000-3299 (airlines); `onboarding_call_vanguard.txt`
    [00:27] says field reps buy "occasionally a hotel if a job runs long" while the Seasonal
    row says "NO meals NO hotels"; [03:21] Carol says the field gets no approvals while
    [03:33] Ahmed describes HQ approvals — the config carries an HQ policy but no HQ users.
    The audit log treats the last as `missing_information_flags[5]`, not a conflict.
  - **B — 3 conflicts** across two documents in three languages, one of which
    (`politica_gastos_2026.txt` line 5) states of itself: `"Las secciones no están
    totalmente armonizadas entre sí."` The third conflict entry is an explicit "no conflict
    found" record against that warning.
  - **C — 3 conflicts** across a call and a mandatory compliance document.
  - **A — 5**, **D — 5**.
- **stated basis:** `references/AUDIT_PATTERNS.md:463` — "`conflicts: []` is legitimate.
  Westbrook's packet is one email from one author, so nothing disagrees with anything."

## R-20 — Sample's explicit-null habit not reproduced

- **packet:** all five
- **JSON path:** sample `spend_programs[0].spending_restrictions` carries
  `"transaction_amount_limit_cents": null` and `"lock_date": null` explicitly.
- **what is there:** no packet emits an explicit `null` inside `spending_restrictions`. The
  `null` values that do appear are `users[].direct_manager_email` only (A 2, B 5, C 1, D 6,
  E 3). Absent fields are simply omitted.
- **the sample counterpart:** as above.
- **evidence:** the schema makes both fields optional, so both forms validate.
- **stated basis:** none given.

## R-21 — `"N/A"` used as a sentinel in fields the sample fills with real or null values

- **packet:** B, C, D, E
- **JSON path:** `users[].email` (B ×5, C ×6, D ×6, E ×3);
  `out/client_c_apex_health/ramp_config.json → limits[1].assigned_to.user_email`, `limits[2]`,
  `limits[3]` (all `"N/A"`); `out/client_c_apex_health/ramp_config.json → users[1..5].direct_manager_email` (five users carry the string `"N/A"`, not `null`).
- **what is there:** a non-address string in an address field, in three different roles.
- **the sample counterpart:** the sample carries real addresses in `email` and
  `assigned_to.user_email`, and `null` in `direct_manager_email` for the one user with no
  manager (`users[0].direct_manager_email: null`).
- **evidence:** the schema says of `direct_manager_email`: `"null if unknown — and if
  unknown, say so in the audit log"`. C is the only packet that uses the string `"N/A"`
  there; A, B, D and E all use `null`.
- **stated basis:** B `assumptions_made[2]`, C `assumptions_made[2]`, D `assumptions_made[2]`,
  E `assumptions_made[10]` each justify `"N/A"` for **`email`** ("rather than constructed
  from a pattern"). No entry in any packet addresses `"N/A"` in `direct_manager_email` or in
  `assigned_to.user_email`.

---

# Dimension 3 — Reasoning inheritance

Every configured value the packet does not state, and what filled the gap. Entries marked
**[checked clean]** are recorded because the reader needs to see what was examined, not only
what stood out.

## 3.1 `permitted_spend_types.reimbursements_enabled` — every programme, all five packets

Full inventory (24 programmes):

| packet | program | reimb | packet mentions reimbursement? |
|---|---|---|---|
| A | `spend_programs[0]` Software | **false** | yes |
| A | `spend_programs[1]` Travel | **true** | yes |
| B | `[0]` Combustible MX choferes | true | yes |
| B | `[1]` Combustible/mant. supervisores | true | yes |
| B | `[2]` Viajes MX Comercial | true | yes |
| B | `[3]` Oficina MX Administración | true | yes |
| B | `[4]` **Software centralizado** | **false** | yes (but not about software) |
| B | `[5]` Combustível BR motoristas | true | yes |
| B | `[6]` Viagens BR Comercial | true | yes |
| B | `[7]` Escritório Brasil | true | yes |
| B | `[8]` Miami travel | true | yes |
| B | `[9]` Miami office | true | yes |
| C | `[0]`–`[3]` all four | **false ×4** | **no** |
| D | `[0]` Software | **false** | yes (contractors, jj's dinners) |
| D | `[1]` November Offsite | **false** | yes |
| E | `[0]`–`[5]` all six | **false ×6** | yes |

### R-22 — Packet A: Software false / Travel true

- **JSON path:** `out/client_a_acme_corp/ramp_config.json → spend_programs[0].permitted_spend_types.reimbursements_enabled` (false), `spend_programs[1]…` (true)
- **evidence:** `discovery_call_01.txt` [02:31], Diane Marsh: `"Nobody buys software on a
  personal card, period."` — a card-only rule stated for software specifically. [06:48]:
  `"We want to basically kill reimbursements. Card-first culture. Keep reimbursements on for
  edge cases — mileage, the occasional personal-card emergency"` — company-wide, not
  travel-specific. The packet never says anything about reimbursement on the travel programme.
- **the sample counterpart:** `spend_programs[0].permitted_spend_types.reimbursements_enabled: false` on Westbrook's software programme.
- **stated basis:** `audit_log.json → conflicts[3].provisional_resolution` — "Reimbursements
  remain enabled company-wide and are disabled on the Software programme, where a card-only
  rule was explicit."

### R-23 — Packet B: nine programmes true, `Software centralizado` false, with no entry explaining the exception

- **JSON path:** `out/client_b_logistica_globex/ramp_config.json → spend_programs[4].permitted_spend_types.reimbursements_enabled` = `false`; `spend_programs[0..3,5..9]` = `true`
- **what is there:** one programme out of ten differs, silently.
- **the sample counterpart:** `false` on Westbrook's single (software) programme.
- **evidence:** packet B on software says only `politica_gastos_2026.txt` §2.5:
  `"Software (centralizado, Sistemas): $25,000 MXN mensuales, tarjeta única virtual."` and
  `entrevista_descubrimiento_es.txt` [03:45]: `"una sola tarjeta virtual para todo el
  software, la maneja sistemas"`. Neither says card-only or mentions reimbursement. The only
  reimbursement statements in packet B are §2.6 (`"Los reembolsos en efectivo quedan
  ELIMINADOS a partir del Q4 2026"`), R. Ortega's inline note (`"Mantener reembolsos para
  hoteles/alimentos en ruta"`), and [05:45] (`"El memo es aspiracional en esa parte"`).
- **stated basis:** `audit_log.json → assumptions_made[10]` states, without qualification,
  `"Reimbursements remain enabled."` — the config's one `false` is not mentioned there or
  anywhere else in B's audit log (grep for "reimburse" in B's audit log returns lines 55–57
  and 128–131 only, all about the company-wide question). `spend_programs[4].description`
  does not mention reimbursement either.
- **traceability:** `work/client_b_logistica_globex/traceability.json` maps no requirement to
  `spend_programs[4].permitted_spend_types`; `work/.../requirements.json` has no requirement
  whose `source_quote` concerns reimbursement on the software card.

### R-24 — Packet C: false on all four, packet silent, mileage named

- **JSON path:** `out/client_c_apex_health/ramp_config.json → spend_programs[0..3].permitted_spend_types.reimbursements_enabled`
- **the sample counterpart:** `false`.
- **evidence:** the words *reimbursement*, *expense claim*, *expense report*, *out of pocket*
  appear nowhere in `discovery_call_apex.txt` or `security_requirements.doc` — verified by
  grep. The one adjacent statement is [04:33], Millie Vance, on nurses: `"They need cards for
  assignment expenses — lodging near the clinic, meals, mileage."` `mcc_controls[6].translation_notes`
  records: `"Mileage was mentioned as an expense type but is a reimbursement rather than a
  card category."`
- **stated basis:** `audit_log.json → assumptions_made[12]` — "No programme permits
  reimbursements. The words reimbursement and expense claim appear nowhere in this packet, so
  card spend is the only route enabled… An earlier draft enabled reimbursements on three
  programmes by inference; that was withdrawn, because enabling a spend route nobody asked
  for is not recoverable the way a missing one is." Paired with
  `missing_information_flags[12]`.

### R-25 — Packet D: false on both, one justified, one not

- **JSON path:** `out/client_d_hypergrowth/ramp_config.json → spend_programs[0]` (Software, false), `spend_programs[1]` (November Offsite, false)
- **evidence:** packet D mentions reimbursement three times, none about the software card:
  `fragmented_notes_feb2026.md` — `"contractors (the 3 offshore QA folks): DO NOT give them
  cards. reimburse via invoice like now."`; `"per diem vs actuals for meals — rachel to
  propose something"`; `slack_export_finance.txt` [2026-07-29 09:44], jj: `"can we finally
  kill the thing where I pay for prospect dinners personally and expense it 45 days later"`.
- **stated basis:** `assumptions_made[13]` covers the offsite programme only:
  "…reimbursements are switched off on the offsite programme because the packet never asks
  for reimbursements". `missing_information_flags[13]` likewise names only the offsite
  programme. **No entry addresses `spend_programs[0]` (Software).** Separately,
  `assumptions_made[9].impact_if_wrong` asserts `"Reimbursements remain enabled company-wide
  so invoice reimbursement is unaffected."` while both programmes in the config carry `false`
  and the schema has no company-wide reimbursement field.

### R-26 — Packet E: false on all six, with a stated basis

- **JSON path:** `out/client_e_vanguard_retail/ramp_config.json → spend_programs[0..5]`
- **evidence:** `onboarding_call_vanguard.txt` [00:27], Carol Jimenez: `"Today it's per diems
  and reimbursements and it's a mess: reps front money, finance drowns in receipts… We want
  every rep on a card"`; `mcc_allowlist_matrix.csv` row 7: `"per diem stays in payroll for
  them"`.
- **stated basis:** `audit_log.json → assumptions_made[9]` — "Reimbursements are not enabled
  on any field programme. The stated goal is to move reps off fronting money, and seasonal
  per diems remain in payroll." `impact_if_wrong` names the risk and says it "should be
  confirmed before the October wave."

## 3.2 `issue_physical_card_if_needed`

Full inventory (24 programmes): A false/true; B true,true,true,false,false,true,true,false,true,false; C false,true,true,false; D false,false; E false×4, true, false.

### R-27 — Packet A [checked clean]

- **JSON path:** `spend_programs[0].issue_physical_card_if_needed` false, `[1]` true
- **evidence:** `discovery_call_01.txt` [02:31] `"a dedicated software card — virtual"`;
  [04:21] `"Physical for travelers… physical for everyone in Sales anyway"`.
- **stated basis:** stated in the packet; `unsupported_api_requests[8]` carries the
  shipping-address gap; `missing_information_flags[4]` raises it as blocking.

### R-28 — Packet B: physical inferred on five of ten programmes

- **JSON path:** `spend_programs[0]` true, `[1]` true, `[2]` true, `[3]` false, `[4]` false,
  `[5]` true, `[6]` true, `[7]` false, `[8]` true, `[9]` false
- **what the packet states:** [03:16] `"Tarjeta física para todos los de Comercial"` → covers
  `[2]` only. [03:16] `"Administración… tarjeta virtual"` → `[3]`. §2.5 / [03:45] `"tarjeta
  única virtual"` → `[4]`. **Nothing** in either document states a card format for the
  Mexican fuel programmes (`[0]`, `[1]`), any Brazilian programme (`[5]`, `[6]`, `[7]`) or
  either Miami programme (`[8]`, `[9]`). [01:43] says only `"Queremos tarjeta por chofer"`.
- **the sample counterpart:** `"issue_physical_card_if_needed": false` on the sample's one
  virtual programme.
- **stated basis:** none given. No `assumptions_made` entry in B addresses card format; the
  only related entry is `unsupported_api_requests[7]`, which speaks of "physical cards for the
  whole commercial team". `traceability.json` leaves `spend_programs[1]`, `[6]`, `[7]`
  uncovered entirely.

### R-29 — Packet C: physical true on two of four, packet silent on format

- **JSON path:** `spend_programs[0]` false (Clinic Supplies), `[1]` **true** (Regional
  Travel), `[2]` **true** (Facilities), `[3]` false (Contract Nursing)
- **what the packet states:** the only mention of card format is `security_requirements.doc`
  REQ-2 — `"Physical cards with a monthly limit exceeding $10,000 USD must remain incapable
  of transacting…"` — a conditional gate, not an issuance instruction; and
  `discovery_call_apex.txt` [03:30], Gordon Pryce: `"Maybe just Bruno's if we raise it for a
  big project, and the regional directors if travel spikes."` — which names Bruno and the
  regional directors as the people who *might* one day exceed $10,000. Those are exactly the
  two programmes set to `true`.
- **the sample counterpart:** `false` (the sample's programme is virtual).
- **stated basis:** none given. C's `missing_information_flags[11]` asks: `"Which cardholders
  need physical cards rather than virtual ones, and what are the shipping addresses?"` —
  i.e. the question is flagged as open while the config has already answered it four times.
  `traceability.json` leaves all four `issue_physical_card_if_needed` paths uncovered.

### R-30 — Packet D: false on both, packet entirely silent

- **JSON path:** `spend_programs[0]`, `[1]` both false
- **evidence:** the words *physical*, *virtual*, *wallet*, *card format* appear nowhere in
  `slack_export_finance.txt` or `fragmented_notes_feb2026.md`.
- **the sample counterpart:** `false`.
- **stated basis:** none given for the setting. `missing_information_flags[9]` records
  `"Which cardholders need physical cards rather than virtual ones… Card format is never
  discussed in this packet."`

### R-31 — Packet E [checked clean]

- **JSON path:** `spend_programs[0..3]` false, `[4]` true, `[5]` false
- **evidence:** `mcc_allowlist_matrix.csv` `Card_Type` column: `Virtual` on rows 2–5 and 7,
  `Physical` on row 6 (District Manager). Corroborated by [02:49]: `"Virtual, in the phone
  wallet… Physical only for district managers."`
- **stated basis:** stated in the packet; every value matches the column.

## 3.3 Role assignments

### R-32 — Packet A: three admin-class roles quoted, 27 users defaulted

- **JSON path:** `out/client_a_acme_corp/ramp_config.json → users[*].role`
- **traceable to a statement naming that person:** `users[1]` Diane Marsh BUSINESS_ADMIN and
  `users[2]` Priya Shetty BUSINESS_ADMIN — [05:41] `"Priya and me."`; `users[6]` Sana Qureshi
  IT_ADMIN — [05:41] `"probably Sana in IT for the user-management side"` + [05:52]
  `"Sana should not be able to change spend limits though."`; `users[5]` Kevin O'Rourke
  GUEST_USER — [04:52] `"Whatever the most locked-down thing you can give him is."`
- **not traceable to a per-person statement:** `users[0]` Marcus Webb BUSINESS_USER and the
  other 26 users, all BUSINESS_USER by default. `work/client_a_acme_corp/traceability.json`
  covers no `users[i].role` path for any of them.
- **the sample counterpart:** Westbrook maps its owner (Priti) to BUSINESS_ADMIN on the basis
  of `"our owner Priti"`.
- **stated basis:** `assumptions_made[1]` for Marcus Webb — "the administrators named on the
  call were Diane Marsh and Priya Shetty… An earlier draft granted that by default on the
  basis of the job title; it was withdrawn". No entry addresses the 26 BUSINESS_USER
  defaults; `unsupported_api_requests[10]` covers role mapping generically.

### R-33 — Packet B: three BUSINESS_ADMIN grants, two quoted, one flagged as broader than asked

- **JSON path:** `users[0]` Alejandra Vidal BUSINESS_ADMIN, `users[1]` Joaquín Esparza
  BUSINESS_ADMIN, `users[3]` Elena Ruiz BUSINESS_ADMIN, `users[2]` Rubén Ortega BUSINESS_USER,
  `users[4]` Thiago Moreira BUSINESS_USER
- **evidence:** [04:37] `"Yo y Joaquín, mi gerente de contabilidad."` covers `users[0]`,
  `[1]`. `"en cada país va a haber un administrador local cuando arranquen — en Miami ya
  sabemos que es Elena Ruiz"` covers `users[3]`, with the scope caveat.
  `users[2]` Rubén Ortega BUSINESS_USER — the packet never states a role for him;
  `traceability.json` leaves `users[2].role` uncovered.
- **the sample counterpart:** Nora Bailey BUSINESS_ADMIN on the strength of `"Ops (me…)"`
  and holding the software card.
- **stated basis:** `assumptions_made[7]` for Elena Ruiz — "Elena Ruiz is given the Business
  Admin role, which is company-wide. The request was for an administrator scoped to Miami."
  `users[2].notes`: "Operations director. Not named as an administrator." No entry states why
  BUSINESS_USER rather than a manager-class role.

### R-34 — Packet C: two BUSINESS_ADMIN, one AUDITOR, all quoted; GUEST_USER referenced but not emitted

- **JSON path:** `users[0]` Gordon Pryce BUSINESS_ADMIN, `users[1]` Dana Whitfield
  BUSINESS_ADMIN, `users[2]` Millie Vance AUDITOR, `users[3..5]` BUSINESS_USER
- **evidence:** [05:51] `"Our controller, Dana Whitfield, plus me."` covers `users[0]`, `[1]`.
  [05:58] `"Auditor-style access, no spend capability, no admin capability."` + REQ-5 cover
  `users[2]`.
- **observation:** `assumptions_made[5]` states `"Traveling nurses are assigned the Guest User
  role as contract clinical staff"` and `unsupported_api_requests[8]` discusses Guest User
  deactivation — but **no `users[]` record in C's config carries GUEST_USER**, and no nurse
  user record exists at all; the nurses appear only as `limits[5].assigned_to.group =
  "Contract Nurses"`.
- **the sample counterpart:** none — the sample has no auditor, contractor or guest.
- **stated basis:** `assumptions_made[1]` (AUDITOR / REQ-5), `assumptions_made[5]` (nurses).

### R-35 — Packet D: two BUSINESS_ADMIN, one IT_ADMIN, all quoted; CEO defaulted down with a stated reason

- **JSON path:** `users[1]` Rachel Kim BUSINESS_ADMIN, `users[2]` Maya Osei BUSINESS_ADMIN,
  `users[4]` Stan Pollard IT_ADMIN, `users[0]` Leo Novak BUSINESS_USER, `users[3]` Dev Batra
  BUSINESS_USER, `users[5]` jj BUSINESS_USER
- **evidence:** [2026-08-04 10:12] `"admin setup: me and maya as admins. stan does user
  onboarding/offboarding ONLY — he should not be able to touch limits"`;
  [2026-08-04 10:16] `"because leo will ask you to change things and i'd rather you do it
  than him."`
- **the sample counterpart:** the owner→BUSINESS_ADMIN mapping.
- **stated basis:** `assumptions_made[13]` for Leo Novak; `users[0].notes` names the reason.
  `users[3].role` (Dev Batra) is uncovered by `traceability.json` and has no entry.
- **cross-reference:** `references/CAPABILITY_LEDGER.md:1186` records this as the fixed error
  — "Do NOT infer it from the job title: Acme Corp's CEO and Hypergrowth Inc.'s CEO were both
  excluded from the stated administrator list".

### R-36 — Packet E: BUSINESS_ADMIN granted to a person the packet does not name

- **JSON path:** `out/client_e_vanguard_retail/ramp_config.json → users[2]` —
  `{"email": "N/A", "first_name": "(first name not stated)", "last_name": "(surname not
  stated)", "role": "BUSINESS_ADMIN", "department": "Finance"}`
- **what is there:** a full administrator grant attached to a record with no name and no
  address.
- **the sample counterpart:** the sample's placeholder user (`Priti`,
  `"(surname pending roster)"`) is *also* BUSINESS_ADMIN — the same pairing of an incomplete
  identity with an administrator role.
- **evidence:** `onboarding_call_vanguard.txt` [03:42], Ahmed Nasser: `"Me and our
  controller."` The controller is named by office, never by name, anywhere in packet E.
- **stated basis:** `users[2].notes` — "Controller, named as the second account administrator
  by role only — the person is not named in this packet."
  `missing_information_flags[1]` (blocking): "Who is the controller named as the second
  administrator?" No `assumptions_made` entry covers the role grant itself.
  `users[0]` Carol Jimenez BUSINESS_USER is uncovered by `traceability.json`; her
  `notes` say "VP Field Operations. Not named as an account administrator."

## 3.4 Receipt and memo policy

### R-37 — Omission and its pairing, all five packets

- **JSON path:** no packet's `ramp_config.json` contains any receipt or memo field (the
  schema has none).
- See the table in **R-14** for the per-packet disposition. The gap surfaced there:
  packet C, whose packet states the requirement twice and marks it MANDATORY, has **no
  `assumptions_made` entry** for the omission — the sample's pairing is receipts-omitted +
  `assumptions_made` entry. C records it in `unsupported_api_requests[3]` instead.
- **the sample counterpart:** `assumptions_made[0]`, quoted in R-05.
- **stated basis:** C `unsupported_api_requests[3].reason_unsupported`, quoted in R-14.

## 3.5 Department names

### R-38 — Packet A [checked clean]

- **JSON path:** `departments[0..4]` = Engineering, Sales, Marketing, G&A, IT
- **evidence:** `discovery_call_01.txt` [00:47] names Engineering, Sales, Marketing, G&A
  verbatim; `department_roster.csv` row 8 supplies IT.
- **stated basis:** `assumptions_made[8]` (IT as a fifth department) and `conflicts[2]`.

### R-39 — Packet B: `Sistemas` created as a top-level department the packet places inside Administración

- **JSON path:** `out/client_b_logistica_globex/ramp_config.json → departments[3]` = `{"name": "Sistemas"}`
- **what is there:** a fourth department alongside Operaciones, Administración and Comercial.
- **the sample counterpart:** the sample creates exactly the two departments the email names
  ("two teams for spend purposes: Studio… and Ops").
- **evidence:** `entrevista_descubrimiento_es.txt` [01:18], Rubén Ortega: `"Tres áreas
  grandes. Operaciones — choferes, supervisores de patio, coordinadores de ruta. Es el
  grueso… Luego Administración — finanzas, recursos humanos, sistemas. Y Comercial — ventas
  y atención a clientes"` — *sistemas* is named as a component **of Administración**. The
  only other mention is [03:45]: `"la maneja sistemas"`, and §2.5 `"Software (centralizado,
  Sistemas)"`.
- **cross-reference:** `work/client_b_logistica_globex/requirements.json → REQ-007` records
  the claim as `"Three Mexican areas: Operaciones, Administración and Comercial"` with the
  quote above. No requirement asserts a Sistemas department.
  `work/client_b_logistica_globex/traceability.json` leaves `departments[3]` uncovered.
- **stated basis:** none given. B's `assumptions_made[5]` addresses only whether departments
  are shared across entities. `limits[4].assigned_to.group` is `"Sistemas (México)"`.

### R-40 — Packet C: three of six department names constructed

- **JSON path:** `departments[0]` Clinics, `[1]` Central Finance, `[2]` Procurement,
  `[3]` Facilities, `[4]` Compliance, `[5]` Regional Operations
- **what the packet says:** `discovery_call_apex.txt` [00:08], Gordon Pryce: `"each clinic has
  a clinic manager who buys supplies, and then there's a small central team — finance,
  procurement, facilities, and Millie's compliance group."` That yields *finance*,
  *procurement*, *facilities*, *compliance*. **`Clinics`**, **`Central Finance`** and
  **`Regional Operations`** are constructed labels; the last has no antecedent phrase at all
  beyond the job title `"Regional Operations Director"` ([00:32]).
- **the sample counterpart:** none — Westbrook's names are lifted verbatim from its email.
- **stated basis:** none given. C's `assumptions_made` has no department-naming entry.
  `traceability.json` maps `departments[0..4]` to REQ-002 as a block; `departments[5]`
  (Regional Operations) is uncovered.

### R-41 — Packet D [checked clean]

- **JSON path:** `departments[0..3]` = Eng, GTM, Ops, Exec
- **evidence:** `slack_export_finance.txt` [2026-07-29 09:20], Rachel Kim: `"keep it simple:
  Eng, GTM, Ops, Exec. that's it."` — verbatim, including the abbreviations.
- **stated basis:** `requirements.json → REQ-001`.

### R-42 — Packet E: all three department names constructed

- **JSON path:** `departments[0]` Field Operations, `[1]` Finance, `[2]` HQ
- **what the packet says:** the only literal is `HQ` (`onboarding_call_vanguard.txt` [03:33]:
  `"HQ is different… HQ is twenty people and boring."`). `Field Operations` is Carol
  Jimenez's job title (`VP Field Operations`); `Finance` is a fragment of Ahmed Nasser's
  (`Finance Systems Manager`). The matrix's six role names are used as spend-programme and
  group names, not as departments.
- **the sample counterpart:** none.
- **stated basis:** none given. `traceability.json` leaves `departments[0]`, `[1]`, `[2]` all
  uncovered.

## 3.6 `base_currency`, `entities[].status`, `generated_at`, `locations`

### R-43 — `base_currency` = `"USD"` in all five configs

- **JSON path:** `<packet>/ramp_config.json → base_currency`
- **the sample counterpart:** `"base_currency": "USD"`.
- **evidence:** A, C, D, E are single-entity US companies and the field is uncontroversial —
  none of the four packets states a base currency. **B** is the case where the packet speaks:
  `entities[0]` is `{"name": "Logística Globex, S.A. de C.V.", "country": "MX", "currency":
  "MXN"}` and `entrevista_descubrimiento_es.txt` [02:27]: `"todo el gasto de México se maneja
  en pesos… Los límites, los reportes, todo en moneda local."` The countervailing statement
  is [02:50] `"Para consolidar, mi equipo y yo vemos todo en dólares"` and
  `politica_gastos_2026.txt` §5.1 `"La consolidación ejecutiva se realiza en USD."`
- **stated basis:** B `assumptions_made[0]` and `[1]` discuss FX for approval thresholds and
  state that limits are not converted; neither mentions `base_currency` itself.
  `traceability.json` leaves `base_currency` uncovered in A, C, D, E (B's is covered via the
  consolidation requirement).

### R-44 — `entities[].status` = `"existing"` by default

- **JSON path:** A `entities[0].status`, C `[0]`, D `[0]`, E `[0]` — all `"existing"`.
  B `entities[0]`, `[1]` `"existing"`, `entities[2]` (Brazil) `"requested"`.
- **the sample counterpart:** `{"name": "Westbrook Design Studio LLC", "country": "US",
  "currency": "USD", "status": "existing"}` — and the sample's email never names a legal
  entity or its status either.
- **evidence:** none of A, C, D, E states whether the customer already exists in a Ramp
  instance. B states it: [00:42] `"Miami sí — Globex Logistics USA LLC, ya está constituida…
  São Paulo está en proceso."`
- **stated basis:** A `assumptions_made[16]` — "Acme Corp operates as a single existing US
  entity. The packet names no legal entity and does not discuss more than one." No equivalent
  entry in C, D or E. `traceability.json` leaves `entities[0].status` uncovered in A, D, E.

### R-45 — `generated_at` convention

- **JSON path:** A `2026-08-30T00:00:00Z`, B `2026-08-31T00:00:00Z`, C `2026-08-30T00:00:00Z`,
  D `2026-08-31T00:00:00Z`, E `2026-08-31T00:00:00Z`
- **the sample counterpart:** `"generated_at": "2026-08-24T00:00:00Z"` — a date at midnight
  Z, matching the sample audit log's `"checked 2026-08-24"`.
- **evidence:** no packet states a generation date. All five follow the sample's
  midnight-Z form. In A and C the date matches the audit-log check date (`snapshot dated
  2026-08-30`, `checked 2026-08-30`); in B, D and E `generated_at` is 2026-08-31 while every
  evidence line still reads `snapshot dated 2026-08-30` / `checked 2026-08-30`.
- **stated basis:** none given in any packet. `traceability.json` leaves `generated_at`
  uncovered in all five.

### R-46 — `locations`

- **JSON path:** only `out/client_b_logistica_globex/ramp_config.json → locations[0..2]`
  (Monterrey/MX, Miami/US, São Paulo/BR) and `users[*].location`. A, C, D, E emit no
  `locations` array and no `users[].location`.
- **the sample counterpart:** the sample emits no `locations` array either (the field is
  optional).
- **evidence:** C's packet describes `"Fourteen clinics across three states"` [00:08] and
  C's own `missing_information_flags[7]` (blocking) asks `"What are the names of the fourteen
  clinics and which state is each in?"` — so C has a stated geography and no locations.
  E's packet describes `"across thirty states"` and six districts; E emits no locations and
  its `missing_information_flags[0]` asks for the spreadsheet containing districts.
- **stated basis:** B `assumptions_made[6]` explains why locations carry no entity binding.
  No entry in C or E explains the absence of `locations`.

## 3.7 Other silence-filled values

### R-47 — `lock_date`

- **JSON path:** D `spend_programs[1].spending_restrictions.lock_date` = `"2026-12-01"` and
  `limits[5]…lock_date` = same; E `spend_programs[5]…lock_date` = `"2026-12-24"` and
  `limits[5]…lock_date` = same. C sets **no** lock date on `Contract Nursing` despite REQ-4.
- **the sample counterpart:** `"lock_date": null` on the sample's programme.
- **evidence:** D — [2026-07-31 14:31] `"can ramp do a 'this money stops existing on dec 1'
  thing"`. E — [02:07] `"ending December 24th… the cards must stop working December 24th"`
  and matrix row 7 `"Cards must hard-stop Dec 24"`. C — REQ-4 requires expiry on the
  assignment end date; no end dates exist in the packet.
- **stated basis:** C `limits[5].notes` — "No end dates are supplied in the packet, so no lock
  date is set here."; `missing_information_flags[3]` (blocking). D `assumptions_made[7]`.
  E `assumptions_made[7]`.

### R-48 — `primary_card_enabled` = `true` on all 24 programmes [checked clean]

- **JSON path:** every `spend_programs[*].permitted_spend_types.primary_card_enabled`
- **the sample counterpart:** `true`.
- **evidence:** every programme in every packet exists because the packet asked for cards; no
  packet describes a reimbursement-only programme.
- **stated basis:** none given anywhere; not flagged in any audit log.

### R-49 — Allowed-category selections where the packet named a category-shaped thing but not a Ramp category [checked clean]

- **JSON path:** A `spend_programs[1]…allowed_categories`; B `[0]`,`[2]`,`[4]`,`[5]`;
  C `[0]`,`[1]`,`[3]`; D `[0]`; E `[0]`–`[5]`
- **evidence:** every one is accompanied by an `mcc_controls[*].translation_notes` naming the
  Ramp category, its integer code where known, and what is lost. Exclusions are stated
  explicitly and repeated as questions: A `"Car rental (5) was not named and is excluded"` +
  `missing_information_flags[8]`; D `"Cloud computing (41) is deliberately NOT included"` +
  `missing_information_flags[12]`, with `assumptions_made[13]` recording that an earlier draft
  added it and it was withdrawn.
- **the sample counterpart:** `mcc_controls[0].translation_notes` — "Email says 'shouldn't
  work for anything that isn't software' — expressed as a category allowlist on the program."
- **stated basis:** as quoted.

### R-50 — `assigned_to.group` names that are not departments

- **JSON path:** A `limits[30].assigned_to.group` = `"Travelers"`; C `limits[0]` =
  `"Clinic Managers"`, `limits[5]` = `"Contract Nurses"`; D `limits[3]` = `"GTM Managers"`,
  `limits[4]` = `"Ops Managers"`, `limits[5]` = `"Offsite Organisers"`; B `limits[0..9]` use
  compound names such as `"Operaciones — choferes (México)"`; E uses the matrix role names.
- **what is there:** cohorts invented to carry a limit, none of which appears in
  `departments[]`.
- **the sample counterpart:** `"assigned_to": {"group": "Studio"}` — the sample's group **is**
  one of its two departments.
- **evidence:** the schema permits it: `group` is described as "a department name or a named
  cohort, e.g. 'Field Reps'". Cohort membership is stated in `notes` in every case
  (see R-16), except D `limits[5]` `"Offsite Organisers"`, whose note says "the packet does
  not say whether the budget sits with one person or is shared, so the holder is unresolved."
- **stated basis:** D `missing_information_flags[7]`; A `assumptions_made[15]`;
  C `assumptions_made[4]`, `[11]`.

### R-51 — Approval-policy `applies_to` values

- **JSON path:** A `[0]` `"all"`, `[1]` `"Software"`; B `[0]`
  `"Logística Globex, S.A. de C.V. (México)"`, `[1]`, `[2]` similar entity strings, `[3]`
  `"Software centralizado"`; C `[0]` `"Clinic Supplies"`, `[1]` `"Central Finance"`,
  `[2]` `"all"`; D `[0]`, `[1]` both `"all"`; E `[0]` `"HQ"`
- **the sample counterpart:** `"applies_to": "all"`.
- **evidence:** the schema says `applies_to` is "a department, spend program, or 'all'".
  B's three entity-scoped values are none of those three; C's `"Central Finance"` is a
  department; D `approval_policies[0]` is scoped `"all"` although the underlying rule
  (`"ALL travel needs my direct approval"`) is travel-only and D has no travel programme.
- **stated basis:** D `approval_policies[0].source` records the encoding note and marks the
  policy `PROVISIONAL`; `conflicts[0]` and `missing_information_flags[1]` carry it.
  B's entity-scoped strings have no entry explaining the departure from the enumerated forms.

### R-52 — Per-user limits in A vs group limits everywhere else [checked clean]

- **JSON path:** A emits 30 individual `limits[]` with `assigned_to.user_email`; B, C, D, E
  emit almost entirely group limits (C has three individual limits, all with
  `user_email: "N/A"` — see R-21).
- **the sample counterpart:** the sample does both: one group limit (`Studio`) and one
  individual (`priti@…`).
- **evidence:** A is the only packet with a roster (`department_roster.csv`), which supplies
  a per-person `Target_Limit_USD_Monthly`.
- **stated basis:** `discovery_call_01.txt` [04:31], Priya Shetty: `"On the roster I marked
  target monthly limits per person… Where the roster and anything I say today disagree, the
  roster wins."`

---

# Dimension 4 — Value provenance

Method: `money_map.py --packet <p> --json` per packet, joined against every
`limit_amount_cents`, `transaction_amount_limit_cents` and non-zero `threshold_usd_cents` in
that packet's config, matching on both amount **and** currency. 108 config figures checked
(A 35, B 26, C 13, D 9, E 25).

## R-53 — Packet A: 35 of 35 figures trace to packet A

- **JSON path:** `spend_programs[0..1]`, `limits[0..30]`, `approval_policies[0].tiers[1..2]`
- **result:** all 35 return an exact amount+currency match in `department_roster.csv` or
  `discovery_call_01.txt`. Spelled-out forms resolved by money_map: `"Fifty grand"` →
  5,000,000¢ (`limits[0]`), `"five hundred"` → 50,000¢, `"five thousand"` → 500,000¢
  (`approval_policies[0].tiers[1..2]`), `"eight thousand… cap it at ten"` → 1,000,000¢
  (`spend_programs[0]`), `"two thousand"` → 200,000¢ (`spend_programs[1]`).
- **stated basis for the one interpretive figure:** `limits[0]` $50,000 —
  `assumptions_made[0]`, `conflicts[0]`, `unsupported_api_requests[2]`, and
  `missing_information_flags[3]` (blocking).

## R-54 — Packet B: 22 of 26 trace; 4 are FX-derived with a stated rate

- **JSON path:** `approval_policies[0].tiers[1]` = 11111, `tiers[2]` = 111111;
  `approval_policies[1].tiers[1]` = 7273, `tiers[2]` = 72727
- **what is there:** four USD threshold values that appear nowhere in packet B.
- **evidence:** the packet's thresholds are 2,000 / 20,000 MXN ([04:11]) and 400 / 4,000 BRL
  (§3.6). money_map finds all four in their own currencies. The Miami pair (10000, 100000¢)
  is stated directly in §4.5 and matches.
- **stated basis:** `approval_policies[0].source` — "converted at 18.0 MXN to the dollar
  because this format expresses thresholds only in USD"; `approval_policies[1].source` —
  "converted at 5.5 BRL to the dollar"; `assumptions_made[0]` gives the rates and states
  "These rates were not taken from a rate provider — no live rate source was available";
  `missing_information_flags[3]` (blocking) asks the customer to accept them.
  All 22 card limits are unconverted and match their own packet figures, including
  `R$ 6.000` → 600,000¢ BRL (dot separator) and `R$ 450` → 45,000¢.

## R-55 — Packet C: 13 of 13 trace

- **JSON path:** `spend_programs[0..3]`, `limits[0..5]`, `approval_policies[1].tiers[1]`
- **result:** all match. Spelled-out forms resolved: `"four thousand"` → 400,000¢,
  `"a thousand"` → 100,000¢, `"three thousand"` → 300,000¢, `"twenty-five hundred"` →
  250,000¢ (`spend_programs[2]` Facilities), `"Fifteen hundred"` → 150,000¢
  (`spend_programs[3]` Contract Nursing), `"five hundred"` → 50,000¢ (`limits[4]`,
  `approval_policies[1].tiers[1]`).
- **note:** the $10,000 REQ-2 threshold is not a configured figure; it is carried in
  `assumptions_made[10]` and `unsupported_api_requests[1]`.

## R-56 — Packet D: 7 of 9 trace; 2 are arithmetic derivations

- **JSON path:** `limits[3]` GTM manager monthly = 375,000¢; `limits[4]` Ops manager monthly
  = 150,000¢
- **what is there:** neither figure appears in packet D.
- **the sample counterpart:** none.
- **evidence:** `slack_export_finance.txt` [2026-07-30 11:03], Rachel Kim: `"GTM ICs:
  $2500/mo / ops ICs: $1000/mo / managers +50% on top of their team's IC number"`, corrected
  at [11:09]: `"eng managers don't need +50%… just GTM and ops managers get the bump"`.
  2500 × 1.5 = 3750; 1000 × 1.5 = 1500. The derivation is exact and the rule is stated.
- **stated basis:** `limits[3].notes` = "GTM IC limit plus 50%."; `limits[4].notes` = "Ops IC
  limit plus 50%."; `assumptions_made[5]` and `conflicts[3]` record the correction.
  This is a derivation, not an untraced figure.

## R-57 — Packet E: 25 of 25 trace to the matrix

- **JSON path:** `spend_programs[0..5]` (limit + per-transaction), `limits[0..5]` (same),
  `approval_policies[0].tiers[1]`
- **result:** every figure matches `mcc_allowlist_matrix.csv` columns `Monthly_Cap_USD` and
  `Per_Transaction_Cap_USD` exactly. The one non-matrix figure,
  `approval_policies[0].tiers[1]` = 50,000¢, matches [03:33] `"normal manager approvals over
  five hundred dollars"`.

## R-58 — Coincidences with Westbrook's five figures

The sample uses $50 (5,000¢), $800 (80,000¢), $1,000 (100,000¢), $2,000 (200,000¢) and
$5,000 (500,000¢). Every coincidence found, with its own-packet source:

| config path | value | Westbrook figure | own-packet source |
|---|---|---|---|
| A `spend_programs[1]` Travel `.limit_amount_cents` | 200000 | $2,000 | `discovery_call_01.txt` [03:49] `"two thousand a month per traveling rep"` |
| A `limits[2]` Priya Shetty | 500000 | $5,000 | roster row 4 `…,pshetty@acme.example,…,5000` |
| A `limits[4]` Talia Nguyen | 100000 | $1,000 | roster row 6 `…,1000` |
| A `limits[6]` Sana Qureshi | 200000 | $2,000 | roster row 8 `…,2000` |
| A `limits[18..21]` Sales AEs ×4 | 200000 | $2,000 | roster rows 21–24 `…,2000` |
| A `limits[22..23]` SDRs ×2 | 100000 | $1,000 | roster rows 25–26 `…,1000` |
| A `limits[27]` Sophie Amado | 80000 | **$800** | roster row 30 `Sophie Amado,samado@acme.example,Content Manager,Marketing,ltran@acme.example,2022-11-28,800` |
| A `limits[30]` Travel per traveller | 200000 | $2,000 | [03:49] as above |
| A `approval_policies[0].tiers[2]` | 500000 | $5,000 | [02:14] `"anything over five thousand comes to me"` |
| B `spend_programs[1]`/`limits[1]` `.transaction_amount_limit_cents` | 200000 **MXN** | $2,000 | §2.2 `"refacciones menores (< $2,000 MXN por transacción)"` |
| B `spend_programs[3]`/`limits[3]` Oficina MX | 500000 **MXN** | $5,000 | §2.4 / [03:16] `"cinco mil pesos al mes"` |
| B `approval_policies[2].tiers[2]` Miami | 100000 | $1,000 | §4.5 `"over USD $1,000, CFO (Monterrey)"` |
| C `spend_programs[0]`/`limits[0]` `.transaction_amount_limit_cents` | 100000 | $1,000 | [00:49] `"a per-transaction cap of a thousand"` |
| D `limits[2]` Ops IC monthly | 100000 | $1,000 | [2026-07-30 11:03] `"ops ICs: $1000/mo"` |
| E `spend_programs[4]`/`limits[4]` DM `.transaction_amount_limit_cents` | 100000 | $1,000 | matrix row 6 `Per_Transaction_Cap_USD` = 1000 |

- **finding of fact:** every coincidence has an independent source quote in its own packet.
  The $800 figure — the sample's most distinctive — appears exactly once in `out/`, at
  A `limits[27]`, and comes from a roster cell.
- **stated basis:** as tabulated.

## R-59 — Figures in the packets that were deliberately not configured [checked clean]

- **JSON path:** absent from all configs.
- **what is there:** D's `$10,000` CEO-notification threshold (in
  `unsupported_api_requests[1]` only); D's `$18k/yr` fare-difference estimate (in
  `assumptions_made[0].impact_if_wrong` only); C's `$10,000` REQ-2 gate (in
  `assumptions_made[10]` only); C's `$500` PO threshold (in `conflicts[0]` and
  `missing_information_flags[5]`, not as a `transaction_amount_limit_cents`); A's `$75`
  receipt and `$500` memo thresholds (R-14); D's `$50-60k` February estimate
  (`conflicts[2]`).
- **stated basis:** as cited.

---

# Inventory

| dimension | entries | range |
|---|---|---|
| 1 — Literal content | 10 | R-01 … R-10 |
| 2 — Structural idioms | 11 | R-11 … R-21 |
| 3 — Reasoning inheritance | 31 | R-22 … R-52 |
| 4 — Value provenance | 7 | R-53 … R-59 |
| **total** | **59** | |

**Entries per packet** (an entry that covers several packets is counted once per packet it
names with a specific JSON path):

| packet | D1 | D2 | D3 | D4 | total |
|---|---|---|---|---|---|
| client_c_apex_health | 2 | 6 | 12 | 2 | **22** |
| client_b_logistica_globex | 1 | 5 | 11 | 2 | **19** |
| client_d_hypergrowth | 4 | 6 | 8 | 2 | **20** |
| client_e_vanguard_retail | 3 | 6 | 8 | 2 | **19** |
| client_a_acme_corp | 4 | 6 | 7 | 2 | **19** |

Packets C and D carry the most entries. Dimension 3 is heaviest in C (12) and B (11).

**Coverage note on method:** `work/<packet>/traceability.json` records `config_paths` at
mixed granularity — some entries name a bare `spend_programs[i]`, which my prefix-matching
counts as covering every sub-field of that programme. Where a dimension-3 entry above says a
path is "uncovered", it means no traceability entry names it or any prefix of it; where an
entry is marked **[checked clean]** the basis was read directly out of the packet, not
inferred from traceability coverage.
