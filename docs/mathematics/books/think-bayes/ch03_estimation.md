# Ch 3: Estimation

## Table of Contents

- [1. The Estimation Workflow](#1-the-estimation-workflow)
- [2. The Dice Problem](#2-the-dice-problem)
- [3. The Locomotive Problem](#3-the-locomotive-problem)
- [4. Choosing a Prior](#4-choosing-a-prior)
- [5. Summarizing the Posterior](#5-summarizing-the-posterior)
- [6. Real-World Application and the Prior Debate](#6-real-world-application-and-the-prior-debate)

## 1. The Estimation Workflow

- **Estimation** — using Bayesian updating to infer an unknown numeric quantity (e.g., the number of sides on a die, the size of a fleet) rather than choosing among labeled hypotheses; the posterior is a distribution over candidate values.
- **Three-step strategy** — Downey's recipe for setting up an estimation problem: (1) choose a representation for the hypotheses, (2) choose a representation for the data, (3) write the likelihood function. Earlier chapters used strings; estimation problems naturally use numbers.

## 2. The Dice Problem

- **The dice problem** — a box holds one each of a 4-, 6-, 8-, 12-, and 20-sided die (the Dungeons & Dragons set); you draw one at random, roll it, and get a 6. Wanted: the probability that you rolled each die.
- **Hypothesis and data representation** — the integers 4, 6, 8, 12, 20 represent the hypotheses (`Dice([4, 6, 8, 12, 20])`); integers 1–20 represent the data.
- **Likelihood function** — if `hypo < data` the roll exceeds the die's sides, which is impossible, so likelihood is 0; otherwise the chance of rolling any face on a `hypo`-sided die is `1/hypo`, independent of the actual value rolled.
- **Single-update result** — after rolling a 6, the 4-sided die has probability 0; the 6-sided die is most likely (\~39%), but the 20-sided die still carries almost 12%.
- **Accumulating evidence** — updating on the further rolls 6, 8, 7, 7, 5, 4 eliminates the 6-sided die (a 7 and 8 are impossible on it) and pushes the 8-sided die to \~94%, leaving the 20-sided die under 1%. More data sharpens the posterior.

## 3. The Locomotive Problem

- **The locomotive problem** — from Mosteller's *Fifty Challenging Problems in Probability*: a railroad numbers its locomotives 1..N; you see number 60; estimate N. Seeing 60 tells you N ≥ 60, but not how much more.
- **Two-step framing** — split into (1) what you knew about N before the data (the prior) and (2) for a given N, the likelihood of seeing number 60.
- **Uniform prior** — with no strong basis, assume N is equally likely to be any value from 1 to 1000.
- **Identical likelihood to the dice problem** — assuming one train-operating company and equal chance of seeing any locomotive, the chance of seeing number 60 in a fleet of N is `1/N` (0 if N < 60) — the same form as the dice likelihood.
- **Posterior after seeing 60** — all values below 60 are eliminated; the most likely single value is 60 itself, so to maximize the chance of being exactly right, guess 60.
- **Posterior mean** — an alternative point estimate is the mean of the posterior (333 here); using the posterior mean minimizes mean squared error over repeated play.

## 4. Choosing a Prior

- **Sensitivity to the prior** — with only one observation, the posterior depends heavily on the arbitrary upper bound of the uniform prior:

| Upper bound | Posterior mean (after seeing 60) |
|-------------|----------------------------------|
| 500 | 207 |
| 1000 | 333 |
| 2000 | 552 |

- **Two ways to reduce sensitivity** — (1) get more data, or (2) get more background information.
- **More data converges** — after also seeing trains 30 and 90, the posterior means for the three upper bounds become 152, 164, and 171: the differences shrink because posteriors from different priors converge as data accumulate.
- **Power law prior** — company sizes follow a power law (Robert Axtell, *Science*): many small companies, few large ones. The number of companies of a given size is inversely proportional to size, `PMF(x) ∝ x^(−α)` with α near 1, built by setting each hypothesis's probability to `hypo**(-alpha)` and normalizing.
- **Why the power law helps** — it encodes realistic background information, all but eliminates values of N above 700, and makes the posterior far less sensitive to the arbitrary upper bound:

| Upper bound | Posterior mean (power law prior, trains 30/60/90) |
|-------------|---------------------------------------------------|
| 500 | 131 |
| 1000 | 133 |
| 2000 | 134 |

  With an arbitrarily large upper bound the mean converges on 134.

## 5. Summarizing the Posterior

- **Point estimates** — a posterior is often summarized by a single value: the mean, the median, or the value of maximum likelihood.
- **Credible interval** — two values such that there is a chosen probability (e.g., 90%) that the unknown quantity falls between them; computed as the 5th and 95th percentiles of the posterior. For the locomotive problem (power law prior, three trains) the 90% credible interval is 91 to 243 — wide, correctly signaling continued uncertainty.
- **Percentile** — `Percentile(pmf, percentage)` walks the values accumulating probability and returns the value where the cumulative total first reaches the target fraction.
- **Cumulative distribution function (Cdf)** — represents a distribution by cumulative probability; equivalent to a Pmf (same information, convertible either way) but better for computing many percentiles.
- **Cdf efficiency** — converting Pmf → Cdf costs time proportional to the number of values; because the Cdf stores values and probabilities in sorted lists, looking up a percentile (or a probability) then takes "log time," making Cdfs efficient when many lookups are needed.

## 6. Real-World Application and the Prior Debate

- **The German tank problem** — in WWII the Economic Warfare Division estimated German tank production from captured serial numbers. Numbers were allocated by manufacturer and type in sequential blocks of 100, so estimation within each block reduced to the locomotive problem.
- **Validated accuracy** — these statistical estimates were substantially lower than other intelligence estimates and, postwar records confirmed, substantially more accurate; the same method gave actionable intelligence on tires, trucks, and rockets. It illustrates the short path from a toy problem to a real research-frontier application.
- **Informative prior** — a prior chosen to best represent background information about the problem; criticized as subjective because people may use or interpret background information differently.
- **Uninformative prior** — a prior intended to be as unrestricted as possible to "let the data speak for themselves"; appealing because it seems more objective, sometimes uniquely identifiable by a desirable property like minimal prior information.
- **Downey's position** — he favors informative priors: all Bayesian analysis rests on modeling decisions (the prior is just one, perhaps not the most subjective), so an uninformative prior does not make the whole analysis objective.
- **When the prior matters** — with a lot of data, informative and uninformative priors give nearly the same result; with little data (the locomotive problem) relevant background information makes a big difference; and for life-and-death decisions (the German tank problem) you should use all available information rather than feigning objectivity.
