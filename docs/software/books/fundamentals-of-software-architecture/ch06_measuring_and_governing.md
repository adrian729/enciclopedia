# Ch 6: Measuring and Governing Architecture Characteristics

## Table of Contents

- [1. Why Measurement Is Hard](#1-why-measurement-is-hard)
- [2. Operational Measures](#2-operational-measures)
- [3. Structural Measures](#3-structural-measures)
- [4. Process Measures](#4-process-measures)
- [5. Governance and Fitness Functions](#5-governance-and-fitness-functions)
- [6. Fitness Function Examples](#6-fitness-function-examples)
- [7. Chaos Engineering and the Simian Army](#7-chaos-engineering-and-the-simian-army)

## 1. Why Measurement Is Hard

- **Architecture characteristics aren't physics** — terms like *agility*, *deployability*, and *wicked fast performance* have vague, contested meanings across the industry.
- **Wildly varying definitions** — within a single organization, developers, architects, and operations may disagree on what "performance" means; without a shared definition there is no productive conversation.
- **Too composite** — many desirable characteristics decompose into smaller ones (e.g., **agility** = modularity + deployability + testability). Decomposing composites into objectively measurable parts solves the ambiguity problem.
- **Ubiquitous language** — when an organization adopts standard, concrete definitions for architecture characteristics, it produces a shared vocabulary that exposes objectively measurable features.

## 2. Operational Measures

- **Direct metrics with nuance** — performance and scalability seem obvious to measure, yet averages hide outliers. Measuring only the average response time misses the 1% of requests that take 10× longer; track maximum response times too.
- **Statistical baselines beat hard numbers** — a video streaming team measures scale over time, builds statistical models, and alarms when real-time metrics deviate. Failure means either the model is wrong or something is amiss; both are useful signals.
- **Metrics evolve with the ecosystem** — modern teams track performance budgets like *first contentful paint* and *first CPU idle*, which speak to mobile web users.
- **K-weight budgets** — forward-thinking organizations cap the total bytes of libraries and frameworks per page, derived from physics: only so many bytes traverse a low-bandwidth mobile connection at once.

## 3. Structural Measures

- **No comprehensive metric for architecture quality** exists, but narrow code-structure measures help architects govern modularity.
- **Cyclomatic Complexity (CC)** — Thomas McCabe Sr. (1976), an objective complexity measure at function/method, class, or application level. Computed from graph theory on **decision points**: zero conditionals ⇒ CC = 1; one conditional ⇒ CC = 2.
- **Formula** — `CC = E − N + 2` for a single function (E = edges/decisions, N = nodes/lines). General form for fan-out: `CC = E − N + 2P` where P is connected components.
- **Code smell** — overly complex code damages modularity, testability, and deployability; left unmonitored, complexity dominates the codebase.
- **Essential vs. accidental complexity** — CC measures complexity but cannot distinguish a hard problem from a poor design. Useful for assessing both human-written and generative AI code (the latter often brute-forces accidental complexity).
- **Threshold guidance** — industry says CC < 10 acceptable; the authors prefer < 5. Crap4J flags code as "crappy" once CC × low coverage cross a threshold (CC > 50 is unsalvageable). Neal once saw a single C function with CC > 800 (4,000 LOC, liberal `GOTO`).
- **TDD lowers CC** — writing the smallest code to pass small tests yields cohesive, well-factored methods with low CC as a side effect.

## 4. Process Measures

- **Composite characteristics like agility** decompose into testability and deployability, both objectively measurable.
- **Testability metrics** — code-coverage tools report execution percentage, but 100% coverage with weak assertions provides no real confidence. Tools cannot replace thinking and intent.
- **Deployability metrics** — percentage of successful deployments, deployment duration, deployment-induced bug counts. Each team must arrive at measurements that capture qualitative and quantitative data fitting its priorities.
- **Process drives structure** — when deployability and testability rank high, architects emphasize modularity and isolation at the architecture level. Almost anything in a project's scope can rise to the level of an architecture characteristic if it forces significant decisions.

## 5. Governance and Fitness Functions

- **Governance** — derived from Greek *kubernan* ("to steer"); architects govern any aspect of software development they want to influence, including quality, security, and modularity.
- **Important but not urgent** — modularity exemplifies architectural concerns that get crowded out by schedule pressure unless automated.
- **Automation lineage** — Extreme Programming begat continuous integration; CI begat DevOps; DevOps begat automated architectural governance via **fitness functions**, introduced in *Building Evolutionary Architectures* (Neal Ford et al., O'Reilly 2022).
- **Fitness function origin** — borrowed from evolutionary computing: an objective function that assesses how close an output comes to its goal (e.g., genetic algorithm solving the traveling salesperson problem uses one fitness function for route length, another for cost, another for time away).
- **Architectural fitness function** — *any mechanism that provides an objective integrity assessment of some architecture characteristic or combination of architecture characteristics.* Not a new framework — a perspective that overlaps existing tools: chaos engineering, metrics, monitors, unit-test libraries.

## 6. Fitness Function Examples

- **Cyclic Dependencies antipattern** — auto-import IDE features tempt developers to create cycles between components, so reuse becomes impossible without dragging dependencies along, sliding the architecture toward **Big Ball of Mud**. Code reviews catch it too late.
- **JDepend cycle test** — fitness function using `jdepend.containsCycles()` wired into the CI build catches cycles immediately. A textbook example of automating an *important rather than urgent* concern.
- **Distance from the Main Sequence** — JDepend can also assert each package stays within a tolerance (e.g., 0.5) of the ideal, failing the test otherwise.
- **ArchUnit (JVM)** — JUnit-style framework for architectural rules. Lets architects express layered-architecture constraints declaratively:

```java
layeredArchitecture()
    .layer("Controller").definedBy("..controller..")
    .layer("Service").definedBy("..service..")
    .layer("Persistence").definedBy("..persistence..")
    .whereLayer("Controller").mayNotBeAccessedByAnyLayer()
    .whereLayer("Service").mayOnlyBeAccessedByLayers("Controller")
    .whereLayer("Persistence").mayOnlyBeAccessedByLayers("Service")
```

- **NetArchTest (.NET)** — analogous tool for C#; e.g., assert that types in `Presentation` namespace `ShouldNot().HaveDependencyOn("...Data")`.
- **Gaming the metric** — once developers learn the measurement, some code to it (e.g., unit tests with no assertions inflate coverage). ArchUnit-style rules can require every test to contain at least one assertion; dedicated rule-breakers will still find ways, but accidental lapses are blocked.

- **Collaboration over imposition** — architects must ensure developers understand the *purpose* of a fitness function before imposing it on them. The intent is automated governance, not ivory-tower esoterica.

## 7. Chaos Engineering and the Simian Army

- **Chaos engineering origin** — when Netflix moved to AWS it lost direct operational control, so it built tools that simulate failure in production. The discipline asks not *if* something will break but *when*.
- **Chaos Monkey & Latency Monkey** — simulate general chaos and high-latency conditions; **Chaos Kong** simulates an entire AWS data-center failure (and has helped Netflix survive real ones).
- **Conformity Monkey** — production fitness function enforcing rules architects defined (e.g., every service must respond without errors for all requests).
- **Security Monkey** — checks each service for known security defects: open ports that shouldn't be, configuration errors.
- **Janitor Monkey** — finds orphan services no one routes to anymore (the inevitable byproduct of evolutionary architecture) and disintegrates them to stop burning cloud spend.
- **Checklist Manifesto framing** — Atul Gawande's book (Metropolitan, 2009) describes how pilots and surgeons use checklists not because they forget their jobs, but because succinct reminders are effective for highly detailed repetitive work. Fitness functions are checklists for architecture: lightweight automated reminders, not heavyweight bureaucracy.
