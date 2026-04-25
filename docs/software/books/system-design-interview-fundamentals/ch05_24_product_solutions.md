# Ch 5.24: Product Solutions

## Table of Contents

- [1. Why Product Thinking in a Technical Interview](#1-why-product-thinking-in-a-technical-interview)
- [2. Example: Location with Poor Reception](#2-example-location-with-poor-reception)
- [3. Example: Complicated User Experience](#3-example-complicated-user-experience)

## 1. Why Product Thinking in a Technical Interview

- **Not every problem is solved with more infrastructure** — taking a step back to reframe the user problem can reveal a non-technical solution that obviates the technical complexity
- **User empathy is a senior-level signal** — the more senior the role, the more product sense and empathy matter; a pure-infra answer can come across as narrow

## 2. Example: Location with Poor Reception

- **Situation** — ridesharing service: how do you handle drivers in areas with poor cell reception?
- **Engineering-only answer** — rely on heartbeats to mark the driver offline when reception drops. Correct but cold; doesn't address the driver's frustration
- **Product-aware answer** — also surface known poor-reception regions to drivers in the app so they can avoid them while waiting for a ride. Pairs the heartbeat with empathy for the user

## 3. Example: Complicated User Experience

- **Situation** — initial design fans out a ride request to three drivers and lets any of them accept
- **Problems introduced by the design** — acceptance races between drivers, locked-up drivers multiplying 3× per request, risk of depleting the driver pool
- **Product redesign** — backend auto-assigns a single driver; the driver has the right to cancel and go offline if they don't want the ride. Same (or better) user experience, dramatically simpler technical implementation
- **Lesson** — when the technical complexity gets hairy, ask whether the product requirement can change to sidestep it entirely
