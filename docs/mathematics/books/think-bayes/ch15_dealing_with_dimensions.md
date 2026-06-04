# Ch 15: Dealing with Dimensions

## Table of Contents

- [1. The Unseen Species Problem](#1-the-unseen-species-problem)
- [2. Lions, Tigers and Bears: The Dirichlet Distribution](#2-lions-tigers-and-bears-the-dirichlet-distribution)
- [3. The Hierarchical Solution](#3-the-hierarchical-solution)
- [4. Scaling Up: Four Optimizations](#4-scaling-up-four-optimizations)
- [5. The Belly Button Data](#5-the-belly-button-data)
- [6. Predictive Distributions and Coverage](#6-predictive-distributions-and-coverage)
- [7. Closing Themes](#7-closing-themes)

## 1. The Unseen Species Problem

- **Belly button bacteria (BBB2)** — *Belly Button Biodiversity 2.0* is a citizen-science project studying the human microbiome; researchers swabbed the navels of 60 volunteers, used multiplex pyrosequencing on 16S rDNA, and identified the species/genus of each fragment. Each identified fragment is a **read**.
- **The Unseen Species problem** — four related questions from the data: (1) estimate the total number of species in the environment; (2) estimate the prevalence (population fraction) of each species; (3) predict how many *new* species more sampling will reveal; (4) how many additional reads are needed to reach a target fraction of observed species.

## 2. Lions, Tigers and Bears: The Dirichlet Distribution

- **The simplified problem** — assume exactly three species (lions, tigers, bears) and observe 3 lions, 2 tigers, 1 bear. With equal observation chance, the counts follow the **multinomial distribution**: the likelihood of that observation is proportional to `p_lion**3 * p_tiger**2 * p_bear**1`.
- **The tempting wrong approach** — modeling each species' prevalence separately with a beta distribution (treat "3 lions vs. 3 non-lions" as 3 heads / 3 tails) gives MLEs of 50%, 33%, 17%. It is wrong for two reasons: (1) the uniform 0–1 prior per species is incorrect, since knowing there are three species means the prior mean should be 1/3 with zero chance of any prevalence at 100%; (2) the per-species distributions are *not independent* — the prevalences must sum to 1, requiring a joint distribution.
- **Dirichlet distribution** — the multi-dimensional generalization of the beta distribution: where beta handles two outcomes (heads/tails), Dirichlet handles any `n` outcomes and gives a *joint* distribution over their prevalences. It is described by `n` parameters α₁…αₙ, fixing both problems above.
- **Representation and update** — the `Dirichlet` class stores its parameters as a numpy array of `n` ones. To update, simply add the observed counts to the parameters (`params[:m] += data`); `data` may be shorter than `params` when some species are unobserved.
- **Marginal beta** — the marginal distribution of any single prevalence `i` is a beta distribution `Beta(αᵢ, α₀ − αᵢ)`, where α₀ is the sum of all parameters. Prior `Beta(1, 2)` gives each species a prior mean of 1/3; after updating with `[3, 2, 1]` the posterior mean prevalences are 44%, 33%, 22%.

## 3. The Hierarchical Solution

- **Meta-Suite `Species`** — to estimate the *number* of species, build a Suite whose hypotheses are themselves `Dirichlet` objects: the top level holds hypotheses about how many species there are; each bottom level holds hypotheses about prevalences. Candidate counts `ns = range(3, 30)` (at least 3, since 3 were seen; the upper bound is checked later to be safely improbable).
- **Updating top-down** — `Species.Update` updates the parent (the distribution over `n`) first, then loops through the sub-hypotheses and updates each Dirichlet.
- **Likelihood by sampling** — `Dirichlet.Likelihood` does *not* integrate over the whole distribution; it draws one random set of prevalences `p` via `Random()` and computes the multinomial PMF for that sample (`cx · p₁^x₁ ⋯ pₙ^xₙ`). The multinomial coefficient `cx` depends only on the data, not the hypothesis, so it normalizes away and is dropped. If more species are seen than the hypothesis allows (`n < m`), likelihood is 0. `Species.Likelihood` calls this 1000 times and returns the total.
- **Random sampling from a Dirichlet** — the faster method (vs. peeling off marginal betas one at a time): draw values from `n` gamma distributions and normalize by their sum (`p / p.sum()`).
- **Result** — `DistOfN` gives a posterior over `n` peaking at 4; values 3–7 are reasonably likely, then probabilities fall off fast. The result rests on a uniform prior for `n`; background information could justify a different one.

## 4. Scaling Up: Four Optimizations

- **Why optimize** — the clean solution is \~50 lines but slow: fine for 3 species, unusable for belly-button samples with 100+ species. A series of optimizations across three successive versions (`Species2`, `Species4`, `Species5`) makes it scale.

| Version | Key change | Effect |
|---------|-----------|--------|
| `Species2` | Collapse Dirichlets into the top level; share one sample across all hypotheses; use log-likelihoods | First `m` params identical across hypotheses, so store once; fairer comparison converges faster; log-likelihoods avoid underflow |
| `Species4` | Update one species at a time (Dirichlet objects retained) | Only one prevalence affects each likelihood, so a "good" random draw is far more probable |
| `Species5` | Combine `Species4`'s one-at-a-time updates with `Species2`'s collapsed, numpy-array structure | Cuts runtime from ∝ km² back to ∝ km |

- **Collapsing the hierarchy (`Species2`)** — all bottom-level Dirichlets are updated with the same data, so their first `m` parameters match; eliminate the separate objects and merge `params` into the top suite, which now tracks `ns`, `probs`, and shared `params`.
- **Log-likelihoods** — for many species the linear likelihood underflows floating point, so compute `log cx + x₁log p₁ + ⋯ + xₙ log pₙ` instead; before exponentiating back, shift so the max log-likelihood is 0 to keep linear values from going too small. A `BinomialCoef(n, m)` correction ("n choose m") accounts for the number of ways `m` species could have been the observed ones given `n` total.
- **One species at a time (`Species4`)** — updating with the full dataset gets noisy as `m` grows, because a random prevalence vector is almost never approximately right, so most iterations contribute near-zero likelihood. Splitting the update into one-species steps ("I saw 3 lions"; then "2 tigers, no more lions"; then "1 bear, no more lions or tigers") gives the same posterior but makes a good random draw likely. Each first sighting needs a `num_unseen = n − m + 1` correction, since larger `n` means more unseen species that the new one could have been — raising the data's likelihood.
- **Regression testing** — the optimized versions are less readable and more error-prone, which is exactly why starting with the simple version pays off: it serves as a reference to validate that each faster version produces approximately equal results and converges.

## 5. The Belly Button Data

- **Subject B1242** — a real sample of 400 reads yielded 61 species; a few dominant species (top counts 92, 53, 47) plus many **singletons** (species with a single read). The abundance of singletons signals there are probably several unseen species.
- **Modeling caveats** — as with the animals, each bacterium is assumed equally likely to yield a read, though collection steps (swabbing, amplification) introduce bias; and "species" is used loosely — to be precise, the right unit is an **operational taxonomic unit (OTU)**, since bacterial species are ill-defined and some reads identify only a genus.
- **`Subject` class and results** — a `Subject` holds a code and a sorted list of `(count, species name)` pairs, and its `Process` method builds and updates a `Species5` suite. For B1242, `DistN` gives a posterior over `n` with most likely value 72 (90% credible interval 66–79; \~zero probability of exactly 61 with no unseen species). `DistOfPrevalence` mixes the per-`n` marginal betas: the most prevalent species is 23% of reads but its best estimate is 20% prevalence (90% CI 17%–23%), shaded down because unseen species exist.

## 6. Predictive Distributions and Coverage

- **Simulation kernel** — to answer the predictive questions, simulate the future: (1) draw `n` from its posterior; (2) draw prevalences for all species (seen and unseen) from the Dirichlet; (3) generate a random sequence of future observations; (4) compute new species `num_new` as a function of additional reads `k`; (5) repeat and accumulate the joint distribution of `num_new` and `k`.
- **Rarefaction curve** — `RunSimulation` returns a list of `(reads, num_new)` pairs tracking new species as reads accumulate. Plotting 100 such curves (jittered to avoid overlap) for B1242 suggests \~2–6 new species after 400 more reads.
- **Joint posterior** — `MakeJointPredictive` builds a `Joint` (a Pmf over tuples) from the curves; `Joint.Conditional` then gives the distribution of `num_new` for any fixed `k`. After 100 reads the median new-species count is 2 (90% CI 0–5); after 800 reads, 3–12 new species.
- **Coverage** — the fourth question (reads needed to reach a target observed fraction) reuses `RunSimulation` to track `frac_seen = len(seen)/n` instead of new-species counts; the complementary CDF of coverage gives the probability of *exceeding* a threshold. For B1242: \~40% chance of 90% coverage with 200 reads, rising to \~90% chance of 90% coverage with 1000 reads.

## 7. Closing Themes

- **A novel contribution** — Downey notes the Unseen Species problem is active research and believes this chapter's algorithm is novel — in under 200 pages the book reaches the research frontier.
- **The book's three ideas** — Downey states the work presents three related themes: **Bayesian thinking** (use probability distributions to represent uncertain beliefs, update them with data, and use the results to predict and decide); **a computational approach** (computation makes Bayesian analysis easier to understand than math, using reusable building blocks); and **iterative modeling** (start with simple models and add complexity gradually, using each to validate the others).
