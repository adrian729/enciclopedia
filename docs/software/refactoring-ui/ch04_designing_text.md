# Ch 4: Designing Text

## Table of Contents

- [1. Establish a type scale](#1-establish-a-type-scale)
- [2. Picking quality fonts](#2-picking-quality-fonts)
- [3. Paragraph readability](#3-paragraph-readability)
- [4. Aligning mixed text](#4-aligning-mixed-text)
- [5. Alignment rules](#5-alignment-rules)
- [6. Styling links](#6-styling-links)
- [7. Letter-spacing adjustments](#7-letter-spacing-adjustments)

## 1. Establish a type scale

- **Too many sizes is the default failure mode** — without a system, teams end up using nearly every pixel value between 10px and 24px, producing inconsistency and slowing down every size decision.
- **Use a non-linear scale** — smaller jumps at the bottom of the scale are useful, but at the top you don't want to agonize over 46px vs. 48px, so jumps should grow.
- **Modular scales have drawbacks** — deriving sizes from a ratio like 4:5, 2:3, or the golden ratio (1:1.618) on a 16px base is mathematically pure but produces fractional sizes (31.25px, 39.063px) that browsers round inconsistently, and the jumps are often too coarse for interface design.
- **Hand-crafted scales are more practical for UIs** — pick values by hand so you control exactly which sizes exist and avoid subpixel rounding, landing on a set constrained enough to speed decisions but not so tight it feels limiting.
- **Avoid em units when defining the scale** — because em is relative to the current font size, nested elements compute to sizes outside the scale (e.g., inside an element sized at 1.25em/20px, a nested .875em child computes to 17.5px, not a scale value). Stick to `px` or `rem` so you actually stay on the system.

## 2. Picking quality fonts

Developing a real eye for typefaces takes years. These heuristics short-circuit the learning curve.

| Heuristic | What it means |
|---|---|
| **Play it safe** | For UI work, a neutral sans-serif like Helvetica is the safe default. When in doubt, fall back on the system font stack (`-apple-system, Segoe UI, Roboto, Noto Sans, Ubuntu, Cantarell, Helvetica Neue`) — unambitious, but users already know it |
| **Ignore typefaces with less than five weights** | Families with many weights tend to be made with more care. Filtering Google Fonts to 10+ styles (weights plus italics) cuts 85% of the catalog and leaves fewer than 50 sans-serifs |
| **Optimize for legibility** | Fonts meant for headlines have tight letter-spacing and short x-heights; fonts for small sizes have wider spacing and taller lowercase letters. Don't use a condensed, short-x-height headline face for body UI text |
| **Trust the wisdom of the crowd** | Sort font directories by popularity — if a font is widely used, it's probably good. Especially useful for harder picks like a serif with personality |
| **Steal from people who care** | Inspect well-designed sites and borrow their typefaces — strong design teams surface fonts you'd never reach through safer filters |

## 3. Paragraph readability

- **Keep line length between 45 and 75 characters** — fitting paragraph text to the layout width usually produces lines that are too long and hard to read. On the web, a width of 20–35em is a good proxy. Slightly wider than 75 can work, but 45–75 is the safe zone.
- **Limit paragraph width even when surrounding content is wider** — if paragraphs sit alongside images or large components, constrain only the text column. Mixing widths in the same content area looks more polished than stretching prose to match.
- **Line-height is proportional, not a fixed 1.5** — the purpose of line spacing is to help the eye find the next line when text wraps. Longer lines force bigger horizontal eye jumps and need more spacing; narrow content can use 1.5, wide content may need up to 2.
- **Line-height and font size are inversely proportional** — small text needs extra spacing so the eye can reacquire the next line; large headline text often works fine at a line-height of 1.

## 4. Aligning mixed text

- **Baseline, not center** — when two font sizes share a line (e.g., a large card title next to smaller actions), centering them vertically offsets their baselines and looks awkward, especially when the text is close together. Aligning to the baseline — the line letters rest on — uses a reference the eye already perceives and reads as simpler and cleaner.

## 5. Alignment rules

- **Match the direction of the language** — for English and most languages, that means left-aligning the vast majority of text.
- **Don't center long-form text** — center alignment is fine for headlines or short independent blocks, but anything longer than two or three lines looks better left-aligned. If centering a group and one block is too long, rewrite it shorter rather than left-aligning just that one.
- **Right-align numbers in tables** — aligning decimals in the same vertical position makes columns of numbers easier to compare at a glance.
- **Hyphenate justified text** — justification can create awkward word gaps on the web. If you justify (e.g., to mimic a print/magazine look), enable hyphenation to close the gaps. Justified text is otherwise a stylistic choice; left-aligned works just as well.

## 6. Styling links

- **Not every link needs a color** — the classic "pop" treatment makes sense for a link inside paragraph text, but in interfaces where almost everything is a link it becomes overbearing.
- **Emphasize most links subtly** — a heavier font weight or slightly darker color is enough to mark something as clickable without shouting.
- **Ancillary links can skip default emphasis entirely** — for links that aren't on the main path, show the underline or color only on hover. They stay discoverable for users who try, without competing with primary actions.

## 7. Letter-spacing adjustments

As a rule, trust the typeface designer and leave letter-spacing alone. Two situations justify tweaking it.

- **Tightening headlines** — a family built for small-size legibility (e.g., Open Sans) has wider letter-spacing than one built for headlines (e.g., Oswald). If you're using a body-optimized face for titles, decrease the letter-spacing to mimic the condensed look of a purpose-built headline family. The reverse doesn't work — headline fonts rarely work at small sizes even with extra letter-spacing.
- **Improving all-caps legibility** — default letter-spacing is tuned for "sentence case" with its mix of x-height letters, descenders (y, g, p), and ascenders (b, f, t). All-caps text is uniformly tall and loses those distinguishing features, so increasing letter-spacing gives the eye room to separate letters and improves readability.
