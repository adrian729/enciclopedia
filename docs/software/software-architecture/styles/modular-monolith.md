# Modular Monolith Architecture

> *Fundamentals* Ch 11 is the sole source. The modular monolith was added in the 2025 second edition because widespread DDD adoption and increased focus on domain partitioning made it popular enough to warrant its own chapter and characteristic ratings. The style was popularized by Simon Brown and is now the default starting point for new systems whose direction is not yet certain. *The Hard Parts* doesn't cover the style as a style — it covers the decomposition path *out* of one.

## Table of Contents

- [1. Topology](#1-topology)
- [2. Monolithic vs. Modular Structure](#2-monolithic-vs-modular-structure)
- [3. Module Communication — Peer-to-Peer vs. Mediator](#3-module-communication--peer-to-peer-vs-mediator)
- [4. Data Topology and Cloud Fit](#4-data-topology-and-cloud-fit)
- [5. When to Use and When Not To](#5-when-to-use-and-when-not-to)
- [6. Risks and Antipatterns](#6-risks-and-antipatterns)
- [7. Architecture Characteristic Ratings](#7-architecture-characteristic-ratings)
- [8. Example — EasyMeals](#8-example--easymeals)
- [Sources](#sources)

## 1. Topology

The modular monolith is **a single deployment unit with functionality grouped by domain area.** The deployment shape is what every monolith looks like: WAR/JAR in Java, single .NET assembly, EAR file. The differentiating trait is the *partitioning* — by **domain**, not by technical layer.

| Style | Top-level namespace shape |
|---|---|
| **Layered (technical)** | `com.app.presentation.customer.profile` |
| **Modular monolith (domain)** | `com.app.customer.profile` |

Subdivisions *after* the domain may still group by technical concern (`com.app.customer.profile.business`), but the **first** partition is the domain. Each top-level domain — or subdomain — is a **module**. A module is made up of one or more components (see [Components and Quantum](foundations/components-and-quantum.md)).

## 2. Monolithic vs. Modular Structure

The same domain-partitioned shape can be assembled in two ways:

| Structure | Layout | Strength | Risk |
|---|---|---|---|
| **Monolithic** | All modules in a single source-code repository, delineated by directory or namespace, shipped together | Easiest to maintain, test, and deploy | Boundaries erode easily because peer-to-peer module calls are *too* convenient — slides into Big Ball of Mud |
| **Modular** | Each module is a self-contained artifact (JAR/DLL), assembled into a single deployment unit at deploy time. Each module can live in its own repo | Cleaner boundaries; works well for large systems with independent modules | Loses effectiveness when modules need to communicate frequently |

Pick monolithic when modules interact often. Pick modular when modules are largely independent, when the system is large, or when modules need different expertise.

## 3. Module Communication — Peer-to-Peer vs. Mediator

Communication is necessary but undesirable. `OrderPlacement` must reach `InventoryManagement` to adjust stock and `PaymentProcessing` to apply payment.

**Peer-to-peer.** A class in one module instantiates a class in another and calls its methods directly. In the *monolithic* structure this is too convenient — boundaries dissolve. In the *modular* structure, classes in another module live in separate JARs/DLLs, creating a *compile-time* dependency; the usual fix is a shared interface class in a separate artifact so each module still compiles independently. Excessive peer-to-peer in modular structure leads to **DLL Hell** (or Java's **JAR Hell**) — the unmanageable transitive-dependency tangle.

**Mediator.** A mediator component sits between modules, accepting requests and orchestrating delivery to the right module. Modules become decoupled from each other, though each is now coupled to the mediator. The mediator — not the dependent modules — owns the API for invoking functionality elsewhere. Heavier on ceremony, but the boundary discipline survives team turnover.

## 4. Data Topology and Cloud Fit

- **Single database (default).** A monolithic database is typical and reduces inter-module communication because data is shared.
- **Per-module databases.** Independent modules with specific functions can own their own database with contextual data, even within a monolithic deployment — particularly useful for modules that will eventually become their own services.
- **Cloud fit is limited.** Modular monoliths can deploy to the cloud (especially small ones) but the monolithic nature limits use of on-demand provisioning. Smaller systems can still use cloud services like file storage, database, and messaging.

## 5. When to Use and When Not To

**When to use:**

- Tight budget and time constraints.
- **New systems** where direction is unclear — start here, then move to service-based or microservices later if needed.
- Domain-focused, cross-functional teams.
- Teams practicing DDD.
- Majority of changes are **domain-based** (e.g., adding a wishlist-expiration feature).

**When not to use:**

- High scalability, elasticity, availability, fault tolerance, responsiveness, or performance requirements.
- Majority of changes are **technical** (replacing UI or DB technology repeatedly) — those ripple through every domain module, and the layered style is a better fit.

## 6. Risks and Antipatterns

- **Getting too big.** The primary risk with any monolith. Warning signs: changes take too long; changes in one area unexpectedly break others; team members get in each other's way; startup time grows.
- **Too much code reuse.** Over-sharing across modules blurs boundaries and produces an *unstructured monolith* — code so highly interdependent it cannot be unraveled. This is the slow path to Big Ball of Mud.
- **Too much intermodule communication.** Ideally modules are independent and self-contained. Heavy intermodule chatter signals ill-defined domains; redefine the domains before adding more workflows.

Governance focuses on the *module* (a directory / namespace / package):

- Automate checks that every namespace starts with one of the system's defined modules (e.g., `com.orderentry.orderplacement`).
- Limit total dependencies — automate a coupling-points cap per module (e.g., incoming + outgoing references ≤ 5).
- Restrict specific pairs — `OrderPlacement` must not access `Shipping`, expressible in ArchUnit / ArchUnitNet / PyTestArch / TSArch.
- Per-module validation works cleanly with monolithic structure; modular structure is harder because modules may live in separate repos and must be tested individually.

## 7. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | ★★★★★ |
| Simplicity | ★★★★★ |
| Deployability | ★★ |
| Elasticity | ★ |
| Evolutionary | ★★★ |
| Fault tolerance | ★ |
| Modularity | ★★★★ |
| Performance | ★★★ |
| Reliability | ★★★ |
| Scalability | ★ |
| Testability | ★★ |

- **Domain-partitioned with quantum 1.** Application logic is partitioned into modules; monolithic deployment yields an architecture quantum of 1.
- **Strengths — cost, simplicity, modularity.** Monolithic nature avoids distributed complexity; modularity comes from separation of concerns across domain modules.
- **Deployability and testability (2★).** Slightly higher than layered thanks to modularity, but still hampered by monolithic ceremony, deployment risk, and incomplete testing.
- **Elasticity and scalability (1★).** Monolithic deployment limits both; selective scaling demands complex techniques (multithreading, internal messaging) the style isn't built for.
- **Fault tolerance and availability.** Monolithic deployment means one out-of-memory takes down everything; high MTTR hurts availability.

## 8. Example — EasyMeals

A small neighborhood delivery restaurant. No high scalability or responsiveness requirements; limited budget. Modular monolith fits.

Modules:

```
com.easymeals.placeorder
com.easymeals.payment
com.easymeals.prepareorder
com.easymeals.delivery
com.easymeals.recipes
com.easymeals.inventory
```

| Module | Behavior |
|---|---|
| `PlaceOrder` | View menu, select items, capture customer/payment info, submit order. Components: `menu`, `shoppingcart`, `customerdata`, `paymentdata`, `checkout`. |
| `PaymentProcessing` | Applies payment for credit cards, debit cards, PayPal; modularity makes adding new payment types (e.g., loyalty points) easy. |
| `PrepareOrder` | Displays the order to kitchen staff and marks it ready. |
| `Delivery` | Assigns a delivery person, records issues, marks completion. |
| `Recipes` | Kitchen and management maintain menu items and ingredients/measurements. |
| `IngredientsInventory` | Most complex; uses an AI component to forecast sales volume and automate weekly procurement. |

Adding a new payment type touches `PaymentProcessing` only — the modularity benefit in action.

## When to Decompose This Style

Modular monolith is *designed* to be decomposed when the cost-and-simplicity benefit no longer justifies the modularity penalty. The trigger is usually one of the modularity drivers from [When to Decompose](decomposition/when-to-decompose.md) — scalability, elasticity, fault tolerance, or agility — outweighing the cost. If the modules were defined well, the boundaries become service boundaries; if not, the decomposition reveals the domain mistakes first. The decision tree between *tactical forking* and *component-based decomposition* lives in [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md).

## Sources

- [Fundamentals Ch 11: The Modular Monolith Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch11_modular_monolith.md) (sole source — topology, monolithic vs. modular structure, peer-to-peer vs. mediator communication, EasyMeals example, characteristic ratings)


<!-- prev-next-nav -->

---

← [Layered](software/software-architecture/styles/layered.md) | [Pipeline](software/software-architecture/styles/pipeline.md) →
