# Ch 11: Hypothesis Testing

## Table of Contents

- [1. The Euro Problem Revisited](#1-the-euro-problem-revisited)
- [2. The Bayes Factor and the Cheating Trap](#2-the-bayes-factor-and-the-cheating-trap)
- [3. Defining a Fair Comparison](#3-defining-a-fair-comparison)
- [4. SuiteLikelihood as an Update](#4-suitelikelihood-as-an-update)
- [5. Interpreting Bayes Factors](#5-interpreting-bayes-factors)

## 1. The Euro Problem Revisited

- **The Euro problem** — from MacKay's *Information Theory, Inference, and Learning Algorithms*: a Belgian one-euro coin spun on edge 250 times came up heads 140 times. Statistician Barry Blight told *The Guardian* that for a fair coin "the chance of getting a result as extreme as that would be less than 7%." MacKay's real question: do the data give evidence the coin is *biased rather than fair*?
- **Estimation answered the wrong question** — earlier chapters estimated x, the probability of heads, but never addressed whether the data favor "biased" over "fair." This chapter does hypothesis testing instead.
- **Two hypotheses** — F (the coin is fair) and B (the coin is biased). The `Likelihood` function `x**heads * (1-x)**tails` computes the probability of the data for a given x.

## 2. The Bayes Factor and the Cheating Trap

- **Evidence in favor of a hypothesis** — from Chapter 4: data favor a hypothesis if they are more likely under it than under the alternative — equivalently, if the **Bayes factor** (likelihood ratio) exceeds 1.
- **p(D|F) alone is uninformative** — under the fair hypothesis the likelihood is 5.5 × 10⁻⁷⁶; this tiny number only reflects that *any* particular dataset is improbable. A ratio needs a second likelihood, p(D|B), but it is not obvious how to compute the likelihood of "biased" because "biased" is not yet defined.
- **B_cheat** — defining "biased" as x = 140/250 *after looking at the data* gives likelihood 34 × 10⁻⁷⁶ and a Bayes factor of 6.1, seemingly favoring B. But using the data to formulate the hypothesis is bogus: by that definition almost any dataset becomes evidence for B (unless heads are exactly 50%).

## 3. Defining a Fair Comparison

- **Specify B without looking at the data** — a legitimate comparison requires defining "biased" in advance, from background knowledge such as the coin's more prominent heads side.
- **B_two** — the hypothesis that x is either 0.6 or 0.4 (unsure which), treated as two equally weighted sub-hypotheses; the likelihood is the average `0.5*like40 + 0.5*like60`. Bayes factor 1.3 — weak evidence for B.
- **B_uniform** — for no clue about x, a `Suite` of sub-hypotheses spanning 0 to 100 (with x = 50 removed and renormalized, though it barely matters). Bayes factor 0.47 — weak evidence *against* B, relative to F.
- **B_triangle** — a triangle-shaped prior (from Chapter 4) giving higher probability to x near 50%. Bayes factor 0.84 — again weak evidence against B.

| Hypothesis | Likelihood (× 10⁻⁷⁶) | Bayes factor vs. F |
|------------|----------------------|--------------------|
| F | 5.5 | – |
| B_cheat | 34 | 6.1 |
| B_two | 7.4 | 1.3 |
| B_uniform | 2.6 | 0.47 |
| B_triangle | 4.6 | 0.84 |

- **The verdict depends on the definition of B** — different reasonable definitions push the evidence for or against bias, but in every legitimate case the evidence is weak. Specifying B requires background information about coins, so people may reasonably disagree on the right definition; this presentation follows MacKay's and reaches the same conclusion.

## 4. SuiteLikelihood as an Update

- **`SuiteLikelihood`** — computes a composite hypothesis's likelihood as the prior-weighted average of its sub-hypotheses' likelihoods (`Σ prob * Likelihood`).
- **It is the same computation as a normalization** — `Normalize` returns the Suite's total before scaling, which is exactly that prior-weighted average of likelihoods; since `Update` passes this total along, calling `b_uniform.Update(data)` returns the suite's likelihood directly, making a separate `SuiteLikelihood` unnecessary. The same shortcut computes the likelihood of `b_triangle`.

## 5. Interpreting Bayes Factors

- **Jeffreys's scale** — Harold Jeffreys, an early proponent of Bayesian statistics, proposed a scale for the strength of evidence implied by a Bayes factor:

| Bayes factor | Strength |
|--------------|----------|
| 1–3 | Barely worth mentioning |
| 3–10 | Substantial |
| 10–30 | Strong |
| 30–100 | Very strong |
| > 100 | Decisive |

- **Why "weak"** — the Bayes factor of 0.47 for B_uniform is 2.1 in favor of F, which Jeffreys would call "barely worth mentioning."
- **Think in odds instead of adjectives** — to sidestep arguing over wording, combine the Bayes factor with prior odds: prior odds 1:1 with a Bayes factor of 2 give posterior odds 2:1, shifting belief from 50% to 66% — small relative to modeling errors. A Bayes factor of 100 would give posterior odds 100:1 (over 99%), which is unambiguously strong.
