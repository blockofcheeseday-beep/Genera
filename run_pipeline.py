#!/usr/bin/env python3
"""Single entry point for one Ramp deployment packet.

The pipeline is agent-driven on purpose: Python does the deterministic setup
(Phase 0) and the deterministic checking (--verify); the Claude session does the
judgement in between — reading messy transcripts, resolving conflicts, deciding
what Ramp cannot do. This script never writes config or audit content itself.

  python3 run_pipeline.py --list
  python3 run_pipeline.py --packet client_a_acme_corp            # setup + runbook
  python3 run_pipeline.py --packet client_a_acme_corp --verify   # gate the outputs
"""
import argparse, hashlib, json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
PACKETS = ROOT / "candidate" / "customer_packets"
SCRIPTS = ROOT / ".claude" / "skills" / "ramp-deployment" / "scripts"
VALIDATE = ROOT / "candidate" / "tools" / "validate.py"
WORK, OUT = ROOT / "work", ROOT / "out"
DELIVERABLES = ROOT / "deliverables"
NA = "N/A"   # the only permitted stand-in for an unknown identifier
SKILL = ".claude/skills/ramp-deployment/SKILL.md"
SECTIONS = ("entities, departments, locations, users, spend_programs, "
            "limits, approval_policies, mcc_controls")


def packets():
    return sorted(p for p in PACKETS.iterdir() if p.is_dir()) if PACKETS.is_dir() else []


def resolve(arg):
    """Accept a bare packet name or any path form; return the packet directory."""
    cand = pathlib.Path(arg).expanduser()
    for p in (cand, (ROOT / cand), (PACKETS / cand.name)):
        if p.is_dir() and (p.resolve().parent == PACKETS.resolve()):
            return p.resolve()
    return None


