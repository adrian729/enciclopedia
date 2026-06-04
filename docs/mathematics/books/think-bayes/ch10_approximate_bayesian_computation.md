# Ch 10: Approximate Bayesian Computation

## Table of Contents

- [1. The Variability Hypothesis](#1-the-variability-hypothesis)
- [2. Estimating a Gaussian's Mean and Standard Deviation](#2-estimating-a-gaussians-mean-and-standard-deviation)
- [3. Underflow and the Log Transform](#3-underflow-and-the-log-transform)
- [4. Optimization and ABC](#4-optimization-and-abc)
- [5. Robust Estimation and Conclusions](#5-robust-estimation-and-conclusions)

## 1. The Variability Hypothesis

- **Variability Hypothesis** — the early-nineteenth-century claim (Johann Meckel) that males have a greater range of ability than females, so most geniuses and most mentally retarded people are men; Meckel read this supposed greater variability as male superiority. The evidence for it is weak.
- **BRFSS height data** — the CDC's Behavioral Risk Factor Surveillance System provides self-reported heights of 154,407 men and 254,722 women, used here to test the hypothesis quantitatively.
- **Coefficient of variation (CV)** — standard deviation divided by mean, a *dimensionless* measure of variability relative to scale, more meaningful than raw standard deviation when comparing variability between groups. Men average 178 cm (SD 7.7, CV 0.0433); women average 163 cm (SD 7.3, CV 0.0444) — very close, hinting at weak evidence against the hypothesis.
- **Three-step plan** — Downey builds the analysis in stages, each motivated by the failure of the last: (1) a simple implementation that breaks above \~1000 values, (2) a log-transform version that scales to the full dataset but is slow, (3) Approximate Bayesian Computation (ABC) for speed.

## 2. Estimating a Gaussian's Mean and Standard Deviation

- **`Height` suite** — like the Paintball suite of Chapter 9, a `Joint` suite mapping each (mu, sigma) pair to a probability, where mu is the Gaussian mean and sigma the standard deviation; the prior is uniform over all pairs.
- **Likelihood via the Gaussian PDF** — `Likelihood` returns `EvalGaussianPdf(x, mu, sigma)`. Strictly a PDF gives a probability *density*, not a probability, but for Bayesian updating only something *proportional* to the probability is needed, and a density serves fine.
- **Choosing prior ranges with classical estimators** — the hardest part is picking ranges for mus and sigmas: too narrow omits probable values, too wide wastes computation. `FindPriorRanges` uses classical estimates — sample mean m for μ and sample standard deviation s for σ — to locate the parameters, then their standard errors (`s/√n` for the mean, `s/√(2(n−1))` for the standard deviation) to set the spread, covering a few standard errors on each side via `MakeRange`.
- **Using the data twice is acceptable here** — using the data to set the prior range and again for the update would normally be bogus, but here the range merely avoids computing negligible probabilities; with the range wide enough (e.g., `num_stderrs=4`) the result is identical to a truly uniform prior. In effect the prior is uniform but trimmed for efficiency.
- **Posterior distribution of CV** — `CoefVariation` enumerates (mu, sigma) pairs and accumulates a Pmf of `sigma/mu`; `PmfProbGreater` then computes the probability that men's CV exceeds women's.

## 3. Underflow and the Log Transform

- **Underflow** — multiplying \~1000 small probability densities together produces a number too small for floating-point representation, which rounds to zero. With all probabilities zero, `Pmf.Normalize` raises `ValueError: total probability is zero` and the object is no longer a distribution. The first 100 BRFSS values work; the first 1000 fail.
- **Log transform as the fix** — instead of multiplying small likelihoods, add their logarithms. `Pmf.Log` divides every probability by the maximum (`MaxLike`) so the top probability becomes log 0 and the rest negative, removing any zero-probability values; while transformed, `Update`/`UpdateSet`/`Normalize` are forbidden and raise an exception.
- **`LogUpdate` / `LogUpdateSet`** — mirror `Update` but call `LogLikelihood` and use `Incr` instead of `Mult`, since adding a log-likelihood equals multiplying a likelihood. `LogLikelihood` uses `scipy.stats.norm.logpdf`.
- **`Exp` inverts the transform** — log-likelihoods end as large negative numbers; `Exp` shifts them up by the maximum m before exponentiating so the result peaks at 1, inverting the transform with minimal precision loss. The full cycle is `Log` → `LogUpdateSet` → `Exp` → `Normalize`. This processes the whole dataset without underflow but takes about an hour.

## 4. Optimization and ABC

- **Closed-form log-likelihood** — taking the log of the Gaussian PDF and dropping the constant term gives `−log σ − ½((x−μ)/σ)²`; summing over the data and pulling out terms independent of i yields `−n log σ − (1/2σ²)·Σ(xᵢ−μ)²`. `LogUpdateSetFast` evaluates this per hypothesis directly.
- **Memoized summation** — the summation `Σ(xᵢ−μ)²` depends only on mu, not sigma, so `Summation` is factored out and memoized in a dictionary cache; the dataset is converted to a tuple because lists are not hashable cache keys. This speeds the computation by about 100×, processing all 409,129 records in under a minute.
- **Approximate Bayesian Computation (ABC)** — motivated by the observations that the likelihood of any exact dataset is (1) very small, (2) expensive to compute, and (3) not really what we want. We care about the likelihood of *any dataset like* the one observed, judged by summary statistics — just as the Euro problem cares only about heads/tails counts and the Locomotive problem only about the count and maximum serial number.
- **Sampling distributions of the statistics** — for n draws from a Gaussian(μ, σ): the sample mean m is Gaussian(μ, σ/√n) and the sample standard deviation s is Gaussian(σ, σ/√(2n−1)). `LogUpdateSetABC` computes the log-likelihood of the observed m and s under each hypothesis using these distributions, processing the whole dataset in about a second and agreeing with the exact result to about 5 digits.

## 5. Robust Estimation and Conclusions

- **Outliers** — the data contain near-certain errors (three adults reported at 61 cm, four women at 229 cm) that have a disproportionate effect on estimated variability; the estimation must be made robust to them.
- **Robust summary statistics** — because ABC works from summary statistics, it can be made robust simply by choosing robust statistics: the median (for μ) and an inter-percentile range (IPR) such as the inter-quartile range (the 25th-to-75th-percentile spread) instead of the mean and standard deviation.
- **`MedianIPR` and `MedianS`** — `MedianIPR` extracts the median and a chosen-fraction IPR from the CDF; `MedianS` converts an IPR to a sigma estimate using the Gaussian rule that, e.g., the 16th-to-84th percentile range (68% IPR) equals 2σ, so dividing by 2 (or generally by `2·num_sigmas`) estimates σ. Any statistics that capture location and spread may be used; choosing the 49th and 51st percentiles, for instance, would barely constrain σ and leave its posterior looking like the prior.
- **Result depends on interpretation** — with `num_sigmas=1` (weighting people near the mean) the posterior CVs (0.0410 men, 0.0429 women) show no overlap, so women are more variable with near certainty; but with `num_sigmas=2` (weighting the extremes, where there are more short men) the opposite conclusion holds with equal confidence.
- **The hypothesis may be too vague** — because the verdict flips with the interpretation of "variability," evaluating the Variability Hypothesis would require a more precise statement of it.
- **Two readings of ABC** — (1) an approximation that is faster than the exact value; (2) since Bayesian analysis always rests on modeling decisions and there is no single "exact" solution, ABC is an *alternative model of the likelihood* — the likelihood of any outcome *like* the data, where the meaning of "like" (which summary statistics make two datasets alike) is itself a modeling choice.
