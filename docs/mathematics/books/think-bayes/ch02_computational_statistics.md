# Ch 2: Computational Statistics

## Table of Contents

- [1. Distributions and the Pmf Class](#1-distributions-and-the-pmf-class)
- [2. Bayesian Updates with a Pmf](#2-bayesian-updates-with-a-pmf)
- [3. The Suite Framework](#3-the-suite-framework)

## 1. Distributions and the Pmf Class

- **Distribution** — a set of values and their corresponding probabilities; e.g., a six-sided die has values 1–6 with probability 1/6 each, or each English word paired with how often it appears.
- **Pmf class** — Downey's Python class (in `thinkbayes.py`, the module accompanying the book) that represents a distribution as a dictionary mapping each value to its probability; named after the *probability mass function*, the mathematical representation of a distribution.
- **Core methods** — `Set(x, p)` assigns a probability to a value; `Incr(x, n)` increases a value's "probability" by n (adding the value if absent), useful for counting; `Prob(x)` returns the probability of a value.
- **Normalize** — counts are not true probabilities until they sum to 1; `Normalize()` divides through by the total so frequencies become probabilities.
- **Flexible types** — values can be any hashable Python type; probabilities are usually floats.

## 2. Bayesian Updates with a Pmf

- **Hypotheses as Pmf values** — for Bayes's theorem it is natural to use a Pmf mapping each hypothesis to its probability; the cookie problem uses strings `'Bowl 1'`/`'Bowl 2'` with prior 0.5 each.
- **Prior distribution** — the Pmf containing the prior probability of each hypothesis.
- **Update = multiply then renormalize** — multiply each prior by the corresponding likelihood (`Mult('Bowl 1', 0.75)`, `Mult('Bowl 2', 0.5)`); the result is unnormalized, but because the hypotheses are mutually exclusive and collectively exhaustive, `Normalize()` restores a proper distribution.
- **Posterior distribution** — the resulting Pmf with the posterior probability of each hypothesis; for the cookie problem, p(Bowl 1|vanilla) = 0.6, matching the hand calculation of Chapter 1.

## 3. The Suite Framework

- **Generalizing the update** — a `Cookie` class wraps the pattern: `__init__` gives each hypothesis equal prior probability; `Update(data)` loops through hypotheses, multiplies each by `Likelihood(data, hypo)`, and normalizes.
- **Benefit of the abstraction** — the same `Update` handles multiple data points (e.g., drawing several cookies with replacement: `for data in dataset: pmf.Update(data)`) and transfers unchanged across problems.
- **Problem-specific part is Likelihood** — solving the Monty Hall problem computationally reuses the identical `Update`; only `Likelihood` changes (return 0 if hypo == door opened, 0.5 for door A, 1 otherwise), reproducing posteriors 1/3, 0, 2/3.
- **Suite class** — encapsulates the shared framework: a Pmf that provides `__init__`, `Update`, and `Print`. To use it, write a subclass that inherits from `Suite` and provides `Likelihood`.
- **Suite is an abstract type** — it defines the interface (Update and Likelihood) but implements only `Update`; a *concrete type* like `Monty` extends it and implements the missing `Likelihood`. Downey notes this is an example of the **template method pattern**.
- **M&M problem in the framework** — encode the 1994/1996 color mixes as dictionaries, hypotheses A/B as bag→mix mappings; data is a (bag, color) tuple and `Likelihood` looks up the color's frequency in the hypothesized mix. Two updates (`('bag1', 'yellow')`, `('bag2', 'green')`) give p(A) ≈ 0.741 ≈ 20/27, as in Chapter 1.
- **Pattern for the rest of the book** — most later examples define a new class that extends `Suite`, inherits `Update`, and provides `Likelihood`; occasionally `Update` is overridden for performance.
- **Exercise: sampling without replacement** — if drawn cookies are eaten, each draw's likelihood depends on previous draws; the suggested fix is instance variables tracking the hypothetical state of the bowls.
