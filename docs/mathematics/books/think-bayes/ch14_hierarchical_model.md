# Ch 14: A Hierarchical Model

## Table of Contents

- [1. The Geiger Counter Problem](#1-the-geiger-counter-problem)
- [2. Building the Model Bottom-Up](#2-building-the-model-bottom-up)
- [3. Optimization and Extracting Results](#3-optimization-and-extracting-results)
- [4. Causation and Hierarchy](#4-causation-and-hierarchy)

## 1. The Geiger Counter Problem

- **The Geiger counter problem** — a radioactive source emits particles toward a counter at average rate `r` per second, but the counter registers only a fraction `f` of them; given `f` = 10% and 15 particles counted in one second, find the posterior distributions of `n` (particles that actually hit) and `r` (average emission rate). Downey credits Tom Campbell-Ricketts, who got it from E.T. Jaynes's *Probability Theory: The Logic of Science*.
- **Chain of causation** — the system runs cause → effect in three stages: the source emits at rate `r`; in a given second it emits `n` particles; of those, `k` get counted. Modeling starts by tracing this chain from parameters to data.
- **Poisson for n** — radioactive decay is a Poisson process (decay probability is constant over time), so given `r`, the distribution of `n` is Poisson with parameter `r`.
- **Binomial for k** — if each particle is detected independently with probability `f`, then given `n`, the distribution of the count `k` is binomial with parameters `n` and `f`.
- **Forward vs. inverse problem** — the *forward problem* is finding the distribution of the data given the parameters; the *inverse problem* goes the other way (parameters given data). If you can solve the forward problem, Bayesian methods solve the inverse problem.

## 2. Building the Model Bottom-Up

- **Start simple** — first solve the easy case where `r` is known and only `n` must be estimated; this isolates the detection step before adding the harder layer.
- **The `Detector` Suite** — a Suite that models the counter for a *known* `r`: its prior over `n` is `MakePoissonPmf(r, ...)`, and its likelihood of observing `k` particles given hypothesis `n` is the binomial PMF `EvalBinomialPmf(k, n, p=f)`. Running it for `r` ∈ {100, 250, 400} gives a posterior over `n` for each.
- **Make it hierarchical** — relax the assumption that `r` is known by adding a second Suite, `Emitter`, whose hypotheses are themselves `Detector` objects (one per candidate `r`). A Suite whose values are other Suites is a **meta-Suite**.
- **Hierarchical model** — a model with multiple nested levels of Suites; here the top level estimates `r` and each bottom-level `Detector` estimates `n` for its `r`.
- **`SuiteLikelihood`** — to score one `Detector` against the data, loop over its values of `n` and sum `prob × Likelihood(k, n)` — the total probability of the observed `k` under that whole Detector. The `Emitter`'s likelihood for a hypothesis is just that Detector's `SuiteLikelihood`.
- **Updating both levels** — `Emitter.Update` first updates itself (the distribution over `r`), then loops through its Detectors and updates each one too; inference must propagate through every level.

## 3. Optimization and Extracting Results

- **The optimization** — `SuiteLikelihood`'s total is exactly the normalizing constant that `Update` already computes and returns (first seen in "Making a fair comparison," ch. 11). So instead of updating the Emitter and *then* the Detectors, do both at once: `Emitter.Likelihood` becomes simply `return hypo.Update(data)`. Fewer lines, and faster because the normalizing constant isn't computed twice.
- **`DistOfR`** — extract the posterior over `r` by pairing each Detector's `r` with its probability in the Emitter (`MakePmfFromItems`).
- **`DistOfN` via mixture** — the posterior over `n` is the *mixture* of all the Detectors, weighted by their probabilities; since the Emitter is exactly a meta-Pmf mapping each distribution to its probability, `MakeMixture(self)` produces it directly.
- **The result** — the most likely `n` is 150: given `f` and `n` the expected count is `k = f·n`, so given `f` and `k` the expected `n` is `k/f = 15/0.1 = 150`; `r` centers on 150 too. The posteriors of `r` and `n` are similar, but we are slightly *less* certain about `n` — the long-range rate `r` is more constrained than the count in any single second.

## 4. Causation and Hierarchy

- **Structure mirrors causation** — the hierarchy reflects the physical system, with causes at the top and effects at the bottom: `r` causally affects `n`, which causally affects `k`.
- **Information flows two ways** — building the model goes top-down (a range of `r`; for each `r` a prior over `n` that depends on `r`); updating goes bottom-up (posterior of `n` for each `r`, then posterior of `r`). Summary: **causal information flows down the hierarchy, inference flows up.**
- **Mosquito-trap exercise** — a parallel Jaynes-inspired problem: a trap catches 30 then 20 mosquitoes in successive weeks; estimate the percent change in the yard's population. Modeling suggestion: a large number `N` is bred weekly, a fraction `f1` wander into the yard, a fraction `f2` of those are trapped, and an added hierarchy level models week-to-week change in `N`.
