# Ch 5: Component-Based Decomposition Patterns

## Table of Contents

- [1. The pattern set](#1-the-pattern-set)
- [2. Identify and Size Components](#2-identify-and-size-components)
- [3. Gather Common Domain Components](#3-gather-common-domain-components)
- [4. Flatten Components](#4-flatten-components)
- [5. Determine Component Dependencies](#5-determine-component-dependencies)
- [6. Create Component Domains](#6-create-component-domains)
- [7. Create Domain Services](#7-create-domain-services)
- [8. Sysops Squad saga: end state](#8-sysops-squad-saga-end-state)

## 1. The pattern set

- **Purpose** — a sequenced set of refactoring patterns that turn a structured monolith into a service-based architecture in a controlled, incremental way. Each pattern has three sections: pattern description, fitness functions for governance, and a Sysops Squad illustration.
- **The six patterns and their roles**:

| # | Pattern | Role |
|---|---------|------|
| 1 | **Identify and Size Components** | Catalog components and resize outliers. |
| 2 | **Gather Common Domain Components** | Consolidate duplicated business-domain logic. |
| 3 | **Flatten Components** | Push code into leaf-node namespaces; eliminate orphaned classes. |
| 4 | **Determine Component Dependencies** | Map component-to-component coupling; assess migration feasibility and effort. |
| 5 | **Create Component Domains** | Group components into logical domains via namespace alignment. |
| 6 | **Create Domain Services** | Physically extract each component domain into a separately deployed service. |

- **Architecture stories** — used throughout to record code refactoring that affects structure (distinct from user stories and from technical-debt stories). Example: *"As an architect, I need to decouple the payment service to support better extensibility and agility when adding additional payment types."*

## 2. Identify and Size Components

### 2.1. Pattern Description

- **Goal** — identify every component and resize ones that are too big or too small. Oversized components couple to too many others, are harder to break apart, and hurt modularity.
- **Sizing metric** — total **statements** within all source files of the namespace. Source-file count, class count, and lines of code are unreliable because programmers structure code differently. Statements are language-defined (semicolon-terminated in Java, C, C++, C#, Go, JavaScript; newline-terminated in F#, Python, Ruby).
- **Target distribution** — components should fall within one to two standard deviations of the mean component size, and the percentage of total code per component should be roughly even.
- **Inventory columns** — Component name, Component namespace, Percent (component statements / total statements), Statements, Files. *Files* is informational: a 18,409-statement component with only 2 files signals that classes need to be refactored into smaller, more contextual ones.
- **Resizing technique** — when a component is oversized, apply functional decomposition or DDD to identify subdomains within it and split accordingly. If no clear subdomains exist, leave it alone.

### 2.2. Fitness functions

- **Maintain component inventory** — walks the directory tree, diffs the namespace list against a stored prior list, and alerts on added or removed components.
- **No component shall exceed `<percent>` of the codebase** — alerts when a component's statement share crosses a threshold (e.g., 30% for ~10 components, 10% for ~50 components).
- **No component shall exceed `<n> standard deviations` from the mean component size** — pseudocode example uses 3 standard deviations.

### 2.3. Sysops Squad outcome

- **Finding** — Reporting (`ss.reporting`) was 33% of the 82,931-statement codebase, while every other component sat at 2–9%.
- **Refactor** — Sydney split Reporting into a Reporting Shared component plus three functional reports: Ticket Reports (`ss.reporting.tickets`), Expert Reports (`ss.reporting.experts`), and Financial Reports (`ss.reporting.financial`). After the split, all components sat between 2% and 9%, and `ss.reporting` became a subdomain rather than a component.

## 3. Gather Common Domain Components

### 3.1. Pattern Description

- **Goal** — find domain logic duplicated across components and consolidate it into a single shared component, reducing duplicate services in the future distributed architecture.
- **Domain vs infrastructure** — *domain* shared functionality is business processing common to *some* processes (notification, data formatting, validation). *Infrastructure* shared functionality is operational and common to *all* processes (logging, metrics, security). This pattern is about domain.
- **Detection signals** — shared classes used across components (e.g., `SMTPConnection` referenced from five different namespaces) or recurring leaf-node names (e.g., `ticket.audit`, `billing.audit`, `survey.audit` all writing rows to an audit table). Recurring auditing functionality could be consolidated into `ss.shared.audit`.
- **Output options** — consolidated logic can become either a shared *service* or a shared *library* compiled in (trade-offs covered in Chapter 8).

### 3.2. Fitness functions

- **Find common names in leaf nodes of component namespaces** — flags components whose leaf nodes match (with an exclusion file for known-good repeats like `.calculate` or `.validate`).
- **Find common code across components** — flags source files referenced from multiple components, with an exclusion file for known false positives.

### 3.3. Sysops Squad outcome

- **Finding** — three notification components (`ss.customer.notification`, `ss.ticket.notify`, `ss.survey.notify`) all sent information to a customer.
- **Coupling check before consolidation**:

| Component | Ca | Used by |
|-----------|----|---------|
| Customer Notification | 2 | Billing Payment, Support Contract |
| Ticket Notify | 2 | Ticket, Ticket Route |
| Survey Notify | 1 | Survey |

- **After consolidation** — single `Notification` component (`ss.notification`) with Ca = 5 (Billing Payment, Support Contract, Ticket, Ticket Route, Survey). Total incoming coupling for "notifying a customer" remained at 5; consolidation was approved because it didn't worsen the aggregate coupling.

## 4. Flatten Components

### 4.1. Pattern Description

- **Goal** — make sure source code lives only in *leaf-node* namespaces; non-leaf nodes become subdomains.
- **Component** — a collection of classes grouped within a *leaf node* namespace performing specific functionality.
- **Root namespace** — a namespace node that has been extended by another node (e.g., `ss.survey` is a root namespace because `ss.survey.templates` extends it). Also called a *subdomain*.
- **Orphaned classes** — classes that live in a root namespace; they belong to no definable component because the node has been extended. Example: `ss.survey` containing 5 classes while `ss.survey.templates` exists.
- **Two flattening directions** — either pull leaf-node code *down* into the root (collapse), or push the orphaned code *up* into new leaf nodes by applying functional decomposition / DDD (expand).
- **Shared orphaned code** — when shared utilities/abstract classes sit in a root namespace, move them into a uniquely named leaf node like `.sharedcode` or `.commoncode`. Two useful metrics follow: percentage of code in `.sharedcode` namespaces (high % signals decomposition will produce too many shared libraries) and number of `.sharedcode` components (predicts the count of shared libs/services after migration).

### 4.2. Fitness function

- **No source code should reside in a root namespace** — walks the namespace tree and alerts whenever a non-leaf node contains source files.

### 4.3. Sysops Squad outcome

- **Ticket** (`ss.ticket`, 45 orphaned classes) was *raised* into a subdomain. Sydney split the orphans into three new leaf-node components: `ss.ticket.shared`, `ss.ticket.maintenance`, `ss.ticket.completion`; existing `ss.ticket.assign` and `ss.ticket.route` stayed.
- **Survey** (`ss.survey` + `ss.survey.templates`) was *flattened down*. Skyler (the original author) admitted there was no real reason to separate templates ("It just seemed like a good idea at the time"); the 7 template classes moved into `ss.survey`, and `ss.survey.templates` was removed.

## 5. Determine Component Dependencies

### 5.1. Pattern Description

- **Goal** — analyze incoming and outgoing dependencies *between components* (not between classes) to predict the resulting service dependency graph and answer three migration questions:
  1. Is it feasible to break apart the existing monolithic application?
  2. What is the rough overall level of effort?
  3. Will it be a refactor or a rewrite?
- **Component dependency** — formed when a class in one namespace invokes a class in another namespace. Example: `CustomerSurvey` (`ss.survey`) calling `CustomerNotification.send` (`ss.notification`) creates an efferent dependency from Survey and an afferent dependency on Notification. Internal class spaghetti within one component does not count.
- **Sizing heuristic (the CIO question)** — *golfball / basketball / airliner*:

| Visual | Effort | Migration type |
|--------|--------|----------------|
| Few dependency lines between components | **Golf ball** — feasible | Refactor (move existing code into separately deployed services). |
| Many dependencies, dense on one side | **Basketball** — maybe | Combination of refactor and rewrite. |
| Dense matrix everywhere | **Airliner** — turn around and run | Total rewrite. |

- **Refactor opportunity** — splitting a component can lower its coupling. If component A has Ca = 20 but only 14 dependents need a small slice of its functionality, splitting A into A1 (the small slice, Ca = 14) and A2 (the rest, Ca = 6) reduces coupling pressure on the larger component.
- **Total coupling** — `CT = Ca + Ce`.

### 5.2. Fitness functions

- **No component shall have more than `<n>` total dependencies** — pseudocode alerts when `Ca + Ce > 15`. Can be split into separate fitness functions for incoming-only or outgoing-only thresholds.
- **`<some component>` should not have a dependency on `<another component>`** — one fitness function per restriction. Concrete ArchUnit example: `ss.ticket.maintenance` must not access classes in `ss.expert.profile`.

### 5.3. Sysops Squad outcome

- **First view** — the IDE-generated dependency diagram looked discouraging because Notification (a shared component) had the most dependencies, and Ticketing/Reporting also had heavy intra-domain coupling.
- **Filter** — Addison filtered out the Ticketing and Reporting shared components (Ticket Shared, Reporting Shared), reasoning that their shared code is mostly compile-based class references and would likely be implemented as shared libraries rather than services. With those filtered out, dependencies were minimal and the application was confirmed to be a good decomposition candidate.

## 6. Create Component Domains

### 6.1. Pattern Description

- **Goal** — group components into logical domains so coarse-grained domain services can be created later. Service-to-component is one-to-many.
- **Domains live in the namespace** — e.g., `ss.customer.billing.payment.MonthlyBilling` reads as domain `customer`, subdomain `billing`, component `payment`, class `MonthlyBilling`.
- **Refactoring is usually required** — older monoliths predate DDD, so namespaces must be rewritten to express domains. Example: Billing Payment, Billing History, Customer Profile, Support Contract are all customer-related but originally use mismatched namespaces (`ss.billing.payment`, `ss.billing.history`, `ss.customer.profile`, `ss.supportcontract`); the fix is to normalize them under `ss.customer.*`.

### 6.2. Fitness function

- **All namespaces under `<root>` should be restricted to `<list of domains>`** — ArchUnit example restricts an application to only `ss.ticket`, `ss.customer`, and `ss.admin` domains; alerts on any new domain.

### 6.3. Sysops Squad outcome

- **Five domains identified** with product owner Parker:

| Domain | Namespace | Contents |
|--------|-----------|----------|
| Ticketing | `ss.ticket` | Ticket processing, customer surveys, knowledge base |
| Reporting | `ss.reporting` | All reporting |
| Customer | `ss.customer` | Customer profile, billing, support contracts |
| Admin | `ss.admin` | User and Sysops Squad expert maintenance |
| Shared | `ss.shared` | Login, notification |

- **Sample renames** — KB Maint `ss.kb.maintenance` → `ss.ticket.kb.maintenance`; Survey `ss.survey` → `ss.ticket.survey`; Billing Payment `ss.billing.payment` → `ss.customer.billing.payment`; Support Contract `ss.supportcontract` → `ss.customer.supportcontract`; Login → `ss.shared.login`; Notification → `ss.shared.notification`; Expert Profile `ss.expert.profile` → `ss.admin.experts` (renamed to avoid an unnecessary Expert subdomain); User Maintenance `ss.users` → `ss.admin.users`. Reporting components were already aligned and unchanged.

## 7. Create Domain Services

### 7.1. Pattern Description

- **Goal** — physically extract each component domain into a separately deployed **domain service**, producing a service-based architecture (UI talking to coarse-grained domain services over a single shared monolithic database).
- **Why go to service-based architecture first** — gives the team time to learn each domain before deciding whether to break it into finer microservices. Skipping straight to microservices forces the team to handle data decomposition, distributed workflows, distributed transactions, operational automation, and containerization all at once.
- **Important sequencing rule** — do *not* apply this pattern until *all* component domains have been identified and refactored. Otherwise, every reclassification of a component into a different domain forces another modification to an already-extracted service.

### 7.2. Fitness function

- **All components in `<some domain service>` should start with the same namespace** — one fitness function per service. ArchUnit example: every class in the Ticket domain service must reside in `..ss.ticket..`.

### 7.3. Sysops Squad outcome

- **Migration plan** — extract each component domain (Ticketing, Reporting, Customer, Admin, Shared) into its own deployment unit and rewire the UI to reach each service remotely.
- **Result** — five separately deployed domain services backed by the original shared database, the first stage of a distributed Sysops Squad architecture.

## 8. Sysops Squad saga: end state

- **Outcome of the six patterns applied in sequence** — the Sysops Squad monolith became a service-based architecture: Ticketing, Reporting, Customer, Admin, and Shared services, each containing well-sized leaf-node components grouped under aligned namespaces.
- **What's next** — the team must still decompose the monolithic database (Chapter 6) and decide which domain services should split further into fine-grained microservices (Chapter 7). The authors note that "seat-of-the-pants" migrations rarely succeed; this structured pattern flow gives a controlled, incremental path.
