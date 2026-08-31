# 03 - Applied

Agent 3 of 3. Application of `02_verdicts.md` **section C only** (R-04, the single
CONTAMINATION finding). Section D (R-25, JUDGEMENT) and section F (observations) were
**not** acted on. No search for additional problems was performed.

---

## Deviation from 02_verdicts.md, as directed

The replacement text specified in section C contained an em-dash. The user has a standing
preference against em-dashes in prose, so the parent supplied a substitute that splits that
clause into its own sentence and is otherwise identical in meaning. **That em-dash-free text
is what was written in all three locations**, verified programmatically: no `—` (U+2014) and
no `–` (U+2013) appears anywhere in the new string.

Nothing else in section C was altered. In particular the em-dashes in the row's *unchanged*
fields (`evidence_line`, the internal `workaround`, the first `evidence` note) were left
exactly as they were; they are outside the scope of this change.

---

## Change 1 of 3: `out/client_d_hypergrowth/audit_log.json`

JSON path: `unsupported_api_requests[1].proposed_manual_workaround`

**Before:**

```
Ramp has no rule engine for routing spend alerts to a chat channel or to a named person. Ramp's Slack integration, switched on by the deployment owner in the Ramp application, covers the common case of posting card activity to a channel; anything conditional, such as alerting only above a set monthly amount, needs a webhook subscription with the threshold applied by the receiving system.
```

**After:**

```
Ramp has no rule engine for routing spend alerts to a chat channel or to a named person. Ramp does have a Slack integration, switched on by the deployment owner in the Ramp application, which may cover the simple case of posting card activity to a channel. The API specification records only a read-only is_integrated_with_slack flag on the business object and does not describe what that integration posts, so its scope should be confirmed in the Ramp application before anyone relies on it. Anything conditional, such as alerting only above a set monthly amount, needs a webhook subscription with the threshold applied by the receiving system.
```

`requested_feature`, `reason_unsupported` and `evidence` on this entry are byte-unchanged;
`git diff` reports exactly **one** changed line in this file.

## Change 2 of 3: `out/client_e_vanguard_retail/audit_log.json`

JSON path: `unsupported_api_requests[6].proposed_manual_workaround`

Before and after are byte-identical to change 1 (verified: `json_d == json_e` is `True`).
Siblings unchanged; exactly **one** changed line in this file.

## Change 3 of 3: `.claude/skills/ramp-deployment/references/capabilities.yaml`

Ledger row `id: CAP-NOTIFICATIONS`, key `customer_workaround`, the source the two audit logs
are copied from, so that a regeneration cannot re-introduce the claim.

**Before** (folded scalar, `>-`, four-space key indent, six-space continuation):

```yaml
    customer_workaround: >-
      Ramp has no rule engine for routing spend alerts to a chat channel or to a named
      person. Ramp's Slack integration, switched on by the deployment owner in the Ramp
      application, covers the common case of posting card activity to a channel; anything
      conditional, such as alerting only above a set monthly amount, needs a webhook
      subscription with the threshold applied by the receiving system.
```

**After** (same `>-` marker, same indents, re-wrapped):

```yaml
    customer_workaround: >-
      Ramp has no rule engine for routing spend alerts to a chat channel or to a named person.
      Ramp does have a Slack integration, switched on by the deployment owner in the Ramp
      application, which may cover the simple case of posting card activity to a channel. The
      API specification records only a read-only is_integrated_with_slack flag on the business
      object and does not describe what that integration posts, so its scope should be
      confirmed in the Ramp application before anyone relies on it. Anything conditional, such
      as alerting only above a set monthly amount, needs a webhook subscription with the
      threshold applied by the receiving system.
```

**YAML round-trip check (required):** loading the file with `yaml.safe_load` and comparing the
resolved scalar to the JSON string gives:

- `" ".join(value.split()) == json_string` → **True**
- `value == json_string` (raw, no re-normalisation needed, because the folded scalar already resolves
  to a single line with single spaces) → **True**

### Evidence entry appended to the same row

One entry appended to the **end** of `CAP-NOTIFICATIONS.evidence` (2 entries now, was 1).
Appending is safe: `audit_refs` index only into `audit_log.json` arrays, never into this list.

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

