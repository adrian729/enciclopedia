# Ch 12: Procedural Logic

## Table of Contents

- [1. The Game and Its Constraint](#1-the-game-and-its-constraint)
- [2. Procedural Generation in the Usual Sense](#2-procedural-generation-in-the-usual-sense)
- [3. Generating the Rules Themselves](#3-generating-the-rules-themselves)
- [4. Queries and Solutions](#4-queries-and-solutions)
- [5. Improving the Generator](#5-improving-the-generator)
- [6. Rigging the Deck](#6-rigging-the-deck)
- [7. Putting It All Together](#7-putting-it-all-together)

## 1. The Game and Its Constraint

- **Keep Talking and Nobody Explodes** — cooperative bomb-defusal game where only one player (the **Defuser**) sees the screen and the others (**Experts**) read a static manual hosted at bombmanual.com; gameplay hinges on relaying details across that information gap.
- **Single design goal: foster interesting communication** — every PCG decision in the chapter is justified or rejected by whether it makes players talk, trip on words, and make mistakes.
- **The hard constraint** — the printed manual and the running game must never disagree; if rules ever drift, the entire concept collapses.

## 2. Procedural Generation in the Usual Sense

- **Bomb state is randomized** — wires, colors, button symbols, lights, batteries, serial numbers vary per round, so puzzle solutions vary too; this is what makes the game replayable.
- **Missions are authored subsets of the 14 puzzle types** — easy missions pick three simple puzzles, harder missions deliberately pair puzzles that conflict (e.g., a memory puzzle plus one demanding immediate attention) to force time-management challenges.
- **Without tailored missions** — truly random puzzle selection would either skip interesting combinations or produce wildly inconsistent difficulty.

## 3. Generating the Rules Themselves

- **The rules are also procedurally generated** — not just bomb state, but the logic the manual describes and the game executes.
- **Fixed random seed at ship time** — the generator runs the same way every time, so the printed manual stays valid; conceptually similar to locking a generated landscape before release.
- **Why generate at all** — future-proofing (manual variants can refresh content if players memorize the current one) and, more importantly, guaranteeing the manual matches the code.
- **Data-driven approach** — rules are stored as data; templates render the manual from that data and the game's logic executes from the same data, keeping the two in sync by construction.
- **Trivial generation case (Morse code puzzle)** — author a list of four/five-letter words, randomly map each to a response frequency; nothing more sophisticated needed because players already struggle to communicate the dots and dashes.
- **Countable case (Complicated Wires)** — four boolean wire properties yield 2^4 = 16 states; rules are just a "cut/don't cut" assignment per state, optionally enriched with bomb-level conditions like "cut if the bomb has more than two batteries" to force more communication.

## 4. Queries and Solutions

- **Wires puzzle motivates real procedural logic** — three to six wires with five colors each blow up to tens of thousands of states; an exhaustive lookup table would be unprintable and unfun.
- **Rule** — a logical predicate paired with an actionable outcome; covers part of the possibility space, and a list of rules together covers all of it.
- **Query** — a yes/no question about a property of the puzzle or the bomb (e.g., "are there more than two red wires?"); has both a manual text template (with substitutable arguments like `batteryCount`) and a game function (e.g., `MoreThanXBatteries`) so manual and game stay aligned.
- **Solution** — the action a player takes when the rule fires (e.g., text "cut the third wire" / function `CutWire3`); each puzzle type has its own pool of authored solutions.
- **Composition** — a rule = one or more queries + one solution; generation draws from authored pools and combines them.

## 5. Improving the Generator

- **Compound queries** — multiple queries combined ("more than two red wires AND parallel port"); they cover smaller subsets and so fire less often, which means a balanced mix of simple and compound queries is needed so players aren't constantly answering "no" (tested as tiresome).
- **Query contexts: puzzle-specific vs. bomb-specific** — bomb-level facts (serial number, battery count) get cached by the Defuser after the first puzzle, so every rule must include at least one puzzle-specific query; otherwise multiple puzzles degenerate into the same single bomb-level lookup.
- **More expressive solutions** — six wires give only six "cut wire N" solutions, so solutions gain a fragment of logic ("cut the last red wire"); this requires the paired query to guarantee the referenced object exists (e.g., "if there are more than two red wires" guarantees a red wire to cut), and the generator passes that guarantee from query into the solution pool.

## 6. Rigging the Deck

- **Truly random rule selection feels bad** — playtests showed repetitive or trivially easy rules; weighting selections beats raw randomness.
- **Decay weights on use** — once a query (or related-query group) is picked, its weight drops so subsequent rules are unlikely to repeat it; gives a more varied, balanced distribution.
- **Weights, not hard exclusions** — leaving rare exceptions in the pool means players who form shortcuts occasionally get punished by an unexpected rule, which is desirable.
- **Weights also bias toward intended challenge** — e.g., a memory-style puzzle weights later-stage rules to reference earlier stages, emphasizing the "remember previous input" mechanic without rigidly forcing it.
- **Degenerate cases are sometimes fine** — a "find the first matching word in a list" puzzle can randomly place the answer at position one; rather than constrain the generator (which players would learn and exploit), the puzzle uses many lists so an occasional trivial one is a moment of mastery, not a flaw. *More sophisticated PCG is not the solution to every problem.*
- **Avoiding the impossible** — naive composition can yield contradictions like "more than one blue wire AND no blue wires, cut the blue wire"; rather than validate generated rules (intractable across billions of bomb states), the generator removes related queries from the pool as soon as one is selected, sacrificing some valid combinations (e.g., "more than one blue wire AND fewer than five blue wires") in exchange for simplicity. Greater query diversity is cheaper than smarter pruning.

## 7. Putting It All Together

- **Precedence order matters** — multiple rules may match a generated bomb; only the first satisfied rule counts, so the list is ordered.
- **The "otherwise" rule** — every rule list ends with a query-less catchall, guaranteeing exactly one applicable solution and bounding the list size; in practice the catchall also lulls players into assumptions that the rare specific rules then sharply correct.
- **Sort most-specific to least-specific** — putting rules with the most queries first means players check several before finding a match, producing a desirable gradient of specificity rather than always falling through to the catchall.
- **Closing principle** — even logic itself can be procedurally generated when it serves a design goal; resist over-engineering when a simpler culling approach meets the goal, because shipping the game is more fun than perfecting the generator.
