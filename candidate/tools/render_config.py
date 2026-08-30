#!/usr/bin/env python3
"""Render your (ramp_config.json, audit_log.json[, NOTES.md]) into one readable HTML page.

Provided as-is, for self-review and for presenting — not graded (see README).

Usage: python3 tools/render_config.py --config c.json --audit a.json [--notes NOTES.md] [--out view.html]
"""
import argparse
import html
import json
import os

VERSION = "1.0.0"

TITLES = {
    "assumptions_made": "Assumptions made", "missing_information_flags": "Missing information",
    "conflicts": "Conflicts", "unsupported_api_requests": "Unsupported API requests",
    "assumption": "Assumption", "source": "Source", "impact_if_wrong": "Impact if wrong",
    "question": "Question", "affected_config": "Affected config", "blocking": "Blocking",
    "description": "Description", "source_a": "Source A", "source_b": "Source B",
    "provisional_resolution": "Provisional resolution", "requested_feature": "Requested feature",
    "reason_unsupported": "Why unsupported", "evidence": "Evidence",
    "proposed_manual_workaround": "Proposed workaround",
    "allowed_categories": "Allowed categories", "blocked_categories": "Blocked categories",
    "blocked_mcc_codes": "Blocked MCC codes", "allowed_vendors": "Allowed vendors",
    "blocked_vendors": "Blocked vendors",
}


def title(k):
    return TITLES.get(k, k.replace("_", " ").capitalize())


def esc(x):
    return html.escape(str(x)) if x is not None else "—"


def money(cents, currency=""):
    if cents is None:
        return "—"
    return f"{cents/100:,.2f} {currency}".strip()


CSS = """
body{font:15px/1.5 -apple-system,'Segoe UI',sans-serif;color:#1a2233;background:#f5f6f8;margin:0;padding:2rem;}
.wrap{max-width:1100px;margin:0 auto;}
h1{font-size:1.4rem;margin:0 0 .2rem;} h2{font-size:1.05rem;margin:2rem 0 .6rem;border-bottom:2px solid #d8dce4;padding-bottom:.3rem;}
h3{font-size:.95rem;margin:1.2rem 0 .4rem;}
.sub{color:#5a6478;margin-bottom:1.2rem;}
.chips{display:flex;gap:.6rem;flex-wrap:wrap;margin:.8rem 0 1.4rem;}
.chip{padding:.35rem .8rem;border-radius:999px;font-weight:600;font-size:.85rem;background:#e7ecf7;color:#2c4a8a;}
.chip.blocking{background:#fbe3e3;color:#8f1d1d;}
table{border-collapse:collapse;width:100%;background:#fff;font-size:.88rem;margin:.4rem 0 1rem;}
th,td{border:1px solid #e1e5ec;padding:.45rem .6rem;text-align:left;vertical-align:top;}
th{background:#eef1f6;font-size:.8rem;text-transform:uppercase;letter-spacing:.03em;color:#46506a;}
.scroll{overflow-x:auto;}
pre{background:#fff;border:1px solid #e1e5ec;padding:1rem;white-space:pre-wrap;font-size:.82rem;}
.note{color:#5a6478;font-size:.82rem;}
.badge{display:inline-block;padding:.05rem .5rem;border-radius:4px;font-size:.75rem;font-weight:700;margin-right:.4rem;}
.badge.b{background:#fbe3e3;color:#8f1d1d;}
.badge.n{background:#eef1f6;color:#5a6478;}
ul.kv{margin:.15rem 0 .15rem 0;padding-left:1.1rem;}
ul.kv li{margin:.15rem 0;}
@media print {body{background:#fff;padding:0}}
"""


def table(headers, rows):
    h = "".join(f"<th>{esc(x)}</th>" for x in headers)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for cells in rows)
    return f"<div class='scroll'><table><tr>{h}</tr>{b}</table></div>"


