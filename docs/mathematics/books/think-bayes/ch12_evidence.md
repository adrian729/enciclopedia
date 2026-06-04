# Ch 12: Evidence

## Table of Contents

- [1. The Problem and Bayesian Hypothesis Testing](#1-the-problem-and-bayesian-hypothesis-testing)
- [2. The Simple Model: p_correct](#2-the-simple-model-p_correct)
- [3. Comparing Alice and Bob](#3-comparing-alice-and-bob)
- [4. A Better Model: Efficacy and Difficulty](#4-a-better-model-efficacy-and-difficulty)
- [5. Prediction and Nuisance Parameters](#5-prediction-and-nuisance-parameters)

## 1. The Problem and Bayesian Hypothesis Testing

- **Interpreting SAT scores** — motivating problem: as Dean of Admission, you compare Alice (Math SAT 780) and Bob (740) out of a possible 800, and ask the narrower question "How strong is the evidence that Alice is better prepared than Bob?" rather than just deciding who to admit.
- **Bayesian hypothesis testing** — answer the question by defining two competing hypotheses and computing how strongly the data favor one over the other:
  - A: p_correct is higher for Alice than for Bob.
  - B: p_correct is higher for Bob than for Alice.
- **Likelihood ratio (Bayes factor)** — the ratio of the likelihood of the data under A to its likelihood under B; it measures the strength of the evidence independent of the prior. A ratio of 3.8 means the scores are 3.8 times more likely if A is true than if B is true.

## 2. The Simple Model: p_correct

- **p_correct** — the probability that a given test-taker answers any question correctly; defined per test-taker under the deliberate simplification that all SAT questions are equally difficult, which makes the likelihood of a score easy to compute.
- **Start simple, then improve** — Downey starts with a model he knows is wrong (equal difficulty), then later builds a more realistic one and checks whether the simplification mattered.
- **The scale** — each test-taker gets a raw score (number correct minus a 1/4-point penalty per wrong answer; 54 questions on the 2009 math SAT), which the College Board maps to a scaled score in the range 200–800. An `Interpolator` object does the forward (raw→scaled) and reverse (scaled→raw) lookups.
- **The prior** — the College Board publishes the distribution of scaled scores for all test-takers; converting each to a raw score and dividing by 54 yields an estimate of p_correct, giving the prior distribution. It is approximately Gaussian but compressed at the extremes, because the SAT is designed to discriminate best within two standard deviations of the mean.
- **The Sat suite** — a `Suite` subclass that starts from the prior distribution of p_correct and updates on the observed scaled score; one `Sat` object is built per test-taker.
- **Binomial likelihood** — interpreting the raw score as the number of correct answers k out of n questions (ignoring the wrong-answer penalty), the likelihood of a score given a hypothetical p_correct is the binomial probability of k correct out of n, computed via `EvalBinomialPmf`.

## 3. Comparing Alice and Bob

- **Overlapping posteriors** — the posterior distributions of p_correct for Alice and Bob overlap, so it is possible (though it seems unlikely) that Bob's p_correct is actually higher.
- **TopLevel suite** — a `Suite` that computes the posterior probabilities of A and B at once; it overrides `Update` rather than supplying `Likelihood`, because both hypotheses are easier to evaluate together using `PmfProbGreater` and `PmfProbLess`.
- **Splitting the tie** — `c_like`, the probability that the two are "equal," is an artifact of discretizing p_correct (it would be zero if p_correct were continuous), so it is treated as round-off error and split evenly between A and B.
- **Result** — likelihood of A is 0.79, of B is 0.21, giving a likelihood ratio of 3.8. Starting from equal priors, the posterior probability of A is 79%, leaving a 21% chance that Bob is actually better prepared.

## 4. A Better Model: Efficacy and Difficulty

- **Why a better model** — the equal-difficulty simplification might overstate the gap between Alice and Bob; the question is whether the modeling error is large enough to matter. (Spoiler: it is small.)
- **Efficacy and difficulty** — each test-taker has an **efficacy** (ability to answer questions) and each question has a **difficulty**, both on the same scale; the chance of a correct answer depends only on their difference.
- **ProbCorrect curve** — `1 / (1 + exp(-a·(efficacy − difficulty)))`, a simplified version of the curve from item response theory: probability is 50% when efficacy equals difficulty, approaches 100% as efficacy rises, and approaches 0% as difficulty rises.
- **Distribution of raw scores** — for a person of given efficacy, `PmfCorrect` sums two-valued (`BinaryPmf`) distributions across all questions to get their raw-score distribution; across a population of varying efficacy, `MakeRawScoreDist` combines these into a mixture via `MakeMixture`.
- **Efficacy assumed Gaussian** — efficacy is taken to be Gaussian with mean 0 and standard deviation 1.5; this is largely arbitrary, since the units of efficacy can be chosen freely and difficulty calibrated to match.
- **Calibration** — the inverse problem: given the actual distribution of raw scores, infer the distribution of difficulty. Assuming difficulty is uniform with a center and width, `center=-0.05` and `width=1.8` (range roughly −1.85 to 1.75) produce raw scores matching the real data.
- **Sat2 and re-comparison** — `Sat2` uses a Gaussian efficacy prior and a `Likelihood` based on the raw-score distribution. Re-running `TopLevel` gives a likelihood ratio of 3.4 (vs. 3.8 from the simple model) — evidence still favors A, slightly weaker — yielding a 77% posterior for A, so the simplification's error is indeed small.

## 5. Prediction and Nuisance Parameters

- **Predictive distribution** — because efficacy is not directly observable, the model is validated by predicting an observable: "If Alice and Bob take the SAT again, what is the chance Alice does better?" Use the posterior efficacy to generate a predictive raw-score distribution per person, then compare.
- **Confidence vs. outcome** — the probability Alice scores higher on a retake is 63% (Bob 37%). The posterior odds that Alice's *efficacy* is higher are 3:1, but the odds she *scores* higher next time are only 2:1 — more confidence about the underlying parameter than about a single future outcome.
- **Nuisance parameters** — values like p_correct or efficacy that we do not care about in themselves, but must estimate to evaluate the likelihoods of the hypotheses we do care about.
- **The joint-distribution view** — `MakeJoint` builds the joint distribution of two independent Pmfs; plotting the joint posterior of Alice's and Bob's p_correct, the diagonal marks where they are equal. Computing the likelihoods of A and B amounts to summing the probability mass on each side of that diagonal and splitting the mass on the line.
- **The general pattern** — estimating nuisance parameters in order to evaluate the likelihood of competing hypotheses is a common Bayesian approach to problems of this kind.
