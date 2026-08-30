# Session state — paused 2026-08-30 19:43 UTC

Branch `claude/genera-capability-ledger-d3ygam`, everything committed and pushed.
This container is ephemeral; the repo is the only durable record.

## Done

| | Status |
|---|---|
| Capability ledger | 43 rows, 3 evidence-verified passes (snapshot -> live docs -> packet A) |
| Pipeline | SKILL.md + run_pipeline.py + 7 scripts |
| Packet A (Acme Corp) | complete, 8/8 checks green |
| Packet C (Apex Health) | complete, 8/8 checks green |

Outputs in `out/<packet>/` (canonical names, for grading) and `deliverables/<Client>/`
(customer-facing names). Packaging only fires on a fully green run.

## Next, in order

1. **Packet D — `client_d_hypergrowth`.** The hard one and the last of the required three.
   No clean documents: a Slack export and fragmented second-hand notes that disagree.
   The headline conflict is travel approvals — February notes say tiered with a $2,500
   auto-approve; Leo's 2026-07-30 Slack message says ALL travel needs direct approval.
   The later source wins on recency, but the earlier one documents an agreement Leo made,
   and the note-taker explicitly records being unable to confirm the trial was cancelled.
   **This must stay a blocking conflict, not be resolved by recency.**
   Also: the NetSuite/PO message is explicitly retracted ("wrong project, ignore me") —
   do not build on it. "CS goes in Ops. final answer" DOES resolve the department question.
   `cite.py` already handles both D formats (verified).
2. **NOTES.md** — the graded write-up. Never cut this.
3. B and E only if time remains. Cut order if over: E, then B.

## Banked for NOTES.md

**Verification delta** (the README requires two concrete cases; there are five):
- Three ledger verdicts corrected by live docs — `CAP-SCOPED-VISIBILITY`
  UNSUPPORTED -> PARTIAL is the significant one; visibility follows the reporting chain,
  reachable via `direct_manager_id`. Snapshot-only reading said no surface existed.
- `permitted_spend_types` was planned as schema drift; the snapshot shows the exercise
  schema matches the spend-program API exactly. Kept as an explicit NOT-drift row.
- Category vocabulary is 43 codes, not 44 (1-44, no 22). The handoff was self-contradictory.
- The coverage invariant was hollow — `assumptions_made[999]` passed until check (e).
- My own `.title()` normalizer turned `IT` into `It`, orphaning a user from the department
  the same config creates. Both valid strings, so schema validation passed.

**Open item worth a sentence:** the new-vendor approval in packet A is encoded as a
zero-threshold tier that over-captures (catches all software spend, not just new vendors).
Recurs in packet C as the compliance-escalation policy. Honest in the audit log, still a
semantic mismatch.

**Script budget exception:** `cite.py` is 220 lines and `money_map.py` 182, against a ~40-line
guardrail. Defensible
(16 and 9 small functions, longest 40 lines, replacing work otherwise redone per packet) but
should be named in NOTES.md, not hidden.

## money_map.py — documented limits

Its own author listed these; keep them in NOTES.md rather than implying full coverage.
The tool is a prompt to look, not a guarantee that everything was found.

1. A bare unit word with no scale and no currency is not detected — packet A's "cap it at
   ten to be safe" is invisible as a figure. Deliberate: it is indistinguishable from "ten
   clinics". The text does appear in the context line printed for the $8,000 figure on the
   same line (verified), so a reader still sees it.
2. Spanish/Portuguese hundreds words beyond quinientos/quinhentos are not in the table.
   None appear as money in packet B; adding more raises headcount-noise risk.
3. `period` is read from a short window around the figure, so a line stating two amounts can
   leave the further one's period blank rather than wrong. `scope` is line-wide by design and
   can be over-inclusive on dense lines.
4. Currency is inferred from the nearest marker; a spelled-out amount with no marker on its
   line defaults to USD. Non-USD figures are marked, but an unmarked figure is an inference.
5. A range becomes two endpoints, both tagged `range` — "between X and Y" is not one object.
6. Repeated identical amounts on one line are reported once per occurrence, intentionally,
   since each carries different surrounding text.

**Already surfaced, unprompted:** on packet B, 2,000 MXN appears both as a per-transaction
ceiling in the memo and as the auto-approve threshold on the call — the same straddle class
as packet C. Worth checking properly if B gets run.

## Constraints found

- `docs.ramp.com` is blocked by org egress for curl and WebFetch. **WebSearch works** and
  was the only live-docs channel — live-docs rows cite page titles and snippets, not full
  pages. Say so in NOTES.md rather than implying deeper reading.
- Session rate limit was hit once mid-run (an agent died during its own self-verification).
  Verify agent work directly rather than trusting completion reports.
