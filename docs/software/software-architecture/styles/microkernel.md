# Microkernel Architecture

> *Fundamentals* Ch 13 is the sole source. Microkernel (a.k.a. *plug-in architecture*) is decades old and still widely used. It is the **only style in the catalog that can be both domain-partitioned and technically-partitioned** — the dual nature comes from the core handling technical concerns while plug-ins handle domain variation. *The Hard Parts* doesn't cover microkernel as a distinct style.

## Table of Contents

- [1. Topology — Core and Plug-Ins](#1-topology--core-and-plug-ins)
- [2. The Core System](#2-the-core-system)
- [3. Plug-In Components](#3-plug-in-components)
- [4. Spectrum of "Microkern-ality"](#4-spectrum-of-microkern-ality)
- [5. Registry and Contracts](#5-registry-and-contracts)
- [6. Data Topology and Cloud Considerations](#6-data-topology-and-cloud-considerations)
- [7. When to Use and When Not To](#7-when-to-use-and-when-not-to)
- [8. Risks and Antipatterns](#8-risks-and-antipatterns)
- [9. Architecture Characteristic Ratings](#9-architecture-characteristic-ratings)
- [10. Examples](#10-examples)
- [Sources](#sources)

## 1. Topology — Core and Plug-Ins

A relatively simple monolithic architecture composed of two component types and nothing else:

| Component | Role |
|---|---|
| **Core system** | The minimal functionality required to run the system — the *happy path* with little or no custom processing. |
| **Plug-in components** | Independent components containing specialized processing, additional features, and custom code that enhances or extends the core. |

The defining design move: **keep the happy path in the core and the complexity in the plug-ins.** Microkernel takes the application's cyclomatic complexity *out* of the core and pushes it into plug-ins, raising extensibility, maintainability, and testability.

It is the natural fit for *product-based* applications — software packaged and installed as a single monolithic deployment on the customer's site — and equally good for non-product business applications requiring customization (a US insurance company with per-state rules; an international shipping company with per-jurisdiction logistics).

## 2. The Core System

Two equivalent definitions of the core:

- **Minimal functionality definition.** The minimal functionality required to run the system. The Eclipse IDE core, for example, is just a basic text editor (open, change text, save); only plug-ins make Eclipse useful.
- **Happy path definition.** A general processing flow with little or no custom processing. Custom processing lives in plug-ins.

The Going Green electronics-recycling example: instead of a giant `if/else` over `deviceID` inside `assessDevice()`, each device gets its own plug-in component. The core looks up the plug-in via the registry, instantiates it, and invokes `devicePlugin.assess()`. Adding a new device = adding a plug-in and updating the registry.

The core itself can be implemented in different shapes depending on its size and complexity:

- A [Layered Architecture](styles/layered.md) for small cores.
- A [Modular Monolith](styles/modular-monolith.md) when the core itself has internal domain structure.
- Split into separately deployed *domain services*, each domain hosting its own plug-ins (e.g., `Payment Processing` as the core, with one plug-in per payment method — credit card, PayPal, store credit, gift card, purchase order).

The user interface is independently variable: embedded in the core, implemented as a separate UI calling backend services, or itself implemented as a microkernel.

## 3. Plug-In Components

Plug-ins are standalone, independent components. Their philosophy:

- **Specialized processing only.** They isolate highly volatile code, improving maintainability and testability.
- **No dependencies between plug-ins.** Ideally, plug-ins talk only to the core. Most non-microkernel plug-in systems use **dependency-free plug-ins**. Complex applications such as Eclipse do build inter-plug-in dependencies, forcing the core to resolve transitive conflicts (what if two plug-ins need different versions of the same library?). Avoid plug-in-to-plug-in dependencies whenever possible.
- **Point-to-point communication.** The "pipe" is usually a method invocation or function call to the plug-in's entry-point class.

| Plug-in mode | Behavior | Frameworks |
|---|---|---|
| **Compile-based** | Simpler to manage but adding/removing/modifying a plug-in requires redeploying the entire monolith. | Java packages, C# namespaces, shared libraries (JAR/DLL/Gem). |
| **Runtime-based** | Can be added or removed at runtime without redeploying the core or other plug-ins. | **OSGi** (Open Service Gateway Initiative, Java), **Penrose** (Java), **Jigsaw** (Java), **Prism** (.NET). |
| **Remote (REST/messaging)** | Plug-ins deploy as their own services. Better decoupling, scalability, throughput, runtime evolution, and async calls. Trade-offs: turns the architecture distributed (hard to ship as on-prem product), adds complexity and cost, and a plug-in failure now breaks the request. Even so, the topology remains a single architecture quantum because every request still goes through the monolithic core. | — |

Recommended namespace semantics: `app.plug-in.<domain>.<context>` (e.g., `app.plug-in.assessment.iphone6s`) — the second node identifies the component as a plug-in, the third the domain, the fourth the specific context.

## 4. Spectrum of "Microkern-ality"

> Not all plug-in systems are microkernels — but all microkernels support plug-ins.

A system's degree of *microkern-ality* depends on how much standalone functionality lives in the core.

| End of spectrum | Examples | Behavior |
|---|---|---|
| **Pure microkernel** | Eclipse IDE, linter tools | Very little core functionality. A linter parses source and delivers an AST; until someone writes a plug-in, the core is of little use. |
| **Plug-in-supporting** | Web browsers (Chrome, Firefox) | Fully functional without plug-ins; plug-ins simply extend them. |

Volatility of the core decides where the system should sit on the spectrum. The more the core is expected to churn, the further from "pure microkernel" the system should be — pure microkernels assume the core is stable after initial development.

## 5. Registry and Contracts

The core needs to know which plug-ins exist and how to reach them.

- **Plug-in registry.** Holds each plug-in's name, data contract, and remote-access details (depending on connection type). Example: a tax-software plug-in flagging high-risk audit items registers as `AuditChecker`, with its input/output data contract, and contract format (XML).
- **Implementations.** As simple as an in-process map (`Map<String,String>`) keyed by identifier and pointing at the plug-in — `iPhone6s` → `Iphone6sPlugin` for point-to-point, `iphone6s.queue` for messaging, `https://atlas:443/assess/iphone6s` for REST — or as elaborate as **Apache ZooKeeper** or **Consul**.
- **Standard vs. custom contracts.** Contracts are usually standard across a domain of plug-ins and include behavior, input data, and output data. Custom contracts appear when plug-ins come from third parties; create an *adapter* between the plug-in's contract and the core's standard contract so the core needs no specialized code per plug-in.
- **Contract format.** XML, JSON, or objects passed back and forth. The Going Green `AssessmentPlugin` interface defines `assess()`, `register()`, `deregister()`, and an `AssessmentOutput` containing a formatted `assessmentReport`, a `resell` flag, and `value`/`resellPrice`. The core only prints/displays the report; formatting is the plug-in's responsibility.

## 6. Data Topology and Cloud Considerations

- **Single relational database is typical.** Microkernel is usually monolithic and uses a single (typically relational) database.
- **Plug-ins don't connect directly to the central DB.** The core takes that responsibility and passes whatever data the plug-in needs. A database change should affect only the core, not the plug-ins.
- **Plug-ins may own their own data store.** Each Going Green device-assessment plug-in can have its own simple database or rules engine for its specific assessment rules — external, embedded, or in-memory.

Cloud options are coarse-grained because the architecture is monolithic:

- Deploy the entire application on the cloud (cloud facilities or containers).
- Place only the data on the cloud and keep the microkernel on-premises.
- Keep the core on-premises and place the plug-ins on the cloud.

The split deployments look attractive for modularity but plug-in calls are frequent and pass a fair amount of information, so latency between them can produce undesirable overhead.

## 7. When to Use and When Not To

**When to use:**

- Domains dominated by *customization* — per-state insurance rules, per-form tax preparation, per-client packaged products.
- Product-based applications shipped to many customers with per-customer variation.
- Applications with a stable happy path and high-churn extension behavior.

**When not to use:**

- High scalability, elasticity, or fault-tolerance requirements (the monolithic core bottlenecks all three).
- Systems with no meaningful core/extension separation — applying microkernel where the domain doesn't have a stable core produces a *volatile-core* antipattern (see [§ 8](#8-risks-and-antipatterns)).

## 8. Risks and Antipatterns

- **Volatile core.** The core is supposed to be as stable as possible after initial development. A constantly changing core undermines the style; usually the architect has misjudged the core's volatility and the system needs refactoring.
- **Plug-in dependencies.** Microkernel works best when plug-ins talk only to the core, not to each other. When plug-in-to-plug-in dependencies are unavoidable, the core resolves transitive conflicts; avoid where possible.

Governance focuses on the style's philosophy rather than structural checks:

- **Volatility checks for the core** — fitness functions that monitor churn in version control, not code-level checks.
- **Rate of change in the core.**
- **Contract tests** — especially when some plug-ins support different versions due to gradual evolution.

## 9. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | $ |
| Partitioning | Domain *and* technical |
| Quanta | 1 |
| Simplicity | ★★★★ |
| Modularity | ★★★ |
| Testability | ★★★ |
| Deployability | ★★★ |
| Reliability | ★★★ |
| Evolvability | ★★★ |
| Responsiveness | ★★★ |
| Scalability | ★ |
| Elasticity | ★ |
| Fault tolerance | ★ |

- **Quantum is always 1.** All requests go through the core to reach plug-ins, so the architecture quantum is singular. Simplicity and overall cost are the main strengths; scalability, fault tolerance, and elasticity are the main weaknesses.
- **Both domain- and technically-partitioned.** Microkernel is unique in the catalog. Most cores are technically partitioned, but a strong domain-to-architecture isomorphism (per-location or per-client configurations; user-customization-heavy products like Jira or Eclipse) brings in the domain dimension.
- **Testability, deployability, reliability (3★).** Slightly above average because functionality is isolated in plug-ins, reducing testing scope and deployment risk — particularly when plug-ins are runtime-based.
- **Modularity and evolvability (3★).** Slightly above average; functionality can be added, removed, and changed via independent self-contained plug-ins. Tax-prep example: a new US tax form ships as a new plug-in; an obsolete worksheet is simply removed.
- **Responsiveness (3★).** Microkernel apps stay small and don't suffer from the architecture-sinkhole antipattern. Streamlining by *unplugging* unneeded functionality makes the application run faster — **WildFly** (previously JBoss Application Server) runs much faster after removing clustering, caching, and messaging plug-ins.

## 10. Examples

- **Software-development tools.** Most are microkernels: **Eclipse IDE**, **PMD**, **Jira**, **Jenkins**.
- **Web browsers.** Chrome and Firefox use a microkernel core extended by viewers and other plug-ins.
- **Tax preparation software (the 1040 example).** The IRS 1040 form is a two-page summary; each line is a single number computed from many other forms and worksheets. The 1040 acts as the core (driver); each additional form/worksheet is a plug-in. Tax-law changes are isolated to the affected plug-in.
- **Insurance claims processing.** Each US state (or other jurisdiction) has different rules — free windshield replacement is allowed in some states, not others. Putting each jurisdiction's rules in its own plug-in (source code or a rules-engine instance accessed by the plug-in) avoids the Big Ball of Mud trap that large rules engines fall into.

Once you've seen microkernel, you notice it everywhere: an architecture structure (core + plug-ins) that fits the very common domain problem of *customization*.

## When to Decompose This Style

Microkernel is unusual because the natural decomposition is **within** the style — splitting the core into per-domain microkernels, or promoting plug-ins to remote services. The trigger is usually scalability or fault tolerance overcoming the single-quantum constraint. [When to Decompose](decomposition/when-to-decompose.md) frames the modularity drivers; [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md) covers the tactical-fork vs. component-based-decomposition decision tree if the core is collapsing under load.

## Sources

- [Fundamentals Ch 13: Microkernel Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch13_microkernel_architecture.md) (sole source — topology, core, plug-ins, microkern-ality spectrum, registry, contracts, governance, characteristic ratings, examples)


<!-- prev-next-nav -->

---

← [Pipeline](software/software-architecture/styles/pipeline.md) | [Service-Based](software/software-architecture/styles/service-based.md) →