`evidence_line`, `api_mechanism`, `verdict`, `workaround` and `seen_in` on this row are
unchanged, confirmed in the diff (the row's only other change is the appended evidence block).

---

## Post-edit steps

**1. Ledger markdown regenerated.** `capabilities.yaml` changed, so `CAPABILITY_LEDGER.md` was
stale and check 9 would have failed:

```
python3 .claude/skills/ramp-deployment/scripts/gen_ledger.py
  wrote .claude/skills/ramp-deployment/references/CAPABILITY_LEDGER.md (1192 lines)
python3 .claude/skills/ramp-deployment/scripts/gen_ledger.py --check
  CAPABILITY_LEDGER.md is up to date
```

**2. All five packets verified** (the ledger change is global, so all five were run, not just
the two edited). Every packet: **9 passed, 0 failed, 0 skipped**.

| packet | result | notes |
|---|---|---|
| client_a_acme_corp | 9/9 PASS | 37/37 quotes verified |
| client_b_logistica_globex | 9/9 PASS | 43/43 quotes; pre-existing warn on REQ-042 (no archetype_id) |
| client_c_apex_health | 9/9 PASS | 35/35 quotes; pre-existing warn on REQ-020 |
| client_d_hypergrowth | 9/9 PASS | 37/37 quotes |
| client_e_vanguard_retail | 9/9 PASS | 28/28 quotes; pre-existing warn on REQ-006 |

Check 9 (ledger freshness) reports "up to date" on all five. The three warns are the
pre-existing coverage-sweep warnings, unrelated to this change. Each green run repackaged
`deliverables/`; the only deliverables that actually changed are Hypergrowth's and Vanguard
Retail's audit logs, one line each.

**3. Viewers re-rendered** for the two edited packets:

```
work/client_d_hypergrowth/view.html
work/client_e_vanguard_retail/view.html
```

**4. Baseline comparison, proving no array was spliced.** Current audit array lengths against
`00_baseline.json` (recorded at commit `9883a43`):

| packet | assumptions_made | missing_information_flags | conflicts | unsupported_api_requests | match |
|---|---|---|---|---|---|
| client_a_acme_corp | 17 | 10 | 5 | 11 | identical |
| client_b_logistica_globex | 14 | 10 | 3 | 11 | identical |
| client_c_apex_health | 13 | 13 | 3 | 11 | identical |
| client_d_hypergrowth | 15 | 14 | 5 | 7 | identical |
| client_e_vanguard_retail | 12 | 8 | 1 | 10 | identical |

**All five identical to the baseline.** Independently, the index-based `audit_refs` in the five
`work/<packet>/traceability.json` files still total **284** (54 / 61 / 64 / 57 / 48), matching
the baseline per-packet counts. No `traceability.json` was modified.

---

## Scope confirmation

- **Section D (R-25) not touched.** `out/client_d_hypergrowth/audit_log.json`
  `assumptions_made[9].impact_if_wrong` still reads, unchanged: *"None to card behaviour.
  Reimbursements remain enabled company-wide so invoice reimbursement is unaffected."* A human
  decides that one.
- **Section F not acted on.** No observation from section F was investigated or changed.
- **No hunt for further problems.** Only the three strings and the one appended evidence entry.
- **Files deliberately untouched:** `NOTES.md`, `SKILL.md`, anything under `candidate/`, every
  `requirements.json`, every `traceability.json`. None appear in `git status`.
- **No commit or push.** The working tree is left modified for the parent to commit.

**Full set of modified files:**

```
.claude/skills/ramp-deployment/references/capabilities.yaml     (edited by hand)
.claude/skills/ramp-deployment/references/CAPABILITY_LEDGER.md  (regenerated)
out/client_d_hypergrowth/audit_log.json                         (1 line)
out/client_e_vanguard_retail/audit_log.json                      (1 line)
deliverables/Hypergrowth/Hypergrowth_Audit_Log.json              (repackaged, 1 line)
deliverables/Vanguard_Retail/Vanguard_Retail_Audit_Log.json      (repackaged, 1 line)
work/client_d_hypergrowth/view.html                              (re-rendered, 1 line)
work/client_e_vanguard_retail/view.html                          (re-rendered, 1 line)
```
