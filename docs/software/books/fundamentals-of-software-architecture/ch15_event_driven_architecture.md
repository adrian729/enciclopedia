# Ch 15: Event-Driven Architecture Style

## Table of Contents

- [1. Request-Based vs. Event-Based Models](#1-request-based-vs-event-based-models)
- [2. Topology: Broker vs. Mediator](#2-topology-broker-vs-mediator)
- [3. Broker Topology in Action](#3-broker-topology-in-action)
- [4. Events vs. Messages](#4-events-vs-messages)
- [5. Derived Events and Extensible Events](#5-derived-events-and-extensible-events)
- [6. Asynchronous Capabilities](#6-asynchronous-capabilities)
- [7. Broadcast Capabilities](#7-broadcast-capabilities)
- [8. Event Payload: Data-Based vs. Key-Based](#8-event-payload-data-based-vs-key-based)
- [9. Anemic Events and the Swarm of Gnats Antipattern](#9-anemic-events-and-the-swarm-of-gnats-antipattern)
- [10. Error Handling: Workflow Event Pattern](#10-error-handling-workflow-event-pattern)
- [11. Preventing Data Loss](#11-preventing-data-loss)
- [12. Request-Reply Messaging](#12-request-reply-messaging)
- [13. Mediator Topology](#13-mediator-topology)
- [14. Data Topologies](#14-data-topologies)
- [15. Cloud Considerations](#15-cloud-considerations)
- [16. Common Risks](#16-common-risks)
- [17. Governance](#17-governance)
- [18. Team Topology Considerations](#18-team-topology-considerations)
- [19. Style Characteristics](#19-style-characteristics)
- [20. Examples and Use Cases](#20-examples-and-use-cases)

## 1. Request-Based vs. Event-Based Models

- **Distributed asynchronous style** — *event-driven architecture (EDA)* is a popular distributed, asynchronous style for highly scalable, high-performance applications. It is built from decoupled event-processing components that asynchronously trigger and respond to events. It can be standalone or embedded inside other styles (e.g., event-driven microservices).
- **Architectural style, not just a pattern** — the authors maintain EDA is a primary style: entire systems can be built with it.
- **Request-based model** — most apps follow this: a *request orchestrator* (typically a UI, but sometimes an API layer, orchestration service, event hub, event bus, or integration hub) deterministically and synchronously routes a request to *request processors*. Example: "show me my last six months of orders."
- **Event-based model** — reacts to something that has happened. Example: an online-auction bid is not a request — it is an event the system must respond to by comparing concurrent bids and computing the highest bidder.

## 2. Topology: Broker vs. Mediator

- **Two topologies** — EDA has two main shapes: the **broker topology** (choreographed, default in this chapter) and the **mediator topology** (orchestrated, see [§13](#13-mediator-topology)).
- **Fire-and-forget asynchronous communication** — services trigger events; other services respond. The four primary architectural components are an **initiating event**, an **event broker**, an **event processor** (usually called a *service*), and a **derived event**.
- **Initiating event** — starts the entire flow (e.g., placing a bid, or updating a health-benefits system because an employee got married). It is sent to an **event channel** in the event broker.
- **Event processor** — accepts the initiating event, performs its task, then asynchronously advertises what it did by triggering a **derived event** to the broker. Other event processors respond to derived events and trigger their own. The flow ends when all processors are idle and all derived events have been handled.
- **Federated event broker** — typically *federated*: multiple domain-based clustered instances. Each holds the event channels (queues, topics, streams) for its event flow. Because of the decoupled, asynchronous, fire-and-forget broadcast nature, the broker uses topics, topic exchanges (AMQP), or streams with publish-and-subscribe.

## 3. Broker Topology in Action

- **Retail order-entry walkthrough** — `Order Placement` receives the `place order` initiating event, inserts the order, returns the order ID, then advertises an `order placed` derived event. Three event processors react in parallel:
  - **`Notification`** — emails the customer; advertises `email sent`. No one currently listens — *architectural extensibility*: a future `Email Analyzer` can be added with no change to existing processors.
  - **`Inventory`** — adjusts stock; advertises `inventory updated`. The `Warehouse` event processor responds, reorders if needed, and on replenishment triggers `stock replenished`. `Inventory` reacts but does **not** trigger another `inventory adjusted` to avoid a **poison event** — an event that loops forever between services.
  - **`Payment`** — charges the card; emits either `payment applied` or `payment denied`. `Notification` listens for the denial; `Order Fulfillment` listens for the applied event, picks/packs the order, then triggers `order fulfilled`. `Notification` and `Shipping` both listen; `Shipping` later emits `order shipped`, which `Notification` also handles.
- **Relay-race analogy** — once a processor "hands off" the baton (event), it is done with this event and free to react to others. Each event processor scales independently.

## 4. Events vs. Messages

- **Event** — broadcasts that *something has already happened* ("I just placed an order"). Typically requires no response and is broadcast to many processors via **publish-and-subscribe** (one-to-many) over a *topic*, *stream*, or notification service.
- **Message** — a command or query ("apply the payment for this order"; "give the shipping options"). Usually requires a response, almost always directed to a single processor via **point-to-point** (one-to-one) over a *queue* or messaging service.
- **EDA mostly uses events** — but uses messages occasionally (requesting data from another processor; the **mediator topology** uses messages to control event order).
- **Worked classification examples** — "Adventurous Air Flight 6557, turn left, heading 230 degrees" → message (command); "a cold front has moved into the area" → event; "OK, class, turn to page 145" → message (broadcasting a command does not turn it into an event); "Hi, everyone! Sorry I'm late for the meeting" → event.

## 5. Derived Events and Extensible Events

- **Derived event** — created and triggered by an event processor *after* the initiating event. A processor can trigger more than one.
- **Credit-card example** — a `creditcard charged` event triggers `Fraud Detection` (which emits two possible derived events: fraud detected vs. not detected — each meaningful to different downstream processors) and `Credit Limit` in parallel. `Credit Limit` produces three derived events: `limit okay` (payload may also carry remaining credit for downstream use), `limit warning` (notify customer), and `fatal limit exceeded` (consumed by `Notification`, `Decline Purchase`, and a marketing-driven `Extend Credit Limit`).
- **Extensible derived event** — even when no processor currently cares about an event, advertising it provides architectural extensibility: an `email sent` event allows a future `Email Analyzer` to be plugged in with no change to existing processors.

## 6. Asynchronous Capabilities

- **Responsiveness vs. performance** — asynchronous communication boosts *responsiveness* (time to acknowledge the user) but may not change *performance* (end-to-end work time). Posting a comment that takes 3,000 ms to validate: synchronous REST → 3,100 ms total wait; asynchronous messaging → 25 ms perceived wait, with the actual posting still taking 3,025 ms.
- **Trade-off: no synchronous failure path** — async loses the immediate guarantee that the work succeeded. Mitigation: notify the user via a separate channel when something is rejected (e.g., for stock trades or comments containing profanity).
- **Avoiding *Dynamic Quantum Entanglement*** — when two architectural quanta talk synchronously, they become entangled into a single quantum. Example: `Portfolio Management` synchronously sending a trade order to `Trade Order` blocks waiting for a confirmation number, so both share the same architectural characteristics. Replacing the synchronous call with **asynchronous communication** (queue + separate reply channel) detangles them into two independent quanta — `Portfolio Management` can keep submitting orders even if `Trade Order` is unavailable.

## 7. Broadcast Capabilities

- **Semantic decoupling** — a processor can broadcast events without knowing who, if anyone, is listening or what they will do. Stock-ticker example: every new ticker price is broadcast, and many processors (trade analytics, buying, selling) react independently. The publisher has no knowledge of or dependency on the consumers' actions — *semantic decoupling*. Foundational to eventual consistency and complex event processing (CEP).

## 8. Event Payload: Data-Based vs. Key-Based

- **Two payload types** — event payloads can be **data-based** (full data) or **key-based** (only an identifier).
- **Data-based event payload** — carries everything downstream processors might need. Example: a 45-attribute, 500 KB `order_placed` event lets `Payment` and `Inventory Management` work without querying the database.
  - *Pros* — better performance, responsiveness, and scalability (no DB lookups); guarantees data availability even when consumers don't share the database (e.g., strict bounded contexts, database-per-service).
  - *Cons* — harder to maintain consistency with **multiple systems of record** (e.g., a customer corrects an order after submitting; in-flight events still carry the old values, and EDA can't easily control event timing); contract management and versioning headaches (JSON vs. XML, strict vs. loose, vendor MIME types in headers, deprecation strategies); **stamp coupling** — many processors share one big payload but each uses a slice (`Inventory` only needs `item_id` + `quantity` = ~30 bytes from a 500 KB payload), so any payload change can ripple to processors that don't care; and bandwidth (500 orders/sec × 500 KB = 250,000 KB/s vs. 15 KB/s if only the needed 30 bytes were sent — the third fallacy of distributed computing is that bandwidth is infinite).
  - **Consumer-driven contracts** — difficult to leverage in EDA because broadcast publishers do not always know which event processors will respond.
- **Key-based event payload** — carries only the context key (e.g., `{"order_id": "123"}`); each consumer queries the database for what it needs.
  - *Pros* — single system of record (better consistency under change); simple, rarely-changing contracts (loose schema-less JSON/XML); minimal stamp coupling and bandwidth.
  - *Cons* — every consumer hits the database (performance, responsiveness, scalability hit; risk of overwhelming the DB under high concurrency); useless if the data lives in another bounded context.
- **Trade-off summary** — performance & scalability vs. contract management & bandwidth utilization. Each event type can choose its own payload style. Choices live on a spectrum.

## 9. Anemic Events and the Swarm of Gnats Antipattern

- **Anemic event** — a derived event whose payload lacks the context downstream processors need to act. Example: a `profile_updated` event carrying only the customer ID — `Service 1` cannot tell what changed; `Service 2` cannot tell whether to do anything; `Service 3` lacks the prior values it needs. Avoid by including updated values *and* prior values (databases typically do not preserve them).
- **Swarm of Gnats antipattern** — about event *granularity*, not payload granularity. Two failure modes:
  - **Too coarse** — a single `fraud_checked` event forces all three downstream processors (`Credit Card Locking`, `Customer Notify`, `Purchase Profile`) to inspect the payload and decide whether to act. Better: emit two derived events (`fraud_detected` and `no_fraud_detected`) so each processor decides via *event identity*, not payload inspection.
  - **Too fine** — a profile update emits one event per changed field (bill-to address, ship-to address, phone), saturating the system with related-but-tiny events and making event flows unreadable. Better: bundle into a single `profile_updated` derived event with before/after data of all updated fields. Recommended heuristic: focus event granularity on the *outcome* of the processing or state change.

## 10. Error Handling: Workflow Event Pattern

- **Workflow Event pattern (reactive architecture)** — addresses both resiliency and responsiveness in async workflows. A consumer that hits an error immediately delegates the bad message to a **workflow processor (workflow delegate)** via async messaging and moves on to the next message; overall responsiveness is preserved.
- **Workflow processor responsibilities** — analyzes the failure (deterministic check, ML/AI anomaly detection), programmatically repairs the data, and resubmits to the original queue (the consumer treats it as a new message). When the processor cannot repair it, it routes the message to a queue feeding a knowledgeable person's dashboard for manual fixes.
- **Trading example** — a basket of `BUY,AAPL` trade orders includes one row `2WE35HF6DHF,BUY,AAPL,8756 SHARES`; the trailing `SHARES` causes `NumberFormatException` in `TradePlacement`. Without the pattern, no user is around to fix the async failure. With the pattern, `TradePlacement` delegates the bad row to a `Trade Placement Error` service, which strips `SHARES` and resubmits; meanwhile, the rest of the basket is processed without delay.
- **Out-of-sequence consequence** — repaired messages re-enter the queue out of order. When ordering matters (e.g., a `SELL IBM` must precede a `BUY AAPL` in the same brokerage account), buffer subsequent messages for the same context (account number) in a temporary FIFO queue and dequeue them only after the failed message is repaired.

## 11. Preventing Data Loss

- **Three places data can be lost** — between an event broker using AMQP (Amazon SNS, RabbitMQ, Solace, Azure Event Hubs) or JMS (with **durable subscribers**), or with Kafka as an event broker for streaming:
  1. Event processor `A` crashes before the broker acknowledges, or the broker crashes before another processor accepts.
  2. Event processor `B` accepts the event but crashes before processing.
  3. Event processor `B` cannot persist to the database due to a data error.
- **Mitigations (Event Forwarding pattern)**:
  - **Issue 1** — *persistent message queues* (broker stores the event on disk for **guaranteed delivery**) plus **synchronous send** (the producer blocks until the broker acknowledges persistence).
  - **Issue 2** — *client acknowledge mode* (vs. default *auto acknowledge mode*): the event remains in the queue, locked to the client ID, until the consumer confirms successful processing.
  - **Issue 3** — wrap persistence in an *ACID database commit*; **last participant support (LPS)** removes the event from the persisted queue only after all processing and persistence is confirmed.

## 12. Request-Reply Messaging

- **Pseudosynchronous communication** — when a processor needs an immediate response (e.g., a confirmation ID), EDA uses **request-reply messaging** (a.k.a. *pseudosynchronous communications*). Each event channel uses two queues: a *request* queue and a *reply* queue.
- **Correlation ID (CID) technique** — recommended; the producer sends a message (ID 124), then does a blocking wait on the reply queue with a *message selector* `CID == 124`. The consumer processes and emits a reply with `CID = 124`; the producer picks it up because the selector matches.
- **Temporary queue technique** — the producer creates (or auto-creates) a dedicated reply queue per request and sends its name in the `reply-to` header. No selector needed because the queue is private. Simpler, but creating/destroying a queue per request can significantly slow the broker under high concurrency — usually prefer the CID technique.

## 13. Mediator Topology

- **Choreographed vs. orchestrated** — the broker topology covered above is *choreographed*. The **mediator topology** is the *orchestrated* form, used when an architect wants more control over event processing. Components: initiating event, event queue, **event mediator**, event channels, event processors.
- **Messages, not events** — the mediator topology typically uses *messages* (commands like `ship_order`) instead of events that have happened (`order_shipped`).
- **Workflow ownership** — the mediator knows the steps; it accepts the initiating event, generates derived **messages**, and sends them point-to-point to dedicated channels (usually queues). Processors handle messages and reply to the mediator. They do **not** advertise their work to the rest of the system.
- **Multiple mediators** — most implementations use one mediator per domain (customer, order...) to avoid a single point of failure and improve throughput.
- **Mediator implementation choices**:
  - **Apache Camel, Mule ESB, Spring Integration** — simple error handling and orchestration with custom Java/C# routes.
  - **Apache ODE, Oracle BPEL Process Manager** — for conditional, dynamic, error-rich flows; based on Business Process Execution Language (BPEL) — powerful but complex, usually authored via GUI tools.
  - **BPM engines (jBPM)** — for long-running flows with human intervention (e.g., a senior trader manually approving a trade above a threshold).
- **Mediator delegation model** — classify events as simple, hard, or complex; route them all through a simple mediator (Apache Camel/Mule). Simple flows handle themselves; harder flows are forwarded to BPEL or BPM mediators.
- **Retail order-entry under mediator** — same scenario as the broker topology: the `Customer` mediator drives 5 sequential steps. Step 1: `create order` → `Order Placement`. Step 2 (parallel): `email customer`, `apply payment`, `adjust inventory` — wait for all three. Step 3 (parallel): `fulfill order`, `order stock`. Step 4: `ship order` + customer email. Step 5: final shipped notification. Mediator can pause and persist state on errors (e.g., expired credit card) and resume the workflow after the issue is fixed.
- **Mediator trade-offs** — gains workflow control, error handling, and recoverability; loses some performance and scalability (the mediator must scale and can become a bottleneck), processors are less decoupled, and complex dynamic processing is hard to model declaratively. Often a hybrid (mediator + choreographed) is used.

## 14. Data Topologies

- **Single monolithic database topology** — most common; every processor queries the central database directly without inter-service synchronous calls. Cons: single point of failure (one DB down = all processors down), the DB itself must scale, schema changes ripple across many processors, and the system collapses to a single architectural quantum.
- **Domain database topology** — group processors into domains, each owning a database. Better fault tolerance (an order-processing DB outage does not stop order placement; the `payment applied` channel acts as backpressure), scalability, and change control. Cost: queries that cross domains require **synchronous inter-service calls** (e.g., `Order Placement` must call `Order Shipping` for shipping options), which couple services and erode EDA's benefits — combine domains or fall back to monolithic DB if this becomes frequent.
- **Dedicated data topology (database-per-service)** — each processor owns its own database in a tight bounded context (microservices-style). Highest fault tolerance, scalability, and change control: an outage is isolated to one processor. Cons: expensive; promotes the most synchronous dynamic coupling (e.g., `Order Placement` must synchronously call both `Inventory` and `Order Shipment` for its needed data). Best when processors are mostly self-contained.

## 15. Cloud Considerations

- **Strong cloud fit** — EDA's highly decoupled nature pairs naturally with cloud asynchronous services and elastic infrastructure.

## 16. Common Risks

- **Nondeterministic side effects** — processors may unexpectedly trigger derived events or fail to respond when they should; complex workflows are hard to predict.
- **Static coupling via contracts** — dynamic coupling is low, but event-payload contracts create tight static coupling. Architects don't always know which processors consume an event, so contract changes are dangerous. Key-based payloads mitigate this but bring scalability/performance costs and risk of anemic events.
- **Too much synchronous communication between processors** — signals EDA is the wrong style.
- **State management** — knowing when an initiating event is fully processed is hard. Sometimes the architect can identify a final "ending" event and have the originator subscribe to it; usually, no.

## 17. Governance

- **Mostly nonstructural; observability-driven** — uses logs and a governance mesh; some metrics need manual collection.
- **Static coupling** — track rate of contract change and overall **stamp coupling**; record which payload fields are unused to trim contracts and reduce bandwidth.
- **Dynamic coupling** — automated fitness functions track inter-processor synchronous calls (via logs, source-code annotations, standard custom-identifier libraries). Any synchronous call should be challenged, especially with domain or dedicated database topologies.

## 18. Team Topology Considerations

EDA is largely *technically partitioned* (multiple processors, channels, brokers, and possibly databases per domain), but works when teams align by domain.

- **Stream-aligned teams** — struggle as the system grows: a single domain change may touch many processors and rework derived event flows. The larger and more complex the EDA, the less effective stream-aligned teams become.
- **Enabling teams** — *don't work well* in EDA: experimentation within a stream disrupts other stream-aligned teams' understanding of the event flow and demands too much coordination.
- **Complicated-subsystem teams** — work well; complex processing isolates cleanly into separate event processors, with stream-aligned teams coordinating only on contracts and derived events.
- **Platform teams** — leverage the technical partitioning by treating message brokers, event hubs, event buses, and other event-channel artifacts as platform concerns.

## 19. Style Characteristics

| Characteristic | Rating |
|---|---|
| Overall cost | $$$ |
| Partitioning type | Technical |
| Number of quanta | 1 to many |
| Simplicity | 2 stars |
| Modularity | 4 stars |
| Maintainability | 4 stars |
| Testability | 2 stars |
| Deployability | 3 stars |
| Evolvability | 5 stars |
| Responsiveness | 5 stars |
| Scalability | 4 stars |
| Elasticity | 3 stars |
| Fault tolerance | 5 stars |

- **Technically partitioned, 1-to-many quanta** — any domain spreads across multiple processors and is tied together via brokers, payloads, and topics, so EDA is not generally domain-partitioned. A shared database instance or a request-reply pair forces processors into the same quantum even when their main communication is asynchronous.
- **Performance, scalability, fault tolerance (4–5★)** — primary strengths. Performance from async + parallel processing; scalability through programmatic load balancing of event processors (also called *competing consumers* and *consumer groups*); fault tolerance through decoupled async processors (eventual consistency). Scalability is 4★ rather than 5★ because of the database (space-based architecture in Chapter 16 hits 5★).
- **Evolutionary (5★)** — adding features through new or existing processors is straightforward; built-in extensibility hooks via derived events.
- **Simplicity and testability (2★)** — nondeterministic, dynamic event flows are hard to reason about and to test; "event tree diagrams" can branch into thousands of scenarios.
- **Workflow control, error handling, recoverability** — disadvantages: it is hard to know when the business transaction completes, hard to react to failures (without a mediator the rest of the system keeps moving as if nothing went wrong), and often infeasible to resubmit the initiating event because async actions have already happened downstream.
- **Trade-off table** — advantages over request-based: better response to dynamic content, better scalability and elasticity, better agility/change management, better adaptability/extensibility, better responsiveness/performance, better real-time decision making, better situational-awareness reaction. Trade-offs: only eventual consistency, less control over flow, less certainty over outcome, hard to test and debug.
- **Choosing between models** — request-based for well-structured, data-driven requests where certainty and control matter; event-based for flexible, action-based events needing high responsiveness, scale, and dynamic processing.

## 20. Examples and Use Cases

- **Order-entry systems** — the chapter's running example: parallel, decoupled order processing.
- **Going, Going, Gone (GGG) auction** — bidding has unknown participant counts, requires scalability and elasticity (especially as a timed auction closes), and high responsiveness; placing a bid is fundamentally an *event*, not a request. `Bid Capture` receives the bid, validates against the prior price, and emits `bid placed`. `Auctioneer` updates the website price. `Bid Streamer` streams the bid to history and individual bidders. `Bidder Tracker` persists for audit. All three react asynchronously and concurrently.
- **When to skip EDA** — if most processing is request-based, use the microservices style instead (Chapter 18).