def restrictions(r):
    if not r:
        return "—"
    bits = [f"<b>{money(r.get('limit_amount_cents'), r.get('currency',''))}</b> / {esc(r.get('interval'))}"]
    if r.get("transaction_amount_limit_cents") is not None:
        bits.append(f"txn cap {money(r['transaction_amount_limit_cents'], r.get('currency',''))}")
    if r.get("lock_date"):
        bits.append(f"🔒 locks {esc(r['lock_date'])}")
    for f in ("allowed_categories", "blocked_categories", "blocked_mcc_codes", "allowed_vendors", "blocked_vendors"):
        if r.get(f):
            vals = ", ".join(str(v) for v in r[f][:8]) + ("…" if len(r[f]) > 8 else "")
            bits.append(f"{title(f)}: {esc(vals)}")
    return "<br>".join(bits)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--audit", required=True)
    ap.add_argument("--notes")
    ap.add_argument("--out", default="view.html")
    a = ap.parse_args()
    config = json.load(open(a.config))
    audit = json.load(open(a.audit))

    n_block = sum(1 for f in audit.get("missing_information_flags", []) if f.get("blocking"))
    parts = [f"<div class='wrap'><h1>{esc(config.get('client_id'))} — configuration review</h1>",
             f"<div class='sub'>rendered by render_config v{VERSION} · generated {esc(config.get('generated_at'))} · base currency {esc(config.get('base_currency'))}</div>",
             "<div class='chips'>"
             + f"<span class='chip'>{len(config.get('users', []))} users</span>"
             + f"<span class='chip'>{len(config.get('spend_programs', []))} programs</span>"
             + f"<span class='chip'>{len(config.get('limits', []))} limits</span>"
             + f"<span class='chip'>{sum(len(audit.get(s, [])) for s in ('assumptions_made','missing_information_flags','conflicts','unsupported_api_requests'))} audit entries</span>"
             + (f"<span class='chip blocking'>{n_block} BLOCKING question{'s' if n_block != 1 else ''}</span>" if n_block else "")
             + "</div>"]

    parts.append("<h2>Structure</h2>")
    parts.append(table(["type", "details"], [
        ["entities", " · ".join(f"{esc(e.get('name'))} ({esc(e.get('country'))}, {esc(e.get('currency'))}, <b>{esc(e.get('status'))}</b>)" for e in config.get("entities", []))],
        ["departments", ", ".join(esc(d.get("name")) for d in config.get("departments", []))],
        ["locations", ", ".join(esc(l.get("name")) for l in config.get("locations", [])) or "—"],
    ]))

    parts.append(f"<h2>Users ({len(config.get('users', []))})</h2>")
    parts.append(table(["email", "name", "role", "department", "manager", "notes"],
                       [[esc(u.get("email")), esc(f"{u.get('first_name','')} {u.get('last_name','')}"), esc(u.get("role")),
                         esc(u.get("department")), esc(u.get("direct_manager_email")), esc(u.get("notes", ""))]
                        for u in config.get("users", [])]))

    parts.append(f"<h2>Spend programs ({len(config.get('spend_programs', []))})</h2>")
    parts.append(table(["name", "description", "spend types", "restrictions"],
                       [[esc(p.get("display_name")), esc(p.get("description")),
                         esc(", ".join(k for k, v in (p.get("permitted_spend_types") or {}).items() if v)),
                         restrictions(p.get("spending_restrictions"))] for p in config.get("spend_programs", [])]))

    parts.append(f"<h2>Limits ({len(config.get('limits', []))})</h2>")
    parts.append(table(["name", "assigned to", "program", "restrictions", "notes"],
                       [[esc(l.get("display_name")),
                         esc(l.get("assigned_to", {}).get("user_email") or l.get("assigned_to", {}).get("group")),
                         esc(l.get("spend_program", "")), restrictions(l.get("spending_restrictions")),
                         esc(l.get("notes", ""))] for l in config.get("limits", [])]))

    parts.append(f"<h2>Approval policies ({len(config.get('approval_policies', []))}) <span class='note'>— desired state, applied in-app</span></h2>")
    parts.append(table(["name", "applies to", "tiers", "source"],
                       [[esc(p.get("name")), esc(p.get("applies_to")),
                         "<br>".join(f"≥ {money(t.get('threshold_usd_cents'),'USD')} → {esc(t.get('approver'))}" for t in p.get("tiers", [])),
                         esc(p.get("source", ""))] for p in config.get("approval_policies", [])]))

    parts.append(f"<h2>MCC / category controls ({len(config.get('mcc_controls', []))})</h2>")
    parts.append(table(["applies to", "mechanism", "values", "translation notes"],
                       [[esc(m.get("applies_to")), esc(m.get("mechanism")),
                         esc(", ".join(str(v) for v in m.get("values", []))), esc(m.get("translation_notes", ""))]
                        for m in config.get("mcc_controls", [])]))

    parts.append("<h2>Audit log</h2>")
    for name, fields in [("assumptions_made", ["assumption", "source", "impact_if_wrong"]),
                         ("missing_information_flags", ["question", "affected_config", "blocking"]),
                         ("conflicts", ["description", "source_a", "source_b", "provisional_resolution"]),
                         ("unsupported_api_requests", ["requested_feature", "reason_unsupported", "evidence", "proposed_manual_workaround"])]:
        entries = audit.get(name, [])
        parts.append(f"<h3>{title(name)} ({len(entries)})</h3>")
        if not entries:
            parts.append("<p class='note'>none</p>")
            continue
        rows = []
        for e in entries:
            cells = []
            for k in fields:
                if k == "blocking":
                    cells.append("<span class='badge b'>BLOCKING</span>" if e.get(k) else "<span class='badge n'>NOT BLOCKING</span>")
                else:
                    cells.append(esc(e.get(k)))
            rows.append(cells)
        parts.append(table([title(k) for k in fields], rows))

    if a.notes and os.path.exists(a.notes):
        parts.append("<h2>NOTES.md</h2><pre>" + esc(open(a.notes).read()) + "</pre>")
    parts.append("</div>")

    with open(a.out, "w") as f:
        f.write(f"<title>{esc(config.get('client_id'))} · config review</title><style>{CSS}</style>" + "".join(parts))
    print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
