#!/usr/bin/env python3
"""Cross-check requirements, traceability, and the audit log against the ledger.

Four failure modes this catches, all of them explicitly graded:
  (a) coverage      — a requirement that reached neither the config nor the audit log,
                      or a traceability entry citing a requirement that does not exist.
  (b) false positive— telling the customer the API cannot do something the ledger says
                      is SUPPORTED. Over-claiming gaps is as wrong as missing them.
  (c) false negative— a PARTIAL / UI_ONLY / UNSUPPORTED ask quietly written into the
                      config with nothing in the audit log to warn the human.
  (d) evidence      — an unsupported_api_requests entry with undated evidence.

  python3 check_coverage.py --packet client_a_acme_corp [--repo /path/to/repo]

Every check runs; all failures are reported. Exit 1 if any check fails.
"""
import sys, json, re, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
LEDGER = ".claude/skills/ramp-deployment/references/capabilities.yaml"
NEEDS_AUDIT = {"UNSUPPORTED", "UI_ONLY", "PARTIAL"}
# A year, not just any 4-digit number, and not tripped up by "2026_08_30".
YEAR = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")


def check_coverage(reqs, entries):
    """(a) Every requirement lands somewhere; every entry points at a real requirement."""
    fails = []
    landed = {e["req_id"] for e in entries if e.get("config_paths") or e.get("audit_refs")}
    for r in reqs:
        if r["req_id"] not in landed:
            fails.append(f"{r['req_id']} orphaned — no config_path and no audit_ref")
    known = {r["req_id"] for r in reqs}
    for e in entries:
        if e["req_id"] not in known:
            fails.append(f"{e['req_id']} traced but not in requirements.json")
    return fails


def check_false_positives(entries, verdicts):
    """(b) Never file a SUPPORTED capability as an unsupported API request."""
    fails = []
    for e in entries:
        if not any(a.startswith("unsupported_api_requests[") for a in e.get("audit_refs", [])):
            continue
        aid = e.get("archetype_id")
        if aid is None:
            print(f"  warn: {e['req_id']} has no archetype_id — cannot check false positive")
        elif verdicts.get(aid) == "SUPPORTED":
            fails.append(f"{e['req_id']} calls {aid} unsupported, but the ledger says SUPPORTED")
    return fails


def check_false_negatives(entries, verdicts):
    """(c) Anything less than fully supported must leave a trace in the audit log."""
    fails = []
    for e in entries:
        if not e.get("config_paths") or e.get("audit_refs"):
            continue
        aid = e.get("archetype_id")
        if aid is None:
            print(f"  warn: {e['req_id']} has no archetype_id — cannot check false negative")
        elif verdicts.get(aid) in NEEDS_AUDIT:
            fails.append(f"{e['req_id']} configures {aid} ({verdicts[aid]}) with nothing in the audit log")
    return fails


def check_evidence(audit):
    """(d) Evidence must be present and dated — a bare assertion is not evidence."""
    fails = []
    for i, u in enumerate(audit.get("unsupported_api_requests", [])):
        ev = (u.get("evidence") or "").strip()
        if not ev:
            fails.append(f"unsupported_api_requests[{i}] has empty evidence")
        elif not YEAR.search(ev):
            fails.append(f"unsupported_api_requests[{i}] evidence carries no date: {ev[:60]!r}")
    return fails


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    root = pathlib.Path(arg("--repo", ROOT))
    packet = arg("--packet")
    if not packet:
        print("usage: check_coverage.py --packet <packet_name> [--repo <path>]")
        return 1

    needed = [f"work/{packet}/requirements.json", f"work/{packet}/traceability.json",
              f"out/{packet}/audit_log.json", LEDGER]
    for rel in needed:
        if not (root / rel).is_file():
            print(f"missing: {root / rel}")
            return 1
    reqs = json.loads((root / needed[0]).read_text())["requirements"]
    entries = json.loads((root / needed[1]).read_text())["entries"]
    audit = json.loads((root / needed[2]).read_text())
    ledger = yaml.safe_load((root / LEDGER).read_text())
    verdicts = {c["id"]: c["verdict"] for c in ledger["capabilities"]}

    results = [("coverage invariant", check_coverage(reqs, entries)),
               ("false-positive sweep", check_false_positives(entries, verdicts)),
               ("false-negative sweep", check_false_negatives(entries, verdicts)),
               ("evidence completeness", check_evidence(audit))]

    for name, fails in results:
        print(f"{'FAIL' if fails else 'PASS'}  {name} ({len(fails)} problem(s))")
        for f in fails:
            print(f"      - {f}")
    return 1 if any(f for _, f in results) else 0


if __name__ == "__main__":
    sys.exit(main())
