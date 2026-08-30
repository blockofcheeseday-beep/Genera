#!/usr/bin/env python3
"""Find the roster dirt an LLM reading a CSV politely skims past.

Duplicate people with contradictory limits, blank cells, "NO LIMIT" where a number
belongs, "sales" next to "Sales" (two departments, silently), and managers who are not
in the roster at all. Each finding is a conflict, missing-information flag, or assumption
that belongs in the audit log — deterministic detection beats hoping the model noticed.

Columns are matched by case-insensitive substring on the header, so this works on
packets nobody has seen; a missing column just skips its checks.

  python3 lint_roster.py <path-to-roster.csv> [--json]

Always exits 0 — this reports, it does not gate.
"""
import sys, csv, json, collections

def find_col(headers, want, avoid=None):
    for h in headers:
        low = h.lower()
        if want in low and not (avoid and avoid in low):
            return h
    return None


def lint(rows, headers):
    email = find_col(headers, "email", avoid="manager")
    manager = find_col(headers, "manager")
    dept = find_col(headers, "depart")
    limit = find_col(headers, "limit")
    out = []

    def add(kind, detail, rows_):
        out.append({"kind": kind, "detail": detail, "rows": rows_})

    if email:
        seen = collections.defaultdict(list)
        for i, r in enumerate(rows, start=2):  # line numbers as in the file
            addr = (r[email] or "").strip()
            if not addr:
                add("blank_email", f"row {i} has no email", [i])
            else:
                seen[addr].append((i, r))
        for addr, hits in seen.items():
            if len(hits) < 2:
                continue
            differing = {h: sorted({r[h].strip() for _, r in hits})
                         for h in headers if len({r[h].strip() for _, r in hits}) > 1}
            detail = f"{addr} appears {len(hits)}x on rows {[i for i, _ in hits]}"
            if differing:
                detail += "; disagrees on " + ", ".join(f"{h}={v}" for h, v in differing.items())
            add("duplicate_email", detail, [i for i, _ in hits])

    if limit:
        for i, r in enumerate(rows, start=2):
            val = r[limit].strip()
            who = r[email].strip() if email else f"row {i}"
            if not val:
                add("blank_limit", f"{who} has an empty {limit}", [i])
            elif not val.replace(",", "").replace("$", "").replace(".", "").isdigit():
                add("non_numeric_limit", f"{who} has {limit}={val!r}", [i])

    if dept:
        variants = collections.defaultdict(collections.Counter)
        for r in rows:
            variants[r[dept].strip().lower()][r[dept]] += 1
        for key, forms in variants.items():
            if len(forms) > 1:
                odd = [f for f, _ in forms.most_common()[1:]]
                add("department_variant",
                    f"{sorted(forms)} all normalize to {key!r} — would create duplicate departments",
                    [i for i, r in enumerate(rows, start=2) if r[dept] in odd])

    if manager and email:
        members = {r[email].strip().lower() for r in rows if r[email].strip()}
        for i, r in enumerate(rows, start=2):
            mgr = r[manager].strip()
            if mgr and mgr.lower() not in members:
                add("dangling_manager", f"row {i} ({r[email].strip()}) reports to {mgr}, who is not in the roster", [i])
    return out


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print("usage: lint_roster.py <path-to-roster.csv> [--json]")
        return 0

    with open(args[0], newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers, rows = reader.fieldnames or [], list(reader)

    findings = lint(rows, headers)
    if "--json" in sys.argv:
        print(json.dumps({"findings": findings}, indent=2))
        return 0

    print(f"{args[0]}: {len(rows)} rows, {len(findings)} finding(s)")
    for f in findings:
        print(f"  [{f['kind']}] {f['detail']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
