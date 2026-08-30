#!/usr/bin/env python3
"""Lay every monetary figure in a packet side by side so a collision becomes visible.

Packet C: security_requirements.doc REQ-3 declines any transaction over $500 USD without a
purchase order, while discovery_call_apex.txt gives clinic managers "a per-transaction cap of
a thousand". A $700 clinic supply run is therefore approved by the card while sitting inside
the PO requirement. Neither document notices, and nothing else in this skill compares raw
amounts across documents; it is visible only when $500 and $1,000 land next to each other in
one sorted list.

This tool ASSERTS NOTHING. It never claims two figures conflict — that judgement is semantic
and belongs to the agent; a tool that guessed would write false conflicts into the audit log,
which is worse than missing one. It reports every figure with file, line, currency, period and
scope; the reader judges, and writes any real collision up as a `conflicts` entry.

  python3 money_map.py --packet client_c_apex_health [--json] [--repo /path/to/repo]

Always exits 0 — this reports, it does not gate.
"""
import sys, re, csv, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]  # scripts/ -> ramp-deployment/ -> skills/ -> .claude/ -> repo root
SYM, NUM, CUR = r"(?:R\$|US\$|\$)", r"\d[\d.,]*", r"USD|MXN|BRL|dollars?|pesos?|reais|reales|bucks"
RANGE_RE = re.compile(rf"({SYM})\s?({NUM})\s*[-–—]\s*(?:{SYM})?\s?({NUM})\s*(k|m)?\b", re.I)  # "$50-60k"
NUMERIC_RE = re.compile(rf"(?:({CUR})\s*)?({SYM})\s?({NUM})\s*(k|m)?\b\s*({CUR})?", re.I)
BARE_RE = re.compile(rf"\b()()({NUM})\s*(k\b)?\s*({CUR})?\b", re.I)  # "20.000 MXN", "1k"; empty groups keep detect() uniform
MULT = {"": 1, "k": 1000, "m": 1000000}
WORDVAL = {w: i + 1 for i, w in enumerate("one two three four five six seven eight nine ten eleven twelve thirteen "
                                          "fourteen fifteen sixteen seventeen eighteen nineteen".split())}
WORDVAL.update({w: (i + 2) * 10 for i, w in enumerate("twenty thirty forty fifty sixty seventy eighty ninety".split())})
WORDVAL.update(hundred=100, thousand=1000, grand=1000, million=1000000, mil=1000, quinientos=500, quinhentos=500,
               dos=2, tres=3, cuatro=4, cinco=5, seis=6, siete=7, ocho=8, nueve=9, diez=10, quince=15,
               veinte=20, veinticinco=25, treinta=30, cuarenta=40, cincuenta=50)
ART, _W = "an|a|un[ao]?", "|".join(sorted(WORDVAL, key=len, reverse=True))  # the article carries no value of its own
SPELLED_RE = re.compile(rf"\b((?:{ART})[\s-])?((?:{_W})(?:[\s-](?:{_W}))*)\b(?:[\s-]?({CUR})\b)?", re.I)
NOISE_AFTER = re.compile(  # a spelled run followed by one of these counts things, not money
    rf"[\s-]*(?:(?:{_W})[\s-])?(?:employees?|empleados?|people|personas?|pessoas?|ppl|reps?|clinics?|staff|nurses?|"
    r"states?|days?|d[ií]as?|weeks?|semanas?|months?|meses|years?|a[nñ]os?|hours?|minutes?|times|veces|vendors?|"
    r"cards?|tarjetas?|users?|transactions?|field|of them)\b", re.I)
PERIODS = (("daily", r"per day|a day|daily|/day|por d[ií]a|al d[ií]a|di[áa]rio"),
           ("monthly", r"per month|monthly|a month|/mo\b|mensua|al mes|month"),
           ("yearly", r"per year|annual|anual|/yr\b|a year"))
SCOPES = (("per_transaction", r"per[- ]transaction|in one purchase|por transacci|por tarjeta|por cart[ãa]o"),
          ("threshold", r"exceed|\bover\b|\babove\b|\bunder\b|more than|arriba de|acima de|\bhasta\b|\bat[ée]\b|threshold|\bup to\b"),
          ("approval", r"approv|sign off|purchase order|\bPO\b|declin|aprova|aprueb|autoriza|escalat"),
          ("recurring_limit", r"\bcaps?\b|\blimits?\b|budget|l[ií]mite|limite|tope|presupuesto"))
MONEY_HEADER = re.compile(r"limit|cap|usd|mxn|brl|amount|budget|spend|cost|price", re.I)


def cents(tok, mult=1):
    """'1,000'->100000; 'R$ 6.000'->600000; '$2.50'->250. A trailing 1-2 digit group is decimals."""
    t = tok.replace(" ", "").strip(".,")
    tail = re.search(r"[.,](\d{1,2})$", t)
    val = float(re.sub(r"[.,]", "", t[:tail.start()]) + "." + tail.group(1)) if tail else float(re.sub(r"[.,]", "", t) or 0)
    return int(round(val * mult * 100))


def currency(*words):
    """Whatever marker is nearest the figure wins; absent any marker we say USD and say so."""
    w = " ".join(x or "" for x in words).upper()
    return "BRL" if re.search(r"R\$|BRL|REA", w) else "MXN" if re.search(r"MXN|PES", w) else "USD"


def spelled_value(run):
    """Left-to-right accumulator: 'twenty-five hundred'->2500, 'fifty grand'->50000, 'mil quinientos'->1500."""
    total = part = 0
    for w in re.split(r"[\s-]+", run.lower()):
        v = WORDVAL.get(w, 0)
        if v >= 1000: total, part = total + max(part, 1) * v, 0
        elif v == 100: part = max(part, 1) * 100
        else: part += v
    return total + part


