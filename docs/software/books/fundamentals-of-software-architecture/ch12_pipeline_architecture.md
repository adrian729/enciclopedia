# Ch 12: Pipeline Architecture Style

## Table of Contents

- [1. Topology: Pipes and Filters](#1-topology-pipes-and-filters)
- [2. Filters: Producer, Transformer, Tester, Consumer](#2-filters-producer-transformer-tester-consumer)
- [3. Pipes](#3-pipes)
- [4. Data Topologies](#4-data-topologies)
- [5. Cloud Considerations](#5-cloud-considerations)
- [6. Common Risks](#6-common-risks)
- [7. Governance](#7-governance)
- [8. Team Topology Considerations](#8-team-topology-considerations)
- [9. Style Characteristics](#9-style-characteristics)
- [10. When to Use and When Not to Use](#10-when-to-use-and-when-not-to-use)
- [11. Examples and Use Cases](#11-examples-and-use-cases)

## 1. Topology: Pipes and Filters

- **Pipes and filters** — *pipeline* architecture (a.k.a. *pipes and filters*) is one of the fundamental styles. Followed naturally as soon as developers split functionality into discrete parts.
- **Familiar appearances** — Unix shells (Bash, Zsh), MapReduce-based tools, and many functional-programming language constructs share its shape. Useful at low levels and for higher-level business applications.
- **Two component types** — *filters* contain functionality and perform a specific business function; *pipes* transfer data to the next filter (or filters). Pipes are typically one-way and point-to-point.
- **Isomorphic shape** — *a single deployment unit, with functionality contained within filters connected by unidirectional pipes*.

## 2. Filters: Producer, Transformer, Tester, Consumer

- **Filters are components** — self-contained, generally stateless, perform one task only; composite tasks are sequences of filters. Even one-class filters are components (per Ch. 8).
- **Producer** — starting point, outbound only. Sometimes called the *source*. Examples: a UI, an external request to the system.
- **Transformer** — accepts input, optionally transforms some/all of the data, forwards output. Functional-programming analogue: *map*. Used to enhance, transform, or calculate.
- **Tester** — accepts input, tests it against criteria, optionally produces output. Analogue: *reduce*. Used to validate or to act as a switch (e.g., "don't forward if the order amount is less than five dollars").
- **Consumer** — termination point. Often persists results to a database or displays them on a UI.
- **"More Shell, Less Egg" story** — Donald Knuth was asked to read a file, find the *n* most-used words, and print them sorted by frequency; he wrote 10+ pages of Pascal designing a new algorithm. Doug McIlroy demonstrated a shell script small enough to fit in a social media post (`tr -cs A-Za-z '\n' | tr A-Z a-z | sort | uniq -c | sort -rn | sed ${1}q`) that solved it elegantly — illustrating how composable pipes and filters are.

## 3. Pipes

- **Communication channel** — pipes form the channel between filters. Each is typically unidirectional and point-to-point.
- **Payload** — any data format, but architects favor smaller payloads for performance.
- **Distributed pipes** — when filters deploy as separate services, pipes become unidirectional remote calls (REST, messaging, streaming, or other protocols).
- **Sync or async** — works either way; in monolithic deployments, threads or embedded messaging provide async behavior between filters.

## 4. Data Topologies

- **Variable** — most pipeline architectures are monolithic with a single monolithic database, but topology can range from one shared database to *one database per filter*.
- **Continuous fitness function example** — a pipeline that analyzes operational characteristics in production: `Capture Raw Data` (loads its own raw-data DB) → `Time Series Selector` (reads its own configuration DB) → `Trend Analyzer` (stores analytics in its own DB) → `Graphing Tool` (renders the report).

## 5. Cloud Considerations

- **Good cloud fit** — high modularity and separated filter types make pipelines well-suited for cloud, while their typical simplicity also lets them deploy as monoliths.
- **AWS Step Functions** — each filter as a separate lambda in the workflow. Two workflows: *Standard* (each step exactly once) and *Express* (each step may execute more than once); both work. The fitness function example maps to a Step Function with `Capture Raw Data` → `Time Series Selector` → `Trend Analyzer` → `Graphing Tool`.
- **Other cloud shapes** — serverless functions, containerized functions, or a single service containing all four filter components in one monolithic deployment.

## 6. Common Risks

- **Overloaded filters** — most common risk: developers cram too much responsibility into one filter, defeating the single-purpose goal.
- **Bidirectional communication** — pipes are *unidirectional only*. If you need bidirectional flow, the pipeline style is wrong, or the filters are too complex / poorly demarcated.
- **Error handling** — once a pipeline is started, it can be hard to exit cleanly and recover. Identify possible fatal error conditions before defining the architecture.
- **Contract management** — each pipe carries a contract for its data; changing a contract demands strict governance and testing so downstream filters don't break.

## 7. Governance

- **Operational characteristics vary per use case** — but *structurally* architects govern by enforcing each filter type's role and responsibility.
- **Hard to automate** — fitness functions struggle to verify whether a producer is really the start of a pipeline or whether a tester is really conditional. Use guidance techniques rather than purely automated checks.
- **Tag technique** — Java *annotations* / C# *custom attributes* attach metadata to a filter's entry-point class identifying its type:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Filter {
   public FilterType[] value();
   public enum FilterType { PRODUCER, TESTER, TRANSFORMER, CONSUMER }
}
```

- **Entry-point tag** — since filters can span multiple class files, an additional `@FilterEntrypoint` tag marks the class where the filter starts; the `@Filter(FilterType.TRANSFORMER)` tag is attached there. Tags don't enforce behavior but provide context that nudges developers toward correct responsibility (e.g., not letting a transformer perform testing logic).

## 8. Team Topology Considerations

Pipeline is generally independent of team topology and works with any configuration:

- **Stream-aligned teams** — small, self-contained, single-flow nature matches teams owning the journey end-to-end.
- **Enabling teams** — high modularity by technical concern lets specialists add a new transformation filter (e.g., an alternative trend analysis after `Time Series Selector`) without disrupting the existing flow.
- **Complicated-subsystem teams** — each filter's narrow task fits specialist focus; the unidirectional handoff lets team members concentrate inside their filter.
- **Platform teams** — leverage modularity through shared tools, services, APIs, and tasks.

## 9. Style Characteristics

| Characteristic | Rating |
|---|---|
| Overall cost | 5 stars |
| Simplicity | 5 stars |
| Deployability | 3 stars |
| Elasticity | 1 star |
| Evolutionary | 3 stars |
| Fault tolerance | 1 star |
| Modularity | 4 stars |
| Performance | 3 stars |
| Reliability | 3 stars |
| Scalability | 1 star |
| Testability | 3 stars |

- **Technically partitioned with quantum 1** — application logic separates into filter types; monolithic deployment yields an architectural quantum of 1.
- **Strengths: cost, simplicity, modularity** — monolithic shape avoids distributed complexity; filters' separation of concerns means any filter can be modified or replaced without affecting the others (e.g., swapping the calculation in `Duration Calculator`).
- **Deployability and testability (above layered)** — modularity helps, though monolithic deployment ceremony, risk, and incomplete testing still constrain the scores.
- **Elasticity, scalability, fault tolerance (1 star)** — monolithic deployment dooms these. Distributed deployment with async communication can raise them significantly, paying the cost in simplicity and overall cost.
- **Availability** — high MTTR typical of monoliths (startup measured in minutes) hurts availability.

## 10. When to Use and When Not to Use

- **When to use** — systems of any complexity with **distinct, ordered, deterministic one-way processing steps**; tight time and budget constraints.
- **When not to use** — high scalability, elasticity, or fault tolerance needs (mitigated only partially by going distributed); back-and-forth communication between filters (pipes are unidirectional); nondeterministic workflows (event-driven architecture in Ch. 15 is much better suited).
- **Common applications** — EDI tools (transforming one document type to another), database ETL tools, orchestrators/mediators like Apache Camel that pass information between business-process steps.

## 11. Examples and Use Cases

- **Kafka telemetry pipeline** — service telemetry information streams to Apache Kafka; the pipeline processes it:
  - **`Service Info Capture` (producer)** — subscribes to the Kafka topic and receives streaming service info.
  - **`Duration` (tester)** — checks whether the data is duration-related; if yes, forwards to the duration calculator; otherwise forwards to the next tester.
  - **`Duration Calculator` (transformer)** — computes duration metrics.
  - **`Uptime` (tester)** — checks whether the data is uptime-related; if not, the pipeline ends (data is not relevant).
  - **`Uptime Calculator` (transformer)** — computes uptime metrics.
  - **`Database Output` (consumer)** — persists the result to a MongoDB database.
- **Separation of concerns** — `Service Info Capture` only knows how to connect to Kafka; `Duration` only qualifies and routes data; each filter has one job.
- **Extensibility** — adding a new tester filter (e.g., for database connection wait time) after `Uptime` is a small, isolated change.
