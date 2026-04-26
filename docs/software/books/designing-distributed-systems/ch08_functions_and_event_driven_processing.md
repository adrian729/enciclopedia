# Ch 8: Functions and Event-Driven Processing

## Table of Contents

- [1. FaaS and Serverless](#1-faas-and-serverless)
- [2. When FaaS Fits](#2-when-faas-fits)
  - [2.1. Benefits](#21-benefits)
  - [2.2. Challenges](#22-challenges)
  - [2.3. Poor Fits](#23-poor-fits)
- [3. The Decorator Pattern](#3-the-decorator-pattern)
- [4. Event Handling](#4-event-handling)
- [5. Event-Based Pipelines](#5-event-based-pipelines)

## 1. FaaS and Serverless

- **Functions as a service (FaaS)** — a request- or event-driven application style where short-lived code instances are spun up to handle a single request or event, popularized by public cloud providers and now also available on cluster orchestrators.
- **Serverless vs. event-driven** — overlapping but distinct: a multi-tenant container-as-a-service is *serverless* but not event-driven; an open-source FaaS running on physical machines you administer is *event-driven* but not serverless.
- **Component, not whole system** — FaaS is typically one piece of a larger architecture, not a complete replacement for long-running services.

## 2. When FaaS Fits

### 2.1. Benefits

- **Shortest path from code to running service** — no artifact to build or push beyond the source itself; deploy directly from laptop or browser.
- **Automatic scaling and recovery** — more traffic spawns more function instances; failed instances restart elsewhere automatically.
- **Granular building block** — functions are stateless, forcing modular, decoupled designs more granular than containers or single binaries.

### 2.2. Challenges

- **Forced decoupling cuts both ways** — strong decoupling speeds development but complicates operations: each function is independent, communicates only over the network, and must externalize all state to a storage service.
- **Hidden interaction bugs** — with no representation of inter-function dependencies, pathologies like an unintended cycle (`functionA → functionB → functionC → functionA`) become hard to detect and only stop when the original request times out or you run out of money.
- **Monitoring is mandatory** — adopters must invest in rigorous monitoring and alerting to compensate, which adds friction that offsets FaaS's deployment simplicity.

### 2.3. Poor Fits

- **Background processing** — FaaS instance runtime is time-bounded, making it a poor fit for long-running jobs like video transcoding or log compression; scheduled triggers help with temporal events (e.g., wake-up text alarms) but not generic background work, which needs a pay-per-consumption model.
- **In-memory data needs** — functions spin up *while the user is waiting*, so workloads that must load large amounts of data (e.g., a search index) suffer perceived latency spikes; if traffic is high enough to keep a function warm and amortize loading, you're likely overpaying for per-request pricing anyway.
- **Sustained request volume** — per-request pricing is great when idle but scales linearly with traffic, while VM costs decrease per-core and via reservations; once a service can keep a processor continuously busy, FaaS economics deteriorate. One mitigation: run an open-source FaaS on top of an orchestrator like Kubernetes to keep developer ergonomics with VM-style pricing.

## 3. The Decorator Pattern

- **Decorator pattern (FaaS)** — a stateless function that transforms an HTTP request before it reaches a service or transforms a response before it returns, named for the analogous Python decorator construct.
- **Why FaaS over an adapter sidecar** — packaging the decorator as an adapter container couples its scale to the API service; as a FaaS, the lightweight decorator scales independently and can be experimented with cheaply before being absorbed into the service.
- **Request defaulting example** — JSON's `null` default makes "default to `true`" awkward inline; a FaaS decorator inserts default values (`name` randomized if missing, `color` defaulted to `blue`) between the user and the API, keeping defaulting logic conceptually independent from request handling.
- **Hands-On: request defaulting** — a Python `handler(context)` function fills in missing fields then forwards the modified payload to the real API; deployed as a `kubeless` HTTP-triggered function.

## 4. Event Handling

- **Requests vs. events** — *requests* belong to a larger session/interaction with an app or API; *events* are single-instance, asynchronous, fire-and-forget signals (e.g., new-user signup, file upload to a shared folder, machine-reboot notification).
- **Why events suit FaaS** — events are largely independent and stateless, their rate is highly variable, and new event types are added often; FaaS's lightweight deployment matches this churn, and the forced decoupling actually *reduces* conceptual complexity by letting a developer focus on one event type at a time.
- **Two-factor authentication example** — the login event is fired into a function that generates a code, registers it with the login service, and texts the user, keeping slow text-message latency off the login web server's critical path.
- **Hands-On: two-factor authentication** — a Python `two_factor(context)` function generates a six-digit code, registers it, and uses Twilio to send the SMS; deployed via `kubeless` and invoked asynchronously from client-side JavaScript so the UX can immediately render the code-entry page.

## 5. Event-Based Pipelines

- **Event-based pipeline** — a directed graph of functions/webhooks connected by HTTP calls, resembling a flowchart; nodes share no state but may reference common storage via a context object.
- **Pipeline vs. microservices** — microservices are long-running services handling sessions; pipelines are event-driven, often highly asynchronous, and can splice in non-software steps (e.g., a human approving a Jira ticket) that don't fit a microservices model.
- **Build/deploy pipeline example** — code submission triggers a build; a build-analysis function branches on success (file an approval ticket whose closure triggers production push) or failure (file a bug and terminate the pipeline).
- **Hands-On: new-user signup pipeline** — the user-creation function holds two webhook lists, *required* actions (e.g., welcome email) called universally and *optional* actions (e.g., subscribe to mailing list) called conditionally on input fields; each action (`email_user`, `subscribe_user`) is its own small FaaS, making the flow easy to extend and visualize while avoiding the overhead of operating multiple microservices.
