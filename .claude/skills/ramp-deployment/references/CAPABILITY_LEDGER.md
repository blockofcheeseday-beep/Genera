# Ramp Capability Ledger

**Generated from `capabilities.yaml` by `scripts/gen_ledger.py` — do not edit by hand.**

The unit is *a thing customers ask for*, not an endpoint.
`evidence_line` is copied verbatim into `audit_log.json` evidence fields.

Primary evidence: `candidate/2026_08_30_Ramp_OpenAPI_Schema.json` — 171 paths, 1017 schemas, 76 OAuth scopes, server `https://api.ramp.com`, prefix `/developer/v1/`.

**43 rows.** UNSUPPORTED: 7  UI_ONLY: 4  PARTIAL: 13  SUPPORTED: 16  DRIFT: 3

| id | verdict | title | seen in |
|---|---|---|---|
| [`CAP-NEW-VENDOR-APPROVAL`](#cap-new-vendor-approval) | **UNSUPPORTED** | Approval triggered by vendor novelty rather than amount | 0 sample, a acme corp, b logistica globex |
| [`CAP-MCC-ALLOWLIST`](#cap-mcc-allowlist) | **UNSUPPORTED** | Allow-list spend at raw MCC granularity | c apex health, e vanguard retail |
| [`CAP-UNLIMITED`](#cap-unlimited) | **UNSUPPORTED** | A card with no spending ceiling | a acme corp |
| [`CAP-PREAUTH-PO`](#cap-preauth-po) | **UNSUPPORTED** | Authorization-time match against a purchase order | c apex health |
| [`CAP-NOTIFICATIONS`](#cap-notifications) | **UNSUPPORTED** | Alerts to a chat channel or a named person on matching spend | 0 sample, d hypergrowth |
| [`CAP-DEPT-TO-ENTITY`](#cap-dept-to-entity) | **UNSUPPORTED** | Attach a department to a legal entity | b logistica globex |
| [`CAP-SP-UPDATE`](#cap-sp-update) | **UNSUPPORTED** | Edit a spend program after creation | a acme corp, c apex health, d hypergrowth, e vanguard retail |
| [`CAP-APPROVAL-CHAIN`](#cap-approval-chain) | **UI_ONLY** | Multi-tier spend approval chain (threshold -> approver) | 0 sample, a acme corp, b logistica globex, c apex health, d hypergrowth, e vanguard retail |
| [`CAP-RECEIPT-POLICY`](#cap-receipt-policy) | **UI_ONLY** | Receipt required above a threshold | 0 sample, a acme corp, c apex health |
| [`CAP-MEMO-POLICY`](#cap-memo-policy) | **UI_ONLY** | Memo or justification required above a threshold | a acme corp |
| [`CAP-ENTITY-CREATE`](#cap-entity-create) | **UI_ONLY** | Create a new legal entity | b logistica globex |
| [`CAP-MCC-BLOCKLIST`](#cap-mcc-blocklist) | **PARTIAL** | Block specific MCC codes | c apex health, e vanguard retail |
| [`CAP-FIELD-NAME-DIVERGENCE`](#cap-field-name-divergence) | **PARTIAL** | Same restriction concept, two spellings by object level | — |
| [`CAP-RESTRICTION-REPLACE-SEMANTICS`](#cap-restriction-replace-semantics) | **PARTIAL** | Editing restrictions replaces the whole set rather than merging | — |
| [`CAP-PRODUCTION-WRITES`](#cap-production-writes) | **PARTIAL** | Applying this config against the real API | — |
| [`CAP-VENDOR-BLOCK`](#cap-vendor-block) | **PARTIAL** | Hard block on a specific merchant | c apex health |
| [`CAP-GROUP-LIMIT`](#cap-group-limit) | **PARTIAL** | One shared limit covering a group of people | 0 sample, a acme corp, c apex health, d hypergrowth, e vanguard retail |
| [`CAP-ACTIVATION-GATE`](#cap-activation-gate) | **PARTIAL** | Card stays inert until an external condition is met | c apex health |
| [`CAP-SCOPED-VISIBILITY`](#cap-scoped-visibility) | **PARTIAL** | A manager sees only their own slice of spend | a acme corp, d hypergrowth, e vanguard retail |
| [`CAP-BULK-USERS`](#cap-bulk-users) | **PARTIAL** | Onboard many people from a spreadsheet | e vanguard retail |
| [`CAP-IDEMPOTENCY-SPLIT`](#cap-idempotency-split) | **PARTIAL** | Idempotency is passed two different ways | — |
| [`CAP-GUEST-EXPIRY-DEFAULT`](#cap-guest-expiry-default) | **PARTIAL** | Guest users silently expire after six months | a acme corp, c apex health |
| [`CAP-ROLE-MAPPING`](#cap-role-mapping) | **PARTIAL** | Map customer job titles onto Ramp's role enum | 0 sample, a acme corp, b logistica globex, c apex health, d hypergrowth, e vanguard retail |
| [`CAP-CARD-TYPE`](#cap-card-type) | **PARTIAL** | Choose physical versus virtual cards | a acme corp, e vanguard retail |
| [`CAP-CATEGORY-RESTRICT`](#cap-category-restrict) | **SUPPORTED** | Restrict a card or program to Ramp spend categories | a acme corp, c apex health, e vanguard retail |
| [`CAP-USER-LIMIT`](#cap-user-limit) | **SUPPORTED** | Give one named person a card with a recurring spending limit | 0 sample, a acme corp, b logistica globex, c apex health, d hypergrowth, e vanguard retail |
| [`CAP-AUTO-EXPIRY`](#cap-auto-expiry) | **SUPPORTED** | Card or limit stops working on a fixed date | c apex health, d hypergrowth, e vanguard retail |
| [`CAP-LOCAL-CURRENCY`](#cap-local-currency) | **SUPPORTED** | Limits denominated in the cardholder's local currency | b logistica globex |
| [`CAP-MONEY-MINOR-UNITS`](#cap-money-minor-units) | **SUPPORTED** | Amounts are integers in the smallest currency unit | b logistica globex |
| [`CAP-CARD-SUSPEND`](#cap-card-suspend) | **SUPPORTED** | Freeze a card or fund without deleting it | c apex health |
| [`CAP-READ-ONLY-AUDITOR`](#cap-read-only-auditor) | **SUPPORTED** | Read-only access for compliance or audit staff | c apex health |
| [`CAP-DRAFT-USER`](#cap-draft-user) | **SUPPORTED** | Create a user now, invite them later | b logistica globex, d hypergrowth |
| [`CAP-USER-TO-ENTITY`](#cap-user-to-entity) | **SUPPORTED** | Assign a person to a legal entity | b logistica globex |
| [`CAP-IT-ADMIN-SCOPE`](#cap-it-admin-scope) | **SUPPORTED** | Manage people without being able to touch spend controls | a acme corp |
| [`CAP-DEPT-CREATE`](#cap-dept-create) | **SUPPORTED** | Create departments | a acme corp, c apex health, d hypergrowth |
| [`CAP-LOCATION-CREATE`](#cap-location-create) | **SUPPORTED** | Create locations, optionally tied to an entity | b logistica globex, c apex health |
| [`CAP-SP-CREATE`](#cap-sp-create) | **SUPPORTED** | Create a spend program with its own rules | a acme corp, c apex health, d hypergrowth |
| [`CAP-SP-ISSUANCE-RULES`](#cap-sp-issuance-rules) | **SUPPORTED** | Different teams automatically get different programs | a acme corp, d hypergrowth, e vanguard retail |
| [`CAP-REIMBURSEMENTS`](#cap-reimbursements) | **SUPPORTED** | Turn reimbursements on or off per program | a acme corp, b logistica globex, d hypergrowth |
| [`NOT-DRIFT-SPEND-TYPES`](#not-drift-spend-types) | **SUPPORTED** | permitted_spend_types matches the spend-program API exactly | — |
| [`DRIFT-LIMITS-FUNDS`](#drift-limits-funds) | **DRIFT** | The resource is called limits in the schema and funds in the API | 0 sample, a acme corp, b logistica globex, c apex health, d hypergrowth, e vanguard retail |
| [`DRIFT-INTERVAL-TERTIARY`](#drift-interval-tertiary) | **DRIFT** | The API has an eighth interval value the schema lacks | — |
| [`DRIFT-ROLE-BUSINESS-OWNER`](#drift-role-business-owner) | **DRIFT** | The API has a BUSINESS_OWNER role the schema lacks | 0 sample, a acme corp, d hypergrowth |

## UNSUPPORTED

### CAP-NEW-VENDOR-APPROVAL

**Approval triggered by vendor novelty rather than amount**

How customers say it:

- *“any new vendor needs my sign-off regardless of amount”*
- *“first purchase from a supplier comes to finance”*

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No approval write surface at all (see CAP-APPROVAL-CHAIN). Separately, this rule is not threshold-shaped, so it has no home in the exercise schema either: approval_policies[].tiers[] is keyed on threshold_usd_cents (integer).

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no approval write surface; additionally 'new vendor' is not threshold-shaped and approval_policies[].tiers[] is keyed only on threshold_usd_cents.
```

Config expression: section `audit_log_only`

> A schema-expressiveness gap as well as an API gap. Worth flagging in both directions.

**Workaround.** Record in the audit log as a process control. The deployment owner can approximate it in-app with a low-threshold tier on a dedicated new-vendor spend program, at the cost of catching amount-based traffic too.

### CAP-MCC-ALLOWLIST

**Allow-list spend at raw MCC granularity**

How customers say it:

- *“here is the MCC matrix, these codes are allowed and everything else is denied”*
- *“allow 3000-3299”*
- *“default deny, allow-first”*

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/spend-programs`

Fields: `spending_restrictions.blocked_mcc_codes`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> The string "allowed_mcc" appears nowhere in the 2.3 MB spec. blocked_mcc_codes exists on request bodies only (4 occurrences, all *RequestBody). Allow-listing is available only at Ramp's 43-code category granularity (allowed_categories / allowed_category_codes).

> **support.ramp.com** (checked 2026-08-30)
>
> PASS 2 corroboration. "Setting up category and merchant restrictions" confirms the abstraction is deliberate and product-level, not a gap in the API surface: Ramp "determines the category of a merchant based on the MCC code and a number of factors", then restricts on its own categories. So an MCC allow-list is not expressible anywhere in the product, UI included — this stays UNSUPPORTED rather than becoming UI_ONLY.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — 'allowed_mcc' appears nowhere in the spec; only blocked_mcc_codes exists (request bodies only). support.ramp.com 'Setting up category and merchant restrictions', checked 2026-08-30 — Ramp derives its own category from the MCC plus other factors and restricts on that, so allow-listing is available only at Ramp's 43-code category granularity, in the UI as well as the API.
```

Config expression: section `mcc_controls`, mechanism `allowed_categories`

**Workaround.** Translate the customer's MCC allow-list into Ramp category codes and record every lossy mapping in translation_notes plus an assumptions_made entry. Ranges that straddle categories (e.g. 3000-3299 airlines) collapse to the nearest single category and must be flagged individually.

### CAP-UNLIMITED

**A card with no spending ceiling**

How customers say it:

- *“I never want to see a decline”*
- *“no limit”*
- *“unlimited for the CEO”*

Endpoints: `POST /developer/v1/funds`

Fields: `spending_restrictions.limit`, `spending_restrictions.interval`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> ApiFundSpendingRestrictionsRequestBody requires both interval and limit; limit is a CurrencyAmountRequestBody whose amount is a required integer. There is no null / unlimited sentinel.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — ApiFundSpendingRestrictionsRequestBody requires both 'interval' and 'limit', and limit.amount is a required integer; there is no unlimited sentinel.
```

Config expression: section `limits`

**Workaround.** Encode a deliberately high ceiling and record the exact number as an assumption with impact_if_wrong. Never emit a high number silently — "no limit" and "$50k/mo" are different promises to the person holding the card.

### CAP-PREAUTH-PO

**Authorization-time match against a purchase order**

How customers say it:

- *“purchases over $500 must match an approved PO before the charge goes through”*
- *“pre-authorization matching”*

Endpoints: `GET /developer/v1/purchase-orders`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> There is no authorization-time hook anywhere in the spec — no endpoint that runs during card authorization. /purchase-orders is a record API, not a control surface.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no authorization-time hook exists; /purchase-orders is a record API, not a control surface, so a charge cannot be gated on PO match at authorization.
```

Config expression: section `limits`, mechanism `spending_restrictions.transaction_amount_limit_cents`

**Workaround.** Tightest available compensating control: a hard transaction_amount_limit at the threshold, plus same-day post-transaction PO reconciliation, plus POST /funds/{id}/suspension on violation. Detective rather than preventive — say so plainly, because the difference is the whole point of the requirement.

### CAP-NOTIFICATIONS

**Alerts to a chat channel or a named person on matching spend**

How customers say it:

- *“post every transaction to our #spend channel”*
- *“I want to know about any card over $10k a month”*

Endpoints: `POST /developer/v1/webhooks`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No notification or chat-integration configuration resource. The nearest primitive is POST /developer/v1/webhooks (transaction events), which is a delivery mechanism, not a rule engine — thresholds and routing would live in the consumer.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no notifications resource; nearest primitive is POST /webhooks (transaction events), which delivers events but does not evaluate threshold or routing rules.
```

Config expression: section `audit_log_only`

**Workaround.** Ramp's in-app Slack integration may cover the common case (deployment owner enables it); otherwise a webhook consumer applies the threshold and posts. Note when the customer's phrasing is a wish rather than a rule — "I want to know about" is not a limit.

### CAP-DEPT-TO-ENTITY

**Attach a department to a legal entity**

How customers say it:

- *“each country has its own departments”*

Endpoints: `POST /developer/v1/departments`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> The exercise schema allows departments[].entity, but the API department create body is name-only — no entity_id. Departments are company-wide; only *locations* carry entity_id.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — the department create body is name-only with no entity_id, so departments are company-wide; only locations carry an entity association.
```

Config expression: section `departments`, mechanism `entity`

> The exercise schema is more expressive than the API here. Emit entity where the customer stated it, and log that it cannot be applied as such.

**Workaround.** Model the entity split through locations instead, or accept company-wide departments with entity-prefixed names. Flag rather than silently dropping the entity field.

### CAP-SP-UPDATE

**Edit a spend program after creation**

How customers say it:

- *“we will tune the limits once people are using it”*

Endpoints: `GET /developer/v1/spend-programs`, `POST /developer/v1/spend-programs`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> /spend-programs supports GET and POST; /spend-programs/{id} supports GET only. No PATCH, no DELETE. A program is effectively immutable once created via API.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — /spend-programs has GET and POST only and /spend-programs/{id} is GET-only; there is no PATCH or DELETE, so programs are immutable via the API.
```

Config expression: section `internal_note`

**Workaround.** Get programs right the first time, or edit in-app. This raises the stakes on the config review before go-live and is worth saying in the handoff.

## UI_ONLY

### CAP-APPROVAL-CHAIN

**Multi-tier spend approval chain (threshold -> approver)**

How customers say it:

- *“under $500 auto-approves, $500-5k goes to the manager, over $5k comes to me”*
- *“all travel needs my direct approval”*
- *“anything over $2,500 escalates”*

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No approval-policy write endpoint. The only approval paths are /developer/v1/blank-canvas-approvals/* (which act on already-existing approval trigger instances) and GET /developer/v1/spend-programs/{id}/workflow-nodes (read-only). No approval-related OAuth scope is defined among the 76 scopes.

> **support.ramp.com** (checked 2026-08-30)
>
> PASS 2 CORRECTION to the verdict, not the mechanism. Ramp does support multi-tier approval chains — in the app. "Set up your spend approval policies" and "Setting up spend request approvals" describe an approvals workflow builder where conditions and outcomes (Require approval / Notify / Approve spend) are layered and nested, with amount and user-role routing available to all customers and further conditions on Ramp Plus. So the capability is real and the API cannot reach it. UI_ONLY, not UNSUPPORTED — and the "hand it to the deployment owner" workaround is now evidenced rather than assumed.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no approval-policy write endpoint; only /blank-canvas-approvals/* (acts on existing instances) and GET /spend-programs/{id}/workflow-nodes (read-only); zero approval OAuth scopes. support.ramp.com 'Set up your spend approval policies', checked 2026-08-30 — tiered approval chains ARE configurable in Ramp's in-app approvals workflow builder, so this is a UI-only capability rather than a missing one.
```

Config expression: section `approval_policies`

> Still emitted as desired state. The schema's approval_policies description explicitly invites this ("check API support"), so the config carries the customer's intent and the audit log carries the fact that it cannot be applied via API.

**Workaround.** Emit the full tier structure as desired state, then hand the deployment owner a UI checklist to build the same chain in Ramp's approvals workflow builder.

### CAP-RECEIPT-POLICY

**Receipt required above a threshold**

How customers say it:

- *“receipts over $75”*
- *“receipts on everything, no matter how small”*

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No receipt-threshold configuration resource. /receipts and /receipt-integrations handle receipt objects and ingestion, not policy. The threshold is an in-app policy setting.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no receipt-policy configuration resource; /receipts covers receipt objects and ingestion, not thresholds. Receipt rules are an in-app setting.
```

Config expression: section `audit_log_only`

> Correctly OMITTED from ramp_config.json — the schema has no home for it. Omission is itself a decision, so it belongs in assumptions_made. This is the idiom the Westbrook sample demonstrates with its $50 rule.

**Workaround.** Deployment owner sets the receipt threshold in-app during setup.

### CAP-MEMO-POLICY

**Memo or justification required above a threshold**

How customers say it:

- *“memos over $500”*
- *“they have to say what it was for”*

Endpoints: `GET /developer/v1/memos`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> A memos resource exists for reading memo objects, but there is no memo-policy or memo-threshold configuration surface. Same shape as CAP-RECEIPT-POLICY.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — /memos exposes memo objects but no memo-policy or threshold configuration surface; the rule is an in-app setting.
```

Config expression: section `audit_log_only`

**Workaround.** Deployment owner sets the memo threshold in-app during setup.

### CAP-ENTITY-CREATE

**Create a new legal entity**

How customers say it:

- *“the Brazilian entity is still in formation”*
- *“design everything now, activate later”*

Endpoints: `GET /developer/v1/entities`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> /developer/v1/entities exposes GET only (collection and by-id). The separate POST /developer/v1/accounting/entities is an accounting-side object, not a Ramp legal entity.

> **docs.ramp.com** (checked 2026-08-30)
>
> PASS 2. The accounting guide states it positively rather than by absence: "Entities are created in the Ramp UI, and objects are scoped to an entity_id when fetching via the API." support.ramp.com additionally documents Company > Entities > Create legal entity, and a bulk flow for adding several at once. A positive docs statement is much stronger evidence than an endpoint's absence from a snapshot, and it moves the verdict to UI_ONLY.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — /entities is GET-only; the separate POST /accounting/entities creates an accounting-side object, not a Ramp legal entity. docs.ramp.com accounting guide, checked 2026-08-30 — 'Entities are created in the Ramp UI, and objects are scoped to an entity_id when fetching via the API.'
```

Config expression: section `entities`, mechanism `status`

> The schema's status enum (existing | requested) exists for exactly this situation — use requested rather than inventing an entity.

**Workaround.** Emit status "requested", pair it with is_draft users, and hand the entity creation to the deployment owner as a prerequisite step with a date dependency.

## PARTIAL

### CAP-MCC-BLOCKLIST

**Block specific MCC codes**

How customers say it:

- *“block gambling and crypto MCCs”*
- *“these specific codes must decline”*

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/spend-programs`

Fields: `spending_restrictions.blocked_mcc_codes`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> blocked_mcc_codes is present on ApiFundSpendingRestrictionsRequestBody, ApiFundSpendingRestrictionsUpdateRequestBody and ApiSpendingRestrictionsRequestBody — but on NO *Dump (response) schema. You can set it; you cannot read it back through the API to confirm it applied.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — blocked_mcc_codes is settable on fund and spend-program request bodies but absent from every response (*Dump) schema, so it is write-only via the API.
```

Config expression: section `mcc_controls`, mechanism `blocked_mcc_codes`

**Workaround.** Set it, then verify in the Ramp UI rather than by reading the API back. Note the write-only asymmetry for anyone building reconciliation on top.

### CAP-FIELD-NAME-DIVERGENCE

**Same restriction concept, two spellings by object level**

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/spend-programs`

Fields: `allowed_category_codes`, `allowed_categories`, `allowed_vendor_ids`, `allowed_vendors`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> Fund restrictions use allowed_category_codes / blocked_category_codes / allowed_vendor_ids / blocked_vendor_ids. Spend-program restrictions use allowed_categories / blocked_categories / allowed_vendors / blocked_vendors. Same concept, two spellings, one silent-bug surface.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — fund restrictions use *_category_codes / *_vendor_ids while spend-program restrictions use *_categories / *_vendors; the concepts are identical and the names are not.
```

Config expression: section `internal_note`

**Workaround.** An implementation hazard rather than a customer-facing gap. The exercise schema uses the spend-program spelling; anyone turning this config into fund calls must rename.

### CAP-RESTRICTION-REPLACE-SEMANTICS

**Editing restrictions replaces the whole set rather than merging**

How customers say it:

- *“just add one more blocked vendor”*
- *“we will tune the limits once people are using it”*

Endpoints: `PATCH /developer/v1/funds/{fund_id}`

Fields: `spending_restrictions`

> **docs.ramp.com** (checked 2026-08-30)
>
> PASS 2, found only in the live docs — this is not stated in the OpenAPI snapshot. The spend limits reference says: "If this field is passed, the entire set of new spending restrictions must be passed (i.e. the given spending restrictions will override all existing spending restrictions)."

Evidence line (verbatim into audit logs):

```
docs.ramp.com developer API, spend limits reference, checked 2026-08-30 — passing spending_restrictions overrides the entire existing set rather than merging, so any edit must be read-modify-write.
```

Config expression: section `internal_note`

**Workaround.** Read-modify-write on every restriction edit. A partial update silently drops restrictions the customer still expects — which is the quiet way a vendor block or a category allow-list disappears months after go-live.

### CAP-PRODUCTION-WRITES

**Applying this config against the real API**

How customers say it:

- *“can you just push this into our account”*

> **docs.ramp.com** (checked 2026-08-30)
>
> PASS 2. The developer docs state production write requests are disabled and that sandbox should be used for write operations; sandbox is a separate environment with its own base URL and app credentials, not a mode within production, and requires a separately created app.

Evidence line (verbatim into audit logs):

```
docs.ramp.com developer API, checked 2026-08-30 — production write requests are disabled and writes must go through the sandbox, which is a separate environment with its own base URL and app credentials.
```

Config expression: section `internal_note`

**Workaround.** Out of scope for this exercise, which produces payloads rather than calls — but it is the first thing a deployment owner needs to know, because it means go-live is not a matter of pointing a script at production. Belongs in the go-live handoff.

### CAP-VENDOR-BLOCK

**Hard block on a specific merchant**

How customers say it:

- *“the card must decline for [vendor]”*
- *“vendor-level, not category-level”*
- *“this applies to every card including temps”*

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/spend-programs`

Fields: `spending_restrictions.blocked_vendors`, `spending_restrictions.blocked_vendor_ids`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> blocked_vendors / blocked_vendor_ids accept *merchant* UUIDs, resolved via GET /developer/v1/merchants — NOT the Bill Pay vendor objects created by POST /developer/v1/vendors. Different object graph, easy to conflate. There is no company-wide blocklist resource: the block must be set on every program and every standalone limit.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — blocked_vendors / blocked_vendor_ids take merchant UUIDs from GET /merchants (not Bill Pay vendor objects); no global blocklist resource exists, so the block must be repeated on every spend program and standalone limit.
```

Config expression: section `mcc_controls`, mechanism `blocked_vendors`

**Workaround.** Apply the block on every program and limit, and add a standing process step: any newly created card or program must re-apply it. Trade names that map to one outfit must each be resolved to their own merchant UUID — one name is not one merchant.

### CAP-GROUP-LIMIT

**One shared limit covering a group of people**

How customers say it:

- *“the studio shares a $5k monthly pool”*
- *“give the field reps a limit”*
- *“engineering gets $750 each”*

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/funds/{fund_id}/members`

Fields: `user_id`, `is_shareable`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> POST /developer/v1/funds requires a single user_id (the only required field on ApiFundCreateRequestBody). A group limit therefore fans out to N funds, one per member. is_shareable plus /funds/{id}/members is the nearest genuine shared-pool primitive, and it changes the semantics: one pot drawn down by many, not N pots.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /funds requires a single user_id, so a group limit becomes one fund per member; is_shareable with /funds/{id}/members is the nearest shared-pool primitive and has different semantics (one shared pot, not N).
```

Config expression: section `limits`, mechanism `assigned_to.group`

**Workaround.** Emit assigned_to.group as the customer stated it and record in notes whether the intent was per-person (fan out to N funds) or a genuinely shared pot (one is_shareable fund with members). These are different products and the customer's phrasing usually does not distinguish them — ask.

### CAP-ACTIVATION-GATE

**Card stays inert until an external condition is met**

How customers say it:

- *“the card does nothing until the notarized form is on file”*
- *“must fail closed”*

Endpoints: `POST /developer/v1/cards/physical`, `POST /developer/v1/cards/physical/{id}/suspension`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No native conditioning of card activation on an external attestation. But issue-then-immediately-suspend is expressible, and unsuspending is a deliberate human act, which satisfies "fails closed".

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no native activation gate on external attestation; the composable equivalent is POST /cards/physical followed immediately by POST /cards/physical/{id}/suspension, released only on confirmation.
```

Config expression: section `audit_log_only`

**Workaround.** Issue, then suspend in the same run, and release only on written confirmation. The residual risk is the window between the two calls and the fact that nothing in Ramp enforces the evidence requirement — a human does.

### CAP-SCOPED-VISIBILITY

**A manager sees only their own slice of spend**

How customers say it:

- *“district managers should see only their district”*
- *“she should manage users but not limits”*

Endpoints: `GET /developer/v1/roles`, `POST /developer/v1/users/deferred`

Fields: `direct_manager_id`, `is_manager`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> /developer/v1/roles is GET-only — custom roles are readable, not creatable. The six-value role enum in the exercise schema is company-wide, with no scoping dimension. Partial-permission asks ("users but not limits") have no API surface.

> **support.ramp.com** (checked 2026-08-30)
>
> PASS 2 CORRECTION — this row was a false negative. "User roles overview" states that transaction visibility follows the MANAGEMENT CHAIN, not department labels: being in the same department grants no visibility, and manager permissions give visibility "scoped only to their team". That mechanism IS reachable from the API, via direct_manager_id / is_manager on user create. So "a manager sees only their own slice" is largely achievable by modelling the reporting structure correctly, which is the opposite of what the snapshot-only reading concluded. Separately, "Customizing Roles and Permissions" documents Custom Roles with entity restriction, on Ramp Plus, in-app — so finer scoping exists but is not API-creatable (consistent with GET /roles being read-only).

Evidence line (verbatim into audit logs):

```
support.ramp.com 'User roles overview', checked 2026-08-30 — transaction visibility follows the reporting chain, not department labels, and manager permissions are scoped to the manager's own team; that chain is settable via direct_manager_id on POST /users/deferred. Finer scoping (Custom Roles, entity restriction) exists in-app on Ramp Plus but is not API-creatable — Ramp Developer API specification (snapshot dated 2026-08-30) shows GET /roles is read-only.
```

Config expression: section `users`, mechanism `role`

**Workaround.** First model the reporting chain — set direct_manager_id so each person reports to the manager who should see them, and is_manager on that manager. That covers most of the ask natively. The common partial-permission ask, "manage users but not spend limits", is a stock role rather than a gap — see CAP-IT-ADMIN-SCOPE. Only scoping that follows neither reporting lines nor a stock role needs a Custom Role, which is Ramp Plus and in-app. Confirm the customer's plan tier before promising it.

### CAP-BULK-USERS

**Onboard many people from a spreadsheet**

How customers say it:

- *“I want to hand the system the spreadsheet”*
- *“it cannot require me clicking a form 140 times”*
- *“weekly waves of 30 to 40”*

Endpoints: `POST /developer/v1/users/deferred`, `GET /developer/v1/users/deferred/status/{task_id}`

Fields: `idempotency_key`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No bulk user endpoint. Creation is per-user and asynchronous: POST returns a task to poll at /users/deferred/status/{task_id}. idempotency_key is a required BODY field here, unlike funds which uses an X-Idempotency-Key header.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — no bulk user endpoint; POST /users/deferred is per-user and async (poll /users/deferred/status/{task_id}), with idempotency_key required in the body.
```

Config expression: section `users`

**Workaround.** A loop is entirely adequate at this scale — say so rather than implying a bulk import exists. Idempotency keys make waves safely re-runnable, which matters when a customer onboards in weekly batches.

### CAP-IDEMPOTENCY-SPLIT

**Idempotency is passed two different ways**

Endpoints: `POST /developer/v1/users/deferred`, `POST /developer/v1/funds`

Fields: `idempotency_key`, `X-Idempotency-Key`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> POST /users/deferred requires idempotency_key in the request body. POST /funds takes an X-Idempotency-Key HTTP header. Same guarantee, two transports.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /users/deferred requires a body-level idempotency_key while POST /funds uses an X-Idempotency-Key header.
```

Config expression: section `internal_note`

**Workaround.** Implementation hazard for anyone writing the apply step. No customer-facing impact.

### CAP-GUEST-EXPIRY-DEFAULT

**Guest users silently expire after six months**

How customers say it:

- *“contractors just need occasional access”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `role`, `scheduled_deactivation_date`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> GUEST_USER gets scheduled_deactivation_date auto-set to six months from invite unless explicitly nulled. The field cannot be set for admins or owners.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — GUEST_USER accounts receive an automatic scheduled_deactivation_date six months from invite unless explicitly nulled; the field is not settable for admins or owners.
```

Config expression: section `users`, mechanism `notes`

**Workaround.** A default with teeth: choosing GUEST_USER for a long-running contractor quietly schedules their deactivation. Flag it whenever GUEST_USER is assigned.

### CAP-ROLE-MAPPING

**Map customer job titles onto Ramp's role enum**

How customers say it:

- *“Priya runs the books and needs to see everything”*
- *“he is a contractor, give him the most locked-down thing you have”*
- *“Priya and me should administer it”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `role`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> The exercise schema offers six roles (BUSINESS_ADMIN, BUSINESS_USER, BUSINESS_BOOKKEEPER, IT_ADMIN, AUDITOR, GUEST_USER). Customer org charts do not come in six shapes, so most packets need a judgement call per person, and the enum carries no seniority or scoping dimension to encode the rest.

> **support.ramp.com** (checked 2026-08-30)
>
> "User roles overview" and the per-role deep-dives give the semantics the OpenAPI spec does not: what each role can actually see and do. Role choice is a permissions decision, not a titles translation, and it should be made from those pages rather than from the enum name.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) plus support.ramp.com 'User roles overview', checked 2026-08-30 — Ramp exposes six assignable roles with fixed, documented permission sets and no seniority or scoping dimension, so mapping customer job titles onto Ramp roles is a per-person judgement call.
```

Config expression: section `users`, mechanism `role`

**Workaround.** Every non-obvious mapping gets an assumptions_made entry naming the title, the chosen role, and what the person will consequently be able to see or do. Bookkeeper for close-the-books staff, AUDITOR for read-only compliance, GUEST_USER for contractors (see CAP-GUEST-EXPIRY-DEFAULT), IT_ADMIN for identity owners (see CAP-IT-ADMIN-SCOPE), BUSINESS_ADMIN for owners (see DRIFT-ROLE-BUSINESS-OWNER). Never infer a role from seniority alone.

### CAP-CARD-TYPE

**Choose physical versus virtual cards**

How customers say it:

- *“virtual for the field, physical for district managers”*
- *“they need a card in the phone wallet”*

Endpoints: `POST /developer/v1/cards/physical`, `GET /developer/v1/cards/virtual`

Fields: `permitted_spend_types`, `issue_physical_card_if_needed`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> Physical cards have full CRUD (POST /cards/physical requires shipping_address and user_id; automatic_routing_enabled and fund_id are mutually exclusive). Virtual cards are GET-only — they are issued as a side effect of funds, not created directly.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /cards/physical exists (requires shipping_address and user_id) but virtual cards are GET-only and are issued via funds rather than created directly.
```

Config expression: section `spend_programs`, mechanism `issue_physical_card_if_needed`

**Workaround.** Express the physical/virtual split through permitted_spend_types on the fund and issue_physical_card_if_needed on the program. Physical issuance additionally needs shipping addresses, which packets rarely contain — usually a missing-information flag.

## SUPPORTED

### CAP-CATEGORY-RESTRICT

**Restrict a card or program to Ramp spend categories**

How customers say it:

- *“software card should only work for software”*
- *“travel card for airlines, hotels, and restaurants only”*

Endpoints: `POST /developer/v1/funds`, `POST /developer/v1/spend-programs`

Fields: `spending_restrictions.allowed_categories`, `spending_restrictions.blocked_categories`, `spending_restrictions.allowed_category_codes`, `spending_restrictions.blocked_category_codes`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> 43 integer category codes numbered 1-44 with 22 absent — counted directly from the spec, which is 43 usable values, not 44. e.g. 4 = Airlines, 6 = Lodging, 18 = Fuel and gas, 19 = Restaurants, 40 = SaaS / Software. Note the canonical spelling is "SaaS / Software"; the Westbrook sample config writes "Software / SaaS", which validates because the exercise schema takes free strings but does not match the API vocabulary.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — 43 integer category codes, numbered 1-44 with 22 absent, settable via allowed_categories / blocked_categories on spend programs and allowed_category_codes / blocked_category_codes on funds.
```

Config expression: section `mcc_controls`, mechanism `allowed_categories`

### CAP-USER-LIMIT

**Give one named person a card with a recurring spending limit**

How customers say it:

- *“she should have her own card with a decent limit”*
- *“on the roster I marked target monthly limits per person”*
- *“two thousand a month per rep”*

Endpoints: `POST /developer/v1/funds`

Fields: `user_id`, `spending_restrictions.limit`, `spending_restrictions.interval`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> Found missing while running packet A — the most common request in the entire packet set had no ledger row, because the ledger had been written around the hard cases. POST /developer/v1/funds takes a single user_id plus spending_restrictions (interval + limit both required), which is exactly this. Recorded so the false-negative sweep has something to resolve for ordinary per-person limits instead of leaving archetype_id null on half a packet.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /funds takes a single user_id with spending_restrictions (interval and limit both required), so a per-person recurring limit is the API's native shape.
```

Config expression: section `limits`, mechanism `assigned_to.user_email`

### CAP-AUTO-EXPIRY

**Card or limit stops working on a fixed date**

How customers say it:

- *“cards must hard-stop December 24th, not January”*
- *“contractor cards die on the assignment end date”*
- *“the offsite budget expires Dec 1”*

Endpoints: `POST /developer/v1/funds`, `PATCH /developer/v1/funds/{fund_id}`

Fields: `spending_restrictions.lock_date`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> lock_date is settable on ApiFundSpendingRestrictionsRequestBody and on the update body, and surfaces as auto_lock_date on the dump schemas. Editable, so an extension is a PATCH rather than a teardown.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — lock_date is settable on fund create and update bodies (auto_lock_date on read), so a hard stop date is native and extendable via PATCH.
```

Config expression: section `limits`, mechanism `spending_restrictions.lock_date`

### CAP-LOCAL-CURRENCY

**Limits denominated in the cardholder's local currency**

How customers say it:

- *“Mexican limits in pesos, Brazilian in reais”*
- *“we consolidate in USD but the limits should be local”*

Endpoints: `POST /developer/v1/funds`

Fields: `spending_restrictions.limit.currency_code`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> CurrencyAmountRequestBody carries currency_code (ISO-4217, defaults USD) alongside an integer amount in the smallest denomination. Limits genuinely can be MXN / BRL / USD.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — CurrencyAmountRequestBody takes an ISO-4217 currency_code (default USD) with an integer minor-unit amount, so per-limit local currency is native.
```

Config expression: section `limits`, mechanism `spending_restrictions.currency`

### CAP-MONEY-MINOR-UNITS

**Amounts are integers in the smallest currency unit**

Endpoints: `POST /developer/v1/funds`

Fields: `limit.amount`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> CurrencyAmountRequestBody.amount is an integer in the smallest denomination ("cents for USD"). Only amount is required; currency_code defaults to USD.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — CurrencyAmountRequestBody.amount is an integer in the smallest currency denomination ('cents for USD').
```

Config expression: section `internal_note`

**Workaround.** Zero-decimal currencies do not have cents. Any packet quoting round local-currency figures needs the minor-unit conversion stated explicitly rather than assumed x100.

### CAP-CARD-SUSPEND

**Freeze a card or fund without deleting it**

How customers say it:

- *“suspend it the moment they break the rule”*
- *“turn it off until compliance clears them”*

Endpoints: `POST /developer/v1/funds/{fund_id}/suspension`, `DELETE /developer/v1/funds/{fund_id}/suspension`, `POST /developer/v1/cards/physical/{id}/suspension`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> Suspension is a POST/DELETE pair on funds, on individual fund members (/funds/{id}/members/{user_id}/suspension) and on physical cards. Reversible.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — suspension is a reversible POST/DELETE pair on /funds/{id}/suspension, /funds/{id}/members/{user_id}/suspension and physical cards.
```

Config expression: section `internal_note`

### CAP-READ-ONLY-AUDITOR

**Read-only access for compliance or audit staff**

How customers say it:

- *“compliance needs to see everything and change nothing”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `role`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> AUDITOR is a first-class value in the user create/update role enum.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — AUDITOR is a first-class role on ApiUserCreateRequestBody, giving read-only access without a custom role.
```

Config expression: section `users`, mechanism `role`

### CAP-DRAFT-USER

**Create a user now, invite them later**

How customers say it:

- *“set them up but do not turn them on yet”*
- *“the entity is not live until September”*
- *“leave them ready without activating”*

Endpoints: `POST /developer/v1/users/deferred`, `POST /developer/v1/users/{id}/invite`

Fields: `is_draft`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> is_draft is an optional boolean on ApiUserCreateRequestBody; a draft user gets no invite email and is activated later via POST /users/{id}/invite.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — ApiUserCreateRequestBody accepts is_draft, creating a user with no invite email, activated later via POST /users/{id}/invite.
```

Config expression: section `users`, mechanism `notes`

### CAP-USER-TO-ENTITY

**Assign a person to a legal entity**

How customers say it:

- *“these three report into the Mexican entity”*
- *“Miami staff belong to the US LLC”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `location_id`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> There is no entity field on user create. Entity assignment is indirect, via location_id — locations map many-to-one onto entities (POST /locations takes an optional entity_id).

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — user create has no entity field; entity assignment is indirect via location_id, and locations carry an optional entity_id.
```

Config expression: section `users`, mechanism `location`

**Workaround.** Every entity needs at least one location before its people can be placed. Worth stating in the handoff, because it makes location setup a prerequisite rather than a nicety.

### CAP-IT-ADMIN-SCOPE

**Manage people without being able to touch spend controls**

How customers say it:

- *“she should manage users but not change spend limits”*
- *“he runs our identity stuff — joiners and leavers”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `role`

> **support.ramp.com** (checked 2026-08-30)
>
> Found by dry-running the ledger against packet A, which asks for exactly this split. "User role deep-dive: IT Admin" states IT Admins have employee permissions plus access to edit People, Company Settings, Developer API and Integrations, and can invite users of any role including Admin — while they "do not have access to the business's spend information and cannot manage spend controls", and cannot issue spend or cards unless manager permissions are enabled for direct reports. That is the requested split exactly, as a stock role.

Evidence line (verbatim into audit logs):

```
support.ramp.com 'User role deep-dive: IT Admin', checked 2026-08-30 — IT Admins can edit People, Company Settings, Integrations and invite users of any role, but have no access to spend information and cannot manage spend controls; user administration without spend authority is a stock role, not a custom one.
```

Config expression: section `users`, mechanism `role`

**Workaround.** No workaround needed — but note the semantics come from the help centre, not the API spec. The enum value IT_ADMIN tells you nothing about what it permits, so a snapshot-only reading of this requirement would reach for a custom role that does not exist instead of the stock role that solves it.

### CAP-DEPT-CREATE

**Create departments**

How customers say it:

- *“we have four teams”*

Endpoints: `POST /developer/v1/departments`, `PATCH /developer/v1/departments/{id}`

Fields: `name`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> ApiDepartmentCreateRequestBody has exactly one property, name, and it is required.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /departments takes exactly one field, name.
```

Config expression: section `departments`

### CAP-LOCATION-CREATE

**Create locations, optionally tied to an entity**

How customers say it:

- *“fourteen clinics”*
- *“the Miami office”*

Endpoints: `POST /developer/v1/locations`, `PATCH /developer/v1/locations/{id}`

Fields: `name`, `entity_id`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> name required, entity_id optional. This is the only user-reachable entity link.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /locations requires name and accepts an optional entity_id; this is the only entity association reachable from user setup.
```

Config expression: section `locations`

### CAP-SP-CREATE

**Create a spend program with its own rules**

How customers say it:

- *“a software card program”*
- *“a travel program at $2k a month”*

Endpoints: `POST /developer/v1/spend-programs`

Fields: `display_name`, `description`, `icon`, `permitted_spend_types`, `spending_restrictions`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> ApiSpendProgramCreateRequestBody requires display_name, description, icon, permitted_spend_types and spending_restrictions. Note "icon" is REQUIRED by the API and has no home in the exercise schema.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — POST /spend-programs requires display_name, description, icon, permitted_spend_types and spending_restrictions; 'icon' is required by the API but has no field in the exercise schema.
```

Config expression: section `spend_programs`

**Workaround.** The deployment owner must choose an icon at apply time. Small, but it is a required field that this config cannot carry — better named now than discovered mid-deployment.

### CAP-SP-ISSUANCE-RULES

**Different teams automatically get different programs**

How customers say it:

- *“engineering gets X, sales gets Y”*
- *“field reps should be able to request it”*

Endpoints: `POST /developer/v1/spend-programs`

Fields: `issuance_rules.automatic`, `issuance_rules.requestable`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> issuance_rules splits into automatic and requestable, each targeting department_ids / location_ids / user_custom_field_ids / applies_to_all.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — spend program issuance_rules splits into 'automatic' and 'requestable', each targeting department_ids, location_ids, user_custom_field_ids or applies_to_all.
```

Config expression: section `spend_programs`

> The exercise schema has no issuance_rules field; targeting is implied by limits[].assigned_to.

**Workaround.** Real capability with no home in the exercise schema. Record the intended targeting in the audit log so it is not lost between this config and the actual deployment.

### CAP-REIMBURSEMENTS

**Turn reimbursements on or off per program**

How customers say it:

- *“keep reimbursements on for edge cases”*
- *“the drivers pay cash on the road”*

Endpoints: `POST /developer/v1/spend-programs`, `POST /developer/v1/funds`

Fields: `permitted_spend_types.reimbursements_enabled`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> reimbursements_enabled on the spend-program permitted_spend_types; reimbursements on the fund-level body. Independently togglable per object.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — reimbursements are a per-object toggle via permitted_spend_types (reimbursements_enabled on spend programs, reimbursements on funds).
```

Config expression: section `spend_programs`, mechanism `permitted_spend_types.reimbursements_enabled`

### NOT-DRIFT-SPEND-TYPES

**permitted_spend_types matches the spend-program API exactly**

Endpoints: `POST /developer/v1/spend-programs`

Fields: `permitted_spend_types.primary_card_enabled`, `permitted_spend_types.reimbursements_enabled`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> CORRECTION to an earlier planning assumption that this was schema drift. The snapshot contains BOTH shapes, at different object levels: ApiPermittedSpendTypesRequestBody (spend programs) requires exactly primary_card_enabled + reimbursements_enabled — identical to the exercise schema. ApiFundPermittedSpendTypesRequestBody (funds) requires physical_card + virtual_card + reimbursements. The exercise schema attaches permitted_spend_types to spend_programs, so it matches its API counterpart exactly. This is the same level-divergence pattern as CAP-FIELD-NAME-DIVERGENCE, not drift.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — ApiPermittedSpendTypesRequestBody (spend programs) requires exactly primary_card_enabled and reimbursements_enabled, matching the exercise schema; the three-boolean shape belongs to funds (ApiFundPermittedSpendTypesRequestBody), a different object level.
```

Config expression: section `spend_programs`

**Workaround.** Deliberately recorded as a NOT-drift row so no packet's audit log claims drift here. Asserting it would be a false "the API moved on" claim in all five audit logs.

## DRIFT

### DRIFT-LIMITS-FUNDS

**The resource is called limits in the schema and funds in the API**

Endpoints: `POST /developer/v1/funds`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> No /limits path exists in the snapshot; the resource is /developer/v1/funds. BUT both limits:read/limits:write AND funds:read/funds:write are defined among the 76 OAuth scopes — a rename caught in flight rather than a stale schema.

> **docs.ramp.com** (checked 2026-08-30)
>
> PASS 2, and it sharpens the row. The live docs still present this resource as "Creating spend limits" at docs.ramp.com/developer-api/v1/api/limits. So the customer-facing vocabulary is "limits" while the current path is /funds. Do NOT write "the API has no limits concept" in any audit log — it has the concept, under a different path. This is the single most likely place to produce a wrong "the API cannot do this" claim.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — the top-level 'limits' section maps to POST /developer/v1/funds (no /limits path exists), though both limits:* and funds:* OAuth scopes are defined; docs.ramp.com still documents the resource as 'spend limits' (checked 2026-08-30). The concept exists — only the path name differs.
```

Config expression: section `limits`

> Emit the schema shape (limits). Log the mapping. Do not rename.

**Workaround.** Anyone applying this config posts to /funds rather than /limits.

### DRIFT-INTERVAL-TERTIARY

**The API has an eighth interval value the schema lacks**

Endpoints: `POST /developer/v1/funds`

Fields: `spending_restrictions.interval`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> API interval enum has eight values: ANNUAL, DAILY, MONTHLY, QUARTERLY, TERTIARY, TOTAL, WEEKLY, YEARLY. The exercise schema has seven — no TERTIARY.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — the API interval enum carries eight values including TERTIARY; the exercise schema's interval enum has seven and omits it.
```

Config expression: section `limits`

> No packet has asked for a four-monthly interval, so this drift is currently harmless.

**Workaround.** Emit only the seven schema values. Log the difference.

### DRIFT-ROLE-BUSINESS-OWNER

**The API has a BUSINESS_OWNER role the schema lacks**

How customers say it:

- *“I own the company”*

Endpoints: `POST /developer/v1/users/deferred`

Fields: `role`

> **openapi_snapshot_2026_08_30** (checked 2026-08-30)
>
> ApiUserCreateRequestBody role enum has seven values including BUSINESS_OWNER; the exercise schema has six and omits it. Read-side User schemas carry eleven values (adding UNBUNDLED_*). Ramp's own docs note the Owner role is not invitable, so BUSINESS_OWNER would be a poor choice for a new user regardless.

Evidence line (verbatim into audit logs):

```
Ramp Developer API specification (snapshot dated 2026-08-30) — the API user-create role enum has seven values including BUSINESS_OWNER (read schemas carry eleven, adding UNBUNDLED_*); the exercise schema has six and omits BUSINESS_OWNER.
```

Config expression: section `users`, mechanism `role`

> Map a founder/owner to BUSINESS_ADMIN and log the mapping. This is the idiom the Westbrook sample demonstrates with Priti.

**Workaround.** Map owners to BUSINESS_ADMIN. Record the mapping as an assumption.
