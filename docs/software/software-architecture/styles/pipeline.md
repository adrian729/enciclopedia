# Pipeline Architecture

> *Fundamentals* Ch 12 is the sole source. Pipeline (a.k.a. *pipes and filters*) is one of the fundamental styles — it appears naturally the moment developers split functionality into discrete sequential steps. Unix shells, MapReduce pipelines, ETL tools, and many functional-language constructs share its shape. *The Hard Parts* doesn't address pipeline as a distinct style.

## Table of Contents

- [1. Topology — Pipes and Filters](#1-topology--pipes-and-filters)
- [2. The Four Filter Types](#2-the-four-filter-types)
- [3. Pipes](#3-pipes)
- [4. "More Shell, Less Egg"](#4-more-shell-less-egg)
- [5. Data Topology and Cloud Considerations](#5-data-topology-and-cloud-considerations)
- [6. When to Use and When Not To](#6-when-to-use-and-when-not-to)
- [7. Risks and Antipatterns](#7-risks-and-antipatterns)
- [8. Architecture Characteristic Ratings](#8-architecture-characteristic-ratings)
- [9. Example — Kafka Telemetry Pipeline](#9-example--kafka-telemetry-pipeline)
- [Sources](#sources)

## 1. Topology — Pipes and Filters

> **Isomorphic shape.** A single deployment unit with functionality contained within filters connected by unidirectional pipes.

Two component types:

| Component | Role |
|---|---|
| **Filter** | Contains functionality and performs a specific business function. Self-contained, generally stateless, performs **one task only**; composite tasks are sequences of filters. Even a one-class filter counts as a component. |
| **Pipe** | Transfers data to the next filter (or filters). Typically **unidirectional** and point-to-point. |

The unidirectional constraint is the style's signature — back-and-forth communication between filters means the pipeline shape is wrong, or the filters are too complex or poorly demarcated.

## 2. The Four Filter Types

| Filter type | Role | Functional-programming analogue |
|---|---|---|
| **Producer** | Starting point, outbound only. Sometimes called the *source*. Examples: a UI, an external incoming request. | — |
| **Transformer** | Accepts input, optionally transforms some or all of the data, forwards output. | *map* |
| **Tester** | Accepts input, tests it against criteria, optionally produces output. Acts as a validator or a switch ("don't forward if the order amount is less than five dollars"). | *reduce* |
| **Consumer** | Termination point. Often persists results to a database or displays them on a UI. | — |

The four-way classification is more than vocabulary — governance leans on it (see [§ 7](#7-risks-and-antipatterns)).

## 3. Pipes

Pipes are the channel between filters. Each is typically unidirectional and point-to-point. The payload can be any data format, but architects favor smaller payloads for performance.

| Deployment | Pipe form |
|---|---|
| **Monolithic** | In-process method/function calls; threads or embedded messaging provide async behavior. |
| **Distributed** | Unidirectional remote calls — REST, messaging, streaming, or other protocols. Each filter deploys as a separate service. |

Either sync or async works. Distributed deployment buys elasticity, scalability, and fault tolerance — at the cost of simplicity, overall cost, and the [Fallacies of Distributed Computing](styles/overview.md#5-the-fallacies-of-distributed-computing).

## 4. "More Shell, Less Egg"

The classic illustration of the style's compositional power. Donald Knuth was asked to write a program that reads a file, finds the *n* most-used words, and prints them sorted by frequency. He wrote ten-plus pages of Pascal designing a new algorithm. Doug McIlroy demonstrated a shell script small enough to fit in a social media post that solved the same problem:

```
tr -cs A-Za-z '\n' | tr A-Z a-z | sort | uniq -c | sort -rn | sed ${1}q
```

Six filters composed by five pipes. The story is the canonical example of how composable pipes-and-filters can be.

## 5. Data Topology and Cloud Considerations

Most pipeline architectures are monolithic with a single shared database, but the topology spans from one shared database to **one database per filter** when filters deploy independently.

Cloud fit is **good** — high modularity and separated filter types pair well with cloud-native deployment, while the typical simplicity also lets pipelines deploy as monoliths.

**AWS Step Functions** is the canonical cloud implementation: each filter is a separate Lambda in the workflow. Two workflow modes — *Standard* (each step exactly once) and *Express* (each step may execute more than once) — both work. Other shapes: serverless functions, containerized functions, or one service containing all filter components in a single monolithic deployment.

## 6. When to Use and When Not To

**When to use:**

- Systems of any complexity with **distinct, ordered, deterministic one-way processing steps**.
- Tight time and budget constraints (the monolithic deployment is cheap).
- ETL tools, EDI document transformers, mediators like Apache Camel that pass information between business-process steps.

**When not to use:**

- High scalability, elasticity, or fault-tolerance needs (distributed deployment mitigates only partially).
- Back-and-forth communication between filters — pipes are unidirectional.
- Nondeterministic workflows — [Event-Driven Architecture](styles/event-driven.md) is far better suited.

## 7. Risks and Antipatterns

- **Overloaded filters.** Most common risk: developers cram too much responsibility into one filter, defeating the single-purpose goal.
- **Bidirectional communication.** Pipes are unidirectional only. If you need bidirectional flow, the pipeline style is wrong, or filters are poorly demarcated.
- **Error handling.** Once a pipeline starts, exiting cleanly and recovering is hard. Identify possible fatal error conditions *before* defining the architecture.
- **Contract management.** Each pipe carries a contract for its data; changing a contract demands strict governance and downstream testing.

Governance is hard to automate — fitness functions struggle to verify whether a producer is *really* the start of a pipeline or whether a tester is *really* conditional. The recommended technique is **tagging** via Java annotations / C# custom attributes:

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface Filter {
   public FilterType[] value();
   public enum FilterType { PRODUCER, TESTER, TRANSFORMER, CONSUMER }
}
```

A second `@FilterEntrypoint` annotation marks the class where the filter starts, since filters may span multiple class files. The tags don't enforce behavior — they provide context that nudges developers toward correct responsibility (e.g., not letting a transformer perform testing logic).

## 8. Architecture Characteristic Ratings

| Characteristic | Rating |
|---|---|
| Overall cost | ★★★★★ |
| Simplicity | ★★★★★ |
| Deployability | ★★★ |
| Elasticity | ★ |
| Evolutionary | ★★★ |
| Fault tolerance | ★ |
| Modularity | ★★★★ |
| Performance | ★★★ |
| Reliability | ★★★ |
| Scalability | ★ |
| Testability | ★★★ |

- **Technically partitioned with quantum 1.** Application logic separates into filter types; monolithic deployment yields an architecture quantum of 1.
- **Strengths — cost, simplicity, modularity.** Monolithic shape avoids distributed complexity; filter separation of concerns lets any filter be modified or replaced without affecting the others (e.g., swapping the calculation inside a `Duration Calculator`).
- **Deployability and testability (above layered).** Modularity helps; monolithic deployment ceremony, risk, and incomplete testing still constrain the scores.
- **Elasticity, scalability, fault tolerance (1★).** Monolithic deployment dooms these. Distributed deployment with async communication can raise them significantly, paying the cost in simplicity and overall cost.
- **Availability.** High MTTR typical of monoliths hurts availability.

## 9. Example — Kafka Telemetry Pipeline

Service telemetry information streams to Apache Kafka; the pipeline processes it:

| Filter | Type | Behavior |
|---|---|---|
| `Service Info Capture` | Producer | Subscribes to the Kafka topic and receives streaming service info. |
| `Duration` | Tester | Checks whether the data is duration-related; if yes, forwards to `Duration Calculator`; otherwise forwards to the next tester. |
| `Duration Calculator` | Transformer | Computes duration metrics. |
| `Uptime` | Tester | Checks whether the data is uptime-related; if not, the pipeline ends. |
| `Uptime Calculator` | Transformer | Computes uptime metrics. |
| `Database Output` | Consumer | Persists the result to a MongoDB database. |

Separation of concerns is strict: `Service Info Capture` only knows how to connect to Kafka; `Duration` only qualifies and routes. Adding a new tester filter (e.g., for database connection wait time) after `Uptime` is a small, isolated change — the **extensibility** strength of the style.

## When to Decompose This Style

Pipeline is rarely "decomposed" in the same way layered or modular monolith is — it is more often *distributed* by deploying each filter as its own service. That converts pipeline into a service-style topology while preserving the unidirectional flow. If the trigger is scale, elasticity, or fault tolerance, [When to Decompose](decomposition/when-to-decompose.md) frames the modularity drivers and the feasibility check; [Tactical vs. Strategic](decomposition/tactical-vs-strategic.md) covers whether to refactor in place or fork.

## Sources

- [Fundamentals Ch 12: Pipeline Architecture Style](software/software-architecture/books/fundamentals-of-software-architecture/ch12_pipeline_architecture.md) (sole source — topology, four filter types, pipes, "More Shell, Less Egg", AWS Step Functions, tagging governance, Kafka telemetry example, characteristic ratings)


<!-- prev-next-nav -->

---

← [Modular Monolith](software/software-architecture/styles/modular-monolith.md) | [Microkernel](software/software-architecture/styles/microkernel.md) →
