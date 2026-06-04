# Ch 13: Simulation

## Table of Contents

- [1. The Kidney Tumor Problem](#1-the-kidney-tumor-problem)
- [2. The Simple Model](#2-the-simple-model)
- [3. The General Simulation Model](#3-the-general-simulation-model)
- [4. From Joint to Conditional Distributions](#4-from-joint-to-conditional-distributions)
- [5. Serial Correlation and Modeling Errors](#5-serial-correlation-and-modeling-errors)
- [6. Where Bayes Hides](#6-where-bayes-hides)

## 1. The Kidney Tumor Problem

- **The Kidney Tumor problem** — a patient with Stage IV kidney cancer asks, given his retirement date and detection date, whether it is "more likely than not" that his tumor (15.5 cm × 15 cm at detection, Grade II) formed during his military service; the answer affects veterans' benefits.
- **Why this is tractable** — renal tumors grow slowly and are often left untreated, so doctors can measure growth rates by comparing scans of the same patient over time; several papers report these rates.
- **Reciprocal doubling time (RDT)** — the growth-rate metric, in doublings per year: RDT = 1 doubles tumor volume each year, RDT = 2 quadruples it, RDT = −1 halves it.
- **The data** — growth rates for 53 patients from Zhang et al. (raw data refused on privacy grounds, so Downey extracted points by measuring a printed graph with a ruler). The positive tail fits an exponential well, so he models RDT as a mixture of two exponentials.

## 2. The Simple Model

- **Constant-doubling-time assumption** — the simple model assumes a tumor grows at a constant doubling time and is three-dimensional, so when the maximum linear dimension doubles, the volume multiplies by eight.
- **Linear vs. volumetric doubling time** — because volume scales as the cube of a linear dimension, the doubling time for a linear measure is three times longer than the volumetric doubling time.
- **Back-calculation from the median rate** — the time from discharge to diagnosis was 3291 days (\~9 years); at Zhang et al.'s median volume doubling time of 811 days, the tumor would have been about 6 cm at discharge. So if it formed *after* discharge it must have grown far faster than the median rate — hence "more likely than not" it predated discharge.
- **Implied growth rate check** — assuming an initial size of 0.1 cm, reaching 15.5 cm takes 7.3 linear doublings, implying RDT ≈ 2.4; only 20% of tumors in the data grew that fast, reinforcing the same conclusion.
- **Start simple** — a simple model is a good starting point: it may suffice on its own, and if not it serves to validate a more complex model. These calculations were enough to answer the original question, but a friend (an oncologist) suggested a more general model would interest researchers.

## 3. The General Simulation Model

- **The goal of the general model** — given a tumor's size at diagnosis, find the distribution of its possible *ages*, i.e., the probability it formed before any given date.
- **The strategy** — run simulations to get the distribution of *size conditioned on age*, then use a Bayesian approach to invert that into *age conditioned on size*.
- **Simulation steps** — start with a small tumor and repeat until it exceeds the maximum relevant size:
  1. Choose a growth rate from the distribution of RDT.
  2. Compute the tumor's size at the end of an interval.
  3. Record the size at each interval.
  4. Repeat.
- **Simulation parameters** — initial size 0.3 cm (carcinomas smaller than this are less likely to be invasive or well-supplied with blood); interval 245 days (\~8 months, the median time between measurements in the data); maximum size 20 cm (a modest extrapolation beyond the observed 1.0–12.0 cm range).
- **Independence simplification** — the growth rate is chosen independently each interval, so it does not depend on the tumor's age, size, or previous growth rate.
- **Spread of outcomes** — simulated tumors reaching 10 cm vary widely in age: the fastest gets there in 8 years, the slowest takes more than 35.
- **Implementation kernel** — `MakeSequence` drives the simulation, taking an iterator of random RDT values and a time step; `Volume` converts a linear diameter to volume by treating the tumor as a sphere; `ExtendSequence` computes the volume at the end of each interval (`final = initial · 2^(rdt·interval)`).

## 4. From Joint to Conditional Distributions

- **Caching the joint distribution** — a `Cache` object holds a `Joint` Pmf recording the frequency of each age–size pair across all simulated intervals, approximating the joint distribution of age and size.
- **Discretizing size into buckets** — `Diameter` converts volume back to a diameter in cm, and `CmToBucket` maps that to a discrete bucket on a log scale (factor 10: 1 cm → bucket 0, 10 cm → bucket 23).
- **Conditional distributions** — slicing the joint distribution gives conditionals: a vertical slice yields the distribution of sizes for a given age; a horizontal slice yields the distribution of ages for a given size. `ConditionalCdf` returns the CDF of age conditioned on a size bucket.
- **Percentiles vs. size** — summarizing the conditional CDFs by percentiles (95, 75, 50, 25, 5) as a function of size shows how the plausible age range grows with tumor size; a least-squares fit smooths the numerical errors introduced by discretizing size and time.

## 5. Serial Correlation and Modeling Errors

- **Reviewing the assumptions** — Downey lists the main potential sources of error: spherical geometry, the RDT distribution fit (only 53 patients), ignoring tumor subtype/grade, growth rate independent of size, and growth rate independent across intervals. The spherical and serial-correlation assumptions seem most problematic.
- **Serial correlation** — in reality, tumors that grew quickly in the past are probably more likely to keep growing quickly, so growth rates across intervals are likely correlated rather than independent.
- **CorrelatedGenerator** — to simulate correlated growth: (1) generate correlated Gaussian values (each next value drawn with mean `x·rho` and variance `1 − rho²`); (2) map each through the Gaussian CDF to a cumulative probability; (3) map that probability through the desired Cdf to a growth rate (`Transform`). Information loss in the transform can lower the realized correlation (e.g., target rho 0.4 yields actual \~0.37).
- **Effect of correlation** — correlation makes fast tumors faster and slow tumors slower, widening the age range; for a 6 cm tumor the 95th-percentile age shifts by more than 6 years between ρ = 0 and ρ = 0.4.
- **ProbOlder** — answers the original question: convert size to a bucket, take the conditional CDF of age, and return the probability that age exceeds a threshold. For a 15.5 cm tumor older than 8 years: 0.999 with no correlation, 0.995 at ρ = 0.4, 0.978 at ρ = 0.8.
- **Spherical-geometry robustness** — a 15.5 × 15 cm tumor is probably flat, not spherical; even crediting it the smaller volume of a 6 cm sphere and correlation 0.8, the probability it is older than 8 years is still 95%. So even accounting for modeling errors, it is unlikely the tumor formed less than 8 years before diagnosis.

## 6. Where Bayes Hides

- **Bayes as inverting conditional probabilities** — one way to view Bayes's theorem is as an algorithm to compute p(A|B) from p(B|A), p(A), and p(B); it is only useful when p(B|A) is easier to compute than p(A|B).
- **Why simulation fit** — here p(size|age) is easy to estimate by simulation while p(age|size) is hard, which looks like a perfect case for Bayes's theorem.
- **Why Bayes was skipped** — for computational efficiency: estimating p(size|age) for one size already requires running many simulations that incidentally produce the *entire* joint distribution p(size, age). Once the joint distribution is in hand, p(age|size) is just a slice (as in `ConditionalCdf`) — no explicit Bayes step needed. "We side-stepped Bayes, but he was with us in spirit."
