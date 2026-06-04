# Ch 8: Observer Bias

## Table of Contents

- [1. The Red Line Problem](#1-the-red-line-problem)
- [2. Observer Bias and the Biased Gap Distribution](#2-observer-bias-and-the-biased-gap-distribution)
- [3. From Gaps to Wait Times](#3-from-gaps-to-wait-times)
- [4. Predicting Wait Times from Passenger Counts](#4-predicting-wait-times-from-passenger-counts)
- [5. Estimating the Arrival Rate](#5-estimating-the-arrival-rate)
- [6. Incorporating Uncertainty](#6-incorporating-uncertainty)
- [7. Decision Analysis: When to Take a Taxi](#7-decision-analysis-when-to-take-a-taxi)

## 1. The Red Line Problem

- **The Red Line problem** — Downey commutes on Boston's Red Line subway, where rush-hour trains run every 7–8 minutes on average. From the number of passengers already on the platform he wants to predict his wait time, and decide when to give up and take a taxi.
- **Modeling decisions** — *passenger* arrivals are treated as a Poisson process at unknown constant rate λ (passengers per minute); *train* arrivals are **not** Poisson — though scheduled every 7–8 minutes from Alewife, by Kendall Square the gap between trains varies between 3 and 12 minutes.
- **Data collection** — a script pulled real-time MBTA data for south-bound trains at Kendall Square, 4pm–6pm for 5 weekdays (\~15 arrivals/day); consecutive arrival times give the distribution of gaps, labeled **z**.

## 2. Observer Bias and the Biased Gap Distribution

- **Observer bias** — values from the actual distribution are *oversampled in proportion to their value*; a passenger arriving at a random time is more likely to land in a large gap than a small one, so the gaps they experience are biased toward large.
- **Worked intuition** — if gaps are 5 or 10 minutes with equal probability, the true average is 7.5 minutes, but a passenger is twice as likely to arrive during a 10-minute gap; 2/3 of passengers land in the 10-minute gap, so the *passenger-perceived* average is 8.33 minutes.
- **Other examples** — students think classes are bigger than they are (more students are in big classes); airline passengers think planes are fuller than they are (more passengers are on full flights).
- **`BiasPmf`** — converts the actual gap distribution to the passenger-perceived one by multiplying each value's probability by the value itself (`new_pmf.Mult(x, x)`) and renormalizing.
- **z vs. zb** — `z` is the actual gap distribution; `zb` ("z biased") is the gap distribution as seen by passengers.

## 3. From Gaps to Wait Times

- **x, y, and zb** — *wait time* `y` is the time from a passenger's arrival to the next train; *elapsed time* `x` is the time from the previous train to the passenger's arrival; the definitions are chosen so that `zb = x + y`.
- **Wait time as a mixture of uniforms** — within a gap of size `zb`, arrival is equally likely at any moment, so `y` is uniform from 0 to `zb`; the overall distribution of `y` is a mixture of uniform distributions weighted by each gap's probability (`PmfOfWaitTime`, via `MakeMixture`).
- **x distributed like y** — since `x = zb − y` and `y` is uniform on `[0, zb]`, `x` is also uniform on `[0, zb]`; thus the distribution of elapsed time equals the distribution of wait time.
- **`WaitTimeCalculator`** — encapsulates `pmf_z` (unbiased gaps), `pmf_zb` (biased gaps), `pmf_y` (wait time), and `pmf_x` (elapsed time = wait time), computed prior to any passenger count.
- **Observed means** — mean of `z` = 7.8 min; mean of `zb` = 8.8 min (\~13% higher); mean of `y` = 4.4 min (half of `zb`). The MBTA's reported 9-minute headway is close to mean `zb`, deliberately conservative to account for variability.
- **Cdfs over Pmfs** — Downey switches to CDFs for presentation: easier to interpret once familiar and better for plotting several distributions on the same axes.

## 4. Predicting Wait Times from Passenger Counts

- **Motivating question** — seeing 10 (later 15) passengers on the platform, how long should you expect to wait?
- **Three-step plan (known λ)** — (1) use `z` to get the prior of `zp`, the gap as seen by a passenger; (2) use the passenger count to estimate the distribution of elapsed time `x`; (3) use `y = zp − x` to get the wait-time distribution.
- **`Elapsed` suite** — a `Suite` over hypothetical elapsed times `x`; `Likelihood` takes `hypo = x` and `data = (lam, k)` and returns `EvalPoissonPmf(lam · x, k)` — the Poisson probability of seeing `k` passengers arrive in time `x` at rate `lam`.
- **`ElapsedTimeEstimator`** — builds the prior of `x` from the `WaitTimeCalculator`, updates it with `(lam, num_passengers)` to get the posterior of `x`, then computes the predictive distribution of `y`.
- **`PredictWaitTime`** — computes `pmf_y = pmf_zb − pmf_x`; `RemoveNegatives` strips impossible negative wait times (you can't wait longer than the gap you arrived in) and renormalizes.
- **Result** — after seeing 15 passengers, the time since the last train is probably 5–10 minutes, and the next train is expected in under 5 minutes with about 80% confidence.

## 5. Estimating the Arrival Rate

- **Relaxing the known-λ assumption** — a newcomer to Boston doesn't know the passenger arrival rate; λ can be estimated from a few days of observations.
- **Data to record** — each day note `k1` (passengers waiting on arrival), `y` (your wait time), and `k2` (passengers arriving while you wait). Over one example week, 18 minutes of waiting and 36 arrivals give a point estimate of \~2 passengers per minute.
- **`ArrivalRate` suite** — hypotheses are values of λ; `Likelihood` takes `data = (y, k)` and returns `EvalPoissonPmf(lam · y, k)` — nearly identical to `Elapsed.Likelihood`, differing only in that the hypothesis here is `lam` rather than `x`. Both compute the probability of `k` arrivals in a period given `lam`.
- **`ArrivalRateEstimator`** — builds hypothetical λ values, sets the prior, and loops over the `(k1, y, k2)` tuples updating with `(y, k2)` to yield the posterior of λ. The posterior mean/median sit near 2 passengers/minute, with spread capturing uncertainty from the small sample.

## 6. Incorporating Uncertainty

- **General procedure** — to account for uncertainty in an input parameter: (1) implement the analysis for a deterministic value; (2) compute the distribution of the parameter; (3) run the analysis for each value, generating a set of predictive distributions; (4) take a mixture of them weighted by the parameter's distribution.
- **`WaitMixtureEstimator`** — performs steps (3) and (4): for each λ in the posterior it runs an `ElapsedTimeEstimator`, stores the resulting `pmf_y` in a meta-Pmf weighted by the λ probability, then `MakeMixture` collapses them.
- **When it matters** — including parameter variability is important when the system response is *non-linear* (small input changes cause big output changes). Here λ's posterior variability is small and the response is approximately linear, so a single point estimate of λ gives nearly the same result.

## 7. Decision Analysis: When to Take a Taxi

- **The decision** — Downey can wait 15 minutes and still make his commuter-rail connection at South Station; he wants the probability that `y` exceeds 15 minutes as a function of `num_passengers`.
- **Hard-to-estimate long delays** — the analysis is sensitive to rare long delays, but one week of data (longest observed: 15 minutes) can't estimate their frequency.
- **Coarse estimate of major delays** — over a year of commuting Downey saw three long delays (signaling problem, power outage, "police activity"), so \~3 major delays per year.
- **Delays are biased observations** — long delays affect more passengers, so they are observations of `zb`, not `z`. Across \~220 trips home, he samples 220 gaps, biases them, adds delays of 30/40/50 minutes, fits a Pdf via KDE, then **unbiases** (`UnbiasPmf`) to recover `z` for the `WaitTimeCalculator`.
- **`ProbLongWait`** — given a passenger count, builds an `ElapsedTimeEstimator`, takes the CDF of `y`, and returns the probability wait exceeds `minutes`.
- **Decision rule** — with fewer than 20 passengers the system looks normal (small delay probability); at 30 passengers, \~15 minutes have likely elapsed, signaling trouble. Accepting a 10% chance of missing the connection, stay if fewer than 30 passengers wait, take a taxi otherwise. The threshold could be refined by quantifying the costs of a missed connection versus a taxi and minimizing expected cost.
