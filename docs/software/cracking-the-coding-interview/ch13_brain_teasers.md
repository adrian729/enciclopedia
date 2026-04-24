# Ch 13: Brain Teasers

## Table of Contents

- [1. Context on brain teasers](#1-context-on-brain-teasers)
- [2. Start talking](#2-start-talking)
- [3. Develop rules and patterns](#3-develop-rules-and-patterns)
- [4. Worst case shifting](#4-worst-case-shifting)
- [5. Fall back on algorithm approaches](#5-fall-back-on-algorithm-approaches)

## 1. Context on brain teasers

- **Hotly debated** — many companies have policies banning them, though candidates still encounter them because there is no agreed definition of what a brain teaser is.
- **If asked, it's likely to be a fair one** — it probably won't rely on a trick of wording, and it can almost always be logically deduced.
- **Many have foundations in mathematics or computer science** — they are not arbitrary puzzles.

## 2. Start talking

- **Don't panic** — like algorithm questions, the interviewer wants to see how you *tackle* the problem, not whether you know the answer immediately.
- **Talk through your approach** — silence signals being stuck; narration signals problem-solving.

## 3. Develop rules and patterns

- **Write down "rules" or patterns** you discover while solving — really write them, don't just hold them in your head; it helps you remember and reuse them.
- **Example — the two-rope problem** — two ropes each burn in exactly one hour but at uneven densities (so half the rope length-wise does *not* necessarily take half an hour). Time exactly 15 minutes.

| Rule | Statement |
|------|-----------|
| **Rule 1** | Given a rope that burns in `x` minutes and another in `y` minutes, we can time `x + y` minutes |
| **Rule 2** | Given a rope that burns in `x` minutes, lighting both ends lets us time `x / 2` minutes |
| **Rule 3** | If rope 1 takes `x` minutes and rope 2 takes `y` minutes, we can turn rope 2 into a rope that takes `y - x` minutes or `y - x/2` minutes |

**Solution:** light rope 1 at both ends and rope 2 at one end simultaneously. When the two flames on rope 1 meet (30 min passed), rope 2 has 30 minutes of burn-time left. Light rope 2's other end; it burns out in **exactly 15 minutes**.

## 4. Worst case shifting

- **Many brain teasers are worst-case minimization problems** — worded as minimizing an action or doing something at most some number of times.
- **Technique** — try to **balance the worst case**: when an early decision skews the worst case, change the decision to balance it out.
- **Example — "nine balls"** — nine balls, one heavier; a balance scale tells only which side is heavier; find the heavy ball in just two weighings.
  - **Naive split into 4-4-1** — if the 8 balance, the odd ball is heavy (1 weighing). If they don't, finding the heavy one among 4 needs more work — worst case: three weighings. Imbalanced.
  - **Worst-case balanced split into 3-3-3** — one weighing identifies the heavy set of 3. Second weighing picks the heavy ball from that set (weigh 2, pick heavier; or pick the third if they balance). **Worst case: 2 weighings.**
- **General rule** — given N balls where N is divisible by 3, one weighing points to a set of N/3 containing the heavy ball.

## 5. Fall back on algorithm approaches

- **If stuck, apply one of the five algorithm approaches** from the technical-questions chapter — brain teasers are often nothing more than algorithm questions with the technical aspects removed.
- **Especially useful**:
  - **Exemplify**
  - **Simplify and Generalize**
  - **Pattern Matching**
  - **Base Case and Build**
