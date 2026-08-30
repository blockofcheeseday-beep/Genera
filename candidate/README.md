# Genera Deployments — Take-Home Exercise

## What this is

Genera helps AI-era software companies get their customers live. One of our partners is **Ramp**, the spend-management platform. When a company adopts Ramp, someone has to turn their messy reality — call transcripts, policy memos, Slack threads, rosters — into a concrete configuration: departments, users, spend limits, card programs, approval rules. Today a deployment rep does that by hand. Your job in this exercise is to build the agent that does the first pass.

This is real work, in exactly the shape we do it. **You don't need fintech or Ramp experience.** Part of what we're evaluating is how you get up to speed on a real product and its real API from public materials — [ramp.com](https://ramp.com) and the Developer API docs at [docs.ramp.com](https://docs.ramp.com) are your friends, and we expect you to actually consult them.

## The task

Build an agent/pipeline that ingests a customer packet (a folder of raw documents) and produces **two JSON files** per customer:

1. **`ramp_config.json`** — the desired-state configuration, valid against `schemas/ramp_config_schema.json`.
2. **`audit_log.json`** — valid against `schemas/audit_log_schema.json`: every assumption you made, every question you'd ask the customer, every conflict between their own documents, and every request the Ramp API cannot actually fulfill (with evidence and a proposed workaround).

**The audit log is not an appendix — it's half the deliverable.** A deployment rep will trust your config exactly as far as your audit log is honest. When in doubt, flag it; a confidently wrong config is the worst outcome.

Check your outputs with:

```
python3 tools/validate.py out/client_a/ramp_config.json out/client_a/audit_log.json
```

Also provided: a viewer that renders your two JSONs into a readable page —

```
python3 tools/render_config.py --config out/client_a/ramp_config.json --audit out/client_a/audit_log.json --notes NOTES.md --out out/client_a/view.html
```

We recommend rendering and *reading* your outputs before you submit — a config reads very differently as tables than as JSON, and this is roughly what a customer-facing review of your work would look like. You're welcome to present from it at the on-site.

**The viewer is furniture, not a deliverable.** It's provided as-is, it isn't graded, and time spent extending, theming, or replacing it is time spent on nothing we score — the JSONs remain the submission. If it crashes on your valid output, that's our bug: mention it in NOTES.md and move on.

### The API is real, and it moves

Ground your can/can't claims in the current docs, and **cite the date and source you checked** in your audit-log `evidence` fields (the sample packet shows the shape). If the live docs conflict with anything in `schemas/` — a renamed resource, a field that's changed — **log the discrepancy in your audit log**; the schemas are a point-in-time snapshot, and noticing drift is a feature, not a mistake.

One thing drift does *not* change: **the schemas are the submission contract.** Your two JSONs must validate against `schemas/` as shipped, even where you know the live API has moved on — record what you'd emit differently in the audit log, don't change the output shape. (Why: your outputs are compared against everyone else's, and the tooling on our side speaks this schema.)

### Invocation

Your pipeline should be runnable per-packet with a single command, e.g.:

```
python3 run_pipeline.py --packet ./customer_packets/client_a_acme_corp
```

(or the equivalent instruction to a fresh Claude Code / Codex session — see "What we mean by pipeline" below).

## The customer packets

| Packet | Customer | What you're walking into |
|---|---|---|
| **A** | `client_a_acme_corp` | Standard tech-company setup: discovery call transcript + employee roster CSV |
| **B** | `client_b_logistica_globex` | Mexican logistics company expanding internationally — Spanish transcript, mixed Portuguese/English policy memo, multiple currencies |
| **C** | `client_c_apex_health` | Healthcare company with strict compliance demands — some of which may not be things Ramp can do |
| **D** | `client_d_hypergrowth` | No clean documents at all: a messy Slack export and fragmented meeting notes that don't fully agree |
| **E** | `client_e_vanguard_retail` | 150 field reps needing temporary cards, plus a role-by-MCC control matrix |

**Before you start, skim the sample packet.** `sample_packet/client_0_sample_westbrook/` is a worked example, not an exercise: a tiny customer packet with finished output files in `example_output/`. Read it to see the output shapes and audit-log idioms (group limits, empty sections when a packet genuinely has none, evidence lines that cite what was checked and when). There's nothing to run or submit for it.

**Do A, C, and D first — they're the core.** B and E are stretch: do them if you have time, and if you don't, say what your pipeline *would* need to handle them. A pipeline that handles three packets with an honest audit trail beats one that handles five carelessly.

At the on-site you'll meet a sixth customer packet you haven't seen — that's the live segment described below.

## What we mean by "pipeline" — scope guardrails

This is smaller than it might sound. The deliverable is **instructions plus small scripts**: prompt/skill files (in Claude Code, a skill is the natural form; elsewhere, the equivalent) and whatever glue code you find useful, such that a fresh Claude Code or Codex session can run any packet end-to-end and emit the two JSON files.

Explicitly **out of scope** — do not spend your time on:
- UIs or dashboards
- Databases or queues
- Live Ramp API calls, OAuth flows, or sandbox accounts (you're producing the *payloads*, not making the calls)
- Perfect FX handling, HRIS integrations, or anything else that smells like infrastructure

If you genuinely believe the task needs more than instructions and small scripts, build it and tell us why in your notes.

We expect you to use an AI coding agent, and we're interested in how you drive it — your session export is a required deliverable (see below), so work in a tool you can export from, or keep a prompt journal as you go.

## What to hand in

One folder (zip or repo link):

1. **The pipeline** — instructions + scripts, arranged so a fresh session can reproduce your outputs.
2. **`out/`** — `ramp_config.json` + `audit_log.json` for each packet you ran (A, C, D minimum). Both files must validate.
3. **Your session export (required).** How you work *with* an agent is a skill we're hiring for, and this is where we see it. Any reasonable format: Claude Code's `/export` (or the session transcript file), your Codex/Cursor session log, or — if your tool genuinely can't export — a journal of your prompts in order, pasted into a file. Two things to know:
   - **Don't clean it up.** Dead ends, corrections, and abandoned approaches are expected and read well — they're what working looks like. A suspiciously pristine session tells us less than a messy real one.
   - **Do redact secrets** (API keys, tokens, anything personal) before sending. That's the only editing we want.
4. **`NOTES.md`** — at most two pages: what you decided and how you checked it. Where it's easy, point to the moment in your session export that backs what you say (a quoted prompt, a timestamp, "about two-thirds in") — we read the notes and the session together, and rough pointers help us navigate a long transcript.
   - The 3–5 decisions that most shaped your pipeline, and the alternatives you passed on — and roughly where in the session each decision happened.
   - **Verification delta (required):** two concrete places where the agent/pipeline was *wrong*, what you changed, and what evidence caused the change. If you truly found zero errors, say so and tell us how hard you looked — but in our experience, first passes are never clean.
   - What you learned about the Ramp API that changed what you built — cite the docs pages you actually used.
   - **Go-live handoff:** for one packet of your choice, the five bullets you'd send that customer's deployment owner before go-live. Written for *them*, not for us — assume they'll forward it internally.
   - **One capability, one question:** one thing in this packet-set that should become a reusable Genera capability (something we'd build once and use across customers), and one expansion or use-case question you'd raise with one of these customers.
   - What you'd do next with another day.

## Time

Budget **3–5 hours**. Please don't spend more — we're calibrated for it. If you're running over, cut packets (in order: E, then B), not the audit logs or NOTES.md. Depth of judgment beats breadth of coverage.

## What we're looking for

- Did you figure out what Ramp **actually supports** — from the real docs — rather than guessing? (Both failure modes count: claiming the API can't do something it can, and silently configuring something it can't.)
- Did you handle ambiguity and conflict like someone a customer could trust — flagging, not guessing?
- How did you **drive the agent**? We read your session for where you intervened, what you questioned, and what you verified — not for elegant prompts.
- Is the pipeline legible? We should understand how it works in ten minutes.
- Do your outputs survive your own audit log — and does your NOTES.md verification story match what your session shows you actually did?

## The on-site (what to prepare)

45 minutes, three parts:

1. **Walkthrough (15 min).** You present your pipeline and outputs — decisions and tradeoffs first, not a code tour. Any format: screen share of your notes, the outputs themselves, slides if you like.
2. **Discussion (15 min).** A real conversation about your choices. We'll ask "why" a lot — that's curiosity, not a signal you got it wrong. Where you have a reason, say it; where you'd change your mind, say that too. Both are good answers.
3. **Build together (15 min).** We extend your solution live — whiteboard and hands-on, and possibly a run on a customer packet you haven't seen. Bring the laptop your pipeline runs on, in a runnable state. We're watching how you operate and adapt, not whether everything works perfectly the first time.

Bring the laptop your pipeline runs on.

Questions before you start? Email us. Asking a clarifying question is not a mark against you; it's usually a mark for.
