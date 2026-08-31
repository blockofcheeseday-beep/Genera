#!/usr/bin/env python3
"""Check that a finished packet's three artifacts still describe the same thing.

A packet ships three documents that must agree: `out/<packet>/ramp_config.json`,
`out/<packet>/audit_log.json`, and the `work/<packet>/view.html` a reviewer actually
reads. The config and the audit log get edited late — a reviewer's note, a corrected
limit, a flag promoted to blocking — and the viewer is generated once and then quietly
forgotten. `run_pipeline.py --verify` never looks at the viewer, so a packet can be 8/8
green while the page on screen shows last week's numbers.

Freshness is proven by re-rendering, not by timestamps: a fresh clone gives every file
the same checkout mtime, so mtimes here would say "current" about anything. render_config
is deterministic given (config, audit), so a byte-difference against a fresh render is a
stale viewer and nothing else.

  (a) outputs        both graded JSONs exist and parse — a packet missing them is
                     reported as not-run rather than failed
  (b) viewer         present, and byte-identical to a fresh render of the current JSONs
  (c) renderer       the version stamped in the page matches render_config.py's VERSION,
                     so an upgraded renderer does not leave old pages in circulation
  (d) deliverables   the customer-facing copies are byte-identical to out/
  (e) client_id      config, audit log and packet directory all name the same client
  (f) affected_config every section an information flag points at is a real config
                     section — the flag's whole value is that a reader can go look

  python3 check_output_sync.py                      # every packet
  python3 check_output_sync.py --packet client_a_acme_corp
  python3 check_output_sync.py --fix                # re-render stale viewers only

--fix will not touch deliverables/. Those are written by run_pipeline.py only after a
fully green run, and copying an unverified output into them would break that guarantee.

Run this BEFORE `--verify`, not after: a green --verify re-runs packaging, which
overwrites deliverables/ and erases the drift this script exists to report.
"""
import argparse, filecmp, json, pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> output-audit/ -> skills/ -> .claude/ -> repo root
sys.path.insert(0, str(ROOT))
from run_pipeline import client_name  # the out/ -> deliverables/ naming rule, not a second copy of it

PACKETS = ROOT / "candidate" / "customer_packets"
RENDER = ROOT / "candidate" / "tools" / "render_config.py"
SCHEMA = ROOT / "candidate" / "schemas" / "ramp_config_schema.json"
OUT, WORK, DELIVERABLES = ROOT / "out", ROOT / "work", ROOT / "deliverables"
NOTES_HEADING = "<h2>NOTES.md</h2>"


def packets():
    return sorted(p.name for p in PACKETS.iterdir() if p.is_dir()) if PACKETS.is_dir() else []


def rel(p):
    try:
        return str(pathlib.Path(p).resolve().relative_to(ROOT))
    except ValueError:
        return str(p)


def renderer_version():
    m = re.search(r'^VERSION = "([^"]+)"', RENDER.read_text(), re.M)
    return m.group(1) if m else None


def notes_for(packet):
    """The viewer optionally embeds a NOTES.md. Re-render with the same one it was built from."""
    for c in (WORK / packet / "NOTES.md", OUT / packet / "NOTES.md", ROOT / "NOTES.md"):
        if c.is_file():
            return c
    return None


def render(packet, dest, notes=None):
    cmd = [sys.executable, str(RENDER), "--config", str(OUT / packet / "ramp_config.json"),
           "--audit", str(OUT / packet / "audit_log.json"), "--out", str(dest)]
    if notes:
        cmd += ["--notes", str(notes)]
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip()


def check_viewer(packet, fix):
    """Re-render from the current JSONs and compare bytes. Any difference is a stale page."""
    view = WORK / packet / "view.html"
    if not view.exists():
        return [f"{rel(view)}: not rendered — the config and audit log have no reviewable page"]
    current = view.read_text(errors="ignore")
    notes = notes_for(packet) if NOTES_HEADING in current else None
    if NOTES_HEADING in current and notes is None:
        return [f"{rel(view)}: embeds a NOTES.md section but no NOTES.md remains in the repo — "
                f"the page quotes a document that no longer exists"]
    with tempfile.TemporaryDirectory() as td:
        fresh = pathlib.Path(td) / "view.html"
        ok, note = render(packet, fresh, notes)
        if not ok:
            return [f"{rel(view)}: could not re-render from the current outputs — {note.splitlines()[-1] if note else 'no output'}"]
        if filecmp.cmp(view, fresh, shallow=False):
            return []
        if fix:
            view.write_bytes(fresh.read_bytes())
            print(f"      re-rendered {rel(view)}")
            return []
    return [f"{rel(view)}: stale — it does not match a fresh render of the current "
            f"ramp_config.json and audit_log.json; re-render it"]


