# CATEGORY_MAP.md — MCC to Ramp category translation

Ramp does not restrict on raw MCCs in the allow direction. It restricts on its own
category vocabulary. Every MCC allow-list a customer hands you is therefore translated,
every translation is lossy, and every lossy translation is logged.

## The three facts that govern this document

| Fact | Ledger row | Verdict |
|---|---|---|
| You cannot allow-list at raw MCC granularity — anywhere, API or UI | `CAP-MCC-ALLOWLIST` | UNSUPPORTED |
| You **can** block specific MCCs — write-only, no read-back | `CAP-MCC-BLOCKLIST` | PARTIAL |
| You can allow/block on Ramp's integer category codes | `CAP-CATEGORY-RESTRICT` | SUPPORTED |

Evidence strings to copy verbatim into `unsupported_api_requests[].evidence`:

- `CAP-MCC-ALLOWLIST` — "openapi snapshot 2026_08_30 — 'allowed_mcc' appears nowhere in the spec; only blocked_mcc_codes exists (request bodies only). support.ramp.com 'Setting up category and merchant restrictions', checked 2026-08-30 — Ramp derives its own category from the MCC plus other factors and restricts on that, so allow-listing is available only at Ramp's 43-code category granularity, in the UI as well as the API."
- `CAP-MCC-BLOCKLIST` — "openapi snapshot 2026_08_30 — blocked_mcc_codes is settable on fund and spend-program request bodies but absent from every response (*Dump) schema, so it is write-only via the API."
- `CAP-CATEGORY-RESTRICT` — "openapi snapshot 2026_08_30 — 43 integer category codes, numbered 1-44 with 22 absent, settable via allowed_categories / blocked_categories on spend programs and allowed_category_codes / blocked_category_codes on funds."

## Do not tell a customer MCCs are unusable

Blocking by MCC is real. `blocked_mcc_codes` is a settable array of strings on
`ApiFundSpendingRestrictionsRequestBody`, `ApiFundSpendingRestrictionsUpdateRequestBody`
and `ApiSpendingRestrictionsRequestBody` (verified in
`candidate/2026_08_30_Ramp_OpenAPI_Schema.json`). It appears on **no** `*Dump` response
schema, so you can set it and cannot read it back — verify in the UI, and say so.

Practical consequence for a role-by-MCC matrix: **the BLOCKED column usually survives
translation intact; the ALLOWED column never does.** Say exactly that to the customer.

---

## The authoritative category vocabulary

Extracted from `candidate/2026_08_30_Ramp_OpenAPI_Schema.json` — the single
`x-enum-descriptions` map that appears (identically) at 18 sites in the snapshot,
including `components/schemas/ApiSpendingRestrictionsRequestBody/properties/allowed_categories/items`
and `.../ApiFundSpendingRestrictionsRequestBody/properties/allowed_category_codes/items`.

**Say 43, not 44.** The enum in the snapshot carries **43** distinct integer codes,
numbered 1–44 with 22 absent — "1-44 with no 22" is 43 values, not 44. The ledger row
`CAP-CATEGORY-RESTRICT` says 43 and its `evidence_line` above is the string to copy. The
handoff that seeded this work said 44 and the ledger inherited it; both were corrected once
this document and an independent count of the snapshot agreed. Never invent a name for
code 22.

| Code | Name |
|---:|---|
| 1 | Pet |
| 2 | Other |
| 3 | Office |
| 4 | Airlines |
| 5 | Car rental |
| 6 | Lodging |
| 7 | Travel miscellaneous |
| 8 | Taxi and rideshare |
| 9 | Freight, moving and delivery services |
| 10 | Shipping |
| 11 | Utilities |
| 12 | Office supplies and cleaning |
| 13 | General merchandise |
| 14 | Electronics |
| 15 | Clothing |
| 16 | Books and newspapers |
| 17 | Supermarkets and grocery stores |
| 18 | Fuel and gas |
| 19 | Restaurants |
| 20 | Alcohol and bars |
| 21 | Medical |
| **22** | **NOT FOUND — absent from the snapshot enum. No name. Never emit it.** |
| 23 | Fees and financial institutions |
| 24 | Entertainment |
| 25 | Professional services |
| 26 | Taxes and tax preparation |
| 27 | Advertising |
| 28 | Parking |
| 29 | Car services |
| 30 | Gambling |
| 31 | Clubs and memberships |
| 32 | Legal |
| 33 | Education |
| 34 | Charitable donations |
| 35 | Political organizations |
| 36 | Religious organizations |
| 37 | Fines |
| 38 | Government services |
| 39 | Intra-company purchases |
| 40 | SaaS / Software |
| 41 | Cloud computing |
| 42 | Streaming services |
| 43 | Internet and phone |
| 44 | Insurance |

