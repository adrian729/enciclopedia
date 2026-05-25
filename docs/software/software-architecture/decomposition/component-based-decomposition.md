# Component-Based Decomposition

> *The Hard Parts* Ch 5 is the spine of this page — six sequenced refactoring patterns that turn a structured monolith into a service-based architecture, each with its own **fitness function** for governance. The Sysops Squad refactor is worked end-to-end across the chapter and is preserved here because it's where the patterns earn their keep. *Fundamentals* Ch 8 (Component-Based Thinking) is the upstream cross-reference: it covers *how to identify components in the first place* — Workflow vs. Actor/Action, the Entity Trap, refining components via assigned user stories and architecture characteristics. *The Hard Parts* assumes you already have components and shows how to refactor toward services. The two books interlock: read *Fundamentals* Ch 8 to *build* components, then read this page to *extract* them.

## Table of Contents

- [1. From Components to Services](#1-from-components-to-services)
- [2. Pattern 1 — Identify and Size Components](#2-pattern-1--identify-and-size-components)
- [3. Pattern 2 — Gather Common Domain Components](#3-pattern-2--gather-common-domain-components)
- [4. Pattern 3 — Flatten Components](#4-pattern-3--flatten-components)
- [5. Pattern 4 — Determine Component Dependencies](#5-pattern-4--determine-component-dependencies)
- [6. Pattern 5 — Create Component Domains](#6-pattern-5--create-component-domains)
- [7. Pattern 6 — Create Domain Services](#7-pattern-6--create-domain-services)
- [8. The Elephant Migration Anti-Pattern](#8-the-elephant-migration-anti-pattern)
- [Sources](#sources)

## 1. From Components to Services

A **component** is a collection of classes inside a *leaf-node* namespace that performs a specific function — `ss.ticket.assign`, `ss.notification`, `ss.customer.billing.payment`. Components are the architectural unit *Fundamentals* Ch 8 identifies through the Workflow or Actor/Action approach; *The Hard Parts* picks them up after that work is done and adds a structural rule:

> **Build services from components, not classes.** When migrating a monolith to a distributed architecture, the unit of extraction is the component, not the class.

The six patterns share a sequence and a target. The target is a **service-based architecture** — a hybrid distributed style with separately deployed coarse-grained domain services sharing one database. Service-based architecture is useful as a final destination or as a stepping-stone to microservices; the patterns choose it as a first stop because:

- It defers data decomposition (Ch 6, see [Data Decomposition](decomposition/data-decomposition.md)).
- It doesn't require operational automation or containerization — services can ship as the same EAR/WAR/Assembly as before.
- It's a purely technical move; no organizational change is usually needed.
- It exposes which domains genuinely *need* finer microservice granularity (see [Service Granularity](decomposition/service-granularity.md)) and which can stay coarse.

Hard Parts works the **Sysops Squad** scenario through all six patterns, labeled inline so the abstract pattern and the concrete refactor stay aligned.

## 2. Pattern 1 — Identify and Size Components

### 2.1. Pattern

Catalog every component in the codebase and resize outliers. Oversized components couple to too many others, are harder to break apart, and pull modularity down across the system.

The sizing metric is **statements** within all source files of the namespace — *not* lines of code, file count, or class count, all of which vary by coding style. Statements are language-defined (semicolon-terminated in Java, C, C++, C#, Go, JavaScript; newline-terminated in F#, Python, Ruby), so the metric is comparable across the codebase. The target distribution is components within one to two standard deviations of the mean, with roughly even share of total code.

The **component inventory** has five columns: Component name, Component namespace, Percent (statements / total statements), Statements, Files. `Files` is informational — an 18,409-statement component with only 2 files signals classes need to be refactored into smaller, more contextual ones, even if the component itself is fine.

When a component is oversized, apply functional decomposition or DDD to identify subdomains within it and split accordingly. If no clear subdomains exist, leave it alone — splitting for its own sake just shifts the coupling.

### 2.2. Fitness functions

- **Maintain component inventory** — walks the directory tree, diffs the namespace list against a stored prior list, alerts on added or removed components. Surfaces silent additions during ongoing development.
- **No component shall exceed `<percent>` of the codebase** — alerts when a component's statement share crosses a threshold. Rule of thumb: ≈30% for a ≈10-component codebase, ≈10% for a ≈50-component codebase.
- **No component shall exceed `<n>` standard deviations from the mean component size** — typically 3σ.

### 2.3. Sysops Squad

Reporting (`ss.reporting`) was **33% of the 82,931-statement codebase**, while every other component sat at 2–9%. Sydney split it into Reporting Shared plus three functional reports — Ticket Reports (`ss.reporting.tickets`), Expert Reports (`ss.reporting.experts`), Financial Reports (`ss.reporting.financial`). All components now sit between 2% and 9%; `ss.reporting` becomes a *subdomain* rather than a component.

## 3. Pattern 2 — Gather Common Domain Components

### 3.1. Pattern

Find domain logic *duplicated* across components and consolidate it into one shared component. This reduces the number of duplicate services that would otherwise appear in the future distributed architecture.

A critical distinction:

| Shared functionality | Examples | This pattern? |
|---|---|---|
| **Domain** (common to *some* processes) | Notification, data formatting, validation | **Yes** — consolidate here. |
| **Infrastructure** (common to *all* processes) | Logging, metrics, security, auth | No — handled by the [reuse patterns](foundations/components-and-quantum.md) (shared library, sidecar/mesh). |

Detection signals: shared classes used across components (e.g., `SMTPConnection` referenced from five namespaces) or recurring leaf-node names (`ticket.audit`, `billing.audit`, `survey.audit` all writing rows to an audit table). The consolidated logic becomes either a shared *service* or a shared *library*; the choice is the reuse trade-off — see [Components and Quantum](foundations/components-and-quantum.md).

### 3.2. Fitness functions

- **Find common names in leaf nodes** — flags components whose leaf nodes match across the tree, with an exclusion file for known-good repeats (`.calculate`, `.validate`).
- **Find common code across components** — flags source files referenced from multiple components, again with an exclusion file for known false positives.

### 3.3. Sysops Squad

Three notification components — `ss.customer.notification`, `ss.ticket.notify`, `ss.survey.notify` — all sent information to a customer. Before consolidating, Addison checked aggregate coupling:

| Before | CA | Used by |
|---|---|---|
| Customer Notification | 2 | Billing Payment, Support Contract |
| Ticket Notify | 2 | Ticket, Ticket Route |
| Survey Notify | 1 | Survey |

After consolidation into a single `ss.notification` component: CA = 5 (Billing Payment, Support Contract, Ticket, Ticket Route, Survey). Aggregate incoming coupling was unchanged, so the consolidation was approved. **Always check that consolidation doesn't make aggregate coupling worse** — otherwise the "shared component" becomes a hub that drags every domain change through itself.

## 4. Pattern 3 — Flatten Components

### 4.1. Pattern

Ensure source code lives *only in leaf-node namespaces*. Non-leaf nodes become subdomains; code stranded in them is an *orphan*.

| Term | Meaning |
|---|---|
| **Component** | Classes grouped within a *leaf-node* namespace, performing a specific function. |
| **Root namespace / subdomain** | A namespace that has been extended by another (`ss.survey` is a root namespace because `ss.survey.templates` extends it). |
| **Orphaned classes** | Classes living in a root namespace; they belong to no definable component because the node has been extended. |

Two flattening directions:

- **Pull leaf-node code *down* into the root** (collapse). Use when the leaf node has no good reason to exist as a separate component.
- **Push the orphaned code *up* into new leaf nodes** (expand) by applying functional decomposition or DDD.

Shared utilities or abstract classes that legitimately sit in a root namespace should move into a uniquely named leaf node like `.sharedcode` or `.commoncode`. Two derived metrics follow:

- **Percent of code in `.sharedcode` namespaces** — high values predict the decomposition will produce too many shared libraries.
- **Number of `.sharedcode` components** — predicts the count of shared libs/services after migration.

### 4.2. Fitness function

- **No source code should reside in a root namespace** — walks the namespace tree, alerts whenever a non-leaf node contains source files.

### 4.3. Sysops Squad

**Ticket** (`ss.ticket`, 45 orphaned classes) was *raised* into a subdomain. Sydney split the orphans into three new leaf nodes: `ss.ticket.shared`, `ss.ticket.maintenance`, `ss.ticket.completion`. The existing `ss.ticket.assign` and `ss.ticket.route` were kept.

**Survey** (`ss.survey` + `ss.survey.templates`) was *flattened down*. Skyler, the original author, admitted there was no real reason to separate templates ("it just seemed like a good idea at the time"); the 7 template classes moved into `ss.survey` and `ss.survey.templates` was removed.

## 5. Pattern 4 — Determine Component Dependencies

### 5.1. Pattern

Analyze incoming and outgoing dependencies *between components* — not between classes — to predict the resulting service dependency graph and answer three migration questions:

1. Is it feasible to break apart the existing monolith?
2. What is the rough overall level of effort?
3. Will it be a *refactor* or a *rewrite*?

A **component dependency** is formed when a class in one namespace invokes a class in another namespace. `CustomerSurvey` (`ss.survey`) calling `CustomerNotification.send` (`ss.notification`) creates an efferent dependency from Survey onto Notification. Internal class spaghetti within one component does not count.

The sizing heuristic — the *CIO question*, since it's what you show a sponsor — is **golf ball / basketball / airliner**:

| Visual | Effort | Migration type |
|---|---|---|
| Few dependency lines between components | **Golf ball** — feasible | Refactor (move existing code into separately deployed services). |
| Many dependencies, dense on one side | **Basketball** — maybe | Combination of refactor and rewrite. |
| Dense matrix everywhere | **Airliner** — turn around and run | Total rewrite. |

A refactor opportunity often emerges from this view: splitting a component can lower its coupling. If component A has CA = 20 but only 14 dependents need a small slice of its functionality, splitting A into A1 (the small slice, CA = 14) and A2 (the rest, CA = 6) reduces coupling pressure on the larger component. **Total coupling:** `CT = CA + CE`.

### 5.2. Fitness functions

- **No component shall have more than `<n>` total dependencies** — pseudocode alerts when `CA + CE > 15`. Can be split into separate functions for incoming-only and outgoing-only thresholds.
- **`<some component>` should not have a dependency on `<another component>`** — one function per restriction. ArchUnit example: `ss.ticket.maintenance` must not access classes in `ss.expert.profile`.

### 5.3. Sysops Squad

The IDE-generated dependency diagram initially looked discouraging — Notification (a shared component) had the most dependencies, and Ticketing/Reporting had heavy intra-domain coupling. Addison filtered out the Ticketing and Reporting shared components (Ticket Shared, Reporting Shared) on the reasoning that their shared code is mostly compile-based class references and would likely be implemented as **shared libraries** rather than services. With those filtered, dependencies were minimal and the codebase was confirmed a *golf ball* — a good decomposition candidate.

## 6. Pattern 5 — Create Component Domains

### 6.1. Pattern

Group components into logical **domains** so coarse-grained domain services can be created later. Service-to-component is one-to-many: each service ships one domain's worth of components.

Domains live in the namespace. `ss.customer.billing.payment.MonthlyBilling` reads as *domain* `customer`, *subdomain* `billing`, *component* `payment`, *class* `MonthlyBilling`. Older monoliths usually predate DDD, so namespaces must be rewritten to express domains: Billing Payment, Billing History, Customer Profile, and Support Contract are all customer-related, but their original namespaces (`ss.billing.payment`, `ss.billing.history`, `ss.customer.profile`, `ss.supportcontract`) don't say so. The fix is to normalize them under `ss.customer.*`.

### 6.2. Fitness function

- **All namespaces under `<root>` should be restricted to `<list of domains>`** — ArchUnit example restricts an application to only `ss.ticket`, `ss.customer`, and `ss.admin` domains; alerts on any new domain that appears.

### 6.3. Sysops Squad

Five domains identified with product owner Parker:

| Domain | Namespace | Contents |
|---|---|---|
| Ticketing | `ss.ticket` | Ticket processing, customer surveys, knowledge base |
| Reporting | `ss.reporting` | All reporting |
| Customer | `ss.customer` | Customer profile, billing, support contracts |
| Admin | `ss.admin` | User and Sysops Squad expert maintenance |
| Shared | `ss.shared` | Login, notification |

Sample renames: KB Maint `ss.kb.maintenance` → `ss.ticket.kb.maintenance`; Survey `ss.survey` → `ss.ticket.survey`; Billing Payment `ss.billing.payment` → `ss.customer.billing.payment`; Support Contract `ss.supportcontract` → `ss.customer.supportcontract`; Login → `ss.shared.login`; Notification → `ss.shared.notification`; Expert Profile `ss.expert.profile` → `ss.admin.experts`; User Maintenance `ss.users` → `ss.admin.users`. Reporting components were already aligned.

## 7. Pattern 6 — Create Domain Services

### 7.1. Pattern

Physically extract each component domain into a separately deployed **domain service**, producing a service-based architecture: UI talking to coarse-grained domain services over a single shared monolithic database.

> **Important sequencing rule** — do *not* apply this pattern until *all* component domains have been identified and refactored. Every reclassification of a component into a different domain otherwise forces another modification to an already-extracted service.

Going to service-based architecture first (rather than straight to microservices) gives the team time to learn each domain before deciding whether to split further. Skipping that step forces simultaneous handling of data decomposition, distributed workflows, distributed transactions, operational automation, and containerization — the classic *big ball of distributed mud* failure mode.

### 7.2. Fitness function

- **All components in `<some domain service>` should start with the same namespace** — one function per service. ArchUnit example: every class in the Ticket domain service must reside in `..ss.ticket..`.

### 7.3. Sysops Squad

Extract each component domain (Ticketing, Reporting, Customer, Admin, Shared) into its own deployment unit; rewire the UI to reach each service remotely. The result is five separately deployed domain services backed by the original shared database — the first stage of a distributed Sysops Squad.

Next steps live elsewhere: [Data Decomposition](decomposition/data-decomposition.md) for breaking apart the shared database; [Service Granularity](decomposition/service-granularity.md) for deciding which domain services should split further into fine-grained microservices.

## 8. The Elephant Migration Anti-Pattern

> **Elephant Migration Anti-Pattern** — "eat the elephant one bite at a time": pick whatever feature seems easy and pull it out. Without a holistic view it produces a big ball of distributed mud.

The six patterns are deliberately a *sequence*, not a menu. *Identify and Size* must come before *Determine Dependencies* (you can't measure dependencies of components that aren't sized correctly). *Create Component Domains* must come before *Create Domain Services* (otherwise reclassifying a component forces you to modify an already-extracted service). The sequencing protects against the seat-of-the-pants migration the authors warn about: it gives a controlled, incremental path with a fitness function at every step. Apply the patterns in order, govern the result with the fitness functions, and the migration is auditable rather than aspirational.

## Sources

- [The Hard Parts Ch 5: Component-Based Decomposition Patterns](software/software-architecture/books/software-architecture-the-hard-parts/ch05_component_decomposition_patterns.md) (primary — the six patterns, their fitness functions, the Sysops Squad refactor)
- [The Hard Parts Ch 4: Architectural Decomposition](software/software-architecture/books/software-architecture-the-hard-parts/ch04_architectural_decomposition.md) (secondary — Elephant Migration Anti-Pattern, the choice of component-based decomposition over tactical forking)
- [Fundamentals Ch 8: Component-Based Thinking](software/software-architecture/books/fundamentals-of-software-architecture/ch08_component_based_thinking.md) (cross-reference — the upstream component-identification process: Workflow vs. Actor/Action, Entity Trap, refining via user stories and characteristics)


<!-- prev-next-nav -->

---

← [When to Decompose](software/software-architecture/decomposition/when-to-decompose.md) | [Tactical vs. Strategic Decomposition](software/software-architecture/decomposition/tactical-vs-strategic.md) →