def rel(path):
    try:
        return str(pathlib.Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return str(path)


def file_facts(path):
    data = path.read_bytes()
    return {"filename": path.name, "bytes": len(data),
            "lines": data.count(b"\n") + (0 if data.endswith(b"\n") or not data else 1),
            "sha256_12": hashlib.sha256(data).hexdigest()[:12]}


def write_manifest(pkt):
    files = [file_facts(f) for f in sorted(pkt.iterdir()) if f.is_file()]
    manifest = {"packet": pkt.name, "packet_dir": rel(pkt), "file_count": len(files), "files": files}
    dest = WORK / pkt.name / "packet_manifest.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    (OUT / pkt.name).mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest, dest


def runbook(pkt, manifest, dest):
    name = pkt.name
    rows = [f"  {f['filename']:<34} {f['bytes']:>6} B {f['lines']:>5} lines  sha {f['sha256_12']}"
            for f in manifest["files"]]
    for f in manifest["files"]:
        if f["filename"].lower().endswith(".csv"):
            rows += ["  ^ CSV — lint it before Phase 1 and fold the findings into Phase 2:",
                     f"      python3 {rel(SCRIPTS / 'lint_roster.py')} {rel(pkt / f['filename'])} --json"]
    return f"""
{'=' * 78}
RAMP DEPLOYMENT RUNBOOK — {name}
{'=' * 78}
packet    {rel(pkt)}
manifest  {rel(dest)}   ({manifest['file_count']} files)
work dir  {rel(WORK / name)}/          out dir  {rel(OUT / name)}/

Full instructions: {SKILL}   (read it — this runbook is the mechanical spine only)
Ledger:            .claude/skills/ramp-deployment/references/CAPABILITY_LEDGER.md
Schemas:           candidate/schemas/{{ramp_config,audit_log}}_schema.json
Worked example:    candidate/sample_packet/client_0_sample_westbrook/example_output/

Rule that outranks the rest: never invent. Every claim traces to a packet quote or
a ledger row. When the packet does not say, that is a flag, not a default.

PACKET FILES
{chr(10).join(rows)}

PHASE 1 — EXTRACT  ->  {rel(WORK / name)}/requirements.json
  Read every file above start to finish; do not skim or sample. For each thing the
  customer asks for, append one entry:
    {{"req_id": "REQ-001", "claim": "...", "source_file": "<filename as listed above>",
      "source_quote": "<verbatim substring of that file>",
      "archetype_id": "<closest ledger row id, or null>", "confidence": "high|medium|low"}}
  Copy source_quote AT EXTRACTION TIME, character for character. Reconstructing a
  quote later is how citations get hallucinated; check_quotes.py fails anything that
  is not present verbatim in the file it cites.
  File shape: {{"packet": "{name}", "requirements": [ ... ]}}

PHASE 2 — FLAG  ->  {rel(OUT / name)}/audit_log.json   (BEFORE the config, deliberately)
  Flags first so the config is composed downstream of them, instead of becoming a
  rationalization of a config you already wrote. Four trigger classes, four arrays:
    assumptions_made          you filled a gap the packet never stated
    missing_information_flags you need an answer from the customer (set "blocking")
    conflicts                 two packet sources disagree — cite both sides
    unsupported_api_requests  ledger verdict UNSUPPORTED / UI_ONLY / PARTIAL
  For unsupported_api_requests, "evidence" is the ledger row's `evidence_line` copied
  VERBATIM — it carries the dated source, and verbatim reuse is what keeps separate
  audit logs consistent instead of each re-arguing the same point. Do not paraphrase.
  client_id = "{name}". Schema: candidate/schemas/audit_log_schema.json

PHASE 3 — COMPOSE  ->  {rel(OUT / name)}/ramp_config.json
  Walk the eight sections in schema order, deciding each explicitly (an empty array
  is a real answer when the packet has none):
    {SECTIONS}
  limits[].assigned_to carries EXACTLY ONE of user_email or group. The shipped schema
  describes that but cannot enforce it — --verify does.
  Then  ->  {rel(WORK / name)}/traceability.json, one entry per req_id, none skipped:
    {{"packet": "{name}", "entries": [{{"req_id": "REQ-001", "archetype_id": null,
      "disposition": "config|audit|both", "config_paths": [...], "audit_refs": [...]}}]}}

PHASE 4 — VERIFY
    python3 run_pipeline.py --packet {name} --verify
  Fix what it reports and re-run until every row is PASS. Only ramp_config.json and
  audit_log.json belong in {rel(OUT / name)}/ — intermediates stay in work/.
{'=' * 78}
"""


def run(cmd):
    """Run a sibling script; return (ok, combined output). Missing script -> None."""
    if not pathlib.Path(cmd[1]).exists():
        return None, f"missing: {rel(cmd[1])}"
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def load_outputs(name):
    """Check 1: both graded files exist and parse. Returns (ok, note, config)."""
    config, problems = None, []
    for fname in ("ramp_config.json", "audit_log.json"):
        path = OUT / name / fname
        if not path.exists():
            problems.append(f"{fname}: not found")
            continue
        try:
            parsed = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            problems.append(f"{fname}: invalid JSON — {e}")
            continue
        if fname == "ramp_config.json":
            config = parsed
    return (not problems), "; ".join(problems) or "both present and parse", config


def check_cross_refs(cfg):
    """Names that must point at something this config actually emits.

    Every one of these is a valid string to the schema, so validation passes while the
    config quietly refers to a department, program or manager that does not exist. A
    case-normalizer that turns "IT" into "It" is the way this happens in practice.
    """
    if not isinstance(cfg, dict):
        return None, "skipped — ramp_config.json unreadable"
    depts = {d.get("name") for d in cfg.get("departments", [])}
    progs = {p.get("display_name") for p in cfg.get("spend_programs", [])}
    lims = {l.get("display_name") for l in cfg.get("limits", [])}
    users = {u.get("email") for u in cfg.get("users", [])}
    bad = []
    for i, u in enumerate(cfg.get("users", [])):
        if u.get("department") not in depts:
            bad.append(f"users[{i}] department {u.get('department')!r} is not in departments[]")
        m = u.get("direct_manager_email")
        if m and m != NA and m not in users:
            bad.append(f"users[{i}] direct_manager_email {m!r} is not a user in this config")
    for i, m in enumerate(cfg.get("mcc_controls", [])):
        if m.get("applies_to") not in progs | lims:
            bad.append(f"mcc_controls[{i}] applies_to {m.get('applies_to')!r} names no program or limit")
    for i, l in enumerate(cfg.get("limits", [])):
        sp = l.get("spend_program")
        if sp and sp not in progs:
            bad.append(f"limits[{i}] spend_program {sp!r} names no spend program")
    if bad:
        return False, "\n".join("FAIL " + b for b in bad)
    return True, f"{len(cfg.get('users', []))} users, {len(cfg.get('mcc_controls', []))} mcc_controls all resolve"


def check_invented_identifiers(config, packet_dir):
    """No email may be invented. An address that looks real gets used.

    A placeholder like alice.smith@company.example is indistinguishable from a real
    address to whoever runs the deployment, and inviting it either fails silently or
    reaches a stranger. The test is mechanical: every domain must actually appear
    somewhere in the customer's own documents. Where an address is unknown, the config
    says so with the literal N/A rather than guessing a plausible one.
    """
    if not isinstance(config, dict):
        return None, "skipped — ramp_config.json unreadable"
    src = "".join(f.read_text(errors="ignore") for f in packet_dir.iterdir() if f.is_file())
    bad, checked = [], 0
    def audit(where, addr):
        nonlocal checked
        if not addr or addr == NA:
            return
        checked += 1
        dom = addr.rsplit("@", 1)[-1]
        if "@" not in addr or dom not in src:
            bad.append(f"{where}: {addr!r} — domain not found in the packet; use {NA} if unknown")
    for i, u in enumerate(config.get("users", [])):
        audit(f"users[{i}].email", u.get("email"))
        audit(f"users[{i}].direct_manager_email", u.get("direct_manager_email"))
    for i, l in enumerate(config.get("limits", [])):
        audit(f"limits[{i}].assigned_to.user_email", (l.get("assigned_to") or {}).get("user_email"))
    if bad:
        return False, "\n".join("FAIL " + b for b in bad)
    return True, f"{checked} address(es) trace to the packet; the rest declared {NA}"


def check_assigned_to(config):
    """Check 5: exactly one of user_email / group per limit. The validator misses this."""
    bad = []
    for i, limit in enumerate(config.get("limits") or []):
        keys = [k for k in ("user_email", "group") if (limit.get("assigned_to") or {}).get(k)]
        if len(keys) != 1:
            label = limit.get("display_name", "?")
            bad.append(f"limits[{i}] ({label}): {'neither set' if not keys else 'both set: ' + ', '.join(keys)}")
    return (not bad), "; ".join(bad) or f"{len(config.get('limits') or [])} limits, each assigned exactly once"


def client_name(packet):
    """client_a_acme_corp -> Acme_Corp.

    The graded filenames in out/ are fixed by the exercise spec. These are the
    customer-facing copies, so they carry the customer's name rather than the
    exercise's packet id.
    """
    stem = re.sub(r"^client_[0-9a-z]_", "", packet)
    return "_".join(w.capitalize() for w in stem.split("_"))


def package(name):
    """Copy the verified outputs to deliverables/ under customer-facing names.

    out/ keeps the canonical ramp_config.json / audit_log.json the spec asks for, so
    grading tooling still finds them. This runs only after every check passes, so a
    deliverable can never be a copy of output that failed verification.
    """
    client = client_name(name)
    dest = DELIVERABLES / client
    dest.mkdir(parents=True, exist_ok=True)
    written = []
    for src, suffix in (("ramp_config.json", "Ramp_Config"), ("audit_log.json", "Audit_Log")):
        target = dest / f"{client}_{suffix}.json"
        shutil.copyfile(OUT / name / src, target)
        written.append(target)
    return written


def verify(pkt):
    name, rows = pkt.name, []
    outs_ok, outs_note, config = load_outputs(name)
    rows.append(("outputs exist", outs_ok, outs_note))

    cfg, aud = OUT / name / "ramp_config.json", OUT / name / "audit_log.json"
    if outs_ok:
        rows.append(("schema validation", *run([sys.executable, str(VALIDATE), str(cfg), str(aud)])[:2]))
    else:
        rows.append(("schema validation", None, "skipped — outputs missing or unparseable"))

    for label, script in (("quote fidelity", "check_quotes.py"),
                          ("coverage + sweeps", "check_coverage.py"),
                          ("audit log style", "check_audit_style.py")):
        rows.append((label, *run([sys.executable, str(SCRIPTS / script), "--packet", name])[:2]))

    if config is None:
        rows.append(("assigned_to exactly-one", None, "skipped — ramp_config.json unreadable"))
    else:
        rows.append(("assigned_to exactly-one", *check_assigned_to(config)))

    rows.append(("config cross-references", *check_cross_refs(config)))
    rows.append(("no invented identifiers", *check_invented_identifiers(config, pkt)))
    rows.append(("ledger freshness", *run([sys.executable, str(SCRIPTS / "gen_ledger.py"), "--check"])[:2]))

    print(f"\nVERIFY {name}")
    width = max(len(r[0]) for r in rows)
    for i, (label, ok, note) in enumerate(rows, 1):
        status = "SKIP" if ok is None else ("PASS" if ok else "FAIL")
        lines = note.splitlines() or [""]
        # On failure show the first line that actually reports one — the first line of a
        # multi-file check is often a PASS ("OK ramp_config.json") and reads as a lie
        # next to a FAIL status.
        if ok is False:
            lines = [l for l in lines if l.lstrip().startswith(("FAIL", "-", "missing"))] or lines
        head = lines[0][:200]
        print(f"  {i}. {label:<{width}}  {status}  {head}")
    for label, ok, note in rows:
        if ok is False and len(note.splitlines()) > 1:
            print(f"\n--- {label} ---\n{note}")
    failed = [r[0] for r in rows if r[1] is False]
    skipped = [r[0] for r in rows if r[1] is None]
    print(f"\n{len(rows) - len(failed) - len(skipped)} passed, {len(failed)} failed, {len(skipped)} skipped")
    if failed:
        print("failed: " + ", ".join(failed))
    if failed or skipped:
        print("  not packaged — deliverables/ is written only from a fully green run")
    else:
        for f in package(name):
            print(f"  packaged  {rel(f)}")
    return 1 if failed else 0


def main():
    ap = argparse.ArgumentParser(description="Run one Ramp deployment packet end to end.")
    ap.add_argument("--packet", help="packet name or path, e.g. client_a_acme_corp")
    ap.add_argument("--verify", action="store_true", help="check the outputs instead of printing the runbook")
    ap.add_argument("--list", action="store_true", help="list available packets")
    args = ap.parse_args()

    if args.list or not args.packet:
        for p in packets():
            print(f"  {p.name:<28} {sum(1 for f in p.iterdir() if f.is_file())} files")
        if not args.list:
            print("\nnothing to do — pass --packet <name>")
            return 1
        return 0

    pkt = resolve(args.packet)
    if pkt is None:
        print(f"no such packet: {args.packet}\navailable:")
        for p in packets():
            print(f"  {p.name}")
        return 1

    if args.verify:
        return verify(pkt)
    manifest, dest = write_manifest(pkt)
    print(runbook(pkt, manifest, dest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
