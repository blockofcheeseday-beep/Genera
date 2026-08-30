#!/usr/bin/env python3
"""Hold out/<packet>/audit_log.json to the standard the customer reads it at.

The audit log is not an internal artifact: Acme Corp's finance team reads it verbatim, and
their review of the first packet raised three real defects. Each check exists so that
defect cannot ship again, on this packet or any other.

  (a) pronouns  — "he should not see anyone else's spend" left the reviewer guessing who
                  "he" was. Name the person or the role, never a pronoun. One exception: a
                  `source` field carries a VERBATIM customer quote, and the customer's own
                  words are not ours to sanitize, so text inside quotation marks there is
                  exempt while everything around it is still checked.
  (b) jargon    — internal row IDs (CAP-*, DRIFT-*), pipeline vocabulary (req_id, archetype,
                  traceability, the capability ledger) and implementation slang ("fans out")
                  mean nothing to a customer and leak how the sausage is made. Banned
                  everywhere, quotes included.
  (c) citations — "discovery_call_01.txt — 'Priya and me.' [05:41]" was rejected as useless:
                  the reader cannot tell who "me" is or why that line supports the
                  assumption. A citation must name a real packet file, quote it verbatim at
                  useful length, and say who said it or where in the file it sits. A bare
                  timestamp is not attribution — that is the case the customer rejected.
  (d) ordering  — blocking flags come before non-blocking ones, so a reader who stops after
                  the first few has still seen everything that blocks go-live.
  (e) evidence  — an unsupported-API claim with undated evidence is unverifiable.

  python3 check_audit_style.py --packet client_a_acme_corp [--repo /path/to/repo]

Every check runs; all failures are reported. Exit 0 only if all five pass.
"""
import sys, json, re, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
ARRAYS = ("assumptions_made", "missing_information_flags", "conflicts", "unsupported_api_requests")
CITED = {"assumptions_made": ("source",), "conflicts": ("source_a", "source_b")}
PRONOUN = re.compile(r"\b(?:he|she|his|her|hers|him|they|them|their|theirs)\b", re.I)
# A quoted span. An apostrophe inside a word ("else's") must not close a single-quoted span.
QUOTED = re.compile(r"\"[^\"]*\"|(?<![A-Za-z])'.*?'(?![A-Za-z])", re.S)
JARGON = [re.compile(p, re.I) for p in (
    r"\bCAP-[A-Z][A-Z-]*", r"\bDRIFT-[A-Z][A-Z-]*", r"\breq_id\b", r"\bREQ-\d+\b",
    r"\barchetypes?\b", r"\btraceability\b", r"\bcapability ledger\b", r"\bthe ledger\b",
    r"\bfans out\b", r"\bfan[- ]out\b")]
SPEAKER = re.compile(r"\b[A-Z][a-z]+ [A-Z][A-Za-z'-]+\b")       # Priya Shetty
LOCATOR = re.compile(r"\b(?:row|line)s?\s+\d+\b", re.I)          # row 12 / line 47
FILENAME = re.compile(r"[A-Za-z0-9_.-]+\.[A-Za-z0-9]{2,5}\b")
YEAR = re.compile(r"(?<!\d)(19|20)\d{2}(?!\d)")  # not \b\d{4}\b: that fires on 2026_08_30 and on 5000
FOLD = {"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"',
        "„": '"', "–": "-", "—": "-", "−": "-", "…": "..."}


def norm(text):
    """Fold unicode punctuation to ASCII and collapse whitespace. Case is preserved."""
    text = unicodedata.normalize("NFC", text)
    return " ".join("".join(FOLD.get(ch, ch) for ch in text).split())


def strings(audit):
    """Yield (array, index, field, value) for every string in the four audit arrays."""
    for name in ARRAYS:
        for i, entry in enumerate(audit.get(name) or []):
            for field, value in (entry or {}).items():
                if isinstance(value, str):
                    yield name, i, field, value


def unquoted(text):
    """text with every quoted span blanked out."""
    return QUOTED.sub(" ", text)


def spans(text):
    """The contents of each quoted span in text."""
    return [m.group(0)[1:-1] for m in QUOTED.finditer(text)]


