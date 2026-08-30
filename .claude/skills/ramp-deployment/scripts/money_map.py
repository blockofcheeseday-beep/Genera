#!/usr/bin/env python3
"""Lay every monetary figure in a packet side by side so collisions become visible.

Packet C: security_requirements.doc REQ-3 declines any transaction over $500 USD without
a purchase order, while discovery_call_apex.txt gives clinic managers "a per-transaction
cap of a thousand". A $700 clinic supply run is therefore approved by the card while
sitting inside the PO requirement. Neither document notices; no other check in this skill
looks across documents at raw amounts. It is only visible when $500 and $1,000 end up
adjacent in one sorted list.

This tool ASSERTS NOTHING. It never says two figures conflict — that is semantic judgement
the agent makes, and a tool that guessed would write false conflicts into the audit log,
which is worse than missing one. It surfaces the figures with file, line, currency, period
and scope; the reader decides, and writes any real collision up as a `conflicts` entry.

  python3 money_map.py --packet client_c_apex_health [--json] [--repo /path/to/repo]

Always exits 0 — this reports, it does not gate.
"""
import sys, re, csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
SYM, NUM = r"(?:R\$|US\$|\$)", r"\d[\d.,]*"
RANGE_RE = re.compile(rf"({SYM})\s?({NUM})\s*[-–—]\s*(?:{SYM})?\s?({NUM})\s*(k|m)?\b", re.I)
NUMERIC_RE = re.compile(rf"(?:(USD|MXN|BRL)\s*)?({SYM})\s?({NUM})\s*(k|m)?\b\s*(USD|MXN|BRL|dollars?|pesos?|reais|reales)?", re.I)
SUFFIX_RE = re.compile(rf"\b()()({NUM})\s*()(USD|MXN|BRL|pesos?|reais|reales)\b", re.I)
KILO_RE = re.compile(r"\b()()(\d[\d,]*)\s*(k)()\b", re.I)
MULT = {"": 1, "k": 1000, "m": 1000000}
ONES = "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen"
TENS = "twenty thirty forty fifty sixty seventy eighty ninety"
WORDVAL = {w: i + 1 for i, w in enumerate(ONES.split())}
WORDVAL.update({w: (i + 2) * 10 for i, w in enumerate(TENS.split())}, a=1, an=1)
SCALE = {"hundred": 100, "thousand": 1000, "grand": 1000, "k": 1000, "million": 1000000}
_W = "|".join(sorted(WORDVAL, key=len, reverse=True))
SPELLED_RE = re.compile(rf"\b((?:{_W})(?:[\s-](?:{_W}))*)(?:[\s-](hundred|thousand|grand|million|k))?(?:[\s-]?(dollars?|pesos?|bucks|USD))?", re.I)
# a spelled-out run followed by one of these is a count of things, not money
NOISE_AFTER = re.compile(r"\s*(?:employees?|people|ppl|reps?|clinics?|staff|nurses?|states?|days?|weeks?|months?|years?|hours?|minutes?|vendors?|cards?|users?|transactions?|field|of them|to \w+ (?:days?|weeks?))\b", re.I)
PERIODS = (("daily", r"per day|a day|daily|/day|por d[ií]a|al d[ií]a|di[áa]rio"),
           ("monthly", r"per month|monthly|a month|/mo\b|mensua|al mes|month"),
           ("yearly", r"per year|annual|anual|/yr\b|a year"))
SCOPES = (("per_transaction", r"per[- ]transaction|in one purchase|por transacci|por tarjeta"),
          ("threshold", r"exceed|\bover\b|\babove\b|\bunder\b|more than|arriba de|acima de|\bhasta\b|threshold|\bup to\b|at any amount"),
          ("approval", r"approv|sign off|purchase order|\bPO\b|declin|aprueb|autoriza|escalat"),
          ("recurring_limit", r"\bcaps?\b|\blimits?\b|budget|l[ií]mite|tope|\blimite"))
MONEY_HEADER = re.compile(r"limit|cap|usd|mxn|brl|amount|budget|spend|cost|price", re.I)


def cents(tok, mult=1):
    """'1,000'->100000, 'R$ 6.000'->600000, '$2.50'->250. Trailing 1-2 digit group = decimals."""
    t = tok.replace(" ", "").rstrip(".,")
    tail = re.search(r"[.,](\d{1,2})$", t)
    val = float(re.sub(r"[.,]", "", t[:tail.start()]) + "." + tail.group(1)) if tail else float(re.sub(r"[.,]", "", t) or 0)
    return int(round(val * mult * 100))


def currency(*words):
    for w in words:
        w = (w or "").upper()
        if w.startswith("R$") or w[:3] in ("BRL", "REA"):
            return "BRL"
        if w[:3] in ("MXN", "PES"):
            return "MXN"
    return "USD"


def spelled_value(run, scale):
    total = sum(WORDVAL[w.lower()] for w in re.split(r"[\s-]+", run) if w.lower() in WORDVAL)
    return total * SCALE.get((scale or "").lower(), 1)