Anchors confirmed as required: 4 = Airlines, 6 = Lodging, 18 = Fuel and gas,
19 = Restaurants, 20 = Alcohol and bars, 40 = SaaS / Software.

### Where these codes live in the snapshot

| Object level | Allow field | Block field | Readable back? |
|---|---|---|---|
| Spend program (`ApiSpendingRestrictions*`) | `allowed_categories` | `blocked_categories` | yes — present on `...Dump` |
| Fund / limit (`ApiFundSpendingRestrictions*`) | `allowed_category_codes` | `blocked_category_codes` | yes — present on `...Dump` |
| Either | — | `blocked_mcc_codes` (strings) | **no** — request bodies only |

The two spellings are the same concept — see `CAP-FIELD-NAME-DIVERGENCE`. The exercise
schema uses the spend-program spelling (`allowed_categories`), so emit that.

**Three codes have no reliable MCC anchor — never map into them:** 2 (Other), 3 (Office),
39 (Intra-company purchases). The snapshot gives names, not definitions. In particular the
distinction between 3 "Office" and 12 "Office supplies and cleaning" is **unknown**; use
12 for supply purchases and log the choice as an assumption.

---

## MCC → Ramp category

MCC names below are the card-network standard (ISO 18245) — they are **not** in the Ramp
snapshot. Ramp publishes no MCC-to-category crosswalk, and `support.ramp.com` states Ramp
"determines the category of a merchant based on the MCC code and a number of factors"
(per `CAP-MCC-ALLOWLIST` evidence). **Every row below is therefore a best-effort inference,
not documented Ramp behaviour.** A merchant can land in a category you did not predict.
Any control that matters (a compliance block, a default-deny program) must be confirmed
with a test transaction or in the Ramp UI before go-live — put that in the audit log.

LOSSY values: `exact` (same merchant set, no rule meaning changes) · `narrower` (Ramp
category covers less than the MCC) · `broader` (covers more — an allow lets in more than
asked, a block blocks more than asked) · `none` (no corresponding category).

### Fuel, vehicle, parking, transit

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 5541 | Service stations | 18 Fuel and gas | exact | |
| 5542 | Automated fuel dispensers | 18 Fuel and gas | exact | Same category as 5541; two MCCs collapse to one code. |
| 7523 | Parking lots and garages | 28 Parking | exact | |
| 4121 | Taxicabs and limousines | 8 Taxi and rideshare | exact | |
| 4111 | Local/suburban commuter transport | 7 Travel miscellaneous | broader | 8 covers taxi/rideshare only; rail and ferry are not that. Nearest is 7, which is much wider. |
| 4112 | Passenger railways | 7 Travel miscellaneous | broader | |
| 7512 | Automobile rental agency | 5 Car rental | exact | |
| 5533 | Auto parts and accessories stores | 29 Car services | **none** | 29 reads as services, not parts retail. Which category a given parts retailer lands in is **unknown**. Flag per-role. |
| 4784 | Tolls and bridge fees | — | **none** | No toll category exists. Relevant to packet B ("casetas"): a fuel-only card cannot be extended to tolls by category. Say so plainly. |

### Travel and hospitality

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 3000–3299 | Individual airline carrier codes | 4 Airlines | broader | See "Ranges" below. |
| 4511 | Airlines, air carriers | 4 Airlines | exact | |
| 7011 | Lodging — hotels, motels, resorts | 6 Lodging | exact | |
| 4722 | Travel agencies and tour operators | 7 Travel miscellaneous | broader | |
| 5812 | Eating places and restaurants | 19 Restaurants | exact | |
| 5814 | Fast food restaurants | 19 Restaurants | exact | |
| 5813 | Drinking places, bars, taverns | 20 Alcohol and bars | exact | Ramp separates 19 and 20, so "restaurants yes, bars no" survives translation. |
| 5921 | Package stores — beer, wine, liquor | 20 Alcohol and bars | exact | |

