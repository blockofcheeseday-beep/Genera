#!/usr/bin/env python3
"""Export this Claude Code session into session/, as the exercise requires.

Claude Code's `/export` is a terminal command and this work ran in a remote
web session, so this reproduces it from the transcript files the session
writes to disk. Re-runnable: it overwrites its outputs, picking up whatever
the transcript holds at the moment it runs.

    python3 session/export_session.py

Outputs, all under session/:
    transcript.jsonl    the main thread, verbatim apart from redaction
    subagents/          one .jsonl per subagent, same treatment
    TRANSCRIPT.md       readable rendering, tool output truncated
    PROMPTS.md          the human prompts in order, verbatim and complete

Turn numbering matches the pointers in NOTES.md: every user-role record
counts, including task notifications, except skill loads and stop-hook
feedback, which the harness injects.
"""
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "session"
SRC = Path.home() / ".claude" / "projects" / "-home-user-Genera"
SESSION_ID = "e3e4a895-aaba-57b2-b330-579835165a83"

# Secrets and personal data. The scan behind this list found no credentials
# anywhere in the transcript; the address is redacted as personal data.
REDACTIONS = [
    (re.compile(r"blockofcheeseday@gmail\.com"), "[redacted-email]"),
    (re.compile(r"(gh[pousr]_|github_pat_)[A-Za-z0-9_]{10,}"), "[redacted-token]"),
    (re.compile(r"sk-[A-Za-z0-9-]{20,}"), "[redacted-key]"),
]

# Injected by the harness rather than typed by anyone, so they do not take
# a turn number. Task notifications do: they are agents reporting back.
NOT_A_TURN = ("Base directory for this skill:", "Stop hook feedback:", "<system-reminder")

TOOL_INPUT_CHARS = 500
TOOL_OUTPUT_CHARS = 1500
ASSISTANT_TEXT_CHARS = 4000


def redact(text):
    for pattern, replacement in REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


def load(path):
    records = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def text_of(content):
    """Plain text of a message body, ignoring tool calls and images."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = [b.get("text", "") for b in content
             if isinstance(b, dict) and b.get("type") == "text"]
    return "\n".join(p for p in parts if p)


def kind_of(text):
    stripped = text.strip()
    if stripped.startswith("<task-notification"):
        return "notification"
    if stripped.startswith(NOT_A_TURN):
        return "injected"
    return "prompt"


def clip(text, limit):
    text = text.rstrip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + f"\n… [{len(text) - limit} more characters]"


def tool_result_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        out = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text":
                out.append(block.get("text", ""))
            elif block.get("type") == "image":
                out.append("[image]")
        return "\n".join(out)
    return ""


def walk(records):
    """Yield (turn_number_or_None, kind, record) for every user record, and
    ('assistant', record) for assistants, in transcript order."""
    turn = 0
    for record in records:
        rtype = record.get("type")
        if rtype == "user" and not record.get("isSidechain"):
            body = text_of(record.get("message", {}).get("content"))
            if not body.strip():
                yield None, "tool_result", record
                continue
            kind = kind_of(body)
            if kind == "injected":
                yield None, kind, record
            else:
                turn += 1
                yield turn, kind, record
        elif rtype == "assistant" and not record.get("isSidechain"):
            yield None, "assistant", record


def render(records, title, note):
    lines = [f"# {title}", "", note, ""]
    for turn, kind, record in walk(records):
        message = record.get("message", {})
        stamp = (record.get("timestamp") or "")[:19].replace("T", " ")
        if kind == "assistant":
            for block in message.get("content", []) or []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "text" and block.get("text", "").strip():
                    lines += ["**Claude:**", "", clip(block["text"], ASSISTANT_TEXT_CHARS), ""]
                elif block.get("type") == "tool_use":
                    args = json.dumps(block.get("input", {}), ensure_ascii=False)
                    lines += [f"> `{block.get('name')}` {clip(args, TOOL_INPUT_CHARS)}", ""]
        elif kind == "tool_result":
            content = message.get("content")
            body = ""
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_result":
                        body = tool_result_text(block.get("content"))
            if body.strip():
                lines += ["```", clip(body, TOOL_OUTPUT_CHARS), "```", ""]
        else:
            body = text_of(message.get("content"))
            if kind == "injected":
                label = "System (harness)"
            elif kind == "notification":
                label = f"Turn {turn} — agent reporting back — {stamp} UTC"
            else:
                label = f"Turn {turn} — Evan — {stamp} UTC"
            lines += [f"## {label}", "", clip(body, TOOL_OUTPUT_CHARS), ""]
    return redact("\n".join(lines)) + "\n"


def render_prompts(records):
    lines = ["# Prompts, in order",
             "",
             "Every message typed by hand, verbatim and uncut. Turn numbers are the ones",
             "NOTES.md points to. Numbers missing from this list belong to agents reporting",
             "back, which take a turn but are not typed.",
             ""]
    for turn, kind, record in walk(records):
        if kind != "prompt":
            continue
        stamp = (record.get("timestamp") or "")[:19].replace("T", " ")
        body = text_of(record.get("message", {}).get("content"))
        lines += [f"## Turn {turn} — {stamp} UTC", "", body.strip(), ""]
    return redact("\n".join(lines)) + "\n"


def main():
    main_path = SRC / f"{SESSION_ID}.jsonl"
    if not main_path.exists():
        sys.exit(f"no transcript at {main_path}; it lives on the session container only")

    records = load(main_path)
    OUT.mkdir(exist_ok=True)

    (OUT / "transcript.jsonl").write_text(redact(main_path.read_text(errors="replace")))

    sub_src = SRC / SESSION_ID / "subagents"
    sub_out = OUT / "subagents"
    if sub_out.exists():
        shutil.rmtree(sub_out)
    agents = 0
    if sub_src.is_dir():
        sub_out.mkdir()
        for path in sorted(sub_src.iterdir()):
            (sub_out / path.name).write_text(redact(path.read_text(errors="replace")))
            agents += path.suffix == ".jsonl"

    (OUT / "TRANSCRIPT.md").write_text(render(
        records,
        "Session transcript",
        "Rendered from `transcript.jsonl`. Tool arguments and output are truncated here "
        "for reading; the `.jsonl` alongside is complete.",
    ))
    (OUT / "PROMPTS.md").write_text(render_prompts(records))

    turns = [t for t, k, _ in walk(records) if k == "prompt"]
    print(f"{len(records)} records, {len(turns)} typed prompts, "
          f"{max(t for t, k, _ in walk(records) if t) if turns else 0} numbered turns, "
          f"{agents} subagent transcripts")


if __name__ == "__main__":
    main()
