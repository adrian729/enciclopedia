# Ch 5: Working with Color

## Table of Contents

- [1. Ditch hex for HSL](#1-ditch-hex-for-hsl)
- [2. You need more colors than you think](#2-you-need-more-colors-than-you-think)
- [3. Define your shades up front](#3-define-your-shades-up-front)
- [4. Don't let lightness kill your saturation](#4-dont-let-lightness-kill-your-saturation)
- [5. Greys don't have to be grey](#5-greys-dont-have-to-be-grey)
- [6. Accessibility without ugliness](#6-accessibility-without-ugliness)

## 1. Ditch hex for HSL

- **Hex and RGB hide visual relationships** — colors that look closely related to the eye look nothing alike in hex or RGB code, so it's hard to reason about shades and variations.
- **HSL matches how humans perceive color** — it represents every color using three intuitive attributes, so nudging a value in code produces a predictable visual change.

| Attribute | Meaning |
|---|---|
| **Hue** | Position on the color wheel, measured in degrees: 0° red, 120° green, 240° blue. Hue is what lets us call two different colors both "blue" |
| **Saturation** | How vivid the color is. 0% is grey (no color — rotating hue at 0% saturation changes nothing), 100% is vibrant and intense |
| **Lightness** | Proximity to black or white. 0% is pure black, 100% is pure white, 50% is a pure color at the given hue |

- **Don't confuse HSL with HSB** — in HSB, 0% brightness is always black, but 100% brightness is only white when saturation is 0%; at 100% saturation, 100% HSB brightness equals 50% HSL lightness. HSB is more common in design software, but browsers only understand HSL — for web work, use HSL.

## 2. You need more colors than you think

- **Five-color palettes aren't enough to build a real UI** — the palette-generator approach of picking five "perfect" colors is seductive but produces sites that look like the generator output. Real interfaces need a far broader set.
- **A palette breaks into three categories** — greys, primary color(s), and accent colors. All three need shades.

| Category | What it's for | How many shades |
|---|---|---|
| **Greys** | Text, backgrounds, panels, form controls — almost everything in an interface is grey. Start from a very dark grey (true black looks unnatural) and step up to white in even increments | 8–10 shades |
| **Primary color(s)** | One or two colors for primary actions, active nav elements — the colors that define a site's identity (e.g., Facebook blue). Ultra-light shades tint alert backgrounds; darker shades work for colored text | 5–10 shades |
| **Accent colors** | Eye-grabbers for new features, plus semantic colors — red for destructive confirmations, yellow for warnings, green for positive trends. Used sparingly but still need multiple shades | Multiple shades each |

- **Complex UIs can need up to ten colors with 5–10 shades each** — especially when color must distinguish items like graph lines, calendar events, or tags.

## 3. Define your shades up front

- **Don't generate shades on the fly** — CSS preprocessor functions like `lighten` and `darken` produce 35 near-identical blues across a codebase. Define a fixed palette once and pick from it.
- **Choose the base color first** — pick the middle shade your lighter and darker shades will be derived from. For primary and accent colors, a rule of thumb is: would this color work as a button background?
- **Find the edges next** — pick the darkest and lightest shades by thinking about where they'll be used. Darkest is typically for text; lightest is typically for tinted backgrounds. A simple alert component exercises both at once and is a good place to choose them.
- **Fill in the gaps** — nine shades is a useful number because it divides cleanly. Label darkest 900, base 500, lightest 100, then pick 700 and 300 as the midpoints, then 800/600/400/200 the same way.
- **For greys, skip the base and start from the edges** — pick the darkest grey as your darkest-text color and the lightest grey as a subtle off-white background, then fill between them.
- **It's not a science** — a systematic process gets you started, but trust your eyes over the numbers and tweak saturation or lightness once you start using shades in real designs. At the same time, avoid adding new shades constantly — a palette you keep extending isn't really a system.

## 4. Don't let lightness kill your saturation

- **Saturation's impact weakens near 0% and 100% lightness** — the same saturation value that looks vivid at 50% lightness looks washed out at 90%. To keep lighter and darker shades from feeling dull, increase saturation as lightness moves away from 50%.
- **Every hue has an inherent perceived brightness** — the human eye reads yellow as lighter than blue even at identical HSL lightness. Sampling hues at 100% saturation and 50% lightness reveals three local minimums (red, green, blue) and three local maximums (yellow, cyan, magenta).
- **Change brightness by rotating the hue** — instead of only adjusting lightness (which pulls the color toward white or black and saps intensity), shift the hue toward a brighter or darker hue to change perceived brightness while preserving color richness.
  - **To lighten**, rotate the hue toward the nearest bright hue — 60°, 180°, or 300°.
  - **To darken**, rotate the hue toward the nearest dark hue — 0°, 120°, or 240°.
- **Hue rotation works best in small doses** — combining hue rotation with lightness adjustment is fine, but don't rotate more than 20–30° or the result reads as a different color rather than a lighter or darker version. Useful for a light base like yellow: rotating toward orange as you darken produces warm, rich dark shades instead of dull browns.

## 5. Greys don't have to be grey

- **True grey has 0% saturation** — it contains no actual color. But most "greys" in polished interfaces are lightly saturated, which gives them a temperature.
- **Saturate greys to set a temperature** — like warm-white vs. cool-white light bulbs, greys tinted toward blue feel cool, and greys tinted toward yellow or orange feel warm. The amount is up to you — a little tint shifts the mood slightly; heavier tint pushes the whole interface in one direction.
- **Raise saturation for the lighter and darker greys too** — same principle as primary colors: without it, the extremes of the scale will look washed out relative to the mid-tones and break the temperature consistency.

## 6. Accessibility without ugliness

- **WCAG contrast minimums** — the Web Content Accessibility Guidelines recommend a contrast ratio of at least 4.5:1 for normal text (under ~18px) and 3:1 for larger text. Dark text on light backgrounds hits this easily; colored backgrounds make it harder.
- **Flip the contrast instead of fighting for white-on-color** — white text on a colored background often needs a very dark color to reach 4.5:1, which over-emphasizes elements that shouldn't be focal. Swap to dark colored text on a light colored background of the same hue — the color still supports the text but the element stops screaming for attention.
- **Rotate the hue to make colored-on-colored text accessible** — when placing secondary text inside a dark colored panel, simply tweaking lightness and saturation of the background color often can't reach the contrast ratio without going nearly white. Since some hues are inherently brighter, rotating the hue toward cyan, magenta, or yellow increases contrast while keeping the text colorful.
- **Don't rely on color alone** — users with color blindness can't read information encoded only in hue. On red-green metric cards, for example, add icons to indicate positive or negative change.
- **For charts with many series, rely on contrast rather than different hues** — colorblind users distinguish light-vs-dark far more easily than two distinct colors. Color should always support something the design is already communicating, never carry the message by itself.