### Retail

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 5411 | Grocery stores, supermarkets | 17 Supermarkets and grocery stores | broader (in intent) | Category maps cleanly, but Ramp cannot restrict by basket. Packet E's "grocery is for display materials (tape/cleaner) not food" is **not enforceable** — record it as a control the customer must handle by policy. |
| 5732 | Electronic sales | 14 Electronics | exact | |
| 5045 | Computers, peripherals, software | 14 Electronics | broader | Could plausibly land in 40 instead. Unknown. |
| 5200 | Home supply warehouse stores | 13 General merchandise | **none** | No hardware / building-materials category. 13 is far wider — an allow-list on 13 opens general retail. |
| 5211 | Lumber and building materials | 13 General merchandise | **none** | As 5200. |
| 5251 | Hardware stores | 13 General merchandise | **none** | As 5200. This is the single biggest loss in packet E (Installation reps) and packet C (clinic managers' "hardware stores"). |
| 5944 | Jewelry stores | 13 General merchandise | **none** | For a *block*, do not use 13 — use `blocked_mcc_codes: ["5944"]` and keep it exact. |
| 5310 / 5311 / 5399 | Discount, department, misc general merchandise | 13 General merchandise | exact | |
| 5651 | Family clothing stores | 15 Clothing | exact | |
| 5942 | Book stores | 16 Books and newspapers | exact | |
| 5943 | Stationery, office and school supply stores | 12 Office supplies and cleaning | exact | |
| 5111 | Stationery and office supplies (commercial) | 12 Office supplies and cleaning | exact | |
| 5995 | Pet shops, pet food and supplies | 1 Pet | exact | |

### Medical

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 8011 / 8021 / 8062 | Doctors / dentists / hospitals | 21 Medical | exact | |
| 5047 | Medical, dental, hospital equipment and supplies | 21 Medical | broader | Packet C: the Prohibited Vendor sits in this category alongside legitimate suppliers, which is exactly why REQ-1 says category controls are insufficient. Use `blocked_vendors` — see `CAP-VENDOR-BLOCK`. |
| 5122 | Drugs, druggists' sundries | 21 Medical | broader | |
| 5912 | Drug stores and pharmacies | 21 Medical | broader | |

### Software, comms, services

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 5734 | Computer software stores | 40 SaaS / Software | broader | 41 Cloud computing is a separate code; a "software only" card usually needs both 40 and 41. Ask. |
| 7372 | Computer programming, data processing | 40 SaaS / Software | broader | As 5734. |
| 4814 / 4815 | Telecommunication services | 43 Internet and phone | exact | |
| 4899 | Cable, satellite, other pay TV | 42 Streaming services | broader | |
| 4900 | Utilities — electric, gas, water | 11 Utilities | exact | |
| 7311 | Advertising services | 27 Advertising | exact | |
| 7392 | Management, consulting, PR services | 25 Professional services | exact | |
| 8111 | Legal services and attorneys | 32 Legal | exact | |
| 8220 | Colleges and universities | 33 Education | exact | |
| 4214 | Motor freight carriers, trucking | 9 Freight, moving and delivery services | exact | |
| 4215 | Courier services | 10 Shipping | exact | |

### Restricted / financial / civic

| MCC | MCC name | Ramp | LOSSY | Note |
|---|---|---|---|---|
| 7995 | Betting, casino gambling | 30 Gambling | exact | |
| 7997 | Membership clubs, country clubs | 31 Clubs and memberships | exact | |
| 7832 | Motion picture theaters | 24 Entertainment | narrower→exact | 24 is wider than cinemas but is the intended home. |
| 6012 | Financial institutions — merchandise and services | 23 Fees and financial institutions | exact | |
| 6010 / 6011 | Manual and ATM cash disbursements | 23 Fees and financial institutions | **none** | Cash advance is a different concept from fees. Do not rely on 23 to stop ATM withdrawals. |
| 6300 | Insurance sales and underwriting | 44 Insurance | exact | |
| 9311 | Tax payments | 26 Taxes and tax preparation | exact | |
| 9211 / 9222 | Court costs / fines | 37 Fines | exact | |
| 9399 | Government services NEC | 38 Government services | exact | |
| 8398 | Charitable and social service organizations | 34 Charitable donations | exact | |
| 8651 | Political organizations | 35 Political organizations | exact | |
| 8661 | Religious organizations | 36 Religious organizations | exact | |

---

## MCC ranges

Ramp has **no range concept**. `blocked_mcc_codes` is a flat array of strings; there is no
`from`/`to` and no wildcard anywhere in the snapshot. A range in a customer matrix must be
either enumerated (block direction) or collapsed to a category (allow direction).

**Packet E, `mcc_allowlist_matrix.csv`, Trainer and District Manager rows: `3000-3299`,
annotated "Airline range 3000-3299 per amex reporting".**

3000–3299 is the block of per-carrier MCCs Amex reporting uses — one code per airline
(Delta, United, and so on). It appears in the ALLOWED column, so `blocked_mcc_codes` is not
available and it collapses to **category 4 (Airlines)**.

What is lost, stated plainly:

1. **Per-carrier control disappears.** The customer could have allowed 12 carriers and
   denied the rest. Category 4 is all-airlines-or-none.
2. **The range is not the same set as category 4.** Category 4 also picks up merchants
   Ramp classifies as airlines from outside 3000–3299 (e.g. MCC 4511 air carriers, and
   airline-operated ancillary merchants). The allow-list gets *wider* than written.
3. **Ramp classifies "based on the MCC code and a number of factors"** — so a carrier
   inside 3000–3299 is not guaranteed to be classified as 4. The allow-list can also be
   *narrower* than written for a specific merchant. This direction cannot be predicted
   from the snapshot and must be verified in-app.
4. Consequence: a Trainer's card may work at an airline the customer intended to exclude,
   and may decline at one they intended to include. Both directions go in the audit log.

Rule: a range in the ALLOWED column produces one `assumptions_made` entry per range, not
one for the whole matrix.

---

## How to use this

For each row of a customer MCC matrix (one role, one card program):

1. **Split allow from block.** They translate differently.
2. **ALLOWED column → categories.** Map each MCC through the table above, dedupe, sort.
   Emit one `mcc_controls` entry with `mechanism: "allowed_categories"`.
3. **BLOCKED column → keep the MCCs.** Emit a second `mcc_controls` entry with
   `mechanism: "blocked_mcc_codes"` and the customer's codes as strings, unchanged. This is
   exact — say so. Note the write-only caveat (`CAP-MCC-BLOCKLIST`) once per packet in
   `unsupported_api_requests`.
4. **Check for collapse-induced collisions.** After translation, an MCC in the allow column
   and an MCC in the block column can land in the same Ramp category (e.g. anything you
   mapped to 13 General merchandise). If that happens, the rule is no longer expressible as
   written — that is a `conflicts` entry, or an `unsupported_api_requests` entry, not a
   silent choice.
5. **Write `translation_notes`** on the `mcc_controls` entry. Name the input MCCs, the
   output categories, and every non-`exact` row. Example shape:

   > "Matrix ALLOWED for Field Rep - Installation = 5541,5542,7523,5200,5251,5533,5812. Ramp has no per-MCC allow-list (CAP-MCC-ALLOWLIST), so translated to categories 18, 28, 13, 19. Lossy: 5200/5251 (hardware) and 5533 (auto parts) have no Ramp category — 5200/5251 widened to 13 General merchandise, which also permits department and discount stores; 5533 has no clean home and is not represented. Confirm in-app before go-live."

6. **Write an `assumptions_made` entry for every non-`exact` mapping** — not one per matrix.
   `source` = the CSV file and the row's literal cell contents. `impact_if_wrong` = what the
   cardholder can buy that they should not, or is declined for that they should not be.
7. **Never emit an MCC in `allowed_categories`.** If you find a four-digit number in that
   array, the translation step was skipped.

### Value format

The exercise schema types `spending_restrictions.allowed_categories` as an array of
**strings**, while the API takes **integers**. Emit the snapshot name verbatim — e.g.
`"SaaS / Software"`, `"Fuel and gas"` — and put the integer code in `translation_notes`.
Note that the Westbrook sample
(`candidate/sample_packet/client_0_sample_westbrook/example_output/ramp_config.json`)
writes `"Software / SaaS"`, which is **not** the snapshot's spelling of code 40. Pick the
snapshot spelling, use it consistently across a packet, and flag the variance once.
`mcc_controls[].values` accepts strings or integers; `blocked_mcc_codes` is strings.
