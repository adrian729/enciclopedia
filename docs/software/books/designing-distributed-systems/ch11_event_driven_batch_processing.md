# Ch 11: Event-Driven Batch Processing

## Table of Contents

- [1. Workflow Systems](#1-workflow-systems)
- [2. Patterns for Linking Work Queues](#2-patterns-for-linking-work-queues)
  - [2.1. Copier](#21-copier)
  - [2.2. Filter](#22-filter)
  - [2.3. Splitter](#23-splitter)
  - [2.4. Sharder](#24-sharder)
  - [2.5. Merger](#25-merger)
- [3. Publisher/Subscriber Infrastructure](#3-publishersubscriber-infrastructure)
- [4. Hands-On](#4-hands-on)

## 1. Workflow Systems

- **Workflow system** — an event-driven batch processor where the output of one work queue becomes the input to one or more downstream queues, forming a directed acyclic graph (DAG) of stages coordinated by completion events.
- **Why patterns matter** — like event-driven FaaS, workflows can be hard to reason about without a blueprint; the patterns below give a shared vocabulary for how queues link together.
- **Beyond simple chaining** — the trivial case (output of queue A → input of queue B) is straightforward; the patterns in this chapter cover *coordination across multiple queues* and *modification of queue output*.

## 2. Patterns for Linking Work Queues

### 2.1. Copier

- **Copier** — duplicates a single stream of work items into two or more identical streams so multiple independent operations can run on the same input.
- **Example: video transcoding** — one source video is copied into separate render queues for a 4-KB high-resolution hard-drive format, 1080-pixel digital streaming, low-resolution mobile, and an animated GIF thumbnail.

### 2.2. Filter

- **Filter** — reduces a stream to a smaller stream by dropping items that don't meet a criterion.
- **Example: opt-in users** — out of all newly signed-up users, keep only those who ticked the email-promotions checkbox.
- **Implementation as ambassador** — wrap an existing work-queue source with a filter container; the original source provides the full list, the filter container narrows it before returning to the queue infrastructure.

### 2.3. Splitter

- **Splitter** — evaluates a criterion like a filter, but instead of dropping items, routes them to different queues based on the result so nothing is lost.
- **Example: shipping notifications** — one stream of shipped orders is split into an "email notification" queue and a "text notification" queue.
- **Splitter as copier+filter** — a splitter can be expressed as a copier feeding two filters, but the splitter pattern is a more compact, intent-revealing representation. A splitter that sends the same input to multiple queues also acts as a copier (e.g., a user who selected both email and text).

### 2.4. Sharder

- **Sharder** — a generalized splitter that distributes a single queue evenly across N shards via a *sharding function*, mirroring the sharded-server idea applied to workflows.
- **Reliability via shards** — a bad worker rollout to one shard takes down only 1/N of the service instead of all users; staged rollout across shards contains blast radius.
- **Resource distribution** — sharding spreads work across regions/datacenters to even out utilization and survive datacenter failures.
- **Dynamic rebalancing** — when a shard becomes unhealthy, the sharding algorithm sends its work to the remaining healthy queues, even if only one survives.

### 2.5. Merger

- **Merger** — the inverse of the copier; combines two or more work queues into a single queue for downstream processing.
- **Example: shared build/test infrastructure** — many source repositories each emit commits; a merger funnels them into one build-and-test queue rather than running per-repo build infrastructure.
- **Merger as multi-source adapter** — the merger is an adapter pattern where one adapter wraps *multiple* source containers and presents them as a single merged source.

## 3. Publisher/Subscriber Infrastructure

- **Pub/sub API** — defines named queues (called *topics*); *publishers* write messages to topics, *subscribers* listen for new messages, and the queue reliably stores and delivers messages to subscribers.
- **Why pub/sub over filesystems** — local-directory queues are confined to one node; network filesystems work but add code and deployment complexity. Pub/sub APIs are presented as a popular alternative.
- **Implementations** — Azure's EventGrid, Amazon's Simple Queue Service, and the open-source Kafka project are common choices; Kafka is portable across on-prem hardware and cloud VMs.
- **Topics map to workflow stages** — typically each module's output becomes a topic; e.g., a `Photos` sharder with three shards uses topics `Photos-1`, `Photos-2`, `Photos-3`.
- **Replication factor and partitions** — when creating a Kafka topic, `--replication-factor` (recommended 3 or 5) controls redundancy across machines; `--partitions` caps how many machines a topic can spread across for load balancing.

## 4. Hands-On

- **New-user signup workflow** — composes a sharder (for geographic redundancy on verification email), a copier (after email validation, fan out to "send welcome" and "set up notifications"), and a filter pattern that splits the notifications work queue into separate email and text message notification queues.
- **Deploying Kafka on Kubernetes** — install via the Helm package manager using the `incubator/kafka` chart; create topics, then publish/consume from short-lived pods running the Kafka console producer and consumer.
