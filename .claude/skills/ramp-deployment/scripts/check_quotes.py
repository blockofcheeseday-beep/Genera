#!/usr/bin/env python3
"""Verify every requirement's source_quote really appears in the file it cites.

Catches hallucinated citations: a requirement whose source_quote was paraphrased,
stitched together from two turns, or attributed to the wrong file. Every downstream
audit-log `source` field leans on these quotes, so an unverified quote is a lie the
whole deliverable inherits.

  python3 check_quotes.py --packet client_a_acme_corp [--repo /path/to/repo]

Exit 0 if every quote verifies, 1 otherwise.
"""
import sys, json, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
# Transcripts use curly quotes and em dashes; an extractor may have normalized them.
FOLD = {"‘": "'", "’": "'", "‚": "'", "“": '"', "”": '"',
        "„": '"', "–": "-", "—": "-", "−": "-", "…": "..."}


def norm(text):
    """Fold unicode punctuation to ASCII and collapse whitespace. Case is preserved."""
    text = unicodedata.normalize("NFC", text)
    return " ".join("".join(FOLD.get(ch, ch) for ch in text).split())


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    root = pathlib.Path(arg("--repo", ROOT))
    packet = arg("--packet")
    if not packet:
        print("usage: check_quotes.py --packet <packet_name> [--repo <path>]")
        return 1

    src_json = root / "work" / packet / "requirements.json"
    if not src_json.is_file():
        print(f"missing: {src_json}")
        return 1
    reqs = json.loads(src_json.read_text())["requirements"]
    packet_dir = root / "candidate" / "customer_packets" / packet
    cache, bad = {}, []

    for r in reqs:
        src = packet_dir / r["source_file"]
        if src.name not in cache:
            cache[src.name] = norm(src.read_text()) if src.is_file() else None
        haystack = cache[src.name]
        if haystack is None:
            bad.append((r["req_id"], r["source_file"], "MISSING FILE", r.get("source_quote", "")))
        elif norm(r["source_quote"]) not in haystack:
            bad.append((r["req_id"], r["source_file"], "QUOTE NOT FOUND", r["source_quote"]))

    for req_id, src_file, why, quote in bad:
        print(f"FAIL {req_id}  {why}  in {src_file}\n     quote: {norm(quote)[:70]!r}")
    print(f"{len(reqs) - len(bad)}/{len(reqs)} quotes verified")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
