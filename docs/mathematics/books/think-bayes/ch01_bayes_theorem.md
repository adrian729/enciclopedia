# Ch 1: Bayes's Theorem

## Table of Contents

- [1. Probability Foundations](#1-probability-foundations)
- [2. Deriving Bayes's Theorem](#2-deriving-bayess-theorem)
- [3. The Diachronic Interpretation](#3-the-diachronic-interpretation)
- [4. The Table Method and Worked Problems](#4-the-table-method-and-worked-problems)

## 1. Probability Foundations

- **Probability** — a number between 0 and 1 (inclusive) representing a degree of belief in a fact or prediction; 1 = certainty true, 0 = certainty false, 0.5 = as likely to happen as not (e.g., a coin landing face up).
- **Conditional probability** p(A|B) — the probability of A given that B is true; a probability based on background information. Downey's example: his personal heart-attack risk (\~0.2%) differs from the U.S. average (\~0.3%) because it conditions on his age, sex, cholesterol, blood pressure, and non-smoking.
- **Conjoint probability** p(A and B) — the probability that both A and B are true.
- **Independence caveat** — the familiar formula p(A and B) = p(A) p(B) only works when A and B are independent, i.e., p(B|A) = p(B) (two coin tosses qualify; rain today and rain tomorrow do not).
- **General conjunction rule** — p(A and B) = p(A) p(B|A) for *any* A and B; this is the building block for the derivation.

## 2. Deriving Bayes's Theorem

- **The cookie problem** — motivating example: Bowl 1 has 30 vanilla + 10 chocolate cookies, Bowl 2 has 20 of each; you draw a vanilla cookie from a random bowl. Wanted: p(Bowl 1|vanilla). The reverse, p(vanilla|Bowl 1) = 3/4, is easy — Bayes's theorem bridges the gap.
- **Derivation in three steps** — conjunction is commutative, p(A and B) = p(B and A); expand both sides as p(A) p(B|A) = p(B) p(A|B); divide by p(B):

  p(A|B) = p(A) p(B|A) / p(B)

- **Cookie solution** — p(B1|V) = (1/2 × 3/4) / (5/8) = 3/5; the vanilla cookie is evidence in favor of Bowl 1 because vanilla cookies are more likely to come from Bowl 1.
- **Divide-and-conquer strategy** — Bayes's theorem is useful when p(A|B) is hard to compute or measure directly but the right-side terms p(B|A), p(A), and p(B) are easier.

## 3. The Diachronic Interpretation

- **Diachronic interpretation** — "diachronic" means happening over time: Bayes's theorem as a way to *update* the probability of a hypothesis H as new data D arrive: p(H|D) = p(H) p(D|H) / p(D).
- **Named terms** — each part of the update has a standard name:

| Term | Name | Meaning |
|------|------|---------|
| p(H) | **prior** | probability of the hypothesis before seeing the data |
| p(H\|D) | **posterior** | probability of the hypothesis after seeing the data |
| p(D\|H) | **likelihood** | probability of the data under the hypothesis |
| p(D) | **normalizing constant** | probability of the data under any hypothesis |

- **Priors can be objective or subjective** — sometimes background information pins the prior down (cookie problem: bowls chosen at random → 1/2 each); otherwise reasonable people may disagree.
- **Suite** — Downey's term for a set of hypotheses that is *mutually exclusive* (at most one true) and *collectively exhaustive* (at least one true); restricting to a suite makes p(D) computable.
- **Law of total probability** — with a suite, the normalizing constant is the sum over hypotheses: p(D) = p(B1) p(D|B1) + p(B2) p(D|B2) (= 5/8 in the cookie problem).

## 4. The Table Method and Worked Problems

- **Table method** — paper-and-pencil technique for Bayesian updates: one row per hypothesis, columns for prior p(H), likelihood p(D|H), product p(H) p(D|H); sum the product column to get the normalizing constant, divide through for posteriors.
- **Likelihoods can be rescaled** — when the suite is mutually exclusive and collectively exhaustive, multiplying the entire likelihood column by any convenient factor (e.g., using percentages instead of probabilities) cancels out in normalization.
- **The M&M problem** — one bag from 1994 (30% brown, 20% yellow, 20% red, …) and one from 1996 (24% blue, 20% green, 14% yellow, …); one yellow and one green M&M drawn, one from each bag. With independent draws the likelihood is the product per hypothesis — table yields p(yellow came from 1994 bag) = 20/27.
- **The Monty Hall problem** — three doors, one car; you pick Door A, Monty opens B or C (never the car), offers a switch. Careful data statement: D = "Monty chooses Door B *and* there is no car there." Likelihoods: 1/2 if car behind A (he picks B or C at random), 0 if behind B, 1 if behind C → posteriors p(A|D) = 1/3, p(C|D) = 2/3: **switching wins**.
- **Variations reveal the power of the approach** — if Monty always opens B when he can, the likelihood for A becomes 1 and the posteriors are 1/2, 0, 1/2: his choice of B then carries no information (but opening C would prove the car is behind B). The Bayesian framework generalizes cleanly to such variants.
