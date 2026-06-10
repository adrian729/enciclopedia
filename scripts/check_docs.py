#!/usr/bin/env python3
"""Mechanical lint for docs/ markdown: md-standards headings/TOC + docsify anchors/links.

Checks per file (see the md-standards and docsify skills):
- exactly one H1, first heading in the file;
- H2-H4 numbered `N.` / `N.M.` / `N.M.K.` in sequence ('Table of Contents'
  and 'Sources' are the two sanctioned unnumbered H2s); no level skips;
- `## Table of Contents` whose entries mirror every H2-H4 below it: exact
  text, 2-space indent per level, and anchors computed with docsify v4's
  actual slugify (punctuation stripped, spaces->-, runs collapsed; the `_`
  digit-prefix is stripped to match the fixHeadingIds plugin);
- every relative link target exists (paths are root-relative to docs/) and
  every `#anchor` (in-page or cross-page) matches a real heading slug;
- math delimiters: `$` is forbidden outside code (KaTeX uses \\( \\) / \\[ \\]);
  \\( \\[ \\) \\] must not appear inside code fences (the katexMath plugin in
  index.html extracts them from RAW markdown, fences included); per-file
  \\( vs \\) and \\[ vs \\] counts must balance.

Usage:
    python3 scripts/check_docs.py                    # default scope: docs/software/procedural
    python3 scripts/check_docs.py docs/foo docs/bar.md
"""
import os
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

# docsify v4 slugify's strip-list: ASCII punctuation + general/supplemental punctuation blocks.
PUNCT_RE = re.compile(
    "[ -⁯⸀-⹿" + re.escape("\\'!\"#$%&()*+,./:;<=>?@[]^`{|}~") + "]"
)


def docsify_slug(text, cache):
    """docsify v4 slugify + the fixHeadingIds digit-prefix strip."""
    s = text.strip().lower()
    s = re.sub(r"<[^>]+>", "", s)
    s = PUNCT_RE.sub("", s)
    s = re.sub(r"\s", "-", s)
    s = re.sub(r"-+", "-", s)
    count = cache.get(s)
    if count is None:
        cache[s] = 0
    else:
        cache[s] = count + 1
        s = f"{s}-{cache[s]}"
    return s


def strip_md(text):
    return re.sub(r"[*_`]", "", text).strip()


