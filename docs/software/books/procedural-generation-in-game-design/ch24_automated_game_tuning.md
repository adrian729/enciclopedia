# Ch 24: Automated Game Tuning

## Table of Contents

- [1. Why Automate Tuning](#1-why-automate-tuning)
- [2. The Five-Step Pipeline](#2-the-five-step-pipeline)
- [3. Step 1: Set Parameters](#3-step-1-set-parameters)
- [4. Step 2: Generate the Game Level](#4-step-2-generate-the-game-level)
- [5. Step 3: Simulate the Game](#5-step-3-simulate-the-game)
- [6. Step 4: Analyze the Data](#6-step-4-analyze-the-data)
- [7. Step 5: Visualize the Data and Make Adjustments](#7-step-5-visualize-the-data-and-make-adjustments)
- [8. Practical Notes](#8-practical-notes)

## 1. Why Automate Tuning

- **Game variants from parameter sets** — every unique combination of adjustable parameters (character size, gravity, jump height, piece probabilities, etc.) defines a new **game variant**; getting Mario's jump to feel right is far more about parameters than physics accuracy.
- **Manual tuning doesn't scale** — designers iterate by intuition, playtest, observation, analytics, and revision; with hundreds of independent "knobs" exhaustive search is impossible.
- **Designer drift** — designers and playtesters who become expert at a game lose perspective on novice difficulty, so tuning for themselves makes the game obtuse for new players. The system therefore exposes an **adjustable skill level** so both low- and high-skilled players can be modeled.
- **Parameter exploration as creativity tool** — algorithms don't get frustrated with bad results and can keep searching, surfacing surprising variants designers would never reach because every nearby change first breaks the game.
- **Goal of the chapter's method** — usable by ordinary game programmers without an advanced CS degree or heavy maths; requires no human playtesters during the inner loop.

## 2. The Five-Step Pipeline

The chapter's method is a loop of five named steps that explore the space of game variants and estimate each variant's difficulty.

| # | Step | What it accomplishes |
|---|---|---|
| 1 | **Set Parameters** | Choose which knobs to tune and pick a value for each from a valid range, defining one game variant. |
| 2 | **Generate the Game Level** | Place world elements using those parameters, randomizing per-run details so artifacts of any single layout average out. |
| 3 | **Simulate the Game** | Run a human-like AI player (not a champion) through the level, repeating to gather many score samples. |
| 4 | **Analyze the Data** | Aggregate the per-run scores into a histogram and infer a difficulty estimate (mean, median, or survival analysis). |
| 5 | **Visualize the Data and Make Adjustments** | Plot how difficulty depends on parameters, pick the next variant to try (manually, or via an optimizer, or by searching for variants as different as possible from existing ones), and loop back to Step 1. |

- **Running example** — Flappy Bird. Chosen because it is commercially proven, simple to reimplement, and has few parameters. The same pipeline has also been applied to games that speed up over time, such as Canabalt.

## 3. Step 1: Set Parameters

- **Pick the knobs and ranges** — for Flappy Bird the variable parameters are pipe separation, pipe width, pipe gap, pipe gap location range, jump velocity, bird velocity, gravity, world height, and bird size. **pipe gap location range** controls how much pipe heights vary from one pipe to the next; larger values mean more vertical travel between consecutive gaps and so harder play.
- **Constant during a run** — Flappy Bird and its variants hold each parameter constant across a play session because the game itself does not change as the player progresses.
- **Sensible ranges per parameter** — sweeping each within a reasonable interval defines the full space of variants the system will explore.

## 4. Step 2: Generate the Game Level

- **Bird and pipes are placed at the starting positions** dictated by the parameters; pipe gap locations are randomly distributed within the configured range.
- **Re-generate every run, even with parameters fixed** — reusing one random layout lets per-layout artifacts (e.g., gap heights that happen to align across a stretch) bias results; regenerating averages those artifacts out.

## 5. Step 3: Simulate the Game

- **Player modeling, not perfect play** — the goal is to predict how humans perform at novice, intermediate, and advanced skill, not to win the game. Champion AIs misrepresent human-perceived difficulty.
- **Start from a perfect AI** — for Flappy Bird, a simple, fast AI looks ahead to the next pipe, picks a target height a bit above the lower pipe's top, and flaps the moment the bird drops below that line. It should clear all solvable levels and only fail the impossible (e.g., a gap too small for the bird).
- **Add complexity only if needed** — A* or Monte Carlo tree search are options for richer games; the author's recommendation is to start simple.
- **Two human motor traits modeled** — **precision** and **actions per second**. Reaction time to unexpected events was also explored but mattered less and is omitted here.
- **Precision as a normal distribution** — when a player intends to press at exact time *t*, they actually press at *t* shifted by Gaussian noise; the bell curve's standard deviation is the player's imprecision. The user study measured σ between 35.9 ms and 61.1 ms, used as the range for game-space exploration. Precision is treated as independent of bird speed for simplicity, though humans show a **speed–accuracy trade-off** (less reaction time → less accurate response).
- **Actions-per-second cap** — the user study measured ~7.7 actions per second (~1 every 130 ms); the AI is held to the same rate, so even after noise it cannot tap unrealistically fast. The model holds APS constant; a richer model could simulate fatigue.
- **Implementation sketch** — at each frame, run a no-draw copy of the game forward to find the next time *t* the bird will cross the target line (under 1 ms per call), then perturb *t* with a Gaussian (≈30 ms standard deviation). If the perturbed *t* sits within 130 ms of the previous flap, push it out to that limit so the AI cannot exceed the human APS cap.
- **Crucially, AIs do not learn** — human testers improve between sessions, confounding before/after comparisons; reused fixed-skill AIs give reliable difficulty deltas when parameters change.
- **Score per run** — number of pipes passed before crashing; capped at a goal score of 20 to stop runs of trivially-solvable variants. Real Flappy Bird is unbounded but humans tire and err; the AI would not without the cap.
- **Sample size** — about 10,000 simulations was plenty for Flappy Bird and ran in roughly a second once graphics were stripped out. More complex games take longer; speed it up by disabling rendering and lowering the goal score, and tune both empirically.

## 6. Step 4: Analyze the Data

- **Histogram of final scores** — store every score, then either count occurrences directly or **bin** ranges of scores when there are many. Each bar's height is the probability of that score (or bin) under the variant.
- **Reading histogram shapes** — the chapter's four sample shapes:
  - **Hard from the start** — most likely score is 0, descending probabilities for higher scores.
  - **Direct comparison** — overlaying a second histogram in gray; lower probability of low scores and higher probability of high scores marks the gray variant as easier.
  - **Easy at start, gets harder** — low probability of low scores, peak at medium scores, low probability of high scores.
  - **Hard variant overlay** — gray distribution with more low-score mass than the black baseline indicates a harder variant.
- **Difficulty statistics** — the research used **survival analysis**, which tracks how score frequencies fall off as a player continues. Simpler alternatives (median or mean of the histogram) are easier to code and reasonable in practice; a falling median means the game got harder, a rising median means it got easier.
- **Three variant categories** to recognize from the histogram:
  - **Impossible games** — unwinnable for any skill (e.g., jump velocity overpowering gravity, or a pipe gap smaller than the bird). Very low mean score, no high-score cases. Filtered out by first verifying that a perfect, no-noise AI hits the goal score with high frequency.
  - **Playable games** — winnable by some players short of perfection; higher mean → easier. The histogram itself describes the distribution of expected scores.
  - **Trivial games** — every reasonably engaged player reaches the goal (e.g., an enormous pipe gap). Histogram has few low scores, a high mean, many high scores, and a spike at the goal.

## 7. Step 5: Visualize the Data and Make Adjustments

- **One-parameter sweep** — fix all but one parameter and plot difficulty against it for several AI skills. For Flappy Bird, plotting pipe gap vs. difficulty across precision settings shows narrower gaps are harder for everyone and that less-precise players find every variant harder, as expected.
- **Two-parameter dot plots** — visualize difficulty across pairs of parameters using dot radius and colour saturation. Gravity vs. jump velocity reveals dependence: extreme ratios crash the bird into floor or ceiling (impossible games); when balanced, increasing both together tightens reaction time and raises difficulty, while lowering both eases play.
- **Targeted search** — once parameters and difficulty are linked, the system can hunt for an easier or harder variant; with an optimizer it can hit an exact target difficulty, automatically discarding unplayable candidates and returning only human-playable variants.
- **Exploratory computational creativity** — instead of optimizing for difficulty, search for variants that are as different as possible from those already explored. Designers then browse the unique survivors for inspiration.
- **"Frisbee Bird"** — a surprise variant produced by the optimizer when allowed to vary every parameter (speed, player width and height, jump velocity, gravity, pipe distance, pipe width, pipe randomness). Result: a wide, flat bird that races horizontally but moves slowly vertically, demanding short bursts of rapid taps followed by long floats. Same rules as Flappy Bird, very different feel.

## 8. Practical Notes

- **No heavy tooling required** — the technique runs without complex libraries or deep statistics; analysis can sit in Excel or a small Python script.
- **Not a replacement for human testers** — AIs miss problems humans surface, and there is no guarantee AI-perceived and human-perceived difficulty agree. The win is a fast, reliable signal of whether parameter tweaks make the game easier or harder, which speeds up tuning iterations.
