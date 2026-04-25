# Ch 3: Working Code Isn't Enough

## Table of Contents

- [1. Tactical Programming](#1-tactical-programming)
- [2. Strategic Programming](#2-strategic-programming)
- [3. How Much to Invest](#3-how-much-to-invest)
- [4. Startups and Investment](#4-startups-and-investment)

## 1. Tactical Programming

- **Tactical programming** — a mindset focused on getting the current task working as quickly as possible, with little regard for design quality
- **Short-sighted trade-offs** — each shortcut adds "just a little" complexity, but because complexity is incremental (Ch 2), these trade-offs compound into a codebase that is painful to modify
- **Self-reinforcing cycle** — once shortcuts accumulate, fixing them feels too expensive, so developers keep patching around problems, creating even more complexity
- **Tactical tornado** — a developer who ships features fast but leaves a trail of poorly designed code behind. Management may praise the speed, but teammates who inherit and maintain the code pay the real cost

## 2. Strategic Programming

- **Working code is not enough** — the primary goal should be producing a great design that also works, not merely code that works
- **Investment mindset** — deliberately spend time improving the system's structure, knowing it slows you down now but pays off later
- **Proactive investments** — explore multiple design alternatives before committing, anticipate future changes, write good documentation
- **Reactive investments** — when you discover a design mistake, fix it immediately instead of patching around it. Strategic programmers continually make small improvements; tactical programmers continually add small bits of complexity

## 3. How Much to Invest

- **10-20% of total development time** — small enough to avoid schedule disruption, large enough to produce meaningful design improvements over time
- **Break-even comes quickly** — within a few months, the cleaner design speeds development by at least 10-20%, effectively making the investment free from that point on
- **Tactical approach inverts** — a tactical programmer finishes initial tasks 10-20% faster but progressively slows down as complexity accumulates, eventually losing more time than was "saved"
- **Avoid big up-front design** — the ideal design emerges incrementally. Make lots of small, continual investments rather than one massive planning effort (waterfall)

## 4. Startups and Investment

- **Startup pressure is real but overstated** — many startups rationalize tactical coding ("we'll clean it up later"), but once the codebase turns to spaghetti, it is nearly impossible to fix
- **Design payoff arrives fast** — good or bad design choices show their impact quickly, so tactical coding may not even speed up the first release
- **Talent feedback loop** — the best engineers care about code quality. A messy codebase repels top talent, leaving you with mediocre engineers who degrade the system further
- **Facebook vs. Google/VMware** — Facebook's "Move fast and break things" culture eventually led to unstable, poorly documented code, forcing a cultural shift to "Move fast with solid infrastructure." Google and VMware invested in quality from the start, built strong technical reputations, and attracted top talent
- **Consistency matters** — strategic design must be applied today, not deferred to "after the crunch." Each postponement makes the next one easier to justify, and the culture quietly slides into tactical programming