def context(text, m, width=40):
    """About `width` characters around a match, so the offending sentence is findable."""
    return "..." + norm(text[max(0, m.start() - width // 2):m.end() + width // 2]) + "..."


def check_pronouns(audit):
    """(a) No third-person pronouns — except inside a verbatim quote in a source field."""
    fails = []
    for name, i, field, value in strings(audit):
        haystack = unquoted(value) if field.startswith("source") else value
        for m in PRONOUN.finditer(haystack):
            fails.append(f"{name}[{i}].{field}: pronoun {m.group(0)!r} in {context(haystack, m)}")
    return fails


def check_jargon(audit):
    """(b) Internal vocabulary must never reach the customer, quotes included."""
    fails = []
    for name, i, field, value in strings(audit):
        for pattern in JARGON:
            for m in pattern.finditer(value):
                fails.append(f"{name}[{i}].{field}: internal term {m.group(0)!r} in {context(value, m)}")
    return fails


def check_citations(audit, packet_dir):
    """(c) Every source citation names a real file, quotes it verbatim, and attributes it."""
    fails, cache = [], {}
    for name, i, field, value in strings(audit):
        if field not in CITED.get(name, ()):
            continue
        outside = unquoted(value)
        named = [f for f in FILENAME.findall(outside) if (packet_dir / f).is_file()]
        if not named:
            fails.append(f"{name}[{i}].{field}: names no file in {packet_dir.name}/ — {norm(value)[:70]!r}")
            continue
        if named[0] not in cache:
            cache[named[0]] = norm((packet_dir / named[0]).read_text())
        long_spans = [m.group(0)[1:-1] for m in QUOTED.finditer(value) if len(m.group(0)[1:-1].strip()) >= 15]
        if not long_spans:
            fails.append(f"{name}[{i}].{field}: no quoted span of 15+ characters — {norm(value)[:70]!r}")
        elif not any(norm(s) in cache[named[0]] for s in long_spans):
            fails.append(f"{name}[{i}].{field}: quote not verbatim in {named[0]} — {norm(long_spans[0])[:70]!r}")
        if not SPEAKER.search(outside) and not LOCATOR.search(outside):
            fails.append(f"{name}[{i}].{field}: no speaker name or row/line locator outside the "
                         f"quote (a timestamp alone is not attribution) — {norm(value)[:70]!r}")
    return fails


def check_flag_order(audit):
    """(d) Blocking flags first, so a reader who stops early has seen every blocker."""
    flags = audit.get("missing_information_flags") or []
    seen_non_blocking = None
    for i, flag in enumerate(flags):
        if not flag.get("blocking"):
            seen_non_blocking = i if seen_non_blocking is None else seen_non_blocking
        elif seen_non_blocking is not None:
            return [f"missing_information_flags[{i}] is blocking but follows non-blocking "
                    f"entry [{seen_non_blocking}] — move blocking flags first"]
    return []


def check_evidence(audit):
    """(e) Evidence must be present and dated — a bare assertion is not evidence."""
    fails = []
    for i, u in enumerate(audit.get("unsupported_api_requests") or []):
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
        print("usage: check_audit_style.py --packet <packet_name> [--repo <path>]")
        return 1

    audit_json = root / "out" / packet / "audit_log.json"
    packet_dir = root / "candidate" / "customer_packets" / packet
    for path in (audit_json, packet_dir):
        if not path.exists():
            print(f"missing: {path}")
            return 1
    audit = json.loads(audit_json.read_text())

    results = [("third-person pronouns", check_pronouns(audit)),
               ("internal jargon", check_jargon(audit)),
               ("source citations", check_citations(audit, packet_dir)),
               ("blocking flags first", check_flag_order(audit)),
               ("evidence dated", check_evidence(audit))]

    for name, fails in results:
        print(f"{'FAIL' if fails else 'PASS'}  {name} ({len(fails)} problem(s))")
        for f in fails:
            print(f"      - {f}")
    return 1 if any(f for _, f in results) else 0


if __name__ == "__main__":
    sys.exit(main())
