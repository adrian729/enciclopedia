# Ch 7: Working with Images

## Table of Contents

- [1. Use good photos](#1-use-good-photos)
- [2. Text needs consistent contrast](#2-text-needs-consistent-contrast)
- [3. Everything has an intended size](#3-everything-has-an-intended-size)
- [4. Beware user-uploaded content](#4-beware-user-uploaded-content)

## 1. Use good photos

- **Bad photos ruin good designs** — no amount of good layout, type, or color saves a design whose photography is weak.
- **Hire a professional** — for project-specific imagery. Great photos are about lighting, composition, and color, not an expensive camera. Those skills take years.
- **Use high-quality stock photography** — for generic needs, paid stock libraries and free sources like Unsplash offer usable images.
- **Don't design with placeholders and "fix it later"** — swapping in smartphone snaps at the end never works. Decide on real imagery up front.

## 2. Text needs consistent contrast

Photos have both very light and very dark areas, so a single text color gets lost in at least one of them. The fix isn't the text — it's reducing the image's dynamic range so contrast against the text stays consistent everywhere.

| Technique | How it works | Trade-off |
|---|---|---|
| **Add an overlay** | Semi-transparent layer over the image — black overlay tones down light areas so light text stands out; white overlay brightens dark areas so dark text stands out | Lightens or darkens the whole image, not just the problem spots |
| **Lower the image contrast** | Reduce the contrast of the image itself, then compensate brightness so overall feel stays right | More control, but requires editing the source image |
| **Colorize the image** | Three steps: (1) lower image contrast, (2) desaturate to remove existing color, (3) add a solid fill using the "multiply" blend mode | Can double as a way to tie the image into brand colors |
| **Add a text shadow** | Large blur radius, no offset — reads like a subtle glow, not a drop shadow. Boosts contrast only where the text actually is | Best combined with a small contrast reduction; preserves more of the photo's dynamics |

## 3. Everything has an intended size

Scaling bitmap images up produces fuzziness — but size mistakes hurt vectors and screenshots too, even when quality looks "safe."

- **Don't scale up icons** — vector icons drawn at 16–24px won't go blurry when enlarged, but they look disproportionately "chunky" and lack detail at 3x or 4x their intended size. They were never designed for that scale.
- **Enclose small icons in a shape** — when small icons are all you have and you need to fill a larger space, put them inside a container shape with a background color. The icon stays near its intended size while the shape occupies the space.
- **Don't scale down screenshots** — shrinking a full-size screenshot 70% to fit crams too much detail into too little space. A 16px font in the app becomes a 4px font in the screenshot, forcing visitors to squint.
- **Shoot at a smaller screen size** — take the screenshot at a tablet layout (or similar) and reserve plenty of space for it, so less shrinking is needed.
- **Use a partial screenshot** — show only a meaningful slice of the UI when full-app detail isn't essential; no scaling needed.
- **Redraw a simplified UI** — if a whole-app screenshot must fit a tight space, draw a stripped version with details removed and small text replaced by simple lines. Communicates the big picture without tempting readers to decode every pixel.
- **Don't scale down icons either** — icons built for large sizes go choppy and fuzzy when shrunk.
- **Favicons are the extreme case** — a 128px logo crunched into a 16px favicon turns to mush because the browser has to invent how to render that detail. Redraw a simplified version at the target size so you control the compromises, not the browser.

## 4. Beware user-uploaded content

User-uploaded images can't be fine-tuned for contrast, color, or crop. You can't fix the content, but you can stop it from wrecking the layout.

- **Control shape and size** — displaying uploads at their intrinsic aspect ratio throws off page structure, especially with many images on screen. Center images inside fixed containers and crop whatever doesn't fit. CSS makes this easy via a background image with `background-size: cover`.
- **Prevent background bleed** — when an uploaded image's background matches the UI background, the image loses its shape where the two blend. A border fights with the image's colors; a subtle inner box shadow defines the edge without clashing — most people won't notice it's there.
- **Alternative to inner shadow** — if the slight inset look bothers you, a semi-transparent inner border works just as well.
