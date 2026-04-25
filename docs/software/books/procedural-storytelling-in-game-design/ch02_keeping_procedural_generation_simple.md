# Ch 2: Keeping Procedural Generation Simple

## Table of Contents

- [1. Why Simplicity Wins](#1-why-simplicity-wins)
- [2. Spelunky Case Studies](#2-spelunky-case-studies)
- [3. Perception, Context, and Scope](#3-perception-context-and-scope)

## 1. Why Simplicity Wins

- **Technical creep** — procgen attracts people who love technique and who keep reaching for greater complexity to impress an internalised spectator. Fine in research; fatal under a deadline.
- **Brian Reynolds' rule (Rise of Nations AI)** — when designing computer decision-making, first pick a decision *out of a hat at random* and test it. If the AI plays well enough, stop. Only complicate when the naive version fails.
- **Start simple, ship, learn** — you will learn more about a generator's real behaviour once players use it than you ever will in years of internal iteration. Simpler code means more shipped projects and more real feedback.

## 2. Spelunky Case Studies

Two level-generation examples from Derek Yu's *Spelunky* showing "simple" at both ends of the elegance scale.

- **Treasure placement (~1 line)** — for any empty ground tile, probability of treasure is directly proportional to the number of adjacent solid surfaces. Corners and crawlspaces get more loot than open floor; fully enclosed pockets get the most. Matches human intuition about where valuables are hidden.
- **Giant Spider placement (~30 lines, kludgy)** — in the first cave tile set, for every brick tile that isn't the level's ceiling or in a shop, starting room, or the bottom half of a room, check for a 2×2 empty block below; if found and no Giant Spider yet, 1-in-40 chance to spawn one with cobwebs.
- **Takeaway** — one line vs thirty lines, but both avoid A*, cellular automata, and Perlin noise. Both use simple checks against features already in the world model and add no new systems. Good enough beat elegant; *Spelunky* shipped as a modern classic either way.

## 3. Perception, Context, and Scope

- **Perception versus reality** — players assume far more complexity than is present. Kazemi's "Two Headlines" Twitter bot scrapes Google News and does find-and-replace on subjects; audiences routinely guess NLP or machine learning. People attach narratives to explain algorithms, sometimes crediting intelligence to randomness.
- **Context turns trivial into impressive** — the "You Must Be" generator (2011) grabs a random noun and its dictionary definition and wraps it in a pickup line: *"Girl, you must be an earthquake, because you are a shaking of the ground caused by the movement of the earth's tectonic plates."* The algorithm is trivial; the framing makes it a joke. Same pattern as Ken Perlin turning a stepping-gradient algorithm into texture generation. The craft is in the context, not the technique.
- **The problem might not be your procgen** — if a Mario-style level generator keeps producing unjumpable gaps, don't fix the generator: add a run button, rising lava, or crumbling platforms. Changing context around the generator can flip a "bad" generator into a "good" one (and vice versa — *Spelunky*'s level generator would produce terrible Pac-Man levels).
- **Before asking "what's the best way to generate X?"** — ask: what way do I already know, why is that version unsatisfying, and what can I change *outside* the generator to make it feel right? Usually faster, simpler, and more informative about the non-procedural parts of the game.
