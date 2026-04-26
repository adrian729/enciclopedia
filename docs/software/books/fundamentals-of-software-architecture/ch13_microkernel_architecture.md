# Ch 13: Microkernel Architecture Style

## Table of Contents

- [1. Topology: Core System and Plug-Ins](#1-topology-core-system-and-plug-ins)
- [2. The Core System](#2-the-core-system)
- [3. Plug-In Components](#3-plug-in-components)
- [4. The Spectrum of Microkern-ality](#4-the-spectrum-of-microkern-ality)
- [5. Registry and Contracts](#5-registry-and-contracts)
- [6. Data Topologies](#6-data-topologies)
- [7. Cloud Considerations](#7-cloud-considerations)
- [8. Common Risks](#8-common-risks)
- [9. Governance](#9-governance)
- [10. Team Topology Considerations](#10-team-topology-considerations)
- [11. Architecture Characteristics Ratings](#11-architecture-characteristics-ratings)
- [12. Examples and Use Cases](#12-examples-and-use-cases)

## 1. Topology: Core System and Plug-Ins

- **Plug-in architecture** — the *microkernel* style (a.k.a. *plug-in* architecture) was invented decades ago and is still widely used. It is a relatively simple monolithic architecture made of two component types: a **core system** and **plug-in components**.
- **Natural fit for product-based applications** — software packaged and installed as a single, monolithic deployment on the customer's site (third-party products), and equally good for non-product business applications that require customization (e.g., a US insurance company with rules per state, an international shipping company with legal/logistical variations).
- **Two component types only** — application logic is split between independent plug-in components and the basic core system, which isolates features and provides extensibility, adaptability, and custom processing logic.

## 2. The Core System

- **Minimal functionality definition** — the *core system* is formally defined as the minimal functionality required to run the system. The Eclipse IDE core, for example, is just a basic text editor (open, change text, save); only plug-ins make Eclipse useful.
- **Happy path definition** — alternative definition: the *happy path* — a general processing flow with little or no custom processing. Microkernel takes the application's cyclomatic complexity *out* of the core and places it into plug-in components, improving extensibility, maintainability, and testability.
- **Going Green example (electronics recycling)** — instead of a giant `if/else` over `deviceID` inside `assessDevice()`, each device gets its own plug-in component. The core looks up the plug-in via the registry, instantiates it, and invokes `devicePlugin.assess()`. Adding a new device = adding a plug-in and updating the registry.
- **Core system implementation choices** — depending on size/complexity, the core can be built as a layered architecture, as a modular monolith, or even split into separately deployed *domain services* with each domain hosting domain-specific plug-ins. Example: `Payment Processing` as the core, with one plug-in per payment method (credit card, PayPal, store credit, gift card, purchase order).
- **User interface variants** — the Presentation layer can be embedded in the core, or implemented as a separate UI calling backend services, or itself implemented as a microkernel.

## 3. Plug-In Components

- **Standalone, independent components** — plug-ins contain specialized processing, additional features, and custom code that enhances or extends the core. They isolate highly volatile code, improving maintainability and testability. **Ideally, plug-in components should have no dependencies between them**.
- **Point-to-point communication** — communication between plug-ins and the core is generally **point-to-point**: the "pipe" is usually a method invocation or function call to the plug-in's entry-point class.
- **Compile-based vs. runtime-based plug-ins** — *runtime* plug-ins can be added or removed at runtime without redeploying the core or other plug-ins, typically managed via frameworks such as **OSGi** (Open Service Gateway Initiative, Java), **Penrose** (Java), **Jigsaw** (Java), or **Prism** (.NET). *Compile-based* plug-ins are simpler to manage but adding/removing/modifying one requires redeploying the entire monolithic application.
- **Implementation forms** — point-to-point plug-ins can be shared libraries (JAR, DLL, Gem), Java packages, or C# namespaces. Recommended namespace semantics: `app.plug-in.<domain>.<context>` (e.g., `app.plug-in.assessment.iphone6s`) — the second node identifies the component as a plug-in, the third the domain, the fourth the specific context.
- **Remote plug-in access alternative** — plug-ins can also be invoked via REST or messaging, with each plug-in deployed as its own service (or microservice in a container). This enables better decoupling, scalability, throughput, runtime changes without OSGi/Jigsaw/Prism, and asynchronous calls (e.g., kicking off an assessment and notifying the core when complete). Trade-offs: turns the architecture into a *distributed* one (hard to ship as on-prem product), adds complexity and cost, and a plug-in failure now breaks the request (unlike a monolithic deployment). Even so, the topology remains a single architecture quantum because every request still goes through the monolithic core.

## 4. The Spectrum of Microkern-ality

- **Not all plug-in systems are microkernels** — but all microkernels support plug-ins. A system's degree of "**microkern-ality**" depends on how much standalone functionality lives in the core.
- **Pure microkernels (left side)** — Eclipse IDE, linter tools: very little core functionality. A linter parses source and delivers an AST; until someone writes a plug-in, the core is of little use.
- **Plug-in-supporting systems (right side)** — web browsers: fully functional without plug-ins; plug-ins simply extend them.
- **Volatility of the core** — determining how volatile the core will be helps the architect decide between a system that just supports plug-ins and a more "pure" microkernel.

## 5. Registry and Contracts

- **Plug-in registry** — the core needs to know which plug-ins exist and how to reach them. The registry holds each plug-in's name, data contract, and remote-access details (depending on connection type). Example: a tax software plug-in flagging high-risk audit items registers with name `AuditChecker`, its input/output data contract, and contract format (XML).
- **Registry implementations** — as simple as an in-process map (`Map<String,String>`) keyed by an identifier and pointing at the plug-in (e.g., the Going Green core stores `iPhone6s` → `Iphone6sPlugin` for point-to-point, `iphone6s.queue` for messaging, or `https://atlas:443/assess/iphone6s` for REST), or as elaborate as **Apache ZooKeeper** or **Consul**.
- **Standard contracts within a domain** — contracts are usually standard across a domain of plug-ins and include behavior, input data, and output data. **Custom contracts** appear when plug-ins come from third parties; create an *adapter* between the plug-in's contract and the core's standard contract so the core needs no specialized code per plug-in.
- **Contract format** — XML, JSON, or objects passed back and forth. The Going Green `AssessmentPlugin` Java interface defines `assess()`, `register()`, `deregister()` and an `AssessmentOutput` containing a formatted `assessmentReport`, a `resell` flag, and `value`/`resellPrice`. The core only prints/displays the report; formatting is the plug-in's responsibility.

## 6. Data Topologies

- **Single relational database is typical** — microkernel architectures are usually monolithic and use a single (typically relational) database.
- **Plug-ins don't connect directly** — it's uncommon for plug-ins to talk to a centrally shared database. Instead, the core takes that responsibility and passes whatever data the plug-in needs. Reason: decoupling — a database change should affect only the core, not the plug-ins.
- **Plug-ins may own their own data store** — for example, each Going Green device-assessment plug-in can have its own simple database or rules engine for its specific assessment rules. The store can be external, embedded in the plug-in, or in-memory inside the monolithic deployment.

## 7. Cloud Considerations

- **Coarse-grained cloud options** — because the architecture is monolithic, the cloud offers a few coarse choices:
  - Deploy the entire application on the cloud (cloud facilities or containers).
  - Place only the data on the cloud and keep the microkernel on-premises.
  - Keep the core on-premises and place the plug-ins on the cloud.
- **Latency caveat for split deployments** — segregating core from plug-ins looks attractive for modularity, but plug-in calls happen frequently and pass a fair amount of information, so the latency between them can produce undesirable overhead.

## 8. Common Risks

- **Volatile core** — the core is supposed to be as stable as possible after initial development; building a constantly changing core undermines the style. Often this is the result of architects misjudging the core's volatility and must be addressed via refactoring.
- **Plug-in dependencies** — microkernels work best when plug-ins talk only to the core, not to each other. Most non-microkernel plug-in systems use **dependency-free plug-ins**: plug-ins with no dependencies other than the core. Complex applications such as Eclipse do build dependencies between components, forcing the core to resolve transitive dependency conflicts (what if two plug-ins need different versions of the same core library?). Avoid plug-in-to-plug-in dependencies whenever possible.

## 9. Governance

Governance revolves around checking how well architects honor the philosophy of the style. Common checks:

- **Volatility checks for the core** — fitness functions that monitor churn in version control, rather than a code-level check.
- **Rate of change in the core**.
- **Contract tests** — especially when some plug-ins support different versions than others due to gradual evolution.
- **Other structural verifications for the topology**.

## 10. Team Topology Considerations

The obvious split is between core and plug-ins, mirroring the topology:

- **Stream-aligned teams** — the core is a sweet spot; plug-ins may also fall to the team depending on the application.
- **Enabling teams** — extremely well suited; plug-ins isolate behavior so enabling teams can run A/B testing and other experiments cleanly.
- **Complicated-subsystem teams** — well suited because microkernels defer specialized behavior (e.g., analytics) to plug-ins; the stream-enabled team works on the core and calls into the sophisticated plug-in.
- **Platform teams** — concerned mostly with operational details, as with any monolithic architecture.

## 11. Architecture Characteristics Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | $ |
| Partitioning type | Domain and technical |
| Number of quanta | 1 |
| Simplicity | 4 stars |
| Modularity | 3 stars |
| Testability | 3 stars |
| Deployability | 3 stars |
| Reliability | 3 stars |
| Evolvability | 3 stars |
| Responsiveness | 3 stars |
| Scalability | 1 star |
| Elasticity | 1 star |
| Fault tolerance | 1 star |

- **Quantum is always 1** — all requests go through the core to reach plug-ins, so the architecture quantum is singular. Like layered, simplicity and overall cost are the main strengths; scalability, fault tolerance, and elasticity the main weaknesses, due to the typical monolithic deployment.
- **Both domain- and technically partitioned** — microkernel is unique in being the only style that can be both. Most are technically partitioned, but a strong domain-to-architecture isomorphism (different configurations per location/client; user-customization-heavy products like Jira or Eclipse) brings the domain dimension in.
- **Testability, deployability, reliability (3★)** — slightly above average because functionality is isolated in plug-ins, reducing testing scope and deployment risk — particularly when plug-ins are runtime-based.
- **Modularity and evolvability (3★)** — slightly above average; functionality can be added, removed, and changed via independent self-contained plug-ins. Tax-prep example: a new US tax form ships as a new plug-in; an obsolete worksheet is simply removed.
- **Responsiveness (3★)** — microkernel apps generally stay small and don't suffer from the *Architecture Sinkhole* antipattern. Streamlining by *unplugging* unneeded functionality makes the application run faster — e.g., **WildFly** (previously the JBoss Application Server) runs much faster after removing clustering, caching, and messaging plug-ins.

## 12. Examples and Use Cases

- **Software-development tools** — most are microkernels: **Eclipse IDE**, **PMD**, **Jira**, **Jenkins**.
- **Web browsers** — Chrome and Firefox use a microkernel core extended by viewers and other plug-ins.
- **Tax preparation software (1040 example)** — the IRS 1040 form is a two-page summary; each line is a single number computed from many other forms and worksheets. The 1040 acts as the core (driver); each additional form/worksheet is a plug-in. Tax-law changes are isolated to the affected plug-in.
- **Insurance claims processing** — each US-state (or other jurisdiction) has different rules (e.g., free windshield replacement is allowed in some states, not others). Putting each jurisdiction's rules in its own plug-in (source code or a rules-engine instance accessed by the plug-in) avoids the *Big Ball of Mud* trap that large rules engines fall into. New jurisdictions can be added or removed without touching the rest of the system; the core is the standard claim-filing/processing flow that rarely changes.
- **Pervasive style** — once you've seen microkernel, you notice it everywhere: an architecture structure (core + plug-ins) that fits the very common domain problem of *customization*.
