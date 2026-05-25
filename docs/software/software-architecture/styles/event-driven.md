# Event-Driven Architecture

> *Fundamentals* Ch 15 is the sole source — *The Hard Parts* assumes the reader has the catalog and references EDA only via the eight saga patterns in [Transactional Sagas](distributed/transactional-sagas.md). EDA is a popular distributed, asynchronous style for highly scalable, high-performance applications, built from decoupled event-processing components. It can be standalone or embedded inside other styles (e.g., event-driven microservices).

## Table of Contents

- [1. Request-Based vs. Event-Based](#1-request-based-vs-event-based)
- [2. Broker Topology](#2-broker-topology)
- [3. Mediator Topology](#3-mediator-topology)
- [4. Events vs. Messages](#4-events-vs-messages)
- [5. Derived Events and Architectural Extensibility](#5-derived-events-and-architectural-extensibility)
- [6. Asynchronous Capabilities and Dynamic Quantum Entanglement](#6-asynchronous-capabilities-and-dynamic-quantum-entanglement)
- [7. Event Payload — Data-Based vs. Key-Based](#7-event-payload--data-based-vs-key-based)
- [8. Anemic Events and the Swarm of Gnats Antipattern](#8-anemic-events-and-the-swarm-of-gnats-antipattern)
- [9. Error Handling — Workflow Event Pattern](#9-error-handling--workflow-event-pattern)
- [10. Preventing Data Loss — Event Forwarding Pattern](#10-preventing-data-loss--event-forwarding-pattern)
- [11. Request-Reply Messaging](#11-request-reply-messaging)
- [12. Data Topology](#12-data-topology)
- [13. When to Use and When Not To](#13-when-to-use-and-when-not-to)
- [14. Architecture Characteristic Ratings](#14-architecture-characteristic-ratings)
- [Sources](#sources)

## 1. Request-Based vs. Event-Based

| Model | Behavior | Example |
|---|---|---|
| **Request-based** | A *request orchestrator* (UI, API layer, integration hub) deterministically and synchronously routes a request to *request processors*. | "Show me my last six months of orders." |
| **Event-based** | Reacts to something that has happened. The system responds asynchronously to events. | An online-auction bid — not a request; the system must compare concurrent bids and compute the highest. |

EDA is an *architectural style*, not just a pattern — entire systems can be built with it.

## 2. Broker Topology

The default topology in this chapter — **choreographed**, fire-and-forget asynchronous communication. Four primary components:

| Component | Role |
|---|---|
| **Initiating event** | Starts the entire flow (placing a bid; updating health benefits because an employee got married). Sent to an *event channel* in the event broker. |
| **Event broker** | Typically *federated* — multiple domain-based clustered instances. Holds the channels (queues, topics, streams) for its event flow. Uses publish-and-subscribe (topics, AMQP topic exchanges, Kafka streams). |
| **Event processor** | Accepts the initiating event, performs its task, then asynchronously advertises what it did by triggering a **derived event**. |
| **Derived event** | The event a processor emits after acting. Other processors respond and trigger their own. Flow ends when all processors are idle. |

**Retail order-entry walkthrough.** `Order Placement` receives `place order`, inserts the order, returns the order ID, advertises `order placed`. Three event processors react in parallel:

- `Notification` emails the customer; advertises `email sent`. Nobody currently listens — but a future `Email Analyzer` can be added with no change to existing processors. This is **architectural extensibility**.
- `Inventory` adjusts stock; advertises `inventory updated`. `Warehouse` responds, reorders if needed, and on replenishment triggers `stock replenished`. `Inventory` reacts but does **not** trigger another `inventory adjusted` — that would be a **poison event** looping forever between services.
- `Payment` charges the card; emits `payment applied` or `payment denied`. `Notification` listens for denial; `Order Fulfillment` listens for the applied event, picks/packs, then triggers `order fulfilled`. `Notification` and `Shipping` both listen.

The relay-race analogy: once a processor "hands off" the baton (event), it is done with this event and free to react to others. Each processor scales independently.

## 3. Mediator Topology

The *orchestrated* form of EDA. Used when the architect needs more control over event order. Components: initiating event, event queue, **event mediator**, event channels, event processors.

- **Messages, not events.** The mediator topology typically uses *messages* (commands like `ship_order`) instead of events that have happened (`order_shipped`).
- **Workflow ownership.** The mediator knows the steps. It accepts the initiating event, generates derived **messages**, and sends them point-to-point to dedicated channels (usually queues). Processors handle messages and reply to the mediator. They do **not** advertise their work to the rest of the system.
- **Multiple mediators.** Most implementations use one mediator per domain (customer, order…) to avoid a single point of failure and improve throughput.

**Mediator implementation choices:**

| Implementation | Use case |
|---|---|
| **Apache Camel, Mule ESB, Spring Integration** | Simple error handling and orchestration with custom Java/C# routes. |
| **Apache ODE, Oracle BPEL Process Manager** | Conditional, dynamic, error-rich flows; based on Business Process Execution Language (BPEL). Powerful but complex — usually authored via GUI tools. |
| **BPM engines (jBPM)** | Long-running flows with human intervention (e.g., a senior trader manually approving a trade above a threshold). |

**Mediator delegation model.** Classify events as simple, hard, or complex; route them all through a simple mediator (Apache Camel/Mule). Simple flows handle themselves; harder flows are forwarded to BPEL or BPM mediators.

**Trade-offs.** Gains workflow control, error handling, and recoverability. Loses some performance and scalability (the mediator must scale and can become a bottleneck); processors are less decoupled; complex dynamic processing is hard to model declaratively. Often a **hybrid** (mediator + choreographed) is used.

## 4. Events vs. Messages

| Construct | Meaning | Channel |
|---|---|---|
| **Event** | Broadcasts that *something has already happened* ("I just placed an order"). Typically requires no response. | Pub/sub one-to-many over a *topic*, *stream*, or notification service. |
| **Message** | A command or query ("apply the payment for this order"; "give the shipping options"). Usually requires a response. | Point-to-point one-to-one over a *queue* or messaging service. |

EDA mostly uses events but uses messages occasionally — requesting data from another processor, or controlling the mediator topology.

Worked classification examples:

- "Adventurous Air Flight 6557, turn left, heading 230 degrees" → **message** (command).
- "A cold front has moved into the area" → **event**.
- "OK, class, turn to page 145" → **message** (broadcasting a command does not turn it into an event).
- "Hi, everyone! Sorry I'm late for the meeting" → **event**.

## 5. Derived Events and Architectural Extensibility

A **derived event** is created and triggered by an event processor *after* the initiating event. A processor can trigger more than one.

**Credit-card example.** A `creditcard charged` event triggers `Fraud Detection` (which emits two possible derived events — *fraud detected* vs. *not detected*, each meaningful to different downstream processors) and `Credit Limit` in parallel. `Credit Limit` produces three derived events: `limit okay` (payload may also carry remaining credit), `limit warning` (notify customer), and `fatal limit exceeded` (consumed by `Notification`, `Decline Purchase`, and a marketing-driven `Extend Credit Limit`).

**Extensible derived events.** Even when no processor currently cares about an event, advertising it provides architectural extensibility: an `email sent` event allows a future `Email Analyzer` to be plugged in with no change to existing processors.

## 6. Asynchronous Capabilities and Dynamic Quantum Entanglement

- **Responsiveness vs. performance.** Async boosts *responsiveness* (time to acknowledge the user) but may not change *performance* (end-to-end work time). Posting a comment that takes 3,000 ms to validate: sync REST → 3,100 ms total wait; async messaging → 25 ms perceived wait, actual posting still 3,025 ms.
- **Trade-off: no synchronous failure path.** Async loses the immediate guarantee that the work succeeded. Mitigation: notify the user via a separate channel when something is rejected (stock trades, comments containing profanity).
- **Avoiding Dynamic Quantum Entanglement.** When two architectural quanta talk synchronously, they become entangled into a single quantum. Example: `Portfolio Management` synchronously sending a trade order to `Trade Order` blocks waiting for a confirmation, so both share the same architectural characteristics. Replacing the synchronous call with **asynchronous communication** (queue + separate reply channel) detangles them — `Portfolio Management` can keep submitting orders even if `Trade Order` is unavailable. See [Components and Quantum](foundations/components-and-quantum.md).

## 7. Event Payload — Data-Based vs. Key-Based

| Payload type | What the event carries |
|---|---|
| **Data-based** | Full data (e.g., a 45-attribute, 500 KB `order_placed` event). |
| **Key-based** | Only an identifier (e.g., `{"order_id": "123"}`); each consumer queries the database. |

| Payload | Pros | Cons |
|---|---|---|
| **Data-based** | Better performance, responsiveness, scalability (no DB lookups). Guarantees data availability when consumers don't share the database (strict bounded contexts, database-per-service). | Hard to maintain consistency under change (in-flight events still carry old values); contract management and versioning headaches; **stamp coupling** — `Inventory` needs ~30 bytes from a 500 KB payload but any payload change ripples to it; bandwidth (500 orders/sec × 500 KB = 250,000 KB/s vs. 15 KB/s if only needed bytes were sent). Consumer-driven contracts are hard because publishers don't always know who will respond. |
| **Key-based** | Single system of record (better consistency). Simple, rarely-changing contracts. Minimal stamp coupling and bandwidth. | Every consumer hits the DB (performance/responsiveness/scalability hit; can overwhelm the DB under high concurrency). Useless if data lives in another bounded context. |

Each event type can choose its own payload style. The choice lives on a spectrum.

## 8. Anemic Events and the Swarm of Gnats Antipattern

- **Anemic event.** A derived event whose payload lacks the context downstream processors need. Example: a `profile_updated` event carrying only the customer ID — `Service 1` cannot tell what changed; `Service 3` lacks the prior values it needs. Avoid by including updated values *and* prior values (databases typically do not preserve them).
- **Swarm of Gnats antipattern.** About event *granularity*, not payload granularity. Two failure modes:

| Failure mode | Problem | Fix |
|---|---|---|
| **Too coarse** | A single `fraud_checked` event forces all three downstream processors (`Credit Card Locking`, `Customer Notify`, `Purchase Profile`) to inspect the payload and decide whether to act. | Emit two derived events (`fraud_detected` and `no_fraud_detected`) so each processor decides via *event identity*, not payload inspection. |
| **Too fine** | A profile update emits one event per changed field (bill-to, ship-to, phone), saturating the system with related-but-tiny events and making flows unreadable. | Bundle into one `profile_updated` derived event with before/after data of all updated fields. |

> **Heuristic.** Focus event granularity on the *outcome* of the processing or state change.

## 9. Error Handling — Workflow Event Pattern

> **Workflow Event pattern (reactive architecture).** Addresses both resiliency and responsiveness in async workflows.

A consumer that hits an error immediately delegates the bad message to a **workflow processor (workflow delegate)** via async messaging and moves on to the next message; overall responsiveness is preserved.

**Workflow processor responsibilities:**

- Analyze the failure (deterministic check, ML/AI anomaly detection).
- Programmatically repair the data.
- Resubmit to the original queue (the consumer treats it as a new message).
- When the processor cannot repair it, route the message to a queue feeding a knowledgeable person's dashboard for manual fix.

**Trading example.** A basket of `BUY,AAPL` trade orders includes one row `2WE35HF6DHF,BUY,AAPL,8756 SHARES`; the trailing `SHARES` causes `NumberFormatException` in `TradePlacement`. Without the pattern, no user is around to fix the async failure. With the pattern, `TradePlacement` delegates the bad row to a `Trade Placement Error` service, which strips `SHARES` and resubmits; meanwhile, the rest of the basket processes without delay.

**Out-of-sequence consequence.** Repaired messages re-enter the queue out of order. When ordering matters (a `SELL IBM` must precede a `BUY AAPL` in the same brokerage account), buffer subsequent messages for the same context (account number) in a temporary FIFO queue and dequeue them only after the failed message is repaired.

## 10. Preventing Data Loss — Event Forwarding Pattern

Three places data can be lost between an event broker and a processor — and the mitigation for each:

| Issue | Failure mode | Mitigation |
|---|---|---|
| **1** | Processor `A` crashes before the broker acknowledges, or the broker crashes before another processor accepts. | *Persistent message queues* (broker stores the event on disk for **guaranteed delivery**) plus **synchronous send** (the producer blocks until the broker acknowledges persistence). |
| **2** | Processor `B` accepts the event but crashes before processing. | *Client acknowledge mode* (vs. default *auto acknowledge*): the event stays in the queue, locked to the client ID, until the consumer confirms successful processing. |
| **3** | Processor `B` cannot persist due to a data error. | Wrap persistence in an *ACID database commit*; **last participant support (LPS)** removes the event from the persisted queue only after all processing and persistence is confirmed. |

Brokers: Amazon SNS, RabbitMQ, Solace, Azure Event Hubs (AMQP/JMS with **durable subscribers**), Kafka (streaming).

## 11. Request-Reply Messaging

When a processor needs an immediate response (e.g., a confirmation ID), EDA uses **request-reply messaging** (pseudosynchronous communication). Each event channel uses two queues: a *request* queue and a *reply* queue.

| Technique | Behavior | Trade-off |
|---|---|---|
| **Correlation ID (CID)** — recommended | Producer sends a message (ID 124), then does a blocking wait on the reply queue with selector `CID == 124`. Consumer processes and emits a reply with `CID = 124`; producer picks it up. | One reply queue, slightly more code. |
| **Temporary queue** | Producer creates (or auto-creates) a dedicated reply queue per request, sends its name in the `reply-to` header. No selector needed because the queue is private. | Simpler but creating/destroying a queue per request can significantly slow the broker under high concurrency. |

## 12. Data Topology

| Topology | Behavior | Trade-offs |
|---|---|---|
| **Single monolithic database** | Every processor queries the central DB directly without inter-service synchronous calls. Most common topology. | Single point of failure (one DB down = all processors down); the DB must scale; schema changes ripple; collapses to a single architectural quantum. |
| **Domain database** | Group processors into domains, each owning a database. | Better fault tolerance (an order-processing DB outage doesn't stop order placement); the `payment applied` channel acts as backpressure. Cross-domain queries require **synchronous inter-service calls** — combine domains or fall back to monolithic DB if this becomes frequent. |
| **Dedicated (database-per-service)** | Each processor owns its own database in a tight bounded context (microservices-style). | Highest fault tolerance, scalability, change control: an outage is isolated to one processor. Expensive; promotes the most synchronous dynamic coupling. Best when processors are mostly self-contained. |

## 13. When to Use and When Not To

**When to use:**

- High responsiveness or scalability requirements.
- Real-time decision making and situational awareness reactions.
- Adaptable, extensible domains where new processors will be added often.
- Auction systems, stock trading, real-time fraud detection.

**When not to use:**

- Mostly request-based domains (use microservices instead).
- Workflows where ordering must be strictly preserved and recovery must be deterministic.
- Teams without observability and async-debugging maturity.

**Common risks:**

- Nondeterministic side effects.
- Static coupling via contracts — dynamic coupling is low, but event-payload contracts create tight static coupling. Architects don't always know which processors consume an event.
- Too much synchronous communication between processors — signals EDA is the wrong style.
- State management — hard to know when an initiating event is fully processed.

Governance is mostly nonstructural and observability-driven — track contract change rate, **stamp coupling**, unused payload fields, and any inter-processor synchronous calls.

## 14. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | $$$ |
| Partitioning | Technical |
| Quanta | 1 to many |
| Simplicity | ★★ |
| Modularity | ★★★★ |
| Maintainability | ★★★★ |
| Testability | ★★ |
| Deployability | ★★★ |
| Evolvability | ★★★★★ |
| Responsiveness | ★★★★★ |
| Scalability | ★★★★ |
| Elasticity | ★★★ |
| Fault tolerance | ★★★★★ |

- **Technically partitioned, 1-to-many quanta.** Any domain spreads across multiple processors and is tied together via brokers, payloads, and topics. A shared database instance or a request-reply pair forces processors into the same quantum even when their main communication is asynchronous.
- **Performance, scalability, fault tolerance (4–5★).** Primary strengths. Performance from async + parallel processing; scalability through programmatic load balancing (also called *competing consumers* and *consumer groups*); fault tolerance through decoupled async processors (eventual consistency). Scalability is 4★ rather than 5★ because of the database — [Space-Based](styles/space-based.md) hits 5★.
- **Evolutionary (5★).** Adding features through new or existing processors is straightforward; built-in extensibility via derived events.
- **Simplicity and testability (2★).** Nondeterministic, dynamic event flows are hard to reason about and to test; "event tree diagrams" can branch into thousands of scenarios.

## Granularity and Data Ownership

EDA's granularity equilibrium is per-event-processor, and its ownership decisions are sharpened by the *data-based vs. key-based payload* choice in [§ 7](#7-event-payload--data-based-vs-key-based). Two pages walk these:

- [Service Granularity](decomposition/service-granularity.md) — the disintegrators and integrators that decide event-processor size; the Grains of Sand antipattern.
- [Data Ownership](distributed/data-ownership.md) — single / common / joint ownership and the four joint-ownership resolution techniques.

## Sources

- [Fundamentals Ch 15: Event-Driven Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch15_event_driven_architecture.md) (sole source — broker vs. mediator, events vs. messages, derived events, asynchronous capabilities, payload types, Swarm of Gnats antipattern, Workflow Event pattern, Event Forwarding pattern, request-reply, data topologies, characteristic ratings)


<!-- prev-next-nav -->

---

← [Service-Based](software/software-architecture/styles/service-based.md) | [Space-Based](software/software-architecture/styles/space-based.md) →
