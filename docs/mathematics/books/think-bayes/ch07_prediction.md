# Ch 7: Prediction

## Table of Contents

- [1. The Boston Bruins Problem](#1-the-boston-bruins-problem)
- [2. Poisson Processes](#2-poisson-processes)
- [3. Estimating the Scoring Rate](#3-estimating-the-scoring-rate)
- [4. From Posterior to Distribution of Goals](#4-from-posterior-to-distribution-of-goals)
- [5. Probability of Winning a Game and the Series](#5-probability-of-winning-a-game-and-the-series)
- [6. Modeling Decisions and Sensitivity](#6-modeling-decisions-and-sensitivity)

## 1. The Boston Bruins Problem

- **Prediction** — using a posterior distribution to forecast future outcomes; the chapter's goal is to predict the probability the Bruins win their next game and the championship series.
- **The Bruins problem** — in the 2010–11 NHL Finals (best-of-seven), Boston lost the first two games (0–1, 2–3) then won the next two (8–1, 4–0). Question: given these four games, what is the probability Boston wins the next game and the series?
- **Strategy** — (1) choose a prior for λ from previous games; (2) estimate λ for each team from the first four games; (3) use the posterior λ to compute distributions of goals, the goal differential, and the probability of winning a game; (4) compute the probability of winning the series.

## 2. Poisson Processes

- **Process** — a stochastic (randomness-containing) model of a physical system.
- **Bernoulli process** — model of a sequence of *trials* each with two outcomes (success/failure), e.g., coin flips or shots on goal.
- **Poisson process** — the continuous version of a Bernoulli process: an event can occur at any point in time with equal probability. Models customers arriving at a store, buses at a stop, or goals in a hockey game.
- **Modeling justification** — real event rates vary over time (goals are more or less likely at different points in a game), but a Poisson process is a reasonable simplification; Heuer, Müller and Rubner (2010) reach the same conclusion analyzing a German soccer league.
- **λ (lam)** — a team's long-term average goals per game against a particular opponent; the quantity to be estimated. Downey uses the variable name `lam` because `lambda` is a reserved keyword in Python.
- **Poisson PMF** — if the average is `lam`, the probability of exactly `k` goals in a game is `lam^k · exp(−lam) / k!` (`EvalPoissonPmf`).
- **Exponential PDF** — the time between goals is exponentially distributed: `lam · exp(−lam · x)` (`EvalExponentialPdf`).

## 3. Estimating the Scoring Rate

- **Gaussian prior for λ** — built from 2010–11 average goals per game across teams: roughly Gaussian, mean 2.8, standard deviation 0.3. `MakeGaussianPmf` discretizes a Gaussian into a `Pmf` spanning `num_sigmas` standard deviations either side of the mean.
- **`Hockey` suite** — extends `Suite` with the Gaussian prior (mean 2.7, sd 0.3, spanning 4 sigmas); each hypothesis is a possible value of λ, represented by a floating-point value `x`.
- **`Likelihood`** — for hypothesis `lam` and observed goals `k`, returns `EvalPoissonPmf(lam, k)`: the probability a team averaging `lam` scores exactly `k` in a game.
- **Updating with the data** — `suite1.UpdateSet([0, 2, 8, 4])` for the Bruins and `suite2.UpdateSet([1, 3, 1, 0])` for the Canucks, using the four games' scores. Most likely posterior values: 2.9 for the Bruins, 2.6 for the Canucks.

## 4. From Posterior to Distribution of Goals

- **`MakePoissonPmf`** — if λ were known exactly, the per-game goal count is Poisson; this builds a truncated Poisson `Pmf` from 0 to `high` (Downey uses 10, since scoring >10 goals is very unlikely).
- **The complication** — λ is *not* known exactly; we have a posterior distribution of possible λ values.
- **Mixture of Poissons** — the overall goal distribution is a mixture of the per-λ Poisson distributions, weighted by each λ's posterior probability.
- **Meta-Pmf** — a Pmf whose *values are themselves Pmfs*. `MakeGoalPmf` builds a meta-Pmf (one Poisson per λ) then calls `MakeMixture` to collapse it into the distribution of goals.
- **Result** — compared with the Canucks, the Bruins are less likely to score 3 goals or fewer and more likely to score 4 or more.

## 5. Probability of Winning a Game and the Series

- **Goal differential** — `diff = goal_dist1 − goal_dist2`; subtracting two Pmfs (`Pmf.__sub__`) enumerates value pairs and computes differences. Positive diff = Bruins win, negative = Canucks win, 0 = tie.
- **Regulation outcome** — `p_win` 46%, `p_loss` 37%, `p_tie` 17% (`ProbGreater(0)`, `ProbLess(0)`, `Prob(0)`).
- **Sudden death** — on a tie, teams play overtime until the first goal, which ends the game immediately. The relevant statistic is *time until the first goal*, which (per the Poisson assumption) is exponentially distributed.
- **Overtime computation** — `MakeGoalTimePmf` builds, for each team, a mixture of exponential time-between-goals distributions over the posterior λ. `n` is set high to minimize ties, since both teams can't score simultaneously. The Bruins win overtime with probability 52%.
- **Total game win probability** — `p_win = diff.ProbGreater(0) + p_tie · p_overtime` = 55% for the Bruins.
- **Series win probability** — to win the best-of-seven from this point, the Bruins must win the next two games *or* split the next two and win the third: `p_series = p_win² + 2 · p_win · (1−p_win) · p_win` = 57%. (And in 2011, they did win.)

## 6. Modeling Decisions and Sensitivity

- **Modeling is iterative** — start simple for an approximate answer, identify likely error sources, then refine.
- **Improvement options** — (1) the prior averages goals across *all* opponents; against a specific opponent there may be more variability; (2) only the four Finals games were used as data — regular-season games against the same teams could add information, though trades and injuries argue for weighting recent games more; (3) all regular-season results could estimate each team's rate plus a per-matchup adjustment factor.
- **Higher-variance prior** — using pairs of teams that played 4–6 times in the regular season to estimate λ's variability gives mean 2.8 (unchanged) but standard deviation 0.85, much higher than the per-team estimate.
- **Sensitivity to the prior** — rerunning with the higher-variance prior raises the Bruins' series-win probability from 57% to 80%. With so little data the result is sensitive to the prior, so it's worth investing effort in getting the prior right.
