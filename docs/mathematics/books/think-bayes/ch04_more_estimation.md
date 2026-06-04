# Ch 4: More Estimation

## Table of Contents

- [1. The Euro Problem](#1-the-euro-problem)
- [2. Summarizing the Posterior](#2-summarizing-the-posterior)
- [3. Swamping the Priors](#3-swamping-the-priors)
- [4. Optimizing the Computation](#4-optimizing-the-computation)
- [5. The Beta Distribution](#5-the-beta-distribution)
- [6. Limits of Convergence and Cromwell's Rule](#6-limits-of-convergence-and-cromwells-rule)

## 1. The Euro Problem

- **The Euro problem** — from MacKay's *Information Theory, Inference, and Learning Algorithms*: a Belgian one-euro coin spun on edge 250 times came up heads 140, tails 110; a statistician noted that for a fair coin a result this extreme has under 7% chance. The question: do the data give evidence the coin is biased?
- **Two-step plan** — (1) estimate `x`, the probability the coin lands heads; (2) evaluate whether the data support the hypothesis that the coin is biased (the second step is deferred to Chapter 5).
- **Hypotheses** — define 101 hypotheses, `Hx` = "the probability of heads is x%," for x from 0 to 100, starting with a uniform prior.
- **Likelihood function** — if `Hx` is true, a heads has probability `x/100` and a tails `1 − x/100`; the suite is updated once per spin across the dataset of 140 H's and 110 T's.

## 2. Summarizing the Posterior

- **Maximum likelihood estimate** — the value with the highest posterior probability; here it is 56, exactly the observed fraction of heads `140/250 = 56%`, confirming the observed percentage is the maximum likelihood estimator for the population.
- **Mean and median** — the posterior mean is 55.95 and the median is 56, close to the maximum likelihood value.
- **Credible interval** — the 90% credible interval is 51 to 61; because it does not include 50%, it suggests the coin is not fair.
- **Not yet the real question** — MacKay asked whether the data are *evidence* that the coin is biased rather than fair, which requires defining what it means for data to constitute evidence — the subject of the next chapter.
- **Why p(x = 50%) is meaningless** — it is tempting to read off `suite.Prob(50)` (≈ 0.021), but that number is almost meaningless because choosing 101 hypotheses was arbitrary; finer or coarser slicing would change the probability assigned to any single value.

## 3. Swamping the Priors

- **Triangular prior** — an alternative to the uniform prior that assigns higher probability to values of `x` near 50% and lower probability to extreme values, reflecting the belief that the coin is unlikely to be wildly imbalanced (x near 10% or 90%); built by ramping probability up to x = 50 then back down.
- **Swamping the priors** — with enough data, people who start with substantially different priors converge on nearly the same posterior. Updating both the uniform and triangular priors on the same dataset gives identical medians and credible intervals, with means differing by less than 0.5%.

## 4. Optimizing the Computation

- **Optimization philosophy** — Downey writes code that is demonstrably correct first, then optimizes only if it is not fast enough.
- **Normalize once with UpdateSet** — the naive `Update` normalizes after every spin (iterating the hypotheses twice each time); `UpdateSet` does all the multiplications for the whole dataset first and normalizes only once, saving time.
- **Batch the likelihood** — rewriting `Likelihood` to take the dataset as a `(heads, tails)` tuple and compute `x**heads * (1-x)**tails` replaces repeated multiplication with exponentiation, so the update takes the same time regardless of the number of spins.

| Approach | Cost characteristic |
|----------|---------------------|
| `Update` per spin | normalizes once per spin |
| `UpdateSet` | normalizes once for the whole dataset |
| Batched `(heads, tails)` likelihood | constant time, independent of number of spins |

## 5. The Beta Distribution

- **Beta distribution** — a continuous distribution defined on the interval 0 to 1 (inclusive), making it a natural choice for describing proportions and probabilities; shaped by two parameters α (alpha) and β (beta).
- **Conjugate prior** — for a binomial likelihood (as in the Euro problem), the beta distribution is a conjugate prior: if the prior for `x` is beta, the posterior is also beta. This keeps the distribution in the same family through updating.
- **Update by addition** — if the prior is beta with parameters alpha and beta, and you observe h heads and t tails, the posterior is beta with parameters `alpha+h` and `beta+t` — a Bayesian update reduced to two additions.
- **Beta(1, 1) is uniform** — the beta distribution with alpha = 1 and beta = 1 is uniform from 0 to 1, giving a perfect match for the uniform prior; many other realistic priors have a good beta approximation.
- **Solving the Euro problem with Beta** — `Beta()` defaults to uniform, `Update((140, 110))` adds the counts, and `Mean()` returns `alpha / (alpha + beta)` = 56% — the same answer obtained with Pmfs. `EvalPdf` evaluates the density and `MakePmf` produces a discrete approximation.

## 6. Limits of Convergence and Cromwell's Rule

- **Convergence relieves the objectivity worry** — when posteriors from different priors converge, much of the concern about prior subjectivity (Chapter 3) dissolves; even stark prior beliefs can be reconciled by enough data.
- **Modeling decisions can prevent convergence** — convergence is not guaranteed: if two people choose different *models*, they compute different likelihoods from the same data, and their posteriors may never converge.
- **Zero priors are permanent** — a Bayesian update multiplies each prior by a likelihood, so if p(H) = 0 then p(H|D) = 0 regardless of the data; assigning probability 0 to a hypothesis means no evidence can ever revive it.

> **Cromwell's rule** — avoid giving a prior probability of 0 to any hypothesis that is even remotely possible. Named after Oliver Cromwell ("I beseech you, in the bowels of Christ, think it possible that you may be mistaken").
