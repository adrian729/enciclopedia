# Ch 6: Creating Depth

## Table of Contents

- [1. Emulate a light source](#1-emulate-a-light-source)
- [2. Raised vs. inset elements](#2-raised-vs-inset-elements)
- [3. Shadows convey elevation](#3-shadows-convey-elevation)
- [4. Two-part shadows](#4-two-part-shadows)
- [5. Depth without shadows](#5-depth-without-shadows)
- [6. Overlap elements to create layers](#6-overlap-elements-to-create-layers)

## 1. Emulate a light source

- **Light comes from above** — the single rule behind perceived depth. A real-world panel looks raised because its top edge is angled toward the sky (lighter) and its bottom edge angles away (darker); an inset panel reverses the pattern. Mimic this and the brain reads depth automatically.
- **Pick the profile, then light it** — decide whether an element should feel raised or inset, then apply highlights and shadows the way a light source would actually interact with that shape. Don't tweak shadows at random.
- **Don't get carried away** — borrowing real-world cues adds depth, but chasing photo-realism produces busy, unclear interfaces. A little is plenty.

## 2. Raised vs. inset elements

Flat-edged buttons can't show both top and bottom edges at once. Because users look slightly downward at their screens, reveal the edge that's naturally visible and hide the other.

| Element | Visible edge | Highlight | Cast shadow |
|---|---|---|---|
| **Raised** (e.g., button) | Top edge | Top border or inset box shadow with a slight vertical offset, slightly lighter than the face | Small dark box shadow with a slight positive vertical offset below the element, sharp-ish (a couple of pixels of blur, not more) |
| **Inset** (e.g., well, text input, checkbox) | Bottom lip | Bottom border or inset shadow with a negative vertical offset, slightly lighter | Small dark inset box shadow with a slight positive vertical offset, so the top area blocks light as if recessed |

- **Hand-pick the highlight color** — overlaying semi-transparent white sucks saturation out of the underlying color. Choose the lighter shade directly for better results.
- **Sharp, subtle shadows** — real-world references like the shadow under a wall outlet or window frame have sharp edges, not big soft blurs.

## 3. Shadows convey elevation

Shadows are not decoration — they position elements on a virtual z-axis. The closer something feels to the user, the more attention it pulls.

| Shadow size / blur | Perceived elevation | Typical use |
|---|---|---|
| **Small, tight blur** | Slightly off the background | Buttons — noticed, but not dominating |
| **Medium** | Sits a bit above the UI | Dropdowns |
| **Large, higher blur** | Close to the user | Modal dialogs that need to capture attention |

- **Build an elevation system** — like color, type, spacing, and sizing, define a fixed set of shadows. Around five options is usually plenty; pick the smallest and largest first, then fill the middle with roughly linear increments.
- **Shadows as interaction cues** — adding a shadow to a list item when the user clicks it makes it pop forward and signals it can be dragged. Switching a button to a smaller shadow (or removing it) on click makes it feel pressed into the page.
- **Think in z-axis, not in shadow values** — decide where the element should sit in depth and assign the matching system shadow. This avoids endless fiddling with blur and offset.

## 4. Two-part shadows

Nice shadows on real sites are often two shadows stacked, each doing a distinct job.

| Layer | Shape | Role |
|---|---|---|
| **First shadow** | Larger, softer, considerable vertical offset, large blur radius | Simulates the shadow cast behind an object by a direct light source |
| **Second shadow** | Tighter, darker, smaller vertical offset, smaller blur radius | Simulates the shadowed area directly underneath an object where ambient light can't reach |

- **More control than a single shadow** — the larger shadow stays subtle and diffuse while the tighter shadow keeps the edges near the element crisp and defined.
- **Account for elevation** — as an object lifts off a surface, the tight ambient-occlusion shadow underneath fades. Make the second shadow distinct at the lowest elevation and almost (or completely) invisible at the highest.

## 5. Depth without shadows

"Flat design" usually means no shadows, gradients, or light-mimicking effects — but the strongest flat designs still convey depth by other means.

- **Depth with color** — among shades of the same color, lighter reads as closer and darker reads as further away. Make an element lighter than the background to feel raised; darker to feel inset like a well. Color works as a depth tool in non-flat designs too.
- **Solid shadows** — short, vertically offset shadows with no blur radius at all lift a card or button off the page without breaking the flat aesthetic.

## 6. Overlap elements to create layers

- **Overlap is one of the strongest depth cues** — letting elements break out of their containers makes a design feel multi-layered rather than stacked panels.
- **Cross background transitions** — instead of confining a card inside one section, offset it so it straddles two different backgrounds.
- **Overflow the parent** — make an element taller than its parent so it overlaps on both sides; also works for smaller components like carousel controls poking past the image edge.
- **Invisible borders on overlapping images** — overlapping images easily clash. Give each image a border that matches the background color so a small gap always separates them. The layered look stays; the clashing goes.