def parse_file(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    headings = []
    in_fence = False
    for i, line in enumerate(lines, 1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*?)\s*$", line)
        if m:
            headings.append((i, len(m.group(1)), m.group(2)))
    cache = {}
    slugs = [(ln, lvl, text, docsify_slug(text, cache)) for (ln, lvl, text) in headings]
    return lines, slugs


def slugs_for(relpath, slug_cache):
    if relpath not in slug_cache:
        target = DOCS / relpath
        if not target.is_file():
            slug_cache[relpath] = None
        else:
            _, tslugs = parse_file(target)
            slug_cache[relpath] = {s for (_, _, _, s) in tslugs}
    return slug_cache[relpath]


def check_file(path, slug_cache, problems):
    rel = path.relative_to(DOCS)
    fname = str(rel)
    lines, slugs = parse_file(path)
    own_slugs = {s for (_, _, _, s) in slugs}
    slug_cache[str(rel)] = own_slugs

    h1s = [h for h in slugs if h[1] == 1]
    if len(h1s) != 1:
        problems.append(f"{fname}: expected exactly 1 H1, found {len(h1s)}")
    if slugs and slugs[0][1] != 1:
        problems.append(f"{fname}: first heading is not H1")

    prev_lvl = None
    for (ln, lvl, text, _) in slugs:
        if prev_lvl is not None and lvl > prev_lvl + 1:
            problems.append(f"{fname}:{ln}: level skip H{prev_lvl} -> H{lvl} ('{text}')")
        prev_lvl = lvl

    h2n = 0
    h3n = 0
    h4n = 0
    for (ln, lvl, text, _) in slugs:
        if lvl == 2:
            h3n = 0
            if text in ("Table of Contents", "Sources"):
                continue
            m = re.match(r"^(\d+)\.\s+\S", text)
            if not m:
                problems.append(f"{fname}:{ln}: H2 not numbered 'N. ': '{text}'")
                h2n = None
                continue
            n = int(m.group(1))
            if h2n is not None and n != h2n + 1:
                problems.append(f"{fname}:{ln}: H2 numbering jump: expected {h2n + 1}, got {n} ('{text}')")
            h2n = n
        elif lvl == 3:
            h4n = 0
            m = re.match(r"^(\d+)\.(\d+)\.\s+\S", text)
            if not m:
                problems.append(f"{fname}:{ln}: H3 not numbered 'N.M. ': '{text}'")
                continue
            a, b = int(m.group(1)), int(m.group(2))
            if h2n is not None and a != h2n:
                problems.append(f"{fname}:{ln}: H3 parent number {a} != current H2 {h2n} ('{text}')")
            if b != h3n + 1:
                problems.append(f"{fname}:{ln}: H3 sub-number jump: expected {h3n + 1}, got {b} ('{text}')")
            h3n = b
        elif lvl == 4:
            m = re.match(r"^(\d+)\.(\d+)\.(\d+)\.\s+\S", text)
            if not m:
                problems.append(f"{fname}:{ln}: H4 not numbered 'N.M.K. ': '{text}'")
                continue
            a, b, c = (int(g) for g in m.groups())
            if h2n is not None and (a != h2n or b != h3n):
                problems.append(f"{fname}:{ln}: H4 parent {a}.{b} != current {h2n}.{h3n} ('{text}')")
            if c != h4n + 1:
                problems.append(f"{fname}:{ln}: H4 sub-number jump: expected {h4n + 1}, got {c} ('{text}')")
            h4n = c

    toc_start = next((ln for (ln, lvl, text, _) in slugs if lvl == 2 and text == "Table of Contents"), None)
    if toc_start is None:
        problems.append(f"{fname}: no '## Table of Contents'")
    else:
        toc_entries = []
        for i in range(toc_start, len(lines)):
            if i + 1 > toc_start and re.match(r"^#{1,6}\s", lines[i]):
                break
            m = re.match(r"^(\s*)-\s+\[([^\]]+)\]\(#([^)]+)\)\s*$", lines[i])
            if m:
                toc_entries.append((i + 1, len(m.group(1)), m.group(2), m.group(3)))
        expected = [(ln, lvl, text, slug) for (ln, lvl, text, slug) in slugs
                    if lvl in (2, 3, 4) and text != "Table of Contents" and ln > toc_start]
        if len(toc_entries) != len(expected):
            problems.append(f"{fname}: TOC has {len(toc_entries)} entries, document has {len(expected)} H2-H4 headings")
        for (te, ex) in zip(toc_entries, expected):
            t_ln, t_indent, t_text, t_anchor = te
            _, e_lvl, e_text, e_slug = ex
            if strip_md(t_text) != strip_md(e_text):
                problems.append(f"{fname}:{t_ln}: TOC text '{t_text}' != heading '{e_text}'")
            if t_anchor != e_slug:
                problems.append(f"{fname}:{t_ln}: TOC anchor '#{t_anchor}' != computed slug '#{e_slug}' for '{e_text}'")
            if t_indent != (e_lvl - 2) * 2:
                problems.append(f"{fname}:{t_ln}: TOC indent {t_indent} != expected {(e_lvl - 2) * 2} for H{e_lvl} '{e_text}'")

    in_fence = False
    for i, line in enumerate(lines, 1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in re.finditer(r"\[([^\]]*)\]\(([^()\s]+)\)", line):
            href = m.group(2)
            if href.startswith(("http://", "https://", "mailto:")):
                continue
            if href.startswith("#"):
                if href[1:] not in own_slugs:
                    problems.append(f"{fname}:{i}: in-page anchor '{href}' not found")
                continue
            target, _, anchor = href.partition("#")
            if not (DOCS / target).is_file():
                problems.append(f"{fname}:{i}: link target missing: '{target}' (links are root-relative to docs/)")
                continue
            if anchor:
                tslugs = slugs_for(target, slug_cache)
                if tslugs is not None and anchor not in tslugs:
                    problems.append(f"{fname}:{i}: anchor '#{anchor}' not found in '{target}'")

    in_fence = False
    for i, line in enumerate(lines, 1):
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if in_fence:
            if any(tok in line for tok in ("\\(", "\\[", "\\)", "\\]")):
                problems.append(f"{fname}:{i}: math-like delimiter inside code fence (katexMath plugin extracts from raw markdown): {line.strip()[:60]}")
            continue
        if "$" in re.sub(r"`[^`]*`", "", line):
            problems.append(f"{fname}:{i}: '$' outside code span (math must use \\( \\) / \\[ \\]): {line.strip()[:60]}")
    body = []
    in_fence = False
    for line in lines:
        if re.match(r"^\s*```", line):
            in_fence = not in_fence
            continue
        if not in_fence:
            body.append(line)
    whole = "\n".join(body)
    for op, cl in (("\\(", "\\)"), ("\\[", "\\]")):
        if whole.count(op) != whole.count(cl):
            problems.append(f"{fname}: unbalanced math delimiters: {whole.count(op)}x '{op}' vs {whole.count(cl)}x '{cl}'")


def main():
    args = sys.argv[1:] or ["docs/software/procedural"]
    repo = DOCS.parent
    files = []
    for a in args:
        p = (repo / a).resolve() if not os.path.isabs(a) else Path(a)
        if p.is_dir():
            files.extend(sorted(p.rglob("*.md")))
        elif p.is_file():
            files.append(p)
        else:
            print(f"not found: {a}")
            sys.exit(2)

    problems = []
    slug_cache = {}
    for f in files:
        check_file(f, slug_cache, problems)

    if problems:
        print(f"{len(problems)} problem(s):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print(f"CLEAN: all mechanical checks passed for {len(files)} file(s)")


if __name__ == "__main__":
    main()
