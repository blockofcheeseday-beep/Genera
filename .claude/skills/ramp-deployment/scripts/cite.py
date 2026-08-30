#!/usr/bin/env python3
"""Build one verifiable audit-log citation from a packet file, so nobody writes a fourth one.

check_audit_style.py gates every `source` field in audit_log.json: it must name a real packet
file, carry a verbatim quoted span of 15+ characters, and attribute it to a speaker name or a
row/line locator -- a bare timestamp is exactly the case the customer rejected. That gate
shipped with no tool behind it, so the first two packets each grew a throwaway quote-finder,
written from scratch and thrown away; a fresh session on an unseen packet would write a third.
This is the permanent one. It folds text the way the gate folds it, so a quote typed with ASCII
punctuation still matches curly-quoted source, and it never invents attribution: a quote that
is not in the packet exits 1 rather than being dressed up as a citation.

Packet formats differ -- attendee-block transcripts, Slack exports, markdown notes, numbered
memos, CSV rosters -- and the next packet is unseen, so attribution degrades in steps: speaker
if a header roster names one, else document owner plus section, else a bare line number. A line
number alone already satisfies the gate, so an unknown format still yields a VALID citation.

  python3 cite.py --packet client_a_acme_corp --quote "Priya and me" --context "naming admins"
  python3 cite.py --packet client_d_hypergrowth --speakers          [--repo /path/to/repo]
  from cite import cite, locate, packet_speakers   # the pipeline imports; it does not shell out

Exit 0 on one hit, 1 if not found, 2 if ambiguous (every match is printed with its location).
"""
import sys, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
FOLD = {"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"',
        "„": '"', "–": "-", "—": "-", "−": "-", "…": "..."}
HEADER = 12          # a roster or a document owner sits in the first few lines or nowhere
# "  - Diane Marsh, VP Finance, Acme Corp (DM)" / "... Genera (on behalf of Ramp) (JL)"
ATTENDEE = re.compile(r"^\s*[-*]\s*(?P<name>[^,]+),\s*(?P<role>.*?)\s*(?:\([^()]*\)\s*)*"
                      r"\(\s*(?P<key>[A-Z]{2,4})\s*\)\s*$")
MEMBERS = re.compile(r"(?P<key>[a-z0-9][\w.-]*)\s*\((?P<role>[^()]+)\)")  # Slack "Members:" header
TURN = re.compile(r"^\[(?P<ts>[^\]]{2,40})\]\s*(?P<key>[A-Za-z][\w.@-]{0,30}):\s")
OWNER = re.compile(r"^\s*(?:document owner|owner|prepared by|preparad[oa] por|elaborado por)"
                   r"\s*:\s*(?P<who>.+?)\s*$", re.I)
APPROVER = re.compile(r"approved by\s+(?P<who>[^—;(]+)", re.I)
SECTION = re.compile(r"^\s*(?P<num>\d+(?:\.\d+)+)[\s)]")    # a memo subsection "5.3", not "REQ-4"
BREAK = re.compile(r"^[=*_~-]{4,}\s*$")
NAMELIKE = re.compile(r"\b[A-Z][a-z]+ [A-Z][A-Za-z'-]+\b")  # the gate's own SPEAKER test


def fold(text):
    """The gate's norm(): punctuation folded, whitespace collapsed -- plus each char's line."""
    out, lines, line, gap = [], [], 1, False
    for ch in unicodedata.normalize("NFC", text):
        if ch.isspace():
            gap, line = bool(out), line + (ch == "\n")
            continue
        if gap:
            out.append(" "), lines.append(line)
            gap = False
        for c in FOLD.get(ch, ch):
            out.append(c), lines.append(line)
    return "".join(out), lines


def norm(text):
    return fold(text)[0]


def titleize(handle):
    """rachel.kim -> Rachel Kim. A handle with no separator is left alone, not dressed up."""
    return " ".join(p.capitalize() for p in re.split(r"[._]", handle)) if re.search(r"[._]", handle) else handle


def speaker_map(text):
    """key -> display name, from whichever header roster the file happens to carry."""
    head, out = text.splitlines()[:HEADER], {}
    for line in head:
        m = ATTENDEE.match(line)
        if m:
            out[m.group("key")] = f"{m.group('name').strip()} ({m.group('role').strip()})"
    for i, line in enumerate(head):
        if out or not re.match(r"\s*members\s*:", line, re.I):
            continue
        block = []
        while i < len(head) and head[i].strip():
            block.append(head[i])
            i += 1
        for m in MEMBERS.finditer(" ".join(block)):
            out[m.group("key")] = f"{titleize(m.group('key'))} ({m.group('role').strip()})"
    return out


def turn_at(lines, idx):
    """(speaker key, timestamp) of the turn containing line idx, or None if it is not in one."""
    for j in range(idx, -1, -1):
        if not lines[j].strip():
            return None            # a blank line means we are between turns, not inside one
        m = TURN.match(lines[j])
        if m:
            return m.group("key"), m.group("ts")
    return None