def detect(line):
    """Yield (start, end, amount_cents, currency, extra_tags), highest-priority detector first."""
    for m in RANGE_RE.finditer(line):  # before NUMERIC_RE, so "$50-60k" is not read as 50 and 60000
        mult, cur = MULT[(m.group(4) or "").lower()], currency(m.group(1))
        for g in (2, 3):  # a range is reported as its two endpoints, both tagged "range"
            yield m.start(g), m.end(g), cents(m.group(g), mult), cur, ["range"]
    for rx in (NUMERIC_RE, BARE_RE):
        for m in rx.finditer(line):
            if m.group(3) and (rx is NUMERIC_RE or m.group(4) or m.group(5)):  # a bare number needs a k or a currency word
                yield (m.start(), m.end(), cents(m.group(3), MULT[(m.group(4) or "").strip().lower()]),
                       currency(m.group(1), m.group(2), m.group(5)), [])
    for m in SPELLED_RE.finditer(line):
        run, unit = m.group(2), m.group(3)
        if not (unit or max(WORDVAL.get(w.lower(), 0) for w in re.split(r"[\s-]+", run)) >= 100):
            continue  # number words with no scale word and no currency word are counts, not money
        if not NOISE_AFTER.match(line, m.end()):
            yield (m.start(), m.end(), spelled_value(run) * 100,
                   currency(unit) if unit else currency(*re.findall(CUR, line, re.I)), ["spelled_out"])


def tag(line, start, end, extra):
    """Period from the text hugging the figure; scope from the whole line, as the brief asks."""
    near = (line[end:end + 32], line[max(0, start - 25):start])
    period = next((p for p, rx in PERIODS if any(re.search(rx, s, re.I) for s in near)), None)
    return period, extra + [s for s, rx in SCOPES if re.search(rx, line, re.I)]


def trim(line, start=0, width=88):
    line = " ".join(line.split())
    if len(line) > width and start >= 30:
        return "..." + line[start - 25:start + width - 28] + "..."
    return line[:width] + ("..." if len(line) > width else "")


def scan_text(text):
    for ln, line in enumerate(text.splitlines(), 1):
        taken = []
        for start, end, amt, cur, extra in detect(line):
            if amt <= 0 or any(s < end and start < e for s, e in taken):
                continue  # first detector to claim a span keeps it
            taken.append((start, end))
            period, scope = tag(line, start, end, extra)
            yield {"line": ln, "raw": line[start:end].strip(" .,;:"), "amount_cents": amt, "currency": cur,
                   "period": period, "scope": scope, "context": trim(line, start)}


def scan_csv(text):
    """A column is money only when its header says so — that is what makes bare digits readable."""
    rows = list(csv.reader(text.splitlines()))
    for ln, row in enumerate(rows[1:], 2):
        for col, val in zip(rows[0], row):
            val = (val or "").strip()
            if not MONEY_HEADER.search(col) or re.search("mcc", col, re.I) or not re.fullmatch(r"\$?\s*\d[\d,]*(\.\d+)?", val):
                continue
            period = next((p for p, rx in PERIODS if re.search(rx, col, re.I)), None)
            yield {"line": ln, "raw": val, "amount_cents": cents(val.lstrip("$ ")), "currency": currency(col),
                   "period": period, "scope": tag(col.replace("_", " "), 0, 0, ["csv_column:" + col])[1],
                   "context": trim(",".join(row))}


def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    packet = arg("--packet")
    if not packet:
        print("usage: money_map.py --packet <packet_name> [--json] [--repo <path>]")
        return 0
    packet_dir = pathlib.Path(arg("--repo", ROOT)) / "candidate" / "customer_packets" / packet
    if not packet_dir.is_dir():
        print(f"no such packet directory: {packet_dir}")
        return 0

    figures = []
    for path in sorted(p for p in packet_dir.iterdir() if p.is_file()):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        found = list(scan_csv(text)) if path.suffix.lower() == ".csv" else []
        seen = {(f["line"], f["amount_cents"]) for f in found}  # a "$900" money cell is one figure, not two
        found += [f for f in scan_text(text) if (f["line"], f["amount_cents"]) not in seen]
        figures += [dict(file=path.name, **f) for f in sorted(found, key=lambda f: (f["line"], f["amount_cents"]))]

    if "--json" in sys.argv:
        print(json.dumps({"packet": packet, "figures": figures}, indent=2))
        return 0

    print(f"money_map: {packet} — {len(figures)} figure(s) in {len({f['file'] for f in figures})} file(s)\n")
    for name in sorted({f["file"] for f in figures}):
        print(name)
        for f in (x for x in figures if x["file"] == name):
            print(f"  {f['line']:>4}  {f['amount_cents'] / 100:>11,.2f} {f['currency'] + ('' if f['currency'] == 'USD' else '*'):<5} "
                  f"{f['period'] or '-':<8}{','.join(f['scope']) or '-'}\n        {f['context']}")
        print()

    print("FIGURES BY AMOUNT (look for thresholds that straddle a cap)")
    buckets = {}
    for f in figures:
        buckets.setdefault((f["currency"] != "USD", f["currency"], f["amount_cents"]), []).append(f"{f['file']}:{f['line']}")
    for (non_usd, cur, amt), refs in sorted(buckets.items()):
        print(f"  {amt / 100:>11,.2f} {cur + ('*' if non_usd else ''):<5} {', '.join(sorted(set(refs)))}")
    print("\n* = not USD. Amounts are grouped by currency and never converted.")
    print("money_map asserts nothing. Two amounts sitting next to each other above are not a")
    print("conflict until you read both lines and judge them one — then write a `conflicts` entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
