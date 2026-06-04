# Ch 6: Decision Analysis

## Table of Contents

- [1. The Price is Right Problem](#1-the-price-is-right-problem)
- [2. Probability Density Functions and KDE](#2-probability-density-functions-and-kde)
- [3. Building the Prior and the Likelihood](#3-building-the-prior-and-the-likelihood)
- [4. Updating Beliefs](#4-updating-beliefs)
- [5. Optimal Bidding](#5-optimal-bidding)
- [6. Why Posterior Distributions Matter](#6-why-posterior-distributions-matter)

## 1. The Price is Right Problem

- **Decision analysis** — choosing the action that maximizes expected return given a posterior distribution; this chapter's culminating use of Bayes, distinct from mere estimation.
- **The Price is Right Showcase** — motivating game show: each contestant guesses the price of a showcase of prizes; closest bid *without going over* wins. Downey's 2007 example: Nathaniel bid $26,000 on a showcase worth $25,347 (overbid, lost); Letia bid $21,500 on one worth $21,578 (off by $78, won), and because she was within $250 she won both showcases.
- **Three Bayesian questions** — (1) before seeing the prizes, what prior beliefs about the price?; (2) after seeing them, how to update?; (3) given the posterior, what should you bid? Question 3 is the decision-analysis step.

## 2. Probability Density Functions and KDE

- **Probability density function (PDF)** — the continuous analogue of a PMF: a function f(x) giving a *density* rather than a probability mass. Higher density means a value is more likely.
- **Density is not a probability** — a density can be 0 or any positive value, unbounded above; only integrating a density over a range yields a probability. PDFs are used mainly inside likelihood functions, so the raw density suffices.
- **Gaussian PDF** — f(x) = (1 / √(2π)) · exp(−x²/2) for mean 0, standard deviation 1; easy to evaluate and a good fit because many real-world quantities are approximately Gaussian.
- **`Pdf` class** — abstract type defining the PDF interface: `Density(x)` (must be supplied by a child class) and `MakePmf(xs)` (makes a discrete approximation by evaluating density at a sequence of values).
- **Abstract vs. concrete types** — an abstract type defines an interface without full implementation; a concrete child class extends it and supplies the missing methods. `GaussianPdf` is concrete, implementing `Density` via `scipy.stats.norm.pdf`.
- **Kernel density estimation (KDE)** — algorithm that takes a *sample* and finds an appropriately smooth PDF fitting the data; used when the population distribution isn't a simple mathematical function. `EstimatedPdf` wraps `scipy.stats.gaussian_kde`.
- **`linspace`** — "linear space"; returns `n` equally spaced values between `low` and `high` (both included), used to evaluate a PDF and build a discrete `Pmf` approximation.

## 3. Building the Prior and the Likelihood

- **Prior from historical data** — the distribution of showcase prices from 2011–12 seasons (313 prices for the first showcase), smoothed by KDE, serves as the prior belief about price before seeing the prizes. Most common value \~$28,000; first showcase has a second mode near $50,000.
- **Contestant as a price-guessing instrument** — Downey models the contestant as an instrument with known error characteristics: on seeing the prizes they form a total `guess`, ideally ignoring that the prizes form a showcase.
- **`error` vs. `diff`** — `error = price − guess` (the contestant's mental estimate error); `diff = price − bid` (observed difference between actual price and the bid). Negative `diff` means an overbid.
- **Estimating reliability from `diff`** — guesses aren't observed directly, only bids, so Downey assumes `error` is Gaussian with mean 0 and the *same variance* as the observed `diff`. The `diff` distribution shows Player 1 overbids 25% of the time, Player 2 29%, and that bids are biased toward being too low (consistent with the no-overbidding rule).
- **`Player` class** — bundles `pdf_price` (KDE-smoothed price PDF), `cdf_diff` (CDF of `diff`), and `pdf_error` (Gaussian error PDF) for one contestant.
- **Modeling caveat** — using `diff`'s variance to estimate `error`'s variance is imperfect because bids are sometimes strategic (e.g., Player 2 bids low if they think Player 1 overbid), which can inflate the observed variance.
- **`Price` suite** — extends `Suite`; its `Likelihood(data, hypo)` sets `price = hypo`, `guess = data`, `error = price − guess`, and returns `ErrorDensity(error)`. A density is a valid likelihood because the constant of proportionality cancels during normalization.

## 4. Updating Beliefs

- **`MakeBeliefs(guess)`** — builds the prior from `PmfPrice` (discrete approximation of the price PDF over 101 points spanning $0–$75,000), copies it, then `Update`s with the contestant's guess to produce the posterior.
- **Posterior is a compromise between guess and prior** — if Player 1's best guess is $20,000, the posterior mean is $25,096, between the prior's most likely value ($27,750) and the guess. The posterior is shifted left of the prior because the guess is on the low end of the prior range.
- **Resolving the apparent paradox** — combining two information sources (historical data as prior, your guess as data) is symmetric: you could equivalently treat your guess as the prior and update it with historical data, so the posterior's peak need not equal your original guess.

## 5. Optimal Bidding

- **Optimal bid** — the bid that maximizes *expected return*, computed by weighting the gain for each possible actual price by its posterior probability and summing.
- **`GainCalculator`** — holds `player` and `opponent`; `ExpectedGains` sweeps a range of bids and computes expected gain for each via `ExpectedGain`, which sums `prob × Gain(bid, price)` over the posterior.
- **`Gain` rules** — if `bid > price`, gain is 0 (overbid loses everything); otherwise gain = `price × ProbWin(diff)`, doubled to `2 × price × prob` when `diff ≤ 250` (you win both showcases). Downey assumes both showcases have equal price for simplicity since the double-win is rare.
- **`ProbWin(diff)`** — probability of winning = `opponent.ProbOverbid() + opponent.ProbWorseThan(diff)`: you win if the opponent overbids, or if their bid is off by more than your `diff`. Both come from the opponent's `cdf_diff`.
- **`OptimalBid(guess, opponent)`** — ties it together: makes beliefs from the guess, builds a `GainCalculator`, sweeps expected gains, and returns the bid with maximum gain.
- **Worked results** — with Player 1 guessing $20,000 and Player 2 guessing $40,000: Player 1's optimal bid is $21,000 (expected return ≈$16,700), an unusual case where the optimal bid *exceeds* the best guess; Player 2's optimal bid is $31,500 (≈$19,400), the typical case where the optimal bid is *below* the best guess.

## 6. Why Posterior Distributions Matter

- **Posterior vs. point estimate** — Bayesian estimation yields a full posterior distribution, whereas classical estimation gives a single point estimate or confidence interval. A point estimate is fine if estimation is the last step, but not when feeding a subsequent analysis.
- **Asymmetric, discontinuous returns** — the Showcase payoff jumps to 0 the moment you overbid, making it hard to solve analytically but straightforward to compute over the posterior.
- **When Bayesian methods earn their keep** — summarizing the posterior by its mean or maximum likelihood estimate discards its value; the payoff comes from carrying the *whole* posterior into a downstream decision analysis (this chapter) or prediction (next chapter).