def section_at(lines, idx):
    """Nearest numbered subsection above line idx, preferred over a bare line number."""
    for j in range(idx, max(-1, idx - 15), -1):
        if BREAK.match(lines[j]):
            return None
        m = SECTION.match(lines[j])
        if m:
            return m.group("num")
    return None


def person(who):
    """'M. Vance, Director of Compliance' -> 'M. Vance (Director of Compliance)'."""
    who = who.strip().rstrip(".")
    if "(" in who and ")" in who:
        return who[:who.index(")") + 1].strip()          # role already parenthesised; keep it
    name, _, role = who.partition(",")
    return f"{name.strip()} ({role.strip()})" if role.strip() else name.strip()


def header_attribution(lines):
    """'document owner X (role), approved by Y' -- what makes a memo as checkable as a call."""
    bits, head = [], lines[:HEADER]
    owner = next((OWNER.match(l) for l in head if OWNER.match(l)), None)
    approver = next((APPROVER.search(l) for l in head if APPROVER.search(l)), None)
    if owner:
        bits.append("document owner " + person(owner.group("who")))
    if approver:
        bits.append("approved by " + approver.group("who").strip().rstrip(".,"))
    return ", ".join(bits)


def citation(path, text, ln, quote, context=""):
    """Assemble one citation: file, the best attribution available, context, verbatim quote."""
    lines, is_csv = text.splitlines(), path.suffix.lower() == ".csv"
    turn = None if is_csv else turn_at(lines, ln - 1)
    if is_csv:                              # cite the whole row; row 1 is the header row
        prefix, parts, quote = f"{path.name}, row {ln} — ", [], lines[ln - 1].strip()
    elif turn:
        who = speaker_map(text).get(turn[0]) or titleize(turn[0])
        # A handle the gate would not read as a name still needs a locator to count as attribution.
        prefix = f"{path.name} — " if NAMELIKE.search(who) else f"{path.name}, line {ln} — "
        parts = [who, f"[{turn[1]}]"]
    else:
        sec = section_at(lines, ln - 1)
        prefix = f"{path.name}, section {sec} (line {ln}) — " if sec else f"{path.name}, line {ln} — "
        parts = [b for b in [header_attribution(lines)] if b]
    parts += [context] if context else []
    return prefix + ", ".join(parts) + (": " if parts else "") + f'"{quote}"'


def packet_files(packet, repo=None):
    d = pathlib.Path(repo or ROOT) / "candidate" / "customer_packets" / packet
    if not d.is_dir():
        raise FileNotFoundError(f"no such packet: {d}")
    return sorted(p for p in d.iterdir() if p.is_file())


def read(path):
    return path.read_text(encoding="utf-8", errors="replace")


def locate(packet, quote, repo=None):
    """[(path, line)] for every occurrence of quote in the packet, folded as the gate folds."""
    needle, hits = norm(quote), []
    if not needle:
        raise ValueError("empty quote")
    for path in packet_files(packet, repo):
        folded, lineno = fold(read(path))
        i = folded.find(needle)
        while i >= 0:
            hits.append((path, lineno[i]))
            i = folded.find(needle, i + 1)
    return hits


def cite(packet, quote, context="", repo=None):
    """The citation for a quote that occurs exactly once. Never returns a guess."""
    hits = locate(packet, quote, repo)
    if not hits:
        raise LookupError(f"quote not found in {packet}: {norm(quote)[:60]!r}")
    rendered = [citation(p, read(p), ln, quote, context) for p, ln in hits]
    if len(hits) > 1:
        raise ValueError(f"quote occurs {len(hits)} times; quote a longer span:\n  " + "\n  ".join(rendered))
    return rendered[0]


def packet_speakers(packet, repo=None):
    """file -> speaker map, so a human can check the parse before trusting 30 citations to it."""
    return {p.name: speaker_map(read(p)) for p in packet_files(packet, repo)}


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    packet, quote, repo = arg("--packet"), arg("--quote"), arg("--repo")
    if not packet or not (quote or "--speakers" in sys.argv):
        print('usage: cite.py --packet <packet> --quote "<text>" [--context "<clause>"] [--repo <path>]\n'
              "       cite.py --packet <packet> --speakers")
        return 1
    try:
        if "--speakers" in sys.argv:
            for name, speakers in packet_speakers(packet, repo).items():
                print(name)
                for key, who in speakers.items():
                    print(f"    {key:<16} {who}")
                if not speakers:
                    print("    (no speaker roster -- citations fall back to section/line numbers)")
            return 0
        hits = locate(packet, quote, repo)
    except (FileNotFoundError, ValueError) as e:
        print(e)
        return 1
    if not hits:
        print(f"NOT FOUND in {packet}: {norm(quote)[:70]!r}\n"
              "No citation written -- check the wording against the source file.")
        return 1
    for path, ln in hits:
        print(citation(path, read(path), ln, quote, arg("--context", "")))
    if len(hits) > 1:
        print(f"\nAMBIGUOUS: {len(hits)} matches (shown above). Quote a longer span to pin one down.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
