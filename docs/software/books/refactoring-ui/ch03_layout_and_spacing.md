# Ch 3: Layout and Spacing

## Table of Contents

- [1. Start with too much white space](#1-start-with-too-much-white-space)
- [2. Establish a spacing and sizing system](#2-establish-a-spacing-and-sizing-system)
- [3. You don't have to fill the whole screen](#3-you-dont-have-to-fill-the-whole-screen)
- [4. Grids are overrated](#4-grids-are-overrated)
- [5. Relative sizing doesn't scale](#5-relative-sizing-doesnt-scale)
- [6. Avoid ambiguous spacing](#6-avoid-ambiguous-spacing)

## 1. Start with too much white space

- **White space should be removed, not added** — the default habit on the web is to add margin or padding only until something stops looking bad, which gives elements the minimum breathing room rather than enough to look great. Start with way too much space, then remove until you're happy.
- **"Too much" on an element reads as "just enough" in context** — what feels excessive when zoomed in on a single element usually settles into the right amount once you see the full UI.
- **Dense UIs have their place** — dashboards that must show a lot of data on one screen are a legitimate reason to pack things in. The key is making compactness a deliberate decision, not a default — it's much more obvious when to remove white space than when to add it.

## 2. Establish a spacing and sizing system

- **Don't nitpick arbitrary pixel values** — trialing 120px vs. 125px one pixel at a time slows work and produces inconsistent designs. Limit yourself to a constrained set of values defined in advance.
- **A linear scale won't work** — "make everything a multiple of 4px" doesn't help you choose between 120 and 125. A useful scale considers the *relative* difference between adjacent values.
- **Small end: a few pixels is a lot; large end: a few pixels is nothing** — jumping an icon from 12px to 16px is a 33% increase. Growing a card from 500px to 520px is only 4%, eight times less significant.
- **Minimum 25% gap between adjacent values** — ensures every step on the scale produces a visibly different result, so picking the next value up or down is a real choice.
- **Start from a sensible base** — 16px is a great starting number: it divides nicely and is the default browser font size. Build the scale with factors and multiples, packed tightly at the small end and progressively more spaced apart at the large end.
- **Payoff** — design work goes much faster (especially in the browser, where typed numbers are easier to stay within a system than mouse-dragged ones), and designs pick up a subtle consistency.

## 3. You don't have to fill the whole screen

- **Space available != space to use** — modern 1200–1400px canvases tempt you to fill them, but if an interface only needs 600px, use 600px. Spreading things out makes an interface harder to interpret; extra space around the edges never hurts.
- **Sections don't need to match the nav** — just because your navigation is full-width doesn't mean every section under it must be. Give each element the space it needs.
- **Shrink the canvas** — if a small interface is hard to design on a large canvas, design it on a ~400px canvas first. For responsive apps, start mobile-first and then adjust compromises when you move to larger screens — you won't need to change as much as you think.
- **Thinking in columns** — when something works best at a narrow width but feels unbalanced in a wide UI, split it into columns rather than stretching it. For example, break a form's supporting text into a second column so the form itself stays at its optimal width.
- **Don't force it either way** — just as you shouldn't stretch to fill the screen, you shouldn't cram into a small area. If you need the space, use it.

## 4. Grids are overrated

- **Grids give elements fluid, percentage-based widths** — a 12-column grid means each column is 8.33%, and "on the grid" means width is some multiple of 8.33% including gutters.
- **Not all elements should be fluid** — a sidebar given 3 of 12 columns (25%) grows too wide on large screens (wasting space the content could use) and shrinks below its minimum usable width on narrow screens (causing awkward wrapping or truncation). Better: fix the sidebar width to its content, let the main area flex to fill the rest and run its own internal grid.
- **Applies inside components too** — don't use percentages to size something unless you actually want it to scale.
- **Don't shrink an element until you need to** — a login card sized at 6 of 12 columns (50%) can end up *wider* on a medium screen (8 columns of a smaller canvas) than on a large screen, which is silly. If 500px is optimal, give it a `max-width` of 500px and only force it to shrink when the screen gets smaller than that.
- **Don't be a slave to the grid** — give components the space they need and only compromise when actually necessary.

## 5. Relative sizing doesn't scale

- **Don't assume proportions transfer across screen sizes** — if 18px body and 45px headline feel right on desktop, encoding headline as `2.5em` is tempting but misleading. Reduce body to 14px on small screens and `2.5em` becomes 35px — far too big. A better small-screen headline is 20–24px, only 1.5–1.7x the body, a different relationship entirely.
- **Large elements shrink faster than small ones** — as a general rule, the difference between small and large elements should be less extreme at small screen sizes. There's often no real fixed ratio between sizes, so defining one relative unit in terms of another offers no real benefit.
- **Relative sizing within a component also breaks down** — tying a button's padding to its font size does make it scale proportionally, but the result feels like you zoomed the button rather than resized it. Padding should get disproportionately more generous at larger sizes and disproportionately tighter at smaller sizes so large buttons feel genuinely large and small buttons genuinely small.
- **Fine-tune independently** — letting go of "everything must scale proportionately" makes it much easier to design for multiple contexts.

## 6. Avoid ambiguous spacing

- **Spacing signals grouping** — when groups of elements aren't separated by a border or background, spacing is what tells the user which elements belong together. Get it wrong and the grouping disappears.
- **Form labels and inputs** — if the margin below the label equals the margin below the input, the label-and-input pair doesn't feel connected, so users work harder to parse the form and may even put data in the wrong field. Fix it by increasing space *between* form groups relative to the space *inside* each group.
- **Same failure mode elsewhere** — not enough space above article section headings attaches them to the wrong paragraph; bullet spacing equal to the line-height of a single bullet blurs items together; horizontal component layouts can make the same mistake as vertical ones.
- **Rule of thumb** — whenever you're using spacing to connect a group of elements, make sure there's more space around the group than within it. Interfaces that are hard to understand always look worse.