def detect(line):
    """Yield (start, end, amount_cents, currency, extra_tags) in priority order."""
    for m in RANGE_RE.finditer(line):
        mult, cur = MULT[(m.group(4) or "").lower()], currency(m.group(1))
        for g in (2, 3):
            yield m.start(g), m.end(g), cents(m.group(g), mult), cur, ["range"]
    for rx in (NUMERIC_RE, SUFFIX_RE, KILO_RE):
        for m in rx.finditer(line):
            if not m.group(3):
                continue
            yield (m.start(), m.end(), cents(m.group(3), MULT[(m.group(4) or "").lower()]),
                   currency(m.group(1), m.group(2), m.group(5)), [])
    for m in SPELLED_RE.finditer(line):
        scale, unit = m.group(2), m.group(3)
        if not (scale or unit) or NOISE_AFTER.match(line, m.end()):
            continue  # bare number words with no scale and no currency are counts, not money
        yield m.start(), m.end(), spelled_value(m.group(1), scale) * 100, currency(unit), ["spelled_out"]


def tag(line, start, end, extra):
    after, before = line[end:end + 32], line[max(0, start - 25):start]
    period = next((p for p, rx in PERIODS if re.search(rx, after, re.I) or re.search(rx, before, re.I)), None)
    scope = extra + [s for s, rx in SCOPES if re.search(rx, line, re.I)]
    return period, scope


def scan_text(text):
    for ln, line in enumerate(text.splitlines(), 1):
        taken = []
        for start, end, amt, cur, extra in detect(line):
            if amt <= 0 or any(s < end and start < e for s, e in taken):
                continue
            taken.append((start, end))
            period, scope = tag(line, start, end, extra)
            yield {"line": ln, "raw": line[start:end].strip(), "amount_cents": amt, "currency": cur,
                   "period": period, "scope": scope, "context": " ".join(line.split())[:110]}


def scan_csv(text):
    """A column is money only if its header says so — that is what makes bare digits readable."""
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return
    head = rows[0]
    for ln, row in enumerate(rows[1:], 2):
        for col, val in zip(head, row):
            val = (val or "").strip()
            if not MONEY_HEADER.search(col) or re.search(r"mcc", col, re.I) or not re.fullmatch(r"\$?\s*\d[\d,]*(\.\d+)?", val):
                continue
            period = next((p for p, rx in PERIODS if re.search(rx, col, re.I)), None)
            _, scope = tag(col.replace("_", " "), 0, 0, ["csv_column:" + col])
            yield {"line": ln, "raw": val, "amount_cents": cents(val.lstrip("$ ")), "currency": currency(col),
                   "period": period, "scope": scope, "context": " ".join(",".join(row).split())[:110]}


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    packet = arg("--packet")
    if not packet:
        print("usage: money_map.py --packet <packet_name> [--json] [--repo <path>]")
        return 0
    packet_dir = pathlib.Path(arg("--repo", ROOT)) / "candidate" / "customer_packets" / packet
    if not packet_dir.is_dir():
        print(f"missing packet directory: {packet_dir}")
        return 0

    figures = []
    for path in sorted(p for p in packet_dir.iterdir() if p.is_file()):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        found = list(scan_csv(text)) if path.suffix.lower() == ".csv" else []
        seen = {(f["line"], f["amount_cents"]) for f in found}
        found += [f for f in scan_text(text) if (f["line"], f["amount_cents"]) not in seen]
        for f in sorted(found, key=lambda f: (f["line"], f["amount_cents"])):
            figures.append(dict(file=path.name, **f))

    if "--json" in sys.argv:
        print(json.dumps({"packet": packet, "figures": figures}, indent=2))
        return 0

    print(f"money_map: {packet} — {len(figures)} figure(s) across {len({f['file'] for f in figures})} file(s)\n")
    for name in sorted({f["file"] for f in figures}):
        print(name)
        for f in (x for x in figures if x["file"] == name):
            cur = f["currency"] + ("" if f["currency"] == "USD" else " (non-USD)")
            print(f"  {f['line']:>4}  {f['amount_cents'] / 100:>12,.2f} {cur:<16} {f['period'] or '-':<8} "
                  f"{','.join(f['scope']) or '-':<46} {f['context'][:64]}")
        print()

    print("FIGURES BY AMOUNT (look for thresholds that straddle a cap)")
    buckets = {}
    for f in figures:
        buckets.setdefault((f["currency"] != "USD", f["currency"], f["amount_cents"]), []).append(f"{f['file']}:{f['line']}")
    for (_, cur, amt), refs in sorted(buckets.items()):
        print(f"  {amt / 100:>12,.2f} {cur:<5} {', '.join(sorted(set(refs)))}")
    print("\nmoney_map asserts nothing: adjacency above is not a conflict until you read both")
    print("lines and judge it one. If it is real, write it up as a `conflicts` audit entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
