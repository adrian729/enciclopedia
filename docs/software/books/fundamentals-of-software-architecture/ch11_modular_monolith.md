# Ch 11: The Modular Monolith Architecture Style

## Table of Contents

- [1. Topology](#1-topology)
- [2. Monolithic Structure vs. Modular Structure](#2-monolithic-structure-vs-modular-structure)
- [3. Module Communication](#3-module-communication)
- [4. Data Topologies and Cloud Considerations](#4-data-topologies-and-cloud-considerations)
- [5. Common Risks](#5-common-risks)
- [6. Governance](#6-governance)
- [7. Team Topology Considerations](#7-team-topology-considerations)
- [8. Style Characteristics](#8-style-characteristics)
- [9. When to Use and When Not to Use](#9-when-to-use-and-when-not-to-use)
- [10. Examples and Use Cases: EasyMeals](#10-examples-and-use-cases-easymeals)

## 1. Topology

- **Why a new chapter** — thanks to widespread DDD adoption and increased focus on domain partitioning, modular monolith (popularized by Simon Brown) has gained enough popularity since the 2020 first edition that the second edition adds (and rates) it.
- **Monolithic shape** — deployed as a single unit (WAR/JAR in Java, single .NET assembly, EAR file). The isomorphic shape is *a single deployment unit with functionality grouped by domain area*.
- **Domain-partitioned (vs. layered)** — layered organizes by *technical* capability (e.g., `com.app.presentation.customer.profile`); modular monolith organizes by *domain* (`com.app.customer.profile`). Sub-namespaces *after* the domain may further subdivide by technical concern (`com.app.customer.profile.business`).
- **Modules** — domains (or subdomains) are called *modules* in this style. A module is made up of one to many components (see Ch. 8).

## 2. Monolithic Structure vs. Modular Structure

- **Monolithic structure** — all modules live in a single source-code repository, delineated by directory or namespace, and ship together. Simplest option: easier to maintain, test, and deploy. Risk: developers reuse too much code across modules and let modules talk too freely, eroding boundaries into a Big Ball of Mud.
- **Modular structure** — each module is a self-contained artifact (JAR/DLL), assembled into a single deployment unit at deploy time. Each module can live in its own repo. Works well when modules are largely independent, when systems are large, or when modules need different expertise. Tends to produce cleaner boundaries; loses effectiveness when interdependent modules need to communicate often (use monolithic structure instead).

## 3. Module Communication

- **Communication is necessary but undesirable** — `OrderPlacement` must reach `InventoryManagement` to adjust stock, and `PaymentProcessing` to apply payment.
- **Peer-to-peer approach** — a class in one module instantiates a class in another and invokes its methods directly. With monolithic structure, this is *too* convenient and easily slides into Big Ball of Mud. With modular structure, classes in another module live in separate JARs/DLLs, creating a *compile-time* dependency; the usual fix is a shared interface class in a separate JAR/DLL so each module compiles independently. Excessive peer-to-peer in modular structure leads to the *DLL Hell* (Java: *JAR Hell*) antipattern.
- **Mediator approach** — a mediator component sits between modules, accepting requests and orchestrating delivery to the right module. Decouples modules from each other (though each is now coupled to the mediator). The *mediator* — not the dependent modules — owns the API/interface for invoking functionality elsewhere.

## 4. Data Topologies and Cloud Considerations

- **Single database (default)** — a monolithic database is typical and reduces inter-module communication because data is shared.
- **Per-module databases** — independent modules with specific functions can own their own database with contextual data, even within a monolithic deployment.
- **Cloud fit is limited** — modular monoliths can deploy to the cloud (especially small ones) but the monolithic nature limits use of on-demand provisioning. Smaller systems can still use cloud services like file storage, database, and messaging.

## 5. Common Risks

- **Getting too big** — the primary risk with any monolith. Warning signs: changes take too long, changes in one area unexpectedly break others, team members get in each other's way, and startup time grows.
- **Too much code reuse** — over-sharing across modules blurs boundaries and produces an *unstructured monolith*: monolithic code so highly interdependent it cannot be unraveled.
- **Too much intermodule communication** — ideally modules are independent and self-contained. Heavy intercommunication signals ill-defined domains; redefine the domains before adding more workflows.

## 6. Governance

- **Module compliance** — the primary artifact is a *module* (a directory/namespace/package). Automate checks that every namespace starts with one of the system's defined modules (e.g., `com.orderentry.orderplacement`, `com.orderentry.inventorymanagement`, etc.); alert on stragglers.
- **Tooling** — ArchUnit (Java), ArchUnitNet/NetArchTest (.NET), PyTestArch (Python), TSArch (TypeScript/JavaScript).
- **Per-module validation** — works cleanly with monolithic structure (single repo); modular structure makes it harder because modules may live in separate repos and must be tested individually.
- **Limit total dependencies** — automate a coupling-points cap per module (e.g., total incoming + outgoing references ≤ 5) to keep interdependencies low.
- **Restrict specific pairs** — ArchUnit can forbid one module from accessing another (e.g., `OrderPlacement` must not access `Shipping`) using `noClasses().that().resideInAPackage(...).should().accessClassesThat().resideInAPackage(...)`.

## 7. Team Topology Considerations

- **Best fit: domain-aligned teams** — works best when teams align by domain (cross-functional teams with specialization), so a domain feature can be delivered end-to-end by one team. Teams organized by technical category (UI, backend, DB) struggle here because every domain change requires cross-team coordination.
- **Stream-aligned teams** — own end-to-end flow; matches the self-contained shape.
- **Enabling teams** — high modularity lets specialists add or experiment with modules with minimal impact on existing ones.
- **Complicated-subsystem teams** — each module's specific role (e.g., `PaymentProcessing`) suits independent specialist focus.
- **Platform teams** — benefit from the modularity by sharing common tools, services, APIs, and tasks.

## 8. Style Characteristics

| Characteristic | Rating |
|---|---|
| Overall cost | 5 stars |
| Simplicity | 5 stars |
| Deployability | 2 stars |
| Elasticity | 1 star |
| Evolutionary | 3 stars |
| Fault tolerance | 1 star |
| Modularity | 4 stars |
| Performance | 3 stars |
| Reliability | 3 stars |
| Scalability | 1 star |
| Testability | 2 stars |

- **Domain-partitioned with quantum 1** — application logic is partitioned into modules; monolithic deployment yields an architectural quantum of 1.
- **Strengths: cost, simplicity, modularity** — monolithic nature avoids distributed complexity; modularity comes from separation of concerns across domain modules.
- **Deployability and testability (2 stars)** — slightly higher than layered thanks to modularity, but still hampered by monolithic ceremony, deployment risk, and incomplete testing.
- **Elasticity and scalability (1 star)** — monolithic deployment limits both; selective scaling demands complex techniques (multithreading, internal messaging) the style isn't built for.
- **Fault tolerance and availability** — monolithic deployment means one out-of-memory takes down everything; high MTTR (minutes to start up) hurts availability.

## 9. When to Use and When Not to Use

- **When to use** — tight budget/time; new systems where direction is unclear (start here, then move to service-based or microservices later); domain-focused, cross-functional teams; majority of changes are domain-based (e.g., adding wishlist expiration); teams practicing DDD.
- **When not to use** — when the system requires high scalability, elasticity, availability, fault tolerance, responsiveness, or performance; when the majority of changes are technical (replacing UI or DB technology repeatedly), since these ripple through every domain module — in that case prefer the layered style.

## 10. Examples and Use Cases: EasyMeals

- **EasyMeals scenario** — a small neighborhood delivery restaurant. No high scalability/responsiveness needs and limited budget make modular monolith a good fit.
- **Modules:**

```
com.easymeals.placeorder
com.easymeals.payment
com.easymeals.prepareorder
com.easymeals.delivery
com.easymeals.recipes
com.easymeals.inventory
```

- **`PlaceOrder` module** — view menu, select items, capture customer/payment info, submit order. Components: `menu`, `shoppingcart`, `customerdata`, `paymentdata`, `checkout`.
- **`PaymentProcessing` module** — applies payment for credit cards, debit cards, PayPal; modularity makes adding new payment types (e.g., loyalty points) easy. Components: `creditcard`, `debitcard`, `paypal`.
- **`PrepareOrder` module** — displays the order to kitchen staff and marks it ready. Components: `displayorder`, `ready`.
- **`Delivery` module** — assigns a delivery person, records issues (aggressive dog, customer not home), marks completion. Components: `assign`, `issues`, `complete`.
- **`Recipes` module** — kitchen and management maintain menu items and ingredients/measurements. Components: `view`, `maintenance`.
- **`IngredientsInventory` module** — most complex; uses an AI component to forecast sales volume and automate weekly procurement. Components: `maintenance`, `forecasting`, `ordering`, `suppliers`, `invoices`.
