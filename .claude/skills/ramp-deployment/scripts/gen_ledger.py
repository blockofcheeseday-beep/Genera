#!/usr/bin/env python3
"""Generate CAPABILITY_LEDGER.md from capabilities.yaml.

capabilities.yaml is the source of truth. The markdown is committed so a reviewer
can read the ledger without running anything.

  python3 gen_ledger.py           # write the markdown
  python3 gen_ledger.py --check   # exit 1 if the committed markdown is stale
"""
import sys, pathlib, yaml

REF = pathlib.Path(__file__).resolve().parent.parent / "references"
SRC, OUT = REF / "capabilities.yaml", REF / "CAPABILITY_LEDGER.md"
ORDER = ["UNSUPPORTED", "UI_ONLY", "PARTIAL", "SUPPORTED", "DRIFT"]


def render(doc):
    caps = doc["capabilities"]
    by = {v: [c for c in caps if c["verdict"] == v] for v in ORDER}
    L = ["# Ramp Capability Ledger", "",
         "**Generated from `capabilities.yaml` by `scripts/gen_ledger.py` — do not edit by hand.**", "",
         "The unit is *a thing customers ask for*, not an endpoint.",
         "`evidence_line` is copied verbatim into `audit_log.json` evidence fields.", ""]

    m = doc.get("meta", {}).get("snapshot_facts", {})
    if m:
        L += [f"Primary evidence: `{doc['meta']['generated_from']}` — "
              f"{m.get('paths')} paths, {m.get('schemas')} schemas, {m.get('oauth_scopes')} OAuth scopes, "
              f"server `{m.get('server')}`, prefix `{m.get('path_prefix')}`.", ""]

    L += [f"**{len(caps)} rows.** " + "  ".join(f"{v}: {len(by[v])}" for v in ORDER if by[v]), "",
          "| id | verdict | title | seen in |", "|---|---|---|---|"]
    for v in ORDER:
        for c in by[v]:
            seen = ", ".join(s.replace("client_", "").replace("_", " ") for s in c["seen_in"]) or "—"
            L.append(f"| [`{c['id']}`](#{c['id'].lower()}) | **{v}** | {c['title']} | {seen} |")
    L.append("")

    for v in ORDER:
        if not by[v]:
            continue
        L += [f"## {v}", ""]
        for c in by[v]:
            L += [f"### {c['id']}", "", f"**{c['title']}**", ""]
            if c.get("customer_phrasings"):
                L += ["How customers say it:", ""] + [f"- *“{p}”*" for p in c["customer_phrasings"]] + [""]
            am = c.get("api_mechanism") or {}
            if am.get("endpoints"):
                L += ["Endpoints: " + ", ".join(f"`{e}`" for e in am["endpoints"]), ""]
            if am.get("fields"):
                L += ["Fields: " + ", ".join(f"`{f}`" for f in am["fields"]), ""]
            for e in c["evidence"]:
                L += [f"> **{e['source']}** (checked {e['checked_on']})", ">",
                      "> " + " ".join(str(e.get("note", "")).split()), ""]
            L += ["Evidence line (verbatim into audit logs):", "",
                  f"```\n{c['evidence_line']}\n```", ""]
            ce = c.get("config_expression") or {}
            if ce:
                bits = [f"section `{ce['section']}`"] if ce.get("section") else []
                if ce.get("mechanism"):
                    bits.append(f"mechanism `{ce['mechanism']}`")
                if bits:
                    L += ["Config expression: " + ", ".join(bits), ""]
                if ce.get("note"):
                    L += ["> " + " ".join(str(ce["note"]).split()), ""]
            if c.get("workaround"):
                L += ["**Workaround.** " + " ".join(str(c["workaround"]).split()), ""]
    return "\n".join(L).rstrip() + "\n"


def main():
    text = render(yaml.safe_load(SRC.read_text()))
    if "--check" in sys.argv:
        cur = OUT.read_text() if OUT.exists() else ""
        if cur != text:
            print("STALE: CAPABILITY_LEDGER.md does not match capabilities.yaml — run gen_ledger.py")
            return 1
        print("CAPABILITY_LEDGER.md is up to date")
        return 0
    OUT.write_text(text)
    print(f"wrote {OUT} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
