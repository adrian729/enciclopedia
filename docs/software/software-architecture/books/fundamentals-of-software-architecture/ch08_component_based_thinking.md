# Ch 8: Component-Based Thinking

## Table of Contents

- [1. Defining Logical Components](#1-defining-logical-components)
- [2. Logical Versus Physical Architecture](#2-logical-versus-physical-architecture)
- [3. The Component Identification Workflow](#3-the-component-identification-workflow)
- [4. Approaches to Identifying Core Components](#4-approaches-to-identifying-core-components)
- [5. Refining Components](#5-refining-components)
- [6. Component Coupling](#6-component-coupling)
- [7. The Law of Demeter](#7-the-law-of-demeter)
- [8. Case Study: Going, Going, Gone](#8-case-study-going-going-gone)

## 1. Defining Logical Components

- **Component vs. module** — Ch 3 defined a *module* as a collection of related code; this chapter focuses on the architectural facet of modularity, the **logical component**, the building block of a system.
- **Component-based thinking** — seeing the system as a set of logical components interacting to deliver business functions. This is the level at which the architect "sees" the system, not the class level.
- **House analogy** — rooms (kitchen, bedrooms, bathrooms, office) are the components of a house; major business functions (manage inventory, ship orders, process payments) are the components of a system. Each contains source code that implements its function.
- **Manifestation** — components live as namespaces or directory structures. Leaf nodes typically represent components; higher-level nodes represent domains and subdomains. Path `order_entry/ordering/payment` ⇒ `Payment Processing` component; `order_entry/processing/fulfillment` ⇒ `Order Fulfillment` component.
- **Logical architecture is what you read** by analyzing directories and namespaces.

## 2. Logical Versus Physical Architecture

| | Logical architecture | Physical architecture |
|---|---|---|
| **Shows** | Logical components, their interactions, actors, optional repositories | Services, UIs, databases, deployment artifacts |
| **Independent of style** | Yes | No — should reflect a specific architecture style (microservices, layered, EDA, etc.) |
| **Question answered** | What does the system do? How is functionality demarcated? How do parts interact? | How is it deployed? Where does code run? |

- **Don't skip logical architecture.** Many architects start straight from the physical view, but a physical architecture doesn't always show *where* functionality lives or how it fits together (e.g., payment processing might be split across multiple services). Skipping logical architecture leaves teams without guidance on monolith-vs-distributed decisions or code organization, producing unstructured systems that are hard to maintain, test, and deploy.
- **Style is a separate decision** — when designing a logical architecture, the architect may not yet have decided whether components ship as one deployment unit or many.

## 3. The Component Identification Workflow

Component identification is iterative: produce candidates, then refine via a feedback loop.

1. **Identify initial core components** — best guess based on major workflows or actions.
2. **Assign user stories or requirements** — fill the empty buckets with concrete responsibilities.
3. **Analyze roles and responsibilities** — check cohesion; split components that drift toward kitchen-sinks.
4. **Analyze architectural characteristics** — characteristics like scalability, fault tolerance, or agility may force a component to be split or combined.
5. **Restructure components** — apply the analysis; loop back.

- **Greenfield or maintenance** — the same workflow applies to new systems and to feature changes (e.g., adding store pickup to an order-entry system).
- **Don't try to be perfect first time.** Iterating beats over-engineering at the moment of least information.

## 4. Approaches to Identifying Core Components

- **Empty-bucket framing** — initial components are placeholders named for their proposed role; they have no responsibility until user stories are assigned.

### 4.1. Workflow Approach

- **Use major happy-path workflows** to derive components. For an order-entry system:

| Step | Component |
|---|---|
| User browses catalog | `Item Browser` |
| User places an order | `Order Placement` |
| User pays for the order | `Order Payment` |
| Email user with order details | `Customer Notification` |
| Prepare the order | `Order Fulfillment` |
| Ship the order | `Order Shipment` |
| Email user that order has shipped | `Customer Notification` (reused) |
| Track shipment | `Order Tracking` |

- **Not every step yields a new component** — `Customer Notification` covers two workflow steps. Model only the major workflows.

### 4.2. Actor/Action Approach

- **Useful when multiple actors exist.** The system itself is always an actor (for automated functions like billing or inventory replenishment).
- **Order-entry actors** — *customer*, *order packer*, *system*. Map major actions to components:
  - **Customer** — `Item Search`, `Item Details`, `Order Placement`, `Order Cancel`, `Customer Registration`, `Customer Profile`.
  - **Order packer** — `Order Fulfillment` (select box, mark ready), `Order Shipment`.
  - **System** — `Inventory Management`, `Supplier Ordering`, `Order Payment`.
- **Tends to generate more components** than the Workflow approach, depending on how many workflows are modeled.

### 4.3. The Entity Trap (Antipattern)

- **Entity Trap** — naming components after entities (`Customer Manager`, `Item Manager`, `Order Manager`) and dumping all related functionality into them. The authors caution against this approach.
- **Ambiguous names** — "what does `Order Manager` do?" yields the useless answer "manages orders." Suffixes like `Manager`, `Supervisor`, `Controller`, `Handler`, `Engine`, `Processor` are warning signs. Compare with `Validate Order`, which is unmistakable.
- **Dumping ground** — all order functionality (validation, placement, history, fulfillment, shipping, tracking) collapses into one entity component, mirroring the "kitchen sink" utility classes every developer has written.
- **Coarse granularity hurts** — components become hard to maintain, test, and deploy.
- **CRUD escape hatch** — if the system genuinely is entity-based and only does CRUD, it doesn't need an architecture; use a CRUD framework or a low-code/no-code tool instead.

## 5. Refining Components

### 5.1. Assigning User Stories

- **Iterative filling.** Three example user stories applied to four components (`Order Placement`, `Order Fulfillment`, `Order Shipment`, `Inventory Management`):
  - *Validate the order* ⇒ `Order Placement` (the component the customer interacts with).
  - *Determine box size* ⇒ `Order Fulfillment`.
  - *Email customer on each status change* ⇒ no existing component fits all three trigger points (placed, ready, shipped); creating a new `Customer Notification` component avoids replicating code across three directories. The placement, fulfillment, and shipment components now communicate with it.

### 5.2. Analyzing Roles and Responsibilities

- **Check cohesion** — how a component's operations interrelate. A bloated `Order Placement` component asked to validate, display cart, determine shipping address, collect payment info, generate order ID, apply payment, adjust inventory, and email the customer is doing too much.
- **Conjunction sniff test** — when the role statement uses *and*, *also*, *in addition*, *as well as*, or piles up commas, the component likely needs splitting.
- **Directory implication** — all `Order Placement` code lives under one namespace (e.g., `com.app.order.placement`); too much functionality means too much code in one directory. Splitting payment, inventory, and notification into their own components yields clearer responsibility:
  - `Order Placement` — validate, display cart, determine shipping address, collect payment info, generate order ID.
  - `Payment Processing` — apply payment.
  - `Inventory Management` — adjust inventory counts.
  - `Customer Notification` — email order summary.

### 5.3. Analyzing Architectural Characteristics

- **Characteristics can force a split.** Scalability, reliability, availability, fault tolerance, elasticity, and **agility** can change a component's size.
- **Different load profiles ⇒ different components.** If one user-input path serves hundreds of concurrent users and another serves a handful, a single user-interaction component is wrong even if the functional view says one suffices.
- **Sequencing** — characteristics analysis happens after the architect has identified the system's most important architecture characteristics.

### 5.4. Restructuring

- **Continual iteration in collaboration with developers.** No initial decomposition survives contact with edge cases; deeper familiarity with the application reveals where behaviors should really live. Expect frequent restructuring across the lifecycle of any system, not just greenfield ones.

## 6. Component Coupling

- **Definition** — components are *coupled* when they communicate or when a change to one might impact the other. The more coupling, the harder maintenance and testing become.

### 6.1. Static Coupling

- **Static coupling** — components communicating synchronously. Two flavors:
  - **Afferent coupling (CA)** — incoming / fan-in; how many other components depend on this one. `Customer Notification` called by both `Order Placement` and `Order Shipment` ⇒ CA = 2.
  - **Efferent coupling (CE)** — outgoing / fan-out; how many other components this one depends on. `Order Placement` calling `Order Fulfillment` ⇒ CE = 1.

### 6.2. Temporal Coupling

- **Temporal coupling** — non-static dependencies based on timing or transactions (single units of work). `Order Placement` must run before `Order Shipment`. Hard to detect with current tooling; usually surfaced via design documents or error conditions.

## 7. The Law of Demeter

- **Law of Demeter (Principle of Least Knowledge)** — a technique for loose coupling: a component or service should have limited knowledge of other components or services. In Greek mythology, the goddess Demeter produced all the world's grain but had no idea what people did with it — effectively decoupled from the rest of the world.
- **Knowledge is coupling.** Even when a component lacks the *responsibility* to perform an action, holding the *knowledge* that it must occur tightens coupling.
- **Worked example — before applying.** `Order Placement` knows it must: (1) decrement inventory via `Inventory Management`, (2) reorder stock from `Supplier Ordering` if low, (3) adjust the price via `Item Pricing` when supply is low, (4) email the customer via `Email Notification`. Four pieces of knowledge ⇒ tight coupling.
- **Worked example — after applying.** Move the "if stock is low, reorder and reprice" knowledge into `Inventory Management`. `Order Placement`'s knowledge shrinks; it no longer needs to know about supplier ordering or item pricing.
- **Caveat — coupling is redistributed, not eliminated.** Applying the law reduced `Order Placement`'s coupling but increased `Inventory Management`'s. The system-wide coupling level may not change; what improves is the locality of change impact.

## 8. Case Study: Going, Going, Gone

- **Default to Actor/Action** when the team has no special constraints.
- **Three actors** — *bidder*, *auctioneer*, *system*. Actions:
  - **Bidder** — view live video stream, view live bid stream, place a bid.
  - **Auctioneer** — enter live bids into system, receive online bids, mark item as sold.
  - **System** — start auction, make payment, track bidder activity.
- **Initial components:**

| Component | Responsibility |
|---|---|
| `Video Streamer` | Streams the live auction video to users |
| `Bid Streamer` | Streams bids to users as they occur (read-only view alongside `Video Streamer`) |
| `Bid Capture` | Captures bids from auctioneer and bidders |
| `Bid Tracker` | Tracks bids; system of record |
| `Auction Session` | Starts an auction; on win, triggers payment, resolution, and next-item notification |
| `Payment` | Third-party payment processor for credit cards |

- **Refinement via architectural characteristics.** The single `Bid Capture` component handles both auctioneer and bidders, but their characteristics differ:
  - **Bidders** — need elasticity and scalability (potentially thousands).
  - **Auctioneer** — needs reliability (no dropped connections) and availability (the system staying up); a dropped bidder is bad, a dropped auctioneer is disastrous.
- **Resulting split** — `Bid Capture` (bidders) and `Auctioneer Capture` (auctioneer). `Auctioneer Capture` connects to `Bid Streamer` (to push live bids to online bidders) and `Bid Tracker` (which now unifies the auctioneer's single stream with the bidders' many streams).
- **No single right design.** This is *one* viable decomposition. More requirements (account registration, payment administration) will surface and reshape it.
- **Least worst trade-offs.** As an architect, don't obsess over finding the "one true design." Assess trade-offs between design decisions as objectively as possible and choose the one with the **least worst** set.
