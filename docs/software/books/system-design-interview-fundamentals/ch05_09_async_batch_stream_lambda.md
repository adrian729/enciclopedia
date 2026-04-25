# Ch 5.09: Async, Batch, Stream, and Lambda Architecture

## Table of Contents

- [1. Asynchronous Processing](#1-asynchronous-processing)
- [2. Batch Processing](#2-batch-processing)
- [3. Stream Processing](#3-stream-processing)
- [4. Lambda Architecture](#4-lambda-architecture)

## 1. Asynchronous Processing

- **Definition** — a client executes something and doesn't wait for the task to complete before moving on to the next operation
- **Purpose** — offload work to a background process so the caller is unblocked; lowers latency because request processing doesn't block the client
- **Synchronicity is about how much server work the client waits for** — in a synchronous call the user waits for the task result, in an asynchronous call the user does not; candidates frequently confuse the two
- **Task scope matters** — "sync up to where?" changes the user experience. For a checkout API with three steps (click, charge payment, ship), scoping synchronicity to step 1 means the user sees "we're processing your order" immediately; scoping to step 2 gives a faster feedback loop if payment fails so the user can switch payment methods. Use API scope to drive a trade-off discussion
- **Nature of the job is asynchronous** — web crawler with a pre-prepared URL list, log search over already-generated logs, or chat/email where the sender shouldn't wait for the recipient. For user-generated data (tweets, trending topics), a common pattern is a synchronous insert into a queue, asynchronous everything downstream; failure to enqueue yields "unable to tweet, please try again"
- **Indeterministic processing time** — when it's unclear how long a job takes (Uber ride matching), better to tell the user to wait than to block
- **Long-running processing time** — if the job takes a long time (Amazon order delivery, movie transcoding) you can't have the browser spinning for the duration
- **Improve perceived latency** — skipping the wait feels faster, but can be an anti-pattern if downstream failures leave the user with a much worse experience than a synchronous error would have

## 2. Batch Processing

- **Definition** — a form of asynchronous processing that periodically grabs a data source, applies custom business logic, and produces output for later consumption
- **Typical use cases** — payroll/billing/accounting, generating a reverse index for documents, word count for documents, distributed sorting
- **MapReduce is common but not required** — batch processing doesn't have to be MapReduce; you can write custom code. Knowing MapReduce helps if the interviewer asks for algorithm details. Classic MapReduce examples: build a reverse index for search, word count for a document
- **Distributed-system considerations to surface in deep dive**:

| Question | Concern |
|---|---|
| What if the batch runs late? | SLO violation, stale output |
| What if the batch never runs? | Missed output entirely |
| What if the batch runs more than once? | Duplicate output / idempotency |
| What if the batch never finishes? | Stuck job, no progress |
| Do you have enough resources? | Resource-intensive jobs (e.g., transcoding) need prioritization |
| What if the previous run hasn't finished when the next is scheduled? | Overlapping logical runs |

## 3. Stream Processing

- **Data is unbounded** — events arrive continuously and the system must process them near real-time; fresher output than batch, at the cost of complexity
- **Event time vs processing time** — event time = when the event occurred; processing time = when the system processed it. For an event omitted at 10:00 AM but received at 10:01 AM, be explicit about which one the metric uses. Usually you want event time. Event time is irrelevant for an all-time global counter but crucial for per-period aggregations
- **System is down** — a 10-minute outage is a much bigger deal for near real-time than for batch; you also need a plan for how the system catches up on the 10 minutes of unprocessed data once it recovers
- **Late and out-of-order events** — a phone with a dropped network queues events and delivers them late; in a distributed system clock skew means you can't assume events are ordered, so you can't cleanly assert "I've seen everything before time T"
- **Watermark** — a heuristic for "have I received enough data for this time window to move on?" With a watermark delay of 7, seeing a `time_20` event sets the watermark to `time_13`; events earlier than `time_13` are considered past the watermark and may be dropped. A bigger watermark holds more memory but drops fewer late events
- **Handling events that arrive after the watermark** — options are to discard (simple, but lossy and may hurt accuracy) or update the previous record (requires a separate pipeline beyond append-only)
- **Checkpointing** — persists intermediate state so a failed host doesn't have to reprocess from the beginning. More frequent checkpointing means lower performance but faster recovery; less frequent is the reverse
- **Batch size (micro-batching)** — processing event-by-event kills throughput when each event triggers network/disk IO; micro-batching amortizes overhead. A bigger batch size increases delay but improves throughput

## 4. Lambda Architecture

- **Batch vs stream is a spectrum** — modern streaming blurs the line; the knob is how much you batch before processing (once a second vs once a month). Pick based on the use case, not reflexively
- **Prefer batch over streaming when**:

| Reason | Why |
|---|---|
| Data is enormous | A year's aggregation doesn't fit in memory |
| Compute intensive | Processing can't keep up with the production rate, causing backlog |
| Complexity of streaming | Unbounded data + late/out-of-order events + freshness SLOs are hard to maintain |
| Use case doesn't need freshness | Daily payroll gets no value from streaming |

- **Lambda architecture = fast lane + slow lane** — fast lane minimizes latency at the expense of completeness and accuracy (stream-style); slow lane uses most/all data for a more accurate result (batch-style). In practice, running two similar systems carries operational complexity
- **When to bring it up in an interview** — if the interviewer challenges your stream design with a hypothetical (e.g., enormous data) that would break it, propose lambda architecture with batch producing the final accurate result
