# Ch 2: Hierarchy is Everything

## Table of Contents

- [1. Why hierarchy matters](#1-why-hierarchy-matters)
- [2. Don't lean on font size alone](#2-dont-lean-on-font-size-alone)
- [3. Contrast on colored backgrounds](#3-contrast-on-colored-backgrounds)
- [4. Emphasize by de-emphasizing](#4-emphasize-by-de-emphasizing)
- [5. Labels are a last resort](#5-labels-are-a-last-resort)
- [6. Separate visual hierarchy from document hierarchy](#6-separate-visual-hierarchy-from-document-hierarchy)
- [7. Balance weight and contrast](#7-balance-weight-and-contrast)
- [8. Semantics are secondary](#8-semantics-are-secondary)

## 1. Why hierarchy matters

- **Visual hierarchy** — how important elements appear relative to one another; the most effective tool for making an interface feel "designed".
- **Competing elements feel chaotic** — when everything shouts equally, the UI becomes a wall of content where nothing matters. Deliberately de-emphasizing secondary and tertiary information makes the important bits pop without touching color, type, or layout.

## 2. Don't lean on font size alone

- **Size isn't everything** — relying too much on font size produces primary content that's too large and secondary content that's too small. Use font weight or color to do the same job with less distortion.
- **Bolder primary, softer secondary** — making a primary element heavier lets you keep the font size reasonable, and using a softer color for supporting text signals "less important" without shrinking it into unreadability.

Restrict yourself to small palettes for text hierarchy. Stick to two or three colors:

| Role | Color |
|---|---|
| Primary content (e.g., article headline) | Dark color |
| Secondary content (e.g., article date) | Grey |
| Tertiary content (e.g., footer copyright) | Lighter grey |

- **Two font weights are usually enough** — a normal weight (400 or 500 depending on the font) for most text, and a heavier weight (600 or 700) for text you want to emphasize.
- **Avoid weights under 400** — they can work for large headings but are too hard to read at smaller sizes. Reach for a lighter color or smaller font size instead of a lighter weight.

## 3. Contrast on colored backgrounds

- **Grey text works because of reduced contrast, not because it's grey** — the effect relies on the text being closer to the background color. Grey on white works; grey on a colored background does not.
- **White at reduced opacity looks washed out** — it can also let background images or patterns bleed through the text.
- **Hand-pick a tinted color** — pick a color with the same hue as the background, then adjust saturation and lightness until it reads as de-emphasized without looking faded.

## 4. Emphasize by de-emphasizing

- **Turn down the competition, not up the target** — when the main element won't stand out no matter what you add, soften the elements competing with it instead. An active nav item "pops" once the inactive items are given a softer color.
- **Applies at the component level too** — if a sidebar is fighting the main content, drop its background color and let it sit directly on the page background rather than adding more styling to the content.

## 5. Labels are a last resort

- **Avoid naive `label: value` formatting** — giving every piece of data a label forces equal emphasis on all of it, killing hierarchy.
- **Format or context often removes the need for a label** — `janedoe@example.com` is obviously an email, `(555) 765-4321` a phone number, `$19.99` a price. "Customer Support" under a name in an employee directory reads as a department without being labeled.
- **Combine labels and values into one unit** — turn "In stock: 12" into "12 left in stock"; turn "Bedrooms: 3" into "3 bedrooms". Each item can then be styled meaningfully without sacrificing clarity.
- **When labels are necessary, treat them as secondary** — on dashboards with many similar fields, keep the label but de-emphasize it with smaller size, lower contrast, lighter weight, or a mix. The data is what matters; the label just clarifies.
- **When to emphasize the label instead** — on information-dense pages like technical specs, users scan for the label ("depth"), not the value ("7.6mm"). Use a darker color for the label and a slightly lighter color for the value; don't de-emphasize the data too much.

## 6. Separate visual hierarchy from document hierarchy

- **Semantic tag != visual size** — browsers default `h1` to large and `h6` to small, which fits articles but misleads in application UIs. A "Manage Account" page title is legitimately an `h1`, but doesn't need to be huge.
- **Section titles often behave like labels** — they're supporting content and should not steal attention from the content they introduce. Titles should often be pretty small, and sometimes hidden visually (kept in markup for accessibility) when the content speaks for itself.
- **Pick the element for semantics, style it for hierarchy** — don't let the tag you chose dictate the look.

## 7. Balance weight and contrast

- **Bold feels heavy because it covers more surface area** — more pixels of text per unit of background. This relationship extends beyond text to any UI element with visual "weight".
- **Contrast compensates for weight** — icons (especially solid ones) are heavy and tend to dominate adjacent text. Since you can't change an icon's weight, lower its contrast with a softer color to rebalance.
- **Weight compensates for contrast** — when a thin 1px border is too subtle in a soft color but darkening it makes the design feel harsh, thicken the border instead. Increased weight restores emphasis without losing the softer look.

## 8. Semantics are secondary

- **Actions sit in a pyramid of importance** — most pages have one true primary action, a couple of secondary actions, and a few tertiary actions. Designing buttons on semantics alone (e.g., "save is primary because it's the main verb") ignores hierarchy.
- **Match styling to position in the pyramid**:

| Tier | Role | Treatment |
|---|---|---|
| Primary | Should be obvious | Solid, high-contrast background colors |
| Secondary | Clear but not prominent | Outline styles or lower-contrast background colors |
| Tertiary | Discoverable but unobtrusive | Styled like links |

- **Destructive != primary** — being destructive or high-severity doesn't automatically mean big, red, and bold. If the destructive action isn't the primary action on the page, give it secondary or tertiary treatment, then apply the big, red, bold styling on the confirmation step where destroying is genuinely the primary action.