def check_renderer_version(packet):
    """A page stamped with an older renderer is stale even where its numbers happen to agree."""
    view = WORK / packet / "view.html"
    want = renderer_version()
    if not view.exists() or want is None:
        return []
    m = re.search(r"rendered by render_config v([0-9][^\s<·]*)", view.read_text(errors="ignore"))
    if m is None:
        return [f"{rel(view)}: carries no renderer version stamp"]
    if m.group(1) != want:
        return [f"{rel(view)}: rendered by render_config v{m.group(1)}, but the tool is now "
                f"v{want} — re-render"]
    return []


def check_deliverables(packet):
    """The customer-facing copies are the ones that leave the building; drift there is the
    version a customer reads, and it is invisible from out/."""
    client, fails = client_name(packet), []
    for src, suffix in (("ramp_config.json", "Ramp_Config"), ("audit_log.json", "Audit_Log")):
        dest = DELIVERABLES / client / f"{client}_{suffix}.json"
        if not dest.exists():
            fails.append(f"{rel(dest)}: never packaged — run --verify; packaging fires only on a green run")
        elif not filecmp.cmp(OUT / packet / src, dest, shallow=False):
            fails.append(f"{rel(dest)}: differs from {rel(OUT / packet / src)} — the customer-facing "
                         f"copy is not the verified output")
    return fails


def check_client_id(packet, config, audit):
    fails = []
    for label, doc in (("ramp_config.json", config), ("audit_log.json", audit)):
        got = doc.get("client_id")
        if got != packet:
            fails.append(f"{label}: client_id is {got!r}, but the packet is {packet!r}")
    return fails


def check_affected_config(config, audit):
    """Every section a flag points at must exist in the config schema.

    `affected_config` is the flag's only handle on the config — a reader takes that name
    and goes to look. A section that was renamed, or was never a section at all, sends
    them nowhere, and no schema check catches it because the field is a free string.
    """
    sections = set(json.loads(SCHEMA.read_text()).get("properties", {}))
    fails = []
    for i, flag in enumerate(audit.get("missing_information_flags", [])):
        raw = flag.get("affected_config")
        if not raw:
            continue
        for name in (n.strip() for n in str(raw).split(",")):
            if name and name not in sections:
                fails.append(f"missing_information_flags[{i}]: affected_config names {name!r}, "
                             f"which is not a section of ramp_config.json")
    return fails


def audit_packet(packet, fix):
    """Returns (results, ran) — ran is False for a packet with no outputs to audit."""
    cfg, aud = OUT / packet / "ramp_config.json", OUT / packet / "audit_log.json"
    if not cfg.exists() and not aud.exists():
        return [], False
    docs, missing = {}, []
    for path in (cfg, aud):
        if not path.exists():
            missing.append(f"{rel(path)}: not found — the other graded file exists, so this packet is half-written")
            continue
        try:
            docs[path.name] = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            missing.append(f"{rel(path)}: invalid JSON — {e}")
    if missing:
        return [("graded outputs", missing)], True
    config, audit = docs["ramp_config.json"], docs["audit_log.json"]
    return [("graded outputs", []),
            ("viewer current", check_viewer(packet, fix)),
            ("renderer version", check_renderer_version(packet)),
            ("deliverables match out/", check_deliverables(packet)),
            ("client_id agreement", check_client_id(packet, config, audit)),
            ("affected_config resolves", check_affected_config(config, audit))], True


def main():
    ap = argparse.ArgumentParser(description="Audit config / audit-log / viewer agreement.")
    ap.add_argument("--packet", help="one packet; default is every packet with outputs")
    ap.add_argument("--fix", action="store_true", help="re-render stale viewers (never touches deliverables/)")
    args = ap.parse_args()

    names = [args.packet] if args.packet else packets()
    if args.packet and args.packet not in packets():
        print(f"no such packet: {args.packet}\navailable: {', '.join(packets())}")
        return 1

    failed, not_run = [], []
    for name in names:
        results, ran = audit_packet(name, args.fix)
        if not ran:
            not_run.append(name)
            continue
        print(f"\n{name}")
        for label, fails in results:
            print(f"  {'FAIL' if fails else 'PASS'}  {label} ({len(fails)} problem(s))")
            for f in fails:
                print(f"        - {f}")
            if fails:
                failed.append(f"{name}: {label}")

    print(f"\n{len(names) - len(not_run)} packet(s) audited, {len(failed)} check(s) failed")
    if not_run:
        print(f"  no outputs, not audited: {', '.join(not_run)}")
    for f in failed:
        print(f"  FAIL {f}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
