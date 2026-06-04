#!/usr/bin/env python3
"""Detect (and optionally fix) bare `~` in docs/ markdown that renders as strikethrough.

Docsify's bundled marked (1.x) treats a PAIR of single tildes as <del> (GFM
single-tilde del, same as GitHub):

    his risk (~0.2%) differs from the U.S. average (~0.3%)

renders "0.2%) differs from the U.S. average (" struck through.

Policy enforced here (see md-standards skill):
- `~` inside inline code spans or fenced code blocks: fine, ignored.
- `~~text~~`: intentional strikethrough, fine.
- Anywhere else in docs/, a bare `~` MUST be escaped as `\\~` (renders as a
  literal `~`). Zero tolerance — a lone `~` is safe today but becomes a
  strikethrough bug the moment a second one lands in the same paragraph.
- Exception: docs/cooking/macronutrients/README.md — its table is frozen
  byte-for-byte by the cooking-book-summary skill and is safe (one `~` per
  table cell can never pair). Only actual del-pairs are flagged there.

Usage:
    python3 scripts/check_tildes.py          # lint; exit 1 on findings
    python3 scripts/check_tildes.py --fix    # escape offending bare ~ in place
"""

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

# Files whose bare tildes are allowed (frozen content, verified pair-free).
BARE_TILDE_WHITELIST = {DOCS / "cooking" / "macronutrients" / "README.md"}

# Inline code spans: `code`, ``code with ` inside``, etc.
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")

# A bare single tilde: not escaped, not part of a ~~ run.
BARE_TILDE_RE = re.compile(r"(?<![\\~])~(?!~)")

# marked 1.x GFM del rule (single- or double-tilde), non-anchored search.
DEL_RE = re.compile(r"(?<![\\~])(~~?)(?=[^\s~])([\s\S]*?[^\s~])\1(?=[^~]|$)")

FENCE_RE = re.compile(r"^\s{0,3}```")


def non_code_segments(line: str):
    """Yield (start, text) for the parts of a line outside inline code spans."""
    idx = 0
    for m in CODE_SPAN_RE.finditer(line):
        yield idx, line[idx : m.start()]
        idx = m.end()
    yield idx, line[idx:]


def strip_code_spans(line: str) -> str:
    return "".join(text for _, text in non_code_segments(line))


def inline_contexts(line: str):
    """Split a line into the contexts marked inline-lexes independently.

    Table rows are lexed cell by cell, so tildes in different cells can
    never pair; everything else is checked as one context.
    """
    stripped = line.strip()
    if stripped.startswith("|") and stripped.endswith("|"):
        return re.split(r"(?<!\\)\|", stripped)
    return [line]


def fix_line(line: str) -> str:
    out, idx = [], 0
    for m in CODE_SPAN_RE.finditer(line):
        out.append(BARE_TILDE_RE.sub(r"\\~", line[idx : m.start()]))
        out.append(m.group(0))
        idx = m.end()
    out.append(BARE_TILDE_RE.sub(r"\\~", line[idx:]))
    return "".join(out)


def scan_file(path: Path, fix: bool = False):
    """Return (findings, fixed_text). findings = list of (lineno, kind, snippet)."""
    findings = []
    out_lines = []
    in_fence = False
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue

        # 1) Actual rendering bug: a single-tilde del pair in one inline context.
        for ctx in inline_contexts(line):
            ctx_no_code = strip_code_spans(ctx)
            for m in DEL_RE.finditer(ctx_no_code):
                if m.group(1) == "~":
                    findings.append((lineno, "STRUCK", m.group(0)))

        # 2) Latent risk: any unescaped bare tilde outside the whitelist.
        if path not in BARE_TILDE_WHITELIST:
            stripped = strip_code_spans(line)
            for m in BARE_TILDE_RE.finditer(stripped):
                snippet = stripped[max(0, m.start() - 20) : m.start() + 20].strip()
                findings.append((lineno, "BARE", snippet))

        out_lines.append(fix_line(line) if fix and path not in BARE_TILDE_WHITELIST else line)
    return findings, "".join(out_lines)


def main() -> int:
    fix = "--fix" in sys.argv[1:]
    total = 0
    for path in sorted(DOCS.rglob("*.md")):
        findings, fixed = scan_file(path, fix=fix)
        if not findings:
            continue
        total += len(findings)
        for lineno, kind, snippet in findings:
            print(f"{path}:{lineno}: [{kind}] …{snippet}…")
        if fix:
            path.write_text(fixed, encoding="utf-8")
            print(f"{path}: fixed")
    if total and not fix:
        print(f"\n{total} finding(s). STRUCK = renders as strikethrough now; "
              f"BARE = unescaped ~, escape as \\~ (run with --fix).")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
