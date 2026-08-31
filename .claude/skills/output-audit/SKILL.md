---
name: output-audit
description: Audit a finished packet's three artifacts for agreement — out/<packet>/ramp_config.json, out/<packet>/audit_log.json, and the work/<packet>/view.html reviewers read — plus the deliverables/ copies, and confirm every one reflects the most recent changes. Use at the end of the exercise, when asked to audit or sign off the work, to check whether outputs are stale or out of sync, or after any late edit to a config or audit log.
---

# Output audit: do the three documents still agree?

`run_pipeline.py --verify` proves each output is internally correct. It never looks at
`view.html` and never re-reads `deliverables/`. So a packet can be 8/8 green while the
page a reviewer has open shows a limit that was corrected two commits ago.

This skill closes that gap. It is the last thing run before the work is handed over.

**The failure it exists to catch:** the config and the audit log get edited late — a
reviewer's note, a corrected amount, a flag promoted to blocking. The viewer was rendered
once, hours earlier. Nothing complains. The reviewer reads the old numbers and signs off
on a configuration that no longer exists.

## Run it

```
python3 .claude/skills/output-audit/scripts/check_output_sync.py                  # every packet
python3 .claude/skills/output-audit/scripts/check_output_sync.py --packet client_a_acme_corp
python3 .claude/skills/output-audit/scripts/check_output_sync.py --fix            # re-render stale viewers
```

**Order matters: run this BEFORE `--verify`, never after.** A green `--verify` re-runs
packaging, which overwrites `deliverables/` from `out/` — erasing exactly the drift this
script is here to report. Audit first, then verify, then re-audit if anything changed.

Exit 0 only when every check passes. A packet with no outputs is reported as not-run and
skipped, not failed — B and E were never run, and the audit should say so out loud rather
than implying five of five are done.

## What the script proves

| Check | Why it is not covered elsewhere |
|---|---|
| graded outputs | both JSONs parse; one present without the other is a half-written packet |
| viewer current | re-renders from the current JSONs and compares bytes |
| renderer version | an upgraded `render_config.py` leaves old pages in circulation |
| deliverables match `out/` | the customer-facing copy is the one that leaves the building |
| client_id agreement | config, audit log and packet directory name the same client |
| affected_config resolves | every section a flag points at is a real config section |

**Freshness is proven by re-rendering, not by timestamps.** A fresh clone stamps every file
with the same checkout mtime, so an mtime comparison would call anything current.
`render_config.py` is deterministic given `(config, audit)`, so any byte-difference against
a fresh render is a stale viewer and nothing else.

`--fix` re-renders stale viewers and **refuses to touch `deliverables/`**. Those are
written by `run_pipeline.py` only after a fully green run; copying an unverified output
into them would break the one guarantee they carry. If deliverables are flagged, fix the
outputs, run `--verify`, and let packaging write them.

## Then read the documents against each other

The script proves the three files were generated from the same data. It cannot prove they
say the same thing. Do this pass by hand, per packet, before signing off:

1. **Every blocking flag still blocks something that exists.** Open each
   `missing_information_flags` entry with `"blocking": true` and find the thing it names in
   the config. A blocking question about a limit that was later deleted is noise; a limit
   that arrived later with the same gap and no flag is the real failure.
2. **Every conflict's `provisional_resolution` is what the config actually did.** This is
   the entry most likely to go stale: the resolution gets revised in the config and the
   audit log keeps describing the first decision. Read the pair, not the entry alone.
3. **Every assumption still has a config field behind it.** An assumption whose field was
   removed is a claim about a configuration nobody is shipping.
4. **The viewer's headline chips read correctly.** Users / programs / limits / audit-entry
   counts and the BLOCKING count are what a reviewer sees first. Confirm the blocking count
   matches the flags you just read.
5. **Counts quoted in prose match the files.** `README.md`, `session/RESUME.md` and any
   NOTES.md state ledger row counts, packet status and check counts. These are written from
   memory and drift silently — re-count them against the files.

Items 1-3 are the coverage invariant read backwards. Phase 4 proves every requirement
reached the config or the audit log; this proves nothing in the audit log points at a piece
of config that has since moved.

## Report

Finish with a written verdict, per packet: script result, the five judgement items, and
anything corrected during the audit. Name what was **not** audited — a packet with no
outputs, a check that was skipped — in the same breath as what passed. An audit that
reports only its passes is the failure mode this whole repo is built against.
