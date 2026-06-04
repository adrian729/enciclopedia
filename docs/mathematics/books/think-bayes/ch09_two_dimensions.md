# Ch 9: Two Dimensions

## Table of Contents

- [1. The Paintball Problem](#1-the-paintball-problem)
- [2. The Likelihood Function via Trigonometry](#2-the-likelihood-function-via-trigonometry)
- [3. Joint, Marginal, and Conditional Distributions](#3-joint-marginal-and-conditional-distributions)
- [4. Credible Intervals in Multiple Dimensions](#4-credible-intervals-in-multiple-dimensions)
- [5. Scaling to More Dimensions](#5-scaling-to-more-dimensions)

## 1. The Paintball Problem

- **Paintball problem** — locate a hidden opponent in a 30 ft × 50 ft indoor arena from the paint spatters they left on a wall, observed at 15, 16, 18, and 21 feet from the lower-left corner. A modified version of the classic Lighthouse problem of Bayesian analysis (notation follows D.S. Sivia's *Data Analysis: a Bayesian Tutorial*).
- **Parameters alpha and beta** — the shooter's unknown location is a pair of coordinates (α, β): alpha is the position along the wall direction, beta the perpendicular distance from the wall. The spatter location on the wall is x; the firing angle is θ (theta). This is what makes the problem *two-dimensional*: each hypothesis is a coordinate pair, not a single value.
- **The Paintball suite** — a `Suite` whose hypotheses are all (alpha, beta) pairs, built from `alphas = range(0, 31)` and `betas = range(1, 51)`. The class also inherits from `Joint`, a mixin supplying methods for joint distributions.
- **Uniform prior** — all locations in the room are taken as equally likely; given a map of the room one could choose a more detailed prior, but the analysis starts simple.

## 2. The Likelihood Function via Trigonometry

- **Rotating-turret model** — the opponent is modeled as equally likely to shoot in any direction; he is therefore most likely to hit the wall directly opposite at location alpha, and progressively less likely to hit points farther from alpha.
- **Geometry of a shot** — a pellet fired at angle θ hits the wall at x where `x − α = β tan θ`; solving gives `θ = tan⁻¹((x − α) / β)`, so each wall location maps to a firing angle.
- **Strafing speed** — Downey's term for `dx/dθ = β / cos²θ`, the speed at which the target location sweeps along the wall as the firing angle increases. The probability of hitting a given point is *inversely related* to strafing speed: points the beam sweeps past quickly are less likely to be hit.
- **`MakeLocationPmf`** — for fixed (alpha, beta), builds a Pmf over wall locations with each probability set to `1 / StrafingSpeed`, then normalized. For alpha = 10 the most likely spatter is always at x = 10; as beta grows the Pmf spreads wider (a distant shooter sprays a broader area).
- **`Likelihood`** — given hypothesis (alpha, beta) and observed spatter x, returns the probability of x from that location's `MakeLocationPmf`. Updating with `suite.UpdateSet([15, 16, 18, 21])` yields the posterior over all (alpha, beta) pairs.

## 3. Joint, Marginal, and Conditional Distributions

- **Joint distribution** — a distribution in which each value is a tuple of variables, representing the variables *together*; it captures both the individual variables and the relationships (dependence) among them. Here it gives the probability of each (alpha, beta) pair.
- **Marginal distribution** — the distribution of a single parameter, treating the others as unknown. `Joint.Marginal(i)` sums probabilities over the chosen index: i=0 gives alpha, i=1 gives beta. The median alpha is 18 (near the center of mass of the spatters); for beta the nearest values are most likely but beyond 10 feet the distribution is nearly uniform — the data don't strongly distinguish far locations.
- **Conditional distribution** — the distribution of one parameter conditioned on a fixed value of another. `Joint.Conditional(i, j, val)` keeps only items where variable j equals val, then normalizes. Conditioning alpha on beta = 10 gives a narrow distribution; larger beta gives wider ones.
- **Detecting dependence** — if variables were independent, all conditional distributions of alpha would be identical regardless of beta; because they differ, alpha and beta are dependent.
- **Information asymmetry** — from the joint distribution you can derive all marginals and conditionals, and from enough conditionals you can approximately reconstruct the joint; but from the marginals alone you *cannot* recover the joint, because the marginals discard the dependence between variables.

## 4. Credible Intervals in Multiple Dimensions

- **Many intervals share a credibility level** — for any distribution, many different sets of values sum to (say) 50% probability, so a credible interval is not unique.
- **Central credible interval** — the usual one-dimensional choice: the central 50% interval runs from the 25th to the 75th percentile.
- **Maximum likelihood credible interval** — for multiple dimensions, a common choice that collects the *most probable* values until their total probability reaches the target percentage. `Joint.MaxLikeInterval` sorts values by descending probability and accumulates until the threshold is crossed; the resulting set need not be contiguous.
- **Visualizing nested intervals** — `MakeCrediblePlot` colors each (alpha, beta) by how many of the 25%, 50%, 75% intervals contain it. The 25% region hugs the bottom wall; higher percentages grow larger and skew toward the right side of the room.

## 5. Scaling to More Dimensions

- **Extending the framework** — the same Bayesian machinery from earlier chapters handles a two-dimensional parameter space unchanged; the only difference is that each hypothesis is a tuple of parameters.
- **`Joint` as a mixin** — a parent class supplying `Marginal`, `Conditional`, and `MaxLikeInterval` for any joint distribution, in object-oriented terms a mixin.
- **Exponential cost in dimensions** — with n values per parameter, operations cost roughly n² for two parameters and nᵈ for d parameters, quickly becoming impractical. A million-hypothesis budget allows two dimensions at 1000 values each, three at 100 each, or six at 10 each.
- **When more is needed** — for more dimensions or finer resolution, optimizations exist; Downey presents an example in Chapter 15.
