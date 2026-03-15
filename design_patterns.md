# Design Patterns

## Table of Contents
- [1. Creational](#1-creational)
  - [1.1. Singleton](#11-singleton)
    - [1.1.1. Paradigm Fit](#111-paradigm-fit)
    - [1.1.2. Benefits](#112-benefits)
    - [1.1.3. Trade-offs](#113-trade-offs)
    - [1.1.4. Examples](#114-examples)
  - [1.2. Builder](#12-builder)
    - [1.2.1. Paradigm Fit](#121-paradigm-fit)
    - [1.2.2. Benefits](#122-benefits)
    - [1.2.3. Trade-offs](#123-trade-offs)
    - [1.2.4. Examples](#124-examples)
  - [1.3. Factory](#13-factory)
    - [1.3.1. Paradigm Fit](#131-paradigm-fit)
    - [1.3.2. Benefits](#132-benefits)
    - [1.3.3. Trade-offs](#133-trade-offs)
    - [1.3.4. Examples](#134-examples)
  - [1.4. Abstract Factory](#14-abstract-factory)
    - [1.4.1. Paradigm Fit](#141-paradigm-fit)
    - [1.4.2. Benefits](#142-benefits)
    - [1.4.3. Trade-offs](#143-trade-offs)
    - [1.4.4. Examples](#144-examples)
  - [1.5. Prototype](#15-prototype)
    - [1.5.1. Paradigm Fit](#151-paradigm-fit)
    - [1.5.2. Benefits](#152-benefits)
    - [1.5.3. Trade-offs](#153-trade-offs)
    - [1.5.4. Examples](#154-examples)
  - [1.6. Object Pool](#16-object-pool)
    - [1.6.1. Domain Context](#161-domain-context)
    - [1.6.2. Paradigm Fit](#162-paradigm-fit)
    - [1.6.3. Benefits](#163-benefits)
    - [1.6.4. Trade-offs](#164-trade-offs)
    - [1.6.5. Examples](#165-examples)
- [2. Structural](#2-structural)
  - [2.1. Facade](#21-facade)
    - [2.1.1. Paradigm Fit](#211-paradigm-fit)
    - [2.1.2. Benefits](#212-benefits)
    - [2.1.3. Trade-offs](#213-trade-offs)
    - [2.1.4. Examples](#214-examples)
  - [2.2. Adapter](#22-adapter)
    - [2.2.1. Paradigm Fit](#221-paradigm-fit)
    - [2.2.2. Benefits](#222-benefits)
    - [2.2.3. Trade-offs](#223-trade-offs)
    - [2.2.4. Examples](#224-examples)
  - [2.3. Decorator](#23-decorator)
    - [2.3.1. Paradigm Fit](#231-paradigm-fit)
    - [2.3.2. Benefits](#232-benefits)
    - [2.3.3. Trade-offs](#233-trade-offs)
    - [2.3.4. Examples](#234-examples)
  - [2.4. Proxy](#24-proxy)
    - [2.4.1. Paradigm Fit](#241-paradigm-fit)
    - [2.4.2. Benefits](#242-benefits)
    - [2.4.3. Trade-offs](#243-trade-offs)
    - [2.4.4. Examples](#244-examples)
  - [2.5. Composite](#25-composite)
    - [2.5.1. Paradigm Fit](#251-paradigm-fit)
    - [2.5.2. Benefits](#252-benefits)
    - [2.5.3. Trade-offs](#253-trade-offs)
    - [2.5.4. Examples](#254-examples)
  - [2.6. Bridge](#26-bridge)
    - [2.6.1. Paradigm Fit](#261-paradigm-fit)
    - [2.6.2. Benefits](#262-benefits)
    - [2.6.3. Trade-offs](#263-trade-offs)
    - [2.6.4. Examples](#264-examples)
  - [2.7. Flyweight](#27-flyweight)
    - [2.7.1. Paradigm Fit](#271-paradigm-fit)
    - [2.7.2. Benefits](#272-benefits)
    - [2.7.3. Trade-offs](#273-trade-offs)
    - [2.7.4. Examples](#274-examples)
- [3. Behavioral](#3-behavioral)
  - [3.1. Strategy](#31-strategy)
    - [3.1.1. Paradigm Fit](#311-paradigm-fit)
    - [3.1.2. Benefits](#312-benefits)
    - [3.1.3. Trade-offs](#313-trade-offs)
    - [3.1.4. Examples](#314-examples)
  - [3.2. Observer](#32-observer)
    - [3.2.1. Paradigm Fit](#321-paradigm-fit)
    - [3.2.2. Benefits](#322-benefits)
    - [3.2.3. Trade-offs](#323-trade-offs)
    - [3.2.4. Examples](#324-examples)
  - [3.3. Command](#33-command)
    - [3.3.1. Paradigm Fit](#331-paradigm-fit)
    - [3.3.2. Benefits](#332-benefits)
    - [3.3.3. Trade-offs](#333-trade-offs)
    - [3.3.4. Examples](#334-examples)
  - [3.4. State](#34-state)
    - [3.4.1. Paradigm Fit](#341-paradigm-fit)
    - [3.4.2. Benefits](#342-benefits)
    - [3.4.3. Trade-offs](#343-trade-offs)
    - [3.4.4. Examples](#344-examples)
  - [3.5. Template Method](#35-template-method)
    - [3.5.1. Paradigm Fit](#351-paradigm-fit)
    - [3.5.2. Benefits](#352-benefits)
    - [3.5.3. Trade-offs](#353-trade-offs)
    - [3.5.4. Examples](#354-examples)
  - [3.6. Iterator](#36-iterator)
    - [3.6.1. Paradigm Fit](#361-paradigm-fit)
    - [3.6.2. Benefits](#362-benefits)
    - [3.6.3. Trade-offs](#363-trade-offs)
    - [3.6.4. Examples](#364-examples)
  - [3.7. Chain of Responsibility](#37-chain-of-responsibility)
    - [3.7.1. Paradigm Fit](#371-paradigm-fit)
    - [3.7.2. Benefits](#372-benefits)
    - [3.7.3. Trade-offs](#373-trade-offs)
    - [3.7.4. Examples](#374-examples)
  - [3.8. Mediator](#38-mediator)
    - [3.8.1. Paradigm Fit](#381-paradigm-fit)
    - [3.8.2. Benefits](#382-benefits)
    - [3.8.3. Trade-offs](#383-trade-offs)
    - [3.8.4. Examples](#384-examples)
  - [3.9. Memento](#39-memento)
    - [3.9.1. Paradigm Fit](#391-paradigm-fit)
    - [3.9.2. Benefits](#392-benefits)
    - [3.9.3. Trade-offs](#393-trade-offs)
    - [3.9.4. Examples](#394-examples)
  - [3.10. Visitor](#310-visitor)
    - [3.10.1. Paradigm Fit](#3101-paradigm-fit)
    - [3.10.2. Benefits](#3102-benefits)
    - [3.10.3. Trade-offs](#3103-trade-offs)
    - [3.10.4. Examples](#3104-examples)
  - [3.11. Interpreter](#311-interpreter)
    - [3.11.1. Domain Context](#3111-domain-context)
    - [3.11.2. Paradigm Fit](#3112-paradigm-fit)
    - [3.11.3. Benefits](#3113-benefits)
    - [3.11.4. Trade-offs](#3114-trade-offs)
    - [3.11.5. Examples](#3115-examples)
  - [3.12. Null Object](#312-null-object)
    - [3.12.1. Paradigm Fit](#3121-paradigm-fit)
    - [3.12.2. Benefits](#3122-benefits)
    - [3.12.3. Trade-offs](#3123-trade-offs)
    - [3.12.4. Examples](#3124-examples)
  - [3.13. Dependency Injection](#313-dependency-injection)
    - [3.13.1. Paradigm Fit](#3131-paradigm-fit)
    - [3.13.2. Benefits](#3132-benefits)
    - [3.13.3. Trade-offs](#3133-trade-offs)
    - [3.13.4. Examples](#3134-examples)
- [4. Architectural](#4-architectural)
  - [4.1. Repository](#41-repository)
    - [4.1.1. Domain Context](#411-domain-context)
    - [4.1.2. System Fit](#412-system-fit)
    - [4.1.3. Benefits](#413-benefits)
    - [4.1.4. Trade-offs](#414-trade-offs)
    - [4.1.5. Examples](#415-examples)
  - [4.2. Unit of Work](#42-unit-of-work)
    - [4.2.1. Domain Context](#421-domain-context)
    - [4.2.2. System Fit](#422-system-fit)
    - [4.2.3. Benefits](#423-benefits)
    - [4.2.4. Trade-offs](#424-trade-offs)
    - [4.2.5. Examples](#425-examples)
  - [4.3. CQRS](#43-cqrs)
    - [4.3.1. Domain Context](#431-domain-context)
    - [4.3.2. System Fit](#432-system-fit)
    - [4.3.3. Benefits](#433-benefits)
    - [4.3.4. Trade-offs](#434-trade-offs)
    - [4.3.5. Examples](#435-examples)
  - [4.4. Event Sourcing](#44-event-sourcing)
    - [4.4.1. Domain Context](#441-domain-context)
    - [4.4.2. System Fit](#442-system-fit)
    - [4.4.3. Benefits](#443-benefits)
    - [4.4.4. Trade-offs](#444-trade-offs)
    - [4.4.5. Examples](#445-examples)
  - [4.5. Circuit Breaker](#45-circuit-breaker)
    - [4.5.1. Domain Context](#451-domain-context)
    - [4.5.2. System Fit](#452-system-fit)
    - [4.5.3. Benefits](#453-benefits)
    - [4.5.4. Trade-offs](#454-trade-offs)
    - [4.5.5. Examples](#455-examples)
  - [4.6. Saga](#46-saga)
    - [4.6.1. Domain Context](#461-domain-context)
    - [4.6.2. System Fit](#462-system-fit)
    - [4.6.3. Benefits](#463-benefits)
    - [4.6.4. Trade-offs](#464-trade-offs)
    - [4.6.5. Examples](#465-examples)
  - [4.7. Specification](#47-specification)
    - [4.7.1. Domain Context](#471-domain-context)
    - [4.7.2. System Fit](#472-system-fit)
    - [4.7.3. Benefits](#473-benefits)
    - [4.7.4. Trade-offs](#474-trade-offs)
    - [4.7.5. Examples](#475-examples)

<a id="1-creational"></a>

## 1. Creational

Creational patterns abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

| Pattern | When to Use |
|---------|-------------|
| [Singleton](#11-singleton) | A shared resource needs exactly one instance with global access. |
| [Builder](#12-builder) | Constructing complex objects with many optional or ordered parameters. |
| [Factory](#13-factory) | Creating objects without specifying the exact class; letting subclasses decide. |
| [Abstract Factory](#14-abstract-factory) | Creating families of related objects without specifying their concrete classes. |
| [Prototype](#15-prototype) | Creating new objects by cloning an existing instance instead of constructing from scratch. |
| [Object Pool](#16-object-pool) | Reusing expensive-to-create objects instead of repeated creation and destruction. |

<a id="11-singleton"></a>

### 1.1. Singleton

| **Who**  | Applications that need a single shared instance (e.g., configuration managers, logging services, connection pools). |
|----------|--------|
| **What** | Ensures a class has exactly one instance and provides a global point of access to it. |
| **When** | When exactly one object is needed to coordinate access to a shared resource, and uncontrolled instantiation would cause inconsistency or waste. |
| **Where**| Infrastructure or service layers where a single point of control is required (logging, caching, configuration, thread pools). |
| **Why**  | Prevents multiple instances that could lead to inconsistent state, duplicated resource usage, or conflicting behavior. |
| **How**  | Make the constructor private, store the instance in a static field, and expose a static method or property that returns the instance — creating it lazily on first access with appropriate thread-safety guarantees. |

The Singleton pattern restricts a class to exactly one instance and provides a global access point to it. The class itself manages its own lifecycle: it hides its constructor so no external code can call `new`, stores the single instance in a static field, and exposes a static method or property that returns that instance — lazily creating it on first access.

Thread safety is the primary implementation concern. In a concurrent environment, two threads could simultaneously detect that the instance does not yet exist and each create one. Solutions include language-level lazy primitives (C# `Lazy<T>`, Java `enum` singletons), double-checked locking, or static initialization guarantees provided by the runtime.

Singleton is sometimes considered an anti-pattern because it introduces hidden global state, makes unit testing harder (shared state leaks between tests), and obscures dependencies. Prefer dependency injection when possible, and reserve Singleton for genuinely shared, stateless, or infrastructure-level resources (loggers, configuration, connection pools).

<a id="111-paradigm-fit"></a>

#### 1.1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Uncommon** — global mutable state conflicts with purity; module-level constants or managed effects are preferred. |
| Data-Oriented | **Uncommon** — global state contradicts the "data lives in tables/arrays" model; shared resources are system-level parameters. |
| OOP | **Natural fit** — private constructor and static accessor is the canonical form. |
| Procedural | **Workable** — global variable behind an initialization-guard function. |
| Reactive | **Uncommon** — reactive systems favor injected shared services; `shareReplay`/`BehaviorSubject` serve similar sharing purposes within the stream. |

<a id="112-benefits"></a>

#### 1.1.2. Benefits

- Guarantees exactly one instance — no accidental duplicates or conflicting copies.
- Lazy initialization defers resource allocation until the instance is actually needed.
- Provides a well-known global access point, simplifying discovery of shared infrastructure.

<a id="113-trade-offs"></a>

#### 1.1.3. Trade-offs

- Hidden global state makes dependencies implicit and the call graph harder to reason about.
- Shared mutable state leaks between tests, causing order-dependent failures.
- Tight coupling to the concrete class makes substitution difficult; mocking in tests often requires workarounds.
- Concurrency requires explicit thread-safety measures (locking, `Lazy<T>`, `OnceLock`, etc.).

<a id="114-examples"></a>

#### 1.1.4. Examples

##### Rust

Rust discourages global mutable state. `OnceLock` provides thread-safe lazy initialization for an immutable singleton. For mutable shared state, wrap the value in a `Mutex` or `RwLock` — though passing dependencies explicitly is the idiomatic approach.

**Implementation**

```rust
use std::sync::OnceLock;

pub struct Singleton {
    info: String,
}

impl Singleton {
    pub fn instance() -> &'static Singleton {
        static INSTANCE: OnceLock<Singleton> = OnceLock::new();
        INSTANCE.get_or_init(|| Singleton {
            info: "Singleton instance".to_string(),
        })
    }

    pub fn get_info(&self) -> &str {
        &self.info
    }
}
```

**Usage**

```rust
let s = Singleton::instance();
println!("{}", s.get_info());
```

##### C\#

**Implementation**

```csharp
using System;

public sealed class Singleton
{
    private static readonly Lazy<Singleton> _instance =
        new Lazy<Singleton>(() => new Singleton());

    private Singleton() { }

    public static Singleton Instance => _instance.Value;

    public string GetInfo() => "Singleton instance";
}
```

**Usage**

```csharp
var s = Singleton.Instance;
Console.WriteLine(s.GetInfo());
```

##### Python

A Python module is itself a singleton — its top-level state is initialized once and shared across all imports. When class-level singleton semantics are needed, override `__new__`. Note that `__init__` is still called on every invocation of `Singleton()`, so any attribute assignments in `__init__` would silently re-run and reset state. Either keep all initialization inside `__new__` or guard `__init__` with a flag.

**Implementation**

```python
class Singleton:
    _instance: "Singleton | None" = None

    def __new__(cls) -> "Singleton":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_info(self) -> str:
        return "Singleton instance"
```

**Usage**

```python
s1 = Singleton()
s2 = Singleton()
assert s1 is s2
print(s1.get_info())
```

<a id="12-builder"></a>

### 1.2. Builder

| **Who**  | Clients that need to construct complex objects with many optional or conditional parameters. |
|----------|--------|
| **What** | Separates the construction of a complex object from its representation, allowing the same construction process to create different representations. |
| **When** | When an object has many optional fields, when construction involves multiple steps in a specific order, or when a constructor would need too many parameters to remain readable. |
| **Where**| Commonly used in APIs that configure objects (HTTP clients, query builders, UI component configuration, domain object assembly). |
| **Why**  | Eliminates telescoping constructors, makes construction self-documenting through named methods, and enables validation at build time rather than after the fact. |
| **How**  | Create a separate builder object with fields matching the target's configurable options. Provide setter methods that return the builder for method chaining. A terminal build method validates the accumulated state and produces the finished object, returning an error if required fields are missing. |

The Builder pattern separates the construction of a complex object from its final representation. Instead of passing every parameter to a single constructor call — leading to long, unreadable argument lists (telescoping constructors) — the client configures the object step by step through a dedicated builder. Each setter method records one piece of configuration and returns the builder itself so calls can be chained. A terminal `build` method validates the accumulated state and produces the finished object, failing explicitly if required fields are missing.

The key participants are the **product** (the complex object being built), the **builder** (the mutable intermediate that accumulates configuration), and optionally a **director** (a reusable recipe that drives the builder through a fixed sequence of steps). In practice, most modern uses skip the director and let the client drive the builder directly.

Builder is especially valuable when objects have many optional fields, construction invariants that must hold at creation time, or when the same construction process should produce different representations. In Rust, a popular variant is the **typestate builder**, which uses generic type parameters to track which required fields have been set — shifting the "missing field" check from runtime to compile time.

<a id="121-paradigm-fit"></a>

#### 1.2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — pipelines of chained transformations over immutable intermediate values achieve the same goal, though named/default parameters and record update syntax often eliminate the need. |
| Data-Oriented | **Workable** — archetype-builders can batch-initialize component arrays, but per-object ceremony conflicts with bulk-data thinking. |
| OOP | **Natural fit** — mutable builder object with fluent method chaining. |
| Procedural | **Workable** — struct-population helpers, but no fluent chaining. |
| Reactive | **Adapts well** — fluent builder chains mirror operator pipelines; builders can configure stream topologies and subscription options. |

<a id="122-benefits"></a>

#### 1.2.2. Benefits

- Eliminates telescoping constructors — each step is a named method, making construction self-documenting.
- Enforces invariants at build time rather than relying on post-creation validation.
- The same construction process can produce different representations by swapping builder implementations.
- Method chaining provides a fluent, discoverable API that IDEs can autocomplete.

<a id="123-trade-offs"></a>

#### 1.2.3. Trade-offs

- Adds a parallel class (the builder) for every product — more code to maintain.
- Builder fields mirror the product's fields; changes to the product must be reflected in both.
- For simple objects with few required parameters, a plain constructor or factory method is simpler and less ceremony.

<a id="124-examples"></a>

#### 1.2.4. Examples

##### Rust

**Implementation**

```rust
#[derive(Debug)]
pub struct HttpRequest {
    pub method: String,
    pub url: String,
    pub headers: Vec<(String, String)>,
    pub body: Option<Vec<u8>>,
}

pub struct HttpRequestBuilder {
    method: Option<String>,
    url: Option<String>,
    headers: Vec<(String, String)>,
    body: Option<Vec<u8>>,
}

impl HttpRequestBuilder {
    pub fn new() -> Self {
        HttpRequestBuilder {
            method: None,
            url: None,
            headers: Vec::new(),
            body: None,
        }
    }

    pub fn method(mut self, m: &str) -> Self {
        self.method = Some(m.to_string());
        self
    }

    pub fn url(mut self, u: &str) -> Self {
        self.url = Some(u.to_string());
        self
    }

    pub fn header(mut self, k: &str, v: &str) -> Self {
        self.headers.push((k.to_string(), v.to_string()));
        self
    }

    pub fn body(mut self, b: Vec<u8>) -> Self {
        self.body = Some(b);
        self
    }

    pub fn build(self) -> Result<HttpRequest, &'static str> {
        let method = self.method.ok_or("method is required")?;
        let url = self.url.ok_or("url is required")?;
        Ok(HttpRequest {
            method,
            url,
            headers: self.headers,
            body: self.body,
        })
    }
}
```

**Usage**

```rust
let req = HttpRequestBuilder::new()
    .method("GET")
    .url("https://example.com")
    .header("Accept", "application/json")
    .build()?;
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public class HttpRequest
{
    public string Method { get; }
    public string Url { get; }
    public IReadOnlyDictionary<string, string> Headers { get; }
    public byte[]? Body { get; }

    public HttpRequest(string method, string url, Dictionary<string, string> headers, byte[]? body)
    {
        Method = method;
        Url = url;
        Headers = headers;
        Body = body;
    }
}

public class HttpRequestBuilder
{
    private string? _method;
    private string? _url;
    private readonly Dictionary<string, string> _headers = new();
    private byte[]? _body;

    public HttpRequestBuilder Method(string method) { _method = method; return this; }
    public HttpRequestBuilder Url(string url) { _url = url; return this; }
    public HttpRequestBuilder Header(string key, string value) { _headers[key] = value; return this; }
    public HttpRequestBuilder Body(byte[] body) { _body = body; return this; }

    public HttpRequest Build()
    {
        if (_method is null) throw new InvalidOperationException("Method is required");
        if (_url is null) throw new InvalidOperationException("URL is required");
        return new HttpRequest(_method, _url, new Dictionary<string, string>(_headers), _body);
    }
}
```

**Usage**

```csharp
var req = new HttpRequestBuilder()
    .Method("GET")
    .Url("https://example.com")
    .Header("Accept", "application/json")
    .Build();
```

##### Python

Python's keyword arguments and dataclass defaults often eliminate the need for Builder. When the pattern is still valuable (validation, multi-step construction, or a fluent API), the implementation mirrors the class-based approach.

**Implementation**

```python
from dataclasses import dataclass, field

@dataclass
class HttpRequest:
    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes | None = None

class HttpRequestBuilder:
    def __init__(self) -> None:
        self._method: str | None = None
        self._url: str | None = None
        self._headers: dict[str, str] = {}
        self._body: bytes | None = None

    def method(self, method: str) -> "HttpRequestBuilder":
        self._method = method
        return self

    def url(self, url: str) -> "HttpRequestBuilder":
        self._url = url
        return self

    def header(self, key: str, value: str) -> "HttpRequestBuilder":
        self._headers[key] = value
        return self

    def body(self, body: bytes) -> "HttpRequestBuilder":
        self._body = body
        return self

    def build(self) -> HttpRequest:
        if self._method is None:
            raise ValueError("method is required")
        if self._url is None:
            raise ValueError("url is required")
        return HttpRequest(
            method=self._method,
            url=self._url,
            headers=dict(self._headers),
            body=self._body,
        )
```

**Usage**

```python
req = (
    HttpRequestBuilder()
    .method("GET")
    .url("https://example.com")
    .header("Accept", "application/json")
    .build()
)
```

<a id="13-factory"></a>

### 1.3. Factory

| **Who**  | Clients that need to create objects without specifying the exact class to instantiate. |
|----------|--------|
| **What** | Defines an interface for creating an object, but lets subclasses (or trait implementors) decide which concrete class to instantiate, deferring creation to them. |
| **When** | When a class cannot anticipate the type of objects it must create, or when you want to isolate client code from concrete product classes. |
| **Where**| Frameworks, plugin systems, and libraries where the concrete classes are determined by configuration, user choice, or extension code. |
| **Why**  | Eliminates hard-coded instantiation of concrete classes. The client interacts solely with the product interface, making it independent of how objects are created and enabling new products without modifying existing code. |
| **How**  | Define a product interface that all created objects share. Define a creator interface with a factory method that returns the product type. Implement concrete creators that override the factory method to return specific products. Clients depend only on the creator and product interfaces. |

The Factory pattern (specifically Factory Method) defines an interface for creating objects but delegates the choice of concrete type to subclasses or implementors. The client programs against the creator's abstract interface and never references concrete product classes directly, so new product variants can be introduced without modifying existing client logic — a direct application of the Open/Closed Principle.

The key participants are the **product interface** (the abstraction all created objects share), **concrete products** (the specific types being created), the **creator interface** (which declares the factory method), and **concrete creators** (which implement the factory method to return a specific product). The client works only with the creator and product interfaces.

A simpler variant — sometimes called Simple Factory — uses a single function with a discriminator (e.g., an enum or string) to decide which concrete type to return. This trades extensibility for convenience: adding a new product requires modifying the factory function rather than adding a new creator class.

<a id="131-paradigm-fit"></a>

#### 1.3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — factory functions, closures, and higher-order functions returning values. |
| Data-Oriented | **Adapts well** — archetype factories batch-create entities with the correct component layout in a single allocation pass. |
| OOP | **Natural fit** — polymorphic creation through interfaces and subclass overrides. |
| Procedural | **Workable** — dispatch functions (switch/if) returning concrete structs. |
| Reactive | **Adapts well** — factories produce observables/streams or select concrete operators based on runtime configuration. |

<a id="132-benefits"></a>

#### 1.3.2. Benefits

- Decouples client code from concrete product classes — clients depend only on the product interface.
- New products can be added by implementing the interfaces, without modifying existing client code (Open/Closed Principle).
- Centralizes creation logic, making it straightforward to enforce constraints, add logging, or swap implementations.

<a id="133-trade-offs"></a>

#### 1.3.3. Trade-offs

- Each new product typically requires a new concrete creator class — class proliferation.
- Adds indirection: the reader must trace through the factory to discover which concrete type is created.
- The Simple Factory variant re-introduces modification when adding products, losing the Open/Closed benefit.

<a id="134-examples"></a>

#### 1.3.4. Examples

##### Rust

**Implementation**

```rust
trait Shape {
    fn draw(&self);
}

struct Circle;
impl Shape for Circle {
    fn draw(&self) {
        println!("Drawing a Circle");
    }
}

struct Square;
impl Shape for Square {
    fn draw(&self) {
        println!("Drawing a Square");
    }
}

trait ShapeFactory {
    fn create_shape(&self) -> Box<dyn Shape>;
}

struct CircleFactory;
impl ShapeFactory for CircleFactory {
    fn create_shape(&self) -> Box<dyn Shape> {
        Box::new(Circle)
    }
}

struct SquareFactory;
impl ShapeFactory for SquareFactory {
    fn create_shape(&self) -> Box<dyn Shape> {
        Box::new(Square)
    }
}
```

**Usage**

```rust
let factory: Box<dyn ShapeFactory> = Box::new(CircleFactory);
let shape = factory.create_shape();
shape.draw();
```

##### C\#

**Implementation**

```csharp
using System;

public interface IShape
{
    void Draw();
}

public class Circle : IShape
{
    public void Draw() => Console.WriteLine("Drawing a Circle");
}

public class Square : IShape
{
    public void Draw() => Console.WriteLine("Drawing a Square");
}

public interface IShapeFactory
{
    IShape CreateShape();
}

public class CircleFactory : IShapeFactory
{
    public IShape CreateShape() => new Circle();
}

public class SquareFactory : IShapeFactory
{
    public IShape CreateShape() => new Square();
}
```

**Usage**

```csharp
IShapeFactory factory = new CircleFactory();
IShape shape = factory.CreateShape();
shape.Draw();
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def draw(self) -> None: ...

class Circle(Shape):
    def draw(self) -> None:
        print("Drawing a Circle")

class Square(Shape):
    def draw(self) -> None:
        print("Drawing a Square")

class ShapeFactory(ABC):
    @abstractmethod
    def create_shape(self) -> Shape: ...

class CircleFactory(ShapeFactory):
    def create_shape(self) -> Shape:
        return Circle()

class SquareFactory(ShapeFactory):
    def create_shape(self) -> Shape:
        return Square()
```

**Usage**

```python
factory: ShapeFactory = CircleFactory()
shape = factory.create_shape()
shape.draw()
```

<a id="14-abstract-factory"></a>

### 1.4. Abstract Factory

| **Who**  | Systems that must create families of related or dependent objects without coupling to their concrete classes. |
|----------|--------|
| **What** | Provides an interface for creating families of related objects (e.g., Button + Checkbox) without specifying their concrete classes, ensuring that products from one family are used together. |
| **When** | When a system must be independent of how its products are created and composed, and when it must work with multiple families of products that are designed to be used together. |
| **Where**| Cross-platform UI toolkits (one factory per OS), themed component libraries, database access layers that target multiple vendors, and any domain where product variants must remain consistent within a family. |
| **Why**  | Guarantees that related objects are always compatible (a Windows button never paired with a macOS checkbox), isolates client code from concrete product classes, and makes swapping entire product families a single-line change at the factory selection point. |
| **How**  | Define abstract product interfaces for each distinct product kind. Define an abstract factory interface with a creation method per product kind. Implement one concrete factory per family, each returning the corresponding concrete products. Clients receive a factory instance (typically via injection or configuration) and call its creation methods — never referencing concrete product classes. |

Abstract Factory sits one level above Factory Method: instead of producing a single type of object, it produces an entire family of related objects that are designed to work together. The client programs against two layers of abstraction — the factory interface and the product interfaces — so swapping the concrete factory (e.g., from `WindowsFactory` to `MacFactory`) replaces the entire product family in one shot without touching any client logic.

The key participants are the **abstract factory** (declares creation methods for each product kind), **concrete factories** (implement those methods for a specific family), **abstract products** (interfaces for each kind of object), and **concrete products** (family-specific implementations). The client depends only on the abstract factory and abstract product interfaces, making it fully decoupled from any particular family.

A common question is when to prefer Abstract Factory over Factory Method. Factory Method concerns itself with creating one product type and uses inheritance (subclass overrides a method); Abstract Factory concerns itself with creating a coherent family of products and uses composition (the client holds a factory object). When the number of product families grows, consider combining Abstract Factory with a registry or configuration map that selects the concrete factory at startup.

<a id="141-paradigm-fit"></a>

#### 1.4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — a record or module of factory functions (one per product kind) serves as the abstract factory; swapping the record swaps the family. |
| Data-Oriented | **Workable** — factory tables can batch-initialize component arrays per family, but the per-object abstraction layer adds indirection that DOD typically avoids. |
| OOP | **Natural fit** — interfaces for both the factory and the products, with polymorphic dispatch selecting the concrete family. |
| Procedural | **Workable** — a struct of function pointers (one per product kind) passed to client code; switching the struct switches the family. |
| Reactive | **Adapts well** — factory-selected streams or operators can produce family-consistent event pipelines; configuration determines which factory feeds the reactive graph. |

<a id="142-benefits"></a>

#### 1.4.2. Benefits

- Guarantees product compatibility — objects from a single factory are always designed to work together.
- Isolates concrete classes from client code; the client never mentions a specific product implementation.
- Swapping an entire product family requires changing only the concrete factory supplied at the composition root.

<a id="143-trade-offs"></a>

#### 1.4.3. Trade-offs

- Adding a new product kind to the family forces changes across every concrete factory — the interface expands, and all implementations must follow.
- Class proliferation: each family multiplies the number of concrete product classes.
- The additional abstraction layer can be overkill when the system only has one product family or when families are unlikely to change.

<a id="144-examples"></a>

#### 1.4.4. Examples

##### Rust

Rust uses trait objects to achieve the polymorphism Abstract Factory relies on. Each product kind gets its own trait, and the abstract factory is a trait with one method per product kind.

**Implementation**

```rust
trait Button {
    fn render(&self) -> String;
}

trait Checkbox {
    fn render(&self) -> String;
}

trait UiFactory {
    fn create_button(&self) -> Box<dyn Button>;
    fn create_checkbox(&self) -> Box<dyn Checkbox>;
}

struct WinButton;
impl Button for WinButton {
    fn render(&self) -> String {
        "Windows Button".to_string()
    }
}

struct WinCheckbox;
impl Checkbox for WinCheckbox {
    fn render(&self) -> String {
        "Windows Checkbox".to_string()
    }
}

struct MacButton;
impl Button for MacButton {
    fn render(&self) -> String {
        "macOS Button".to_string()
    }
}

struct MacCheckbox;
impl Checkbox for MacCheckbox {
    fn render(&self) -> String {
        "macOS Checkbox".to_string()
    }
}

struct WindowsFactory;
impl UiFactory for WindowsFactory {
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(WinButton)
    }
    fn create_checkbox(&self) -> Box<dyn Checkbox> {
        Box::new(WinCheckbox)
    }
}

struct MacFactory;
impl UiFactory for MacFactory {
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(MacButton)
    }
    fn create_checkbox(&self) -> Box<dyn Checkbox> {
        Box::new(MacCheckbox)
    }
}
```

**Usage**

```rust
fn build_ui(factory: &dyn UiFactory) -> (String, String) {
    let button = factory.create_button();
    let checkbox = factory.create_checkbox();
    (button.render(), checkbox.render())
}

let factory: Box<dyn UiFactory> = Box::new(MacFactory);
let (btn, chk) = build_ui(&*factory);
println!("{btn}, {chk}");
```

##### C\#

**Implementation**

```csharp
using System;

public interface IButton
{
    string Render();
}

public interface ICheckbox
{
    string Render();
}

public interface IUiFactory
{
    IButton CreateButton();
    ICheckbox CreateCheckbox();
}

public class WinButton : IButton
{
    public string Render() => "Windows Button";
}

public class WinCheckbox : ICheckbox
{
    public string Render() => "Windows Checkbox";
}

public class MacButton : IButton
{
    public string Render() => "macOS Button";
}

public class MacCheckbox : ICheckbox
{
    public string Render() => "macOS Checkbox";
}

public class WindowsFactory : IUiFactory
{
    public IButton CreateButton() => new WinButton();
    public ICheckbox CreateCheckbox() => new WinCheckbox();
}

public class MacFactory : IUiFactory
{
    public IButton CreateButton() => new MacButton();
    public ICheckbox CreateCheckbox() => new MacCheckbox();
}
```

**Usage**

```csharp
IUiFactory factory = new MacFactory();
IButton button = factory.CreateButton();
ICheckbox checkbox = factory.CreateCheckbox();
Console.WriteLine($"{button.Render()}, {checkbox.Render()}");
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod

class Button(ABC):
    @abstractmethod
    def render(self) -> str: ...

class Checkbox(ABC):
    @abstractmethod
    def render(self) -> str: ...

class UiFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button: ...

    @abstractmethod
    def create_checkbox(self) -> Checkbox: ...

class WinButton(Button):
    def render(self) -> str:
        return "Windows Button"

class WinCheckbox(Checkbox):
    def render(self) -> str:
        return "Windows Checkbox"

class MacButton(Button):
    def render(self) -> str:
        return "macOS Button"

class MacCheckbox(Checkbox):
    def render(self) -> str:
        return "macOS Checkbox"

class WindowsFactory(UiFactory):
    def create_button(self) -> Button:
        return WinButton()

    def create_checkbox(self) -> Checkbox:
        return WinCheckbox()

class MacFactory(UiFactory):
    def create_button(self) -> Button:
        return MacButton()

    def create_checkbox(self) -> Checkbox:
        return MacCheckbox()
```

**Usage**

```python
factory: UiFactory = MacFactory()
button = factory.create_button()
checkbox = factory.create_checkbox()
print(f"{button.render()}, {checkbox.render()}")
```

<a id="15-prototype"></a>

### 1.5. Prototype

| **Who**  | Systems that need to create new objects by copying existing instances rather than constructing from scratch. |
|----------|--------|
| **What** | Specifies the kind of object to create using a prototypical instance, and creates new objects by cloning that prototype. |
| **When** | When object creation is expensive (complex initialization, database lookups, deep object graphs), when the system should be independent of how its products are created, or when you want to avoid a parallel hierarchy of factory classes just to produce variants. |
| **Where**| Graphic editors (duplicating shapes), game engines (spawning pre-configured entities), configuration systems (deriving new configs from templates), and caching layers that serve copies of expensive-to-compute objects. |
| **Why**  | Avoids costly re-initialization by copying pre-built state. Eliminates the need for subclass-per-variant factories — new variants are created at runtime by cloning and tweaking. Decouples the client from the concrete classes of the objects it copies. |
| **How**  | Define a clone interface (or use a language-provided mechanism like `Clone` in Rust, `ICloneable` / typed `Clone()` methods in C#, or `copy.deepcopy` / `__copy__`/`__deepcopy__` in Python). Each concrete prototype implements deep cloning. A registry can hold named prototypes that clients look up and clone on demand. |

The Prototype pattern creates new objects by copying an existing instance — the prototype — rather than invoking a constructor. The client asks the prototype to clone itself and receives a new, independent copy with the same state. This is particularly valuable when building an object from scratch is expensive (complex computation, I/O, deep nested graphs) or when the exact configuration of the object is determined at runtime rather than compile time.

The key participants are the **prototype interface** (declares the clone method), **concrete prototypes** (classes that implement cloning), and optionally a **prototype registry** (a lookup table of named prototypes that clients can retrieve and clone). The registry decouples the client from knowing which concrete class it is copying.

Deep versus shallow copying is the central implementation concern. A shallow copy shares references with the original, meaning mutations to nested objects propagate to both copies. A deep copy recursively duplicates the entire object graph. Most Prototype usages require deep copies to guarantee independence; choosing the wrong strategy introduces subtle aliasing bugs.

<a id="151-paradigm-fit"></a>

#### 1.5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — immutable data structures are inherently safe to share; structural sharing makes "cloning" nearly free, and variant creation is a record-update expression. |
| Data-Oriented | **Workable** — bulk-copying rows or component arrays from a template archetype; useful for spawning entities from prefab data, though memcpy semantics require care with referenced data. |
| OOP | **Natural fit** — clone methods on objects, often combined with a prototype registry for runtime variant management. |
| Procedural | **Workable** — struct copy plus manual deep-copy of heap-allocated fields; no polymorphism required if types are known statically. |
| Reactive | **Uncommon** — streams and observables are typically constructed via operators, not cloned; however, snapshot-and-fork of stream state can serve similar purposes. |

<a id="152-benefits"></a>

#### 1.5.2. Benefits

- Avoids expensive re-initialization — cloning a pre-built object is often faster than constructing one from scratch.
- Eliminates subclass proliferation — new variants are created by cloning and modifying, not by writing new factory classes.
- Decouples the client from concrete product classes — the client only knows the prototype interface.

<a id="153-trade-offs"></a>

#### 1.5.3. Trade-offs

- Deep cloning complex object graphs (circular references, file handles, sockets) can be difficult to implement correctly.
- Each concrete prototype must support cloning — retrofitting clone into an existing hierarchy may require touching every class.
- Shallow-copy defaults in many languages silently share mutable state, introducing aliasing bugs when deep copy was intended.

<a id="154-examples"></a>

#### 1.5.4. Examples

##### Rust

Rust's `Clone` trait is the idiomatic Prototype mechanism. Deriving `Clone` gives a deep copy for types composed entirely of owned data.

**Implementation**

```rust
use std::collections::HashMap;

#[derive(Clone, Debug)]
enum ShapeKind {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

#[derive(Clone, Debug)]
struct Shape {
    kind: ShapeKind,
    x: f64,
    y: f64,
    color: String,
}

struct ShapeRegistry {
    prototypes: HashMap<String, Shape>,
}

impl ShapeRegistry {
    fn new() -> Self {
        Self { prototypes: HashMap::new() }
    }

    fn register(&mut self, name: &str, shape: Shape) {
        self.prototypes.insert(name.to_string(), shape);
    }

    fn create(&self, name: &str) -> Option<Shape> {
        self.prototypes.get(name).cloned()
    }
}
```

**Usage**

```rust
let mut registry = ShapeRegistry::new();
registry.register("red-circle", Shape {
    kind: ShapeKind::Circle { radius: 10.0 },
    x: 0.0,
    y: 0.0,
    color: "red".to_string(),
});

let mut circle = registry.create("red-circle").unwrap();
circle.x = 50.0;
circle.y = 30.0;
println!("{circle:?}");
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public abstract class Shape : ICloneable
{
    public double X { get; set; }
    public double Y { get; set; }
    public string Color { get; set; } = "";

    public abstract object Clone();
    public abstract string Describe();
}

public class Circle : Shape
{
    public double Radius { get; set; }

    public override object Clone() =>
        new Circle { X = X, Y = Y, Color = Color, Radius = Radius };

    public override string Describe() =>
        $"Circle(r={Radius}, pos=({X},{Y}), color={Color})";
}

public class Rectangle : Shape
{
    public double Width { get; set; }
    public double Height { get; set; }

    public override object Clone() =>
        new Rectangle { X = X, Y = Y, Color = Color, Width = Width, Height = Height };

    public override string Describe() =>
        $"Rect({Width}x{Height}, pos=({X},{Y}), color={Color})";
}

public class ShapeRegistry
{
    private readonly Dictionary<string, Shape> _prototypes = new();

    public void Register(string name, Shape shape) => _prototypes[name] = shape;

    public Shape Create(string name) => (Shape)_prototypes[name].Clone();
}
```

**Usage**

```csharp
var registry = new ShapeRegistry();
registry.Register("red-circle", new Circle { Radius = 10, X = 0, Y = 0, Color = "red" });

Shape circle = registry.Create("red-circle");
circle.X = 50;
circle.Y = 30;
Console.WriteLine(circle.Describe());
```

##### Python

Python's `copy.deepcopy` provides built-in deep cloning. For finer control, implement `__copy__` and `__deepcopy__`.

**Implementation**

```python
import copy
from dataclasses import dataclass, field

@dataclass
class Shape:
    x: float = 0.0
    y: float = 0.0
    color: str = ""

    def clone(self) -> "Shape":
        return copy.deepcopy(self)

@dataclass
class Circle(Shape):
    radius: float = 0.0

@dataclass
class Rectangle(Shape):
    width: float = 0.0
    height: float = 0.0

class ShapeRegistry:
    def __init__(self) -> None:
        self._prototypes: dict[str, Shape] = {}

    def register(self, name: str, shape: Shape) -> None:
        self._prototypes[name] = shape

    def create(self, name: str) -> Shape:
        return self._prototypes[name].clone()
```

**Usage**

```python
registry = ShapeRegistry()
registry.register("red-circle", Circle(radius=10.0, color="red"))

circle = registry.create("red-circle")
circle.x = 50.0
circle.y = 30.0
print(circle)
```

<a id="16-object-pool"></a>

### 1.6. Object Pool

| **Who**  | Infrastructure and server code that repeatedly acquires and releases expensive-to-create resources. |
|----------|--------|
| **What** | Manages a reusable set of pre-initialized objects, lending them out on request and reclaiming them when the client is done — avoiding the cost of repeated creation and destruction. |
| **When** | When object creation is expensive (network connections, threads, large buffers), the rate of acquisition is high, and the number of simultaneously needed instances is bounded. |
| **Where**| Database connection pools, HTTP client pools, thread pools, GPU buffer pools, game entity pools (bullets, particles), and any context where allocation/deallocation dominates runtime cost. |
| **Why**  | Amortizes the cost of initialization across many uses. Bounds resource consumption by capping pool size. Reduces garbage-collection pressure by reusing allocations rather than creating transient objects. |
| **How**  | Maintain a collection of idle objects. When a client requests one, hand out an idle instance (or create a new one if below capacity). When the client returns it, reset its state and place it back in the idle collection. If all instances are in use and the pool is at capacity, either block, return an error, or grow the pool depending on the chosen policy. |

The Object Pool pattern keeps a cache of reusable objects that are expensive to create, lending them to clients on demand and reclaiming them when the client is finished. Instead of paying the initialization cost on every request — opening a TCP connection, spawning a thread, allocating a large buffer — the pool creates a bounded number of instances up front (or lazily) and cycles them through active and idle states.

The key participants are the **pool** (manages the collection of reusable objects and enforces capacity limits), the **reusable resource** (the expensive-to-create object being pooled), and the **client** (which checks out a resource, uses it, and returns it). A well-designed pool also provides a reset mechanism that restores each returned object to a clean state, preventing state leakage between borrowers.

Choosing the right pool policy is critical. A fixed-size pool blocks (or errors) when exhausted, providing backpressure; an elastic pool grows under load but risks unbounded resource consumption. Most production pools combine a core idle set with a maximum cap, and add health-checking (evict broken connections) and idle-timeout eviction (shrink during quiet periods). RAII wrappers or `try-with-resources` / `using` blocks ensure resources are returned even if the client throws an exception.

<a id="161-domain-context"></a>

#### 1.6.1. Domain Context

Object Pool is primarily relevant in infrastructure and server contexts — database connection pools, HTTP client pools, thread pools, and GPU buffer management. It is rarely encountered in simple CLI tools, scripts, or applications where object creation is cheap and the allocation rate is low.

<a id="162-paradigm-fit"></a>

#### 1.6.2. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Workable** — pools are inherently stateful (mutable idle/active sets), which clashes with purity; they can be modeled as managed effects or wrapped behind a functional resource-acquisition API. |
| Data-Oriented | **Natural fit** — pre-allocated arrays of reusable slots map directly to contiguous memory pools; entity/component pools are a core DOD technique. |
| OOP | **Natural fit** — the pool is an object managing a collection, with checkout/return methods and encapsulated lifecycle logic. |
| Procedural | **Adapts well** — a fixed-size array plus an index or free-list; straightforward to implement without objects. |
| Reactive | **Adapts well** — resource acquisition can be modeled as an observable that emits a resource, with disposal triggering return to the pool; backpressure maps naturally to pool exhaustion. |

<a id="163-benefits"></a>

#### 1.6.3. Benefits

- Amortizes expensive initialization — the cost of creating a connection or thread is paid once, not per request.
- Bounds resource consumption with a fixed maximum pool size, providing natural backpressure.
- Reduces garbage-collection pressure by reusing allocations instead of creating short-lived objects.

<a id="164-trade-offs"></a>

#### 1.6.4. Trade-offs

- State leakage between borrowers if the reset mechanism is incomplete — a returned object may carry dirty state.
- Pool sizing requires tuning: too small starves throughput, too large wastes memory and OS resources.
- Added complexity for health-checking (evicting broken resources), idle-timeout eviction, and thread-safe checkout/return.

<a id="165-examples"></a>

#### 1.6.5. Examples

##### Rust

Rust's ownership model pairs well with pooling — a guard type that returns the resource on `Drop` makes leaks impossible.

**Implementation**

```rust
use std::sync::{Arc, Mutex};

pub struct Pool<T> {
    idle: Mutex<Vec<T>>,
    create: Box<dyn Fn() -> T + Send + Sync>,
    max_size: usize,
    total: Mutex<usize>,
}

pub struct PoolGuard<T> {
    value: Option<T>,
    pool: Arc<Pool<T>>,
}

impl<T> Pool<T> {
    pub fn new(max_size: usize, create: impl Fn() -> T + Send + Sync + 'static) -> Arc<Self> {
        Arc::new(Self {
            idle: Mutex::new(Vec::new()),
            create: Box::new(create),
            max_size,
            total: Mutex::new(0),
        })
    }

    pub fn acquire(self: &Arc<Self>) -> Option<PoolGuard<T>> {
        let item = {
            let mut idle = self.idle.lock().unwrap();
            idle.pop()
        };

        let item = match item {
            Some(item) => item,
            None => {
                let mut total = self.total.lock().unwrap();
                if *total >= self.max_size {
                    return None;
                }
                *total += 1;
                (self.create)()
            }
        };

        Some(PoolGuard { value: Some(item), pool: Arc::clone(self) })
    }

    fn release(&self, item: T) {
        self.idle.lock().unwrap().push(item);
    }
}

impl<T> std::ops::Deref for PoolGuard<T> {
    type Target = T;
    fn deref(&self) -> &T {
        self.value.as_ref().unwrap()
    }
}

impl<T> Drop for PoolGuard<T> {
    fn drop(&mut self) {
        if let Some(item) = self.value.take() {
            self.pool.release(item);
        }
    }
}
```

**Usage**

```rust
let pool = Pool::new(4, || {
    println!("Creating expensive resource");
    Vec::<u8>::with_capacity(1024)
});

let r1 = pool.acquire().expect("pool exhausted");
println!("Resource len: {}", r1.len());
drop(r1);

let r2 = pool.acquire().expect("pool exhausted");
println!("Reused resource capacity: {}", r2.capacity());
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Concurrent;

public class Pool<T> where T : class
{
    private readonly ConcurrentBag<T> _idle = new();
    private readonly Func<T> _create;
    private readonly int _maxSize;
    private int _total;

    public Pool(int maxSize, Func<T> create)
    {
        _maxSize = maxSize;
        _create = create;
    }

    public PoolLease<T>? Acquire()
    {
        if (_idle.TryTake(out var item))
            return new PoolLease<T>(item, this);

        if (System.Threading.Interlocked.Increment(ref _total) <= _maxSize)
            return new PoolLease<T>(_create(), this);

        System.Threading.Interlocked.Decrement(ref _total);
        return null;
    }

    internal void Release(T item) => _idle.Add(item);
}

public sealed class PoolLease<T> : IDisposable where T : class
{
    public T Value { get; }
    private readonly Pool<T> _pool;
    private bool _disposed;

    internal PoolLease(T value, Pool<T> pool)
    {
        Value = value;
        _pool = pool;
    }

    public void Dispose()
    {
        if (_disposed) return;
        _disposed = true;
        _pool.Release(Value);
    }
}
```

**Usage**

```csharp
var pool = new Pool<byte[]>(4, () =>
{
    Console.WriteLine("Creating expensive resource");
    return new byte[1024];
});

using (var lease = pool.Acquire()!)
{
    Console.WriteLine($"Resource length: {lease.Value.Length}");
}

using (var lease = pool.Acquire()!)
{
    Console.WriteLine($"Reused resource length: {lease.Value.Length}");
}
```

##### Python

Python's context manager protocol (`__enter__`/`__exit__`) ensures resources are returned to the pool even when exceptions occur.

**Implementation**

```python
from collections import deque
from collections.abc import Callable, Generator
from contextlib import contextmanager


class Pool[T]:
    def __init__(self, max_size: int, create: Callable[[], T]) -> None:
        self._idle: deque[T] = deque()
        self._create = create
        self._max_size = max_size
        self._total = 0

    @contextmanager
    def acquire(self) -> Generator[T, None, None]:
        item = self._checkout()
        try:
            yield item
        finally:
            self._idle.append(item)

    def _checkout(self) -> T:
        if self._idle:
            return self._idle.popleft()
        if self._total >= self._max_size:
            raise RuntimeError("pool exhausted")
        self._total += 1
        return self._create()
```

**Usage**

```python
pool: Pool[bytearray] = Pool(4, lambda: bytearray(1024))

with pool.acquire() as buf:
    print(f"Resource length: {len(buf)}")

with pool.acquire() as buf:
    print(f"Reused resource length: {len(buf)}")
```

<a id="2-structural"></a>

## 2. Structural

Structural patterns deal with the composition of classes and objects, using inheritance and composition to form larger structures while keeping them flexible and efficient.

| Pattern | When to Use |
|---------|-------------|
| [Facade](#21-facade) | Simplifying access to a complex subsystem through one unified entry point. |
| [Adapter](#22-adapter) | Making an existing class work with an interface it wasn't designed for. |
| [Decorator](#23-decorator) | Dynamically adding behavior to an object without modifying its class. |
| [Proxy](#24-proxy) | Controlling access to another object for lazy loading, access control, or caching. |
| [Composite](#25-composite) | Treating individual objects and groups uniformly in tree structures. |
| [Bridge](#26-bridge) | Separating abstraction from implementation so both vary independently. |
| [Flyweight](#27-flyweight) | Sharing common state across many fine-grained objects to save memory. |

<a id="21-facade"></a>

### 2.1. Facade

| **Who**  | Clients that need a simple interface to a complex subsystem. |
|----------|--------|
| **What** | Provides a unified, higher-level interface to a set of interfaces in a subsystem, making the subsystem easier to use. |
| **When** | When a subsystem has many interdependent classes and clients only need a subset of its capabilities, or when you want to layer your architecture with clean entry points. |
| **Where**| Between client code and complex subsystems (e.g., a multimedia framework, a business services layer, OS kernel APIs). |
| **Why**  | Reduces coupling and the learning curve by hiding subsystem complexity behind a single, well-defined interface. Clients are shielded from subsystem changes. |
| **How**  | Create a facade object that composes (owns or references) the subsystem components. Implement methods on the facade that delegate to the appropriate subsystem objects, handling sequencing and data transformation internally. Clients interact only with the facade. |

The Facade pattern provides a single, simplified interface to a complex subsystem of classes. Rather than forcing clients to understand and orchestrate dozens of subsystem objects, the facade wraps that complexity behind one or a few straightforward methods. The client calls the facade; the facade coordinates the subsystem internally — sequencing calls, translating data, and managing dependencies between subsystem components.

The key participants are the **facade** (the simplified entry point), the **subsystem classes** (the complex internals being wrapped), and the **client** (which interacts only with the facade). Importantly, the facade does not prevent advanced clients from accessing subsystem classes directly when finer control is needed.

Facade promotes loose coupling between the client and the subsystem, reduces the learning curve for new developers, and provides a natural boundary for layering an architecture. It is not about adding new functionality — it is about simplifying access to existing functionality.

<a id="211-paradigm-fit"></a>

#### 2.1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — a module exporting simple functions that compose complex internal operations. |
| Data-Oriented | **Natural fit** — modules that hide cache-friendly data transformations behind a clean query API. |
| OOP | **Natural fit** — facade object wrapping and orchestrating subsystem instances. |
| Procedural | **Natural fit** — wrapper functions that sequence subsystem calls behind a simple API. |
| Reactive | **Natural fit** — exposes simple subscribe/observe entry points over complex internal pipelines. |

<a id="212-benefits"></a>

#### 2.1.2. Benefits

- Reduces coupling — the client depends on one facade rather than many subsystem classes.
- Lowers the learning curve by exposing only the operations most clients need.
- Provides a natural layering boundary; the subsystem can evolve internally without breaking clients.

<a id="213-trade-offs"></a>

#### 2.1.3. Trade-offs

- Risk of becoming a "god object" if the facade accumulates too many responsibilities over time.
- May hide functionality that advanced clients need, forcing them to bypass the facade and couple to the subsystem directly.
- Adds an extra layer of indirection between the client and the actual work.

<a id="214-examples"></a>

#### 2.1.4. Examples

##### Rust

**Implementation**

```rust
struct Cpu;
impl Cpu {
    fn freeze(&self) { println!("CPU freezing"); }
    fn jump(&self, position: u32) { println!("CPU jumping to {position}"); }
    fn execute(&self) { println!("CPU executing"); }
}

struct Memory;
impl Memory {
    fn load(&self, position: u32, data: &[u8]) {
        println!("Memory loading {} bytes at {position}", data.len());
    }
}

struct HardDrive;
impl HardDrive {
    fn read(&self, lba: u32, size: u32) -> Vec<u8> {
        println!("HardDrive reading {size} bytes from LBA {lba}");
        vec![0; size as usize]
    }
}

struct ComputerFacade {
    cpu: Cpu,
    memory: Memory,
    hard_drive: HardDrive,
}

impl ComputerFacade {
    fn new() -> Self {
        ComputerFacade { cpu: Cpu, memory: Memory, hard_drive: HardDrive }
    }

    fn start(&self) {
        self.cpu.freeze();
        let boot_data = self.hard_drive.read(0, 1024);
        self.memory.load(0, &boot_data);
        self.cpu.jump(0);
        self.cpu.execute();
    }
}
```

**Usage**

```rust
let computer = ComputerFacade::new();
computer.start();
```

##### C\#

**Implementation**

```csharp
using System;

public class Cpu
{
    public void Freeze() => Console.WriteLine("CPU freezing");
    public void Jump(uint position) => Console.WriteLine($"CPU jumping to {position}");
    public void Execute() => Console.WriteLine("CPU executing");
}

public class Memory
{
    public void Load(uint position, byte[] data) =>
        Console.WriteLine($"Memory loading {data.Length} bytes at {position}");
}

public class HardDrive
{
    public byte[] Read(uint lba, uint size)
    {
        Console.WriteLine($"HardDrive reading {size} bytes from LBA {lba}");
        return new byte[size];
    }
}

public class ComputerFacade
{
    private readonly Cpu _cpu = new();
    private readonly Memory _memory = new();
    private readonly HardDrive _hardDrive = new();

    public void Start()
    {
        _cpu.Freeze();
        byte[] bootData = _hardDrive.Read(0, 1024);
        _memory.Load(0, bootData);
        _cpu.Jump(0);
        _cpu.Execute();
    }
}
```

**Usage**

```csharp
var computer = new ComputerFacade();
computer.Start();
```

##### Python

**Implementation**

```python
class Cpu:
    def freeze(self) -> None:
        print("CPU freezing")

    def jump(self, position: int) -> None:
        print(f"CPU jumping to {position}")

    def execute(self) -> None:
        print("CPU executing")

class Memory:
    def load(self, position: int, data: bytes) -> None:
        print(f"Memory loading {len(data)} bytes at {position}")

class HardDrive:
    def read(self, lba: int, size: int) -> bytes:
        print(f"HardDrive reading {size} bytes from LBA {lba}")
        return bytes(size)

class ComputerFacade:
    def __init__(self) -> None:
        self._cpu = Cpu()
        self._memory = Memory()
        self._hard_drive = HardDrive()

    def start(self) -> None:
        self._cpu.freeze()
        boot_data = self._hard_drive.read(0, 1024)
        self._memory.load(0, boot_data)
        self._cpu.jump(0)
        self._cpu.execute()
```

**Usage**

```python
computer = ComputerFacade()
computer.start()
```

<a id="22-adapter"></a>

### 2.2. Adapter

| **Who**  | Clients that need to use an existing class whose interface does not match the one they require. |
|----------|--------|
| **What** | Converts the interface of an existing class into another interface clients expect, letting incompatible classes work together. |
| **When** | When you want to reuse an existing class but its interface does not match what your code requires, and modifying the class is impossible or undesirable. |
| **Where**| Wrappers around third-party libraries, legacy code, or external APIs that must conform to your application's interface contracts. |
| **Why**  | Avoids modifying existing code (which may be impossible, risky, or a third-party dependency) while still enabling it to integrate with new code through a compatible interface. |
| **How**  | Create an adapter that holds a reference to the adaptee. Implement the target interface on the adapter, delegating each method to the corresponding adaptee method with any necessary translation of data or signatures. |

The Adapter pattern converts the interface of an existing class into the interface that clients expect, allowing classes with incompatible interfaces to collaborate without modifying their source code. The adapter acts as a translator: it wraps the existing class (the **adaptee**), implements the interface the client requires (the **target**), and maps each target method to the corresponding adaptee method — performing any necessary data transformation along the way.

There are two variants. An **object adapter** uses composition: it holds a reference to the adaptee and delegates calls to it. A **class adapter** uses multiple inheritance to combine the target and adaptee interfaces (possible in languages like C++, but not in single-inheritance languages like Java, C#, or Rust). The object adapter is far more common because it works in any language and allows adapting the adaptee's subclasses as well.

Adapter is especially useful when integrating third-party libraries, legacy systems, or external APIs whose interfaces you cannot change but need to conform to your application's contracts.

<a id="221-paradigm-fit"></a>

#### 2.2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — function wrappers and composition translate one signature to another. |
| Data-Oriented | **Workable** — transform functions convert between data layouts (AoS ↔ SoA), but less formalized as a named pattern. |
| OOP | **Natural fit** — wrapper class implementing the target interface, delegating to the adaptee. |
| Procedural | **Workable** — wrapper functions that translate calls and data between interfaces. |
| Reactive | **Natural fit** — operators like `map`/`flatMap` are adapters that translate one stream type to another. |

<a id="222-benefits"></a>

#### 2.2.2. Benefits

- Enables reuse of existing classes without modifying their source code.
- Isolates translation logic in one place — client code stays clean of conversion details.
- Can adapt entire class hierarchies: an object adapter works with the adaptee and all its subclasses.

<a id="223-trade-offs"></a>

#### 2.2.3. Trade-offs

- Adds a wrapper layer with delegation overhead (negligible in most cases, noticeable in hot paths).
- One adapter per incompatible interface can lead to many small wrapper classes.
- If the adaptee's interface changes, the adapter must change too — maintenance coupling shifts rather than disappears.

<a id="224-examples"></a>

#### 2.2.4. Examples

##### Rust

**Implementation**

```rust
trait Logger {
    fn info(&self, msg: &str);
    fn error(&self, msg: &str);
}

struct LegacyLogger;
impl LegacyLogger {
    fn log(&self, level: &str, message: &str) {
        println!("[{level}] {message}");
    }
}

struct LegacyLoggerAdapter {
    legacy: LegacyLogger,
}

impl Logger for LegacyLoggerAdapter {
    fn info(&self, msg: &str) {
        self.legacy.log("INFO", msg);
    }
    fn error(&self, msg: &str) {
        self.legacy.log("ERROR", msg);
    }
}
```

**Usage**

```rust
let logger: Box<dyn Logger> = Box::new(LegacyLoggerAdapter { legacy: LegacyLogger });
logger.info("Adapter works!");
```

##### C\#

**Implementation**

```csharp
using System;

public interface ILogger
{
    void Info(string msg);
    void Error(string msg);
}

public class LegacyLogger
{
    public void Log(string level, string message) =>
        Console.WriteLine($"[{level}] {message}");
}

public class LegacyLoggerAdapter : ILogger
{
    private readonly LegacyLogger _legacy;

    public LegacyLoggerAdapter(LegacyLogger legacy) => _legacy = legacy;

    public void Info(string msg) => _legacy.Log("INFO", msg);
    public void Error(string msg) => _legacy.Log("ERROR", msg);
}
```

**Usage**

```csharp
ILogger logger = new LegacyLoggerAdapter(new LegacyLogger());
logger.Info("Adapter works!");
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def info(self, msg: str) -> None: ...

    @abstractmethod
    def error(self, msg: str) -> None: ...

class LegacyLogger:
    def log(self, level: str, message: str) -> None:
        print(f"[{level}] {message}")

class LegacyLoggerAdapter(Logger):
    def __init__(self, legacy: LegacyLogger) -> None:
        self._legacy = legacy

    def info(self, msg: str) -> None:
        self._legacy.log("INFO", msg)

    def error(self, msg: str) -> None:
        self._legacy.log("ERROR", msg)
```

**Usage**

```python
logger: Logger = LegacyLoggerAdapter(LegacyLogger())
logger.info("Adapter works!")
```

<a id="23-decorator"></a>

### 2.3. Decorator

| **Who**  | Clients that need to extend an object's behavior at runtime without altering its class or affecting other instances. |
|----------|--------|
| **What** | Wraps an object in another object that implements the same interface, transparently adding behavior before or after delegation to the wrapped component. |
| **When** | When subclassing for every combination of features would cause a combinatorial explosion of classes, or when responsibilities need to be added and removed dynamically. |
| **Where**| I/O streams (buffering, compression, encryption layers), middleware stacks, UI component enhancement, notification channels. |
| **Why**  | Allows responsibilities to be composed and stacked at runtime, following the Open/Closed Principle — existing classes stay untouched while new behavior is layered on. |
| **How**  | Define a component interface. Both the concrete component and a decorator base implement it. The decorator base holds a reference to a component and delegates all calls. Concrete decorators extend the base, adding behavior before or after forwarding the call. |

The Decorator pattern attaches additional responsibilities to an object dynamically by wrapping it in another object that shares the same interface. The wrapper delegates every call to the wrapped component, but adds its own behavior before or after the delegation. Because the wrapper and the wrapped object share an interface, decorators can be stacked: the client sees a single component, unaware of how many layers surround it.

The key participants are the **Component** interface, the **ConcreteComponent** that provides the core behavior, the **Decorator** base (which holds a component reference and delegates to it), and **ConcreteDecorators** that override methods to inject additional logic. Each concrete decorator focuses on exactly one concern — logging, caching, input validation, encryption — making each layer small and independently testable.

A common point of confusion is the distinction between Decorator and Proxy. Both wrap another object behind the same interface, but their intent differs: Decorator adds behavior, while Proxy controls access. In practice, a decorator chain is typically assembled by the client, whereas a proxy is usually created by the system and presented in place of the real subject.

<a id="231-paradigm-fit"></a>

#### 2.3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — function composition (`f(g(x))`) is decoration; higher-order functions wrap and extend behavior without mutation. |
| Data-Oriented | **Uncommon** — behavior is attached to data pipelines rather than individual objects; component flags or bitmasks replace wrapper layers. |
| OOP | **Natural fit** — classic GoF pattern: shared interface, composition-based wrapping, polymorphic dispatch. |
| Procedural | **Workable** — function pointer chains or wrapper functions provide similar layering, though without polymorphic dispatch. |
| Reactive | **Adapts well** — operators like `map`, `tap`, `retry` are decorators on a stream, each adding behavior around the data flow. |

<a id="232-benefits"></a>

#### 2.3.2. Benefits

- Extends behavior at runtime without modifying existing code or creating subclass explosions.
- Each decorator is a small, single-responsibility class that is easy to test and reason about.
- Decorators compose freely — any combination and ordering of layers is possible.

<a id="233-trade-offs"></a>

#### 2.3.3. Trade-offs

- Deep decorator stacks produce many small objects, making debugging and stack traces harder to follow.
- The order of wrapping matters and is implicit — swapping two decorators can silently change behavior.
- Identity checks (`obj == original`) break because the outermost wrapper is a different object than the original component.

<a id="234-examples"></a>

#### 2.3.4. Examples

##### Rust

Python's `@decorator` syntax (function/class decorators) is a language feature for wrapping functions, not the GoF Decorator pattern — though the underlying idea of wrapping behavior is the same. The GoF pattern operates on objects sharing an interface; Python's `@decorator` operates on callables.

Rust uses trait objects for polymorphism. Each decorator owns a `Box<dyn Notifier>` and delegates `send` before or after adding its own behavior.

**Implementation**

```rust
trait Notifier {
    fn send(&self, message: &str);
}

struct BaseNotifier;

impl Notifier for BaseNotifier {
    fn send(&self, message: &str) {
        println!("[Email] {message}");
    }
}

struct SmsDecorator {
    inner: Box<dyn Notifier>,
}

impl Notifier for SmsDecorator {
    fn send(&self, message: &str) {
        self.inner.send(message);
        println!("[SMS] {message}");
    }
}

struct SlackDecorator {
    inner: Box<dyn Notifier>,
}

impl Notifier for SlackDecorator {
    fn send(&self, message: &str) {
        self.inner.send(message);
        println!("[Slack] {message}");
    }
}
```

**Usage**

```rust
let notifier: Box<dyn Notifier> = Box::new(SlackDecorator {
    inner: Box::new(SmsDecorator {
        inner: Box::new(BaseNotifier),
    }),
});
notifier.send("Server is down!");
```

##### C\#

**Implementation**

```csharp
using System;

public interface INotifier
{
    void Send(string message);
}

public class BaseNotifier : INotifier
{
    public void Send(string message) => Console.WriteLine($"[Email] {message}");
}

public abstract class NotifierDecorator : INotifier
{
    protected readonly INotifier Inner;
    protected NotifierDecorator(INotifier inner) => Inner = inner;
    public virtual void Send(string message) => Inner.Send(message);
}

public class SmsDecorator : NotifierDecorator
{
    public SmsDecorator(INotifier inner) : base(inner) { }
    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"[SMS] {message}");
    }
}

public class SlackDecorator : NotifierDecorator
{
    public SlackDecorator(INotifier inner) : base(inner) { }
    public override void Send(string message)
    {
        base.Send(message);
        Console.WriteLine($"[Slack] {message}");
    }
}
```

**Usage**

```csharp
INotifier notifier = new SlackDecorator(new SmsDecorator(new BaseNotifier()));
notifier.Send("Server is down!");
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class BaseNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"[Email] {message}")


class NotifierDecorator(Notifier):
    def __init__(self, inner: Notifier) -> None:
        self._inner = inner

    def send(self, message: str) -> None:
        self._inner.send(message)


class SmsDecorator(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"[SMS] {message}")


class SlackDecorator(NotifierDecorator):
    def send(self, message: str) -> None:
        super().send(message)
        print(f"[Slack] {message}")
```

**Usage**

```python
notifier = SlackDecorator(SmsDecorator(BaseNotifier()))
notifier.send("Server is down!")
```

<a id="24-proxy"></a>

### 2.4. Proxy

| **Who**  | Clients that access expensive, remote, or sensitive objects and benefit from an intermediary controlling that access. |
|----------|--------|
| **What** | Provides a surrogate or placeholder for another object to control access to it — adding lazy initialization, access control, logging, or caching without changing the real subject. |
| **When** | When creating or accessing the real object is expensive, when access must be restricted or audited, or when the object resides in a different address space. |
| **Where**| Virtual proxies (lazy image loading), protection proxies (permission checks), remote proxies (network stubs), caching proxies (memoization layers). |
| **Why**  | Defers costly operations until they are actually needed, enforces access policies in a single place, and keeps the client code unchanged since the proxy shares the real subject's interface. |
| **How**  | Define a subject interface. The real subject implements it. The proxy also implements it, holds a reference (or the means to create) the real subject, and intercepts calls to add control logic before delegating. |

The Proxy pattern places an intermediary object in front of a real subject. Both share the same interface, so the client cannot tell them apart. The proxy intercepts every call and decides what to do: it may create the real subject lazily, check permissions, cache results, log access, or forward the call to a remote service — then delegate to the real subject for the actual work.

The most common variants are the **virtual proxy** (delays expensive creation until first use), the **protection proxy** (enforces access control), the **remote proxy** (represents an object in another address space), the **caching proxy** (stores results to avoid repeated computation), and the **smart reference** (manages resource lifecycle — reference counting, locking on access, or first-use loading; e.g., `Rc`/`Arc` in Rust, `shared_ptr` in C++, `WeakReference` in C#). Despite the different motivations, the structural skeleton is the same: proxy wraps subject, both implement interface, proxy adds control logic.

The key distinction from Decorator is intent. A Decorator augments the wrapped object's behavior with additional responsibilities while preserving the same interface; a Proxy controls access to the existing behavior. In practice, a virtual proxy that lazy-loads a heavy resource is the canonical example — the client calls a method, the proxy checks whether the real object exists, creates it if not, then forwards the call.

<a id="241-paradigm-fit"></a>

#### 2.4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — lazy evaluation (thunks, `Lazy<T>`) and memoization are functional proxies; access control maps to wrapper functions. |
| Data-Oriented | **Uncommon** — data-oriented designs avoid indirection; proxies add pointer-chasing that hurts cache locality. |
| OOP | **Natural fit** — shared interface with delegating wrapper is the classic formulation. |
| Procedural | **Workable** — guard functions that check conditions before calling the real function; opaque handles act as proxies. |
| Reactive | **Adapts well** — `shareReplay` caches emissions (caching proxy), `defer` delays subscription (virtual proxy), access control operators gate streams. |

<a id="242-benefits"></a>

#### 2.4.2. Benefits

- Defers costly initialization until the object is actually needed, saving resources in cases where it may never be used.
- Centralizes cross-cutting concerns (logging, caching, access control) without modifying the real subject.
- Transparent to the client — the proxy shares the subject's interface, so no calling code needs to change.

<a id="243-trade-offs"></a>

#### 2.4.3. Trade-offs

- Adds an indirection layer that can increase response latency, especially if the proxy performs locking or network calls.
- Lazy initialization introduces first-access latency spikes that can be surprising in latency-sensitive paths.
- The proxy must stay in sync with the real subject's interface — any change to the subject requires a corresponding update.

<a id="244-examples"></a>

#### 2.4.4. Examples

##### Rust

A virtual proxy that defers expensive image loading until `display` is called for the first time.

**Implementation**

```rust
trait Image {
    fn display(&mut self);
}

struct RealImage {
    filename: String,
}

impl RealImage {
    fn new(filename: &str) -> Self {
        println!("Loading image from disk: {filename}");
        RealImage { filename: filename.to_string() }
    }
}

impl Image for RealImage {
    fn display(&mut self) {
        println!("Displaying {}", self.filename);
    }
}

struct ProxyImage {
    filename: String,
    real: Option<RealImage>,
}

impl ProxyImage {
    fn new(filename: &str) -> Self {
        ProxyImage { filename: filename.to_string(), real: None }
    }
}

impl Image for ProxyImage {
    fn display(&mut self) {
        let real = self.real.get_or_insert_with(|| RealImage::new(&self.filename));
        real.display();
    }
}
```

**Usage**

```rust
let mut image = ProxyImage::new("photo.png");
println!("Image created, not yet loaded.");
image.display();
image.display();
```

##### C\#

**Implementation**

```csharp
using System;

public interface IImage
{
    void Display();
}

public class RealImage : IImage
{
    private readonly string _filename;

    public RealImage(string filename)
    {
        _filename = filename;
        Console.WriteLine($"Loading image from disk: {_filename}");
    }

    public void Display() => Console.WriteLine($"Displaying {_filename}");
}

public class ProxyImage : IImage
{
    private readonly string _filename;
    private RealImage? _real;

    public ProxyImage(string filename) => _filename = filename;

    public void Display()
    {
        _real ??= new RealImage(_filename);
        _real.Display();
    }
}
```

**Usage**

```csharp
IImage image = new ProxyImage("photo.png");
Console.WriteLine("Image created, not yet loaded.");
image.Display();
image.Display();
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Image(ABC):
    @abstractmethod
    def display(self) -> None: ...


class RealImage(Image):
    def __init__(self, filename: str) -> None:
        self._filename = filename
        print(f"Loading image from disk: {filename}")

    def display(self) -> None:
        print(f"Displaying {self._filename}")


class ProxyImage(Image):
    def __init__(self, filename: str) -> None:
        self._filename = filename
        self._real: RealImage | None = None

    def display(self) -> None:
        if self._real is None:
            self._real = RealImage(self._filename)
        self._real.display()
```

**Usage**

```python
image = ProxyImage("photo.png")
print("Image created, not yet loaded.")
image.display()
image.display()
```

<a id="25-composite"></a>

### 2.5. Composite

| **Who**  | Clients that need to treat individual objects and groups of objects uniformly through a single interface. |
|----------|--------|
| **What** | Composes objects into tree structures to represent part-whole hierarchies, letting clients treat leaves and composites identically. |
| **When** | When the core model forms a tree (files/folders, UI widgets, organization charts) and client code should not distinguish between a single element and a group. |
| **Where**| File systems, GUI widget trees, document models (paragraphs containing runs of text), scene graphs, menu hierarchies, expression trees. |
| **Why**  | Eliminates conditional logic that checks "is this a leaf or a group?" — the uniform interface lets recursive operations propagate naturally through the tree. |
| **How**  | Define a component interface with the operations clients need. Leaf classes implement the interface directly. Composite classes also implement it but additionally hold a collection of child components, delegating operations by iterating over children. |

The Composite pattern organizes objects into tree structures where every node — whether a leaf or a branch containing other nodes — implements the same interface. The client calls an operation on the root, and the call propagates recursively: leaves perform the operation directly, while composites iterate over their children and aggregate results. This uniformity eliminates the need for type-checking conditionals scattered throughout client code.

The key participants are the **Component** interface (declaring operations that both leaves and composites support), **Leaf** (a terminal node with no children), and **Composite** (a node that stores child components and implements operations by delegating to each child). The composite's implementation of each operation typically iterates over its children, invokes the same operation on each, and combines the results (summing sizes, concatenating names, rendering nested widgets).

A design tension exists around which operations belong on the component interface. Putting child-management methods (`add`, `remove`) on the base interface maximizes transparency — clients never need to know whether they hold a leaf or composite — but means leaves must handle operations that make no sense for them. The alternative places child-management only on the composite, requiring a downcast when the client wants to add children. Most modern implementations favor the safer approach: child-management on the composite only.

<a id="251-paradigm-fit"></a>

#### 2.5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — algebraic data types (enums with variants) and recursive functions model trees directly; fold/catamorphism traverses the structure. |
| Data-Oriented | **Workable** — trees stored as flat arrays with parent/child indices avoid pointer-chasing; operations iterate linearly over the array. |
| OOP | **Natural fit** — shared interface with polymorphic dispatch makes recursive traversal seamless. |
| Procedural | **Workable** — tree nodes as structs with tagged unions; recursive functions switch on the node type. |
| Reactive | **Adapts well** — composite streams (`merge`, `combineLatest`) unify multiple sources into one, mirroring the part-whole concept. |

<a id="252-benefits"></a>

#### 2.5.2. Benefits

- Clients treat single objects and compositions uniformly — no conditional branching on type.
- New leaf or composite types can be added without changing client code that operates on the component interface.
- Recursive operations (size, render, search) propagate naturally through the tree with minimal boilerplate.

<a id="253-trade-offs"></a>

#### 2.5.3. Trade-offs

- The uniform interface may expose operations on leaves that are meaningless (e.g., `add_child` on a file), requiring no-op or error implementations.
- Deep trees with many small nodes can be expensive to traverse and difficult to debug.
- Enforcing constraints (e.g., "a composite can only hold certain leaf types") is hard when the interface is fully generic.

<a id="254-examples"></a>

#### 2.5.4. Examples

##### Rust

Rust's enums naturally model the leaf-vs-composite distinction without needing a shared trait.

**Implementation**

```rust
enum FsEntry {
    File { name: String, size: u64 },
    Directory { name: String, children: Vec<FsEntry> },
}

impl FsEntry {
    fn name(&self) -> &str {
        match self {
            FsEntry::File { name, .. } | FsEntry::Directory { name, .. } => name,
        }
    }

    fn size(&self) -> u64 {
        match self {
            FsEntry::File { size, .. } => *size,
            FsEntry::Directory { children, .. } => children.iter().map(|c| c.size()).sum(),
        }
    }

    fn print(&self, indent: usize) {
        let pad = " ".repeat(indent);
        match self {
            FsEntry::File { name, size } => println!("{pad}- {name} ({size}B)"),
            FsEntry::Directory { name, children } => {
                println!("{pad}+ {name}/");
                for child in children {
                    child.print(indent + 2);
                }
            }
        }
    }
}
```

**Usage**

```rust
let tree = FsEntry::Directory {
    name: "root".into(),
    children: vec![
        FsEntry::File { name: "readme.md".into(), size: 1024 },
        FsEntry::Directory {
            name: "src".into(),
            children: vec![
                FsEntry::File { name: "main.rs".into(), size: 2048 },
                FsEntry::File { name: "lib.rs".into(), size: 512 },
            ],
        },
    ],
};
tree.print(0);
println!("Total size: {}B", tree.size());
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public abstract class FsEntry
{
    public string Name { get; }
    protected FsEntry(string name) => Name = name;
    public abstract long Size { get; }
    public abstract void Print(int indent = 0);
}

public class File : FsEntry
{
    private readonly long _size;
    public File(string name, long size) : base(name) => _size = size;
    public override long Size => _size;
    public override void Print(int indent = 0) =>
        Console.WriteLine($"{new string(' ', indent)}- {Name} ({Size}B)");
}

public class Directory : FsEntry
{
    private readonly List<FsEntry> _children = new();
    public Directory(string name) : base(name) { }
    public void Add(FsEntry entry) => _children.Add(entry);
    public override long Size => _children.Sum(c => c.Size);
    public override void Print(int indent = 0)
    {
        Console.WriteLine($"{new string(' ', indent)}+ {Name}/");
        foreach (var child in _children)
            child.Print(indent + 2);
    }
}
```

**Usage**

```csharp
var root = new Directory("root");
root.Add(new File("readme.md", 1024));
var src = new Directory("src");
src.Add(new File("main.cs", 2048));
src.Add(new File("utils.cs", 512));
root.Add(src);
root.Print();
Console.WriteLine($"Total size: {root.Size}B");
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class FsEntry(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def size(self) -> int: ...

    @abstractmethod
    def print_tree(self, indent: int = 0) -> None: ...


class File(FsEntry):
    def __init__(self, name: str, size: int) -> None:
        super().__init__(name)
        self._size = size

    def size(self) -> int:
        return self._size

    def print_tree(self, indent: int = 0) -> None:
        print(f"{' ' * indent}- {self.name} ({self._size}B)")


class Directory(FsEntry):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._children: list[FsEntry] = []

    def add(self, entry: FsEntry) -> None:
        self._children.append(entry)

    def size(self) -> int:
        return sum(child.size() for child in self._children)

    def print_tree(self, indent: int = 0) -> None:
        print(f"{' ' * indent}+ {self.name}/")
        for child in self._children:
            child.print_tree(indent + 2)
```

**Usage**

```python
root = Directory("root")
root.add(File("readme.md", 1024))
src = Directory("src")
src.add(File("main.py", 2048))
src.add(File("utils.py", 512))
root.add(src)
root.print_tree()
print(f"Total size: {root.size()}B")
```

<a id="26-bridge"></a>

### 2.6. Bridge

| **Who**  | Developers who face a combinatorial explosion of subclasses because two or more independent dimensions of variation are entangled in a single hierarchy. |
|----------|--------|
| **What** | Separates an abstraction from its implementation so both can evolve independently, connected at runtime through composition rather than inheritance. |
| **When** | When a class varies along two or more orthogonal axes (e.g., shape × rendering engine) and subclassing every combination is impractical. |
| **Where**| UI toolkit renderers (platform-independent widgets × OS-specific drawing), device drivers, persistence layers (domain model × database backend), messaging systems (message type × transport). |
| **Why**  | Prevents N × M subclass explosion by factoring the two dimensions into separate hierarchies linked by composition, so each side can be extended without affecting the other. |
| **How**  | Define an abstraction interface that holds a reference to an implementor interface. Concrete abstractions extend the abstraction. Concrete implementors implement the implementor interface. The abstraction delegates platform-specific work to its implementor. |

The Bridge pattern decouples an abstraction (the high-level interface a client uses) from its implementation (the low-level work that actually happens), allowing both to vary independently. Without Bridge, combining M abstractions with N implementations produces M × N concrete classes. Bridge reduces this to M + N by giving the abstraction a reference to an implementor object and delegating the implementation-specific work.

The key participants are the **Abstraction** (high-level API the client calls), the **RefinedAbstraction** (extensions of the abstraction with additional logic), the **Implementor** interface (low-level operations that the abstraction delegates to), and **ConcreteImplementors** (actual implementations of those operations). At runtime, the client picks one concrete abstraction and one concrete implementor, composing them freely.

Bridge differs from Strategy in scope: Strategy swaps one algorithm within a class, while Bridge separates two entire hierarchies so both sides can grow independently. Bridge is often established early in design to prevent a hierarchy from splitting along two axes, whereas Adapter is applied retroactively to make incompatible interfaces work together.

<a id="261-paradigm-fit"></a>

#### 2.6.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — pass implementation functions (or a record of functions) to the abstraction; higher-order functions bridge the two layers. |
| Data-Oriented | **Workable** — separate data tables for abstraction state and implementation state, joined by an ID; avoids virtual dispatch. |
| OOP | **Natural fit** — two class hierarchies connected by composition, the canonical GoF formulation. |
| Procedural | **Workable** — struct holding a function-pointer table (vtable) for the implementation; abstractions call through the table. |
| Reactive | **Adapts well** — the abstraction emits events; the implementor subscribes and performs platform-specific work, decoupling the stream topology from the effect execution. |

<a id="262-benefits"></a>

#### 2.6.2. Benefits

- Eliminates M × N subclass explosion — each dimension grows independently.
- Implementation can be swapped or selected at runtime without altering abstraction code.
- Hides implementation details from the client, strengthening encapsulation across the boundary.

<a id="263-trade-offs"></a>

#### 2.6.3. Trade-offs

- Adds structural complexity with two parallel hierarchies and an indirection between them.
- The right split point between abstraction and implementation must be identified early; refactoring later is costly.
- Over-engineering risk when only one implementation exists or the two axes are unlikely to vary independently.

<a id="264-examples"></a>

#### 2.6.4. Examples

##### Rust

**Implementation**

```rust
trait Renderer {
    fn render_circle(&self, x: f64, y: f64, radius: f64);
    fn render_rect(&self, x: f64, y: f64, width: f64, height: f64);
}

struct VectorRenderer;
impl Renderer for VectorRenderer {
    fn render_circle(&self, x: f64, y: f64, radius: f64) {
        println!("Vector circle at ({x},{y}) r={radius}");
    }
    fn render_rect(&self, x: f64, y: f64, width: f64, height: f64) {
        println!("Vector rect at ({x},{y}) {width}x{height}");
    }
}

struct RasterRenderer;
impl Renderer for RasterRenderer {
    fn render_circle(&self, x: f64, y: f64, radius: f64) {
        println!("Raster circle at ({x},{y}) r={radius}");
    }
    fn render_rect(&self, x: f64, y: f64, width: f64, height: f64) {
        println!("Raster rect at ({x},{y}) {width}x{height}");
    }
}

trait Shape {
    fn draw(&self);
}

struct Circle<'a> {
    x: f64,
    y: f64,
    radius: f64,
    renderer: &'a dyn Renderer,
}

impl Shape for Circle<'_> {
    fn draw(&self) {
        self.renderer.render_circle(self.x, self.y, self.radius);
    }
}

struct Rectangle<'a> {
    x: f64,
    y: f64,
    width: f64,
    height: f64,
    renderer: &'a dyn Renderer,
}

impl Shape for Rectangle<'_> {
    fn draw(&self) {
        self.renderer.render_rect(self.x, self.y, self.width, self.height);
    }
}
```

**Usage**

```rust
let vector = VectorRenderer;
let raster = RasterRenderer;

let c1 = Circle { x: 1.0, y: 2.0, radius: 5.0, renderer: &vector };
let r1 = Rectangle { x: 0.0, y: 0.0, width: 10.0, height: 4.0, renderer: &raster };
let c2 = Circle { x: 3.0, y: 3.0, radius: 2.5, renderer: &raster };

let shapes: Vec<&dyn Shape> = vec![&c1, &r1, &c2];

for shape in &shapes {
    shape.draw();
}
```

##### C\#

**Implementation**

```csharp
using System;

public interface IRenderer
{
    void RenderCircle(double x, double y, double radius);
    void RenderRect(double x, double y, double width, double height);
}

public class VectorRenderer : IRenderer
{
    public void RenderCircle(double x, double y, double radius) =>
        Console.WriteLine($"Vector circle at ({x},{y}) r={radius}");
    public void RenderRect(double x, double y, double width, double height) =>
        Console.WriteLine($"Vector rect at ({x},{y}) {width}x{height}");
}

public class RasterRenderer : IRenderer
{
    public void RenderCircle(double x, double y, double radius) =>
        Console.WriteLine($"Raster circle at ({x},{y}) r={radius}");
    public void RenderRect(double x, double y, double width, double height) =>
        Console.WriteLine($"Raster rect at ({x},{y}) {width}x{height}");
}

public abstract class Shape
{
    protected readonly IRenderer Renderer;
    protected Shape(IRenderer renderer) => Renderer = renderer;
    public abstract void Draw();
}

public class Circle : Shape
{
    private readonly double _x, _y, _radius;
    public Circle(double x, double y, double radius, IRenderer renderer)
        : base(renderer) => (_x, _y, _radius) = (x, y, radius);
    public override void Draw() => Renderer.RenderCircle(_x, _y, _radius);
}

public class Rect : Shape
{
    private readonly double _x, _y, _width, _height;
    public Rect(double x, double y, double width, double height, IRenderer renderer)
        : base(renderer) => (_x, _y, _width, _height) = (x, y, width, height);
    public override void Draw() => Renderer.RenderRect(_x, _y, _width, _height);
}
```

**Usage**

```csharp
IRenderer vector = new VectorRenderer();
IRenderer raster = new RasterRenderer();

Shape[] shapes =
{
    new Circle(1, 2, 5, vector),
    new Rect(0, 0, 10, 4, raster),
    new Circle(3, 3, 2.5, raster),
};

foreach (var shape in shapes)
    shape.Draw();
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Renderer(ABC):
    @abstractmethod
    def render_circle(self, x: float, y: float, radius: float) -> None: ...

    @abstractmethod
    def render_rect(self, x: float, y: float, w: float, h: float) -> None: ...


class VectorRenderer(Renderer):
    def render_circle(self, x: float, y: float, radius: float) -> None:
        print(f"Vector circle at ({x},{y}) r={radius}")

    def render_rect(self, x: float, y: float, w: float, h: float) -> None:
        print(f"Vector rect at ({x},{y}) {w}x{h}")


class RasterRenderer(Renderer):
    def render_circle(self, x: float, y: float, radius: float) -> None:
        print(f"Raster circle at ({x},{y}) r={radius}")

    def render_rect(self, x: float, y: float, w: float, h: float) -> None:
        print(f"Raster rect at ({x},{y}) {w}x{h}")


class Shape(ABC):
    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer

    @abstractmethod
    def draw(self) -> None: ...


class Circle(Shape):
    def __init__(self, x: float, y: float, radius: float, renderer: Renderer) -> None:
        super().__init__(renderer)
        self._x = x
        self._y = y
        self._radius = radius

    def draw(self) -> None:
        self._renderer.render_circle(self._x, self._y, self._radius)


class Rectangle(Shape):
    def __init__(self, x: float, y: float, w: float, h: float, renderer: Renderer) -> None:
        super().__init__(renderer)
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def draw(self) -> None:
        self._renderer.render_rect(self._x, self._y, self._w, self._h)
```

**Usage**

```python
vector = VectorRenderer()
raster = RasterRenderer()

shapes: list[Shape] = [
    Circle(1, 2, 5, vector),
    Rectangle(0, 0, 10, 4, raster),
    Circle(3, 3, 2.5, raster),
]

for shape in shapes:
    shape.draw()
```

<a id="27-flyweight"></a>

### 2.7. Flyweight

| **Who**  | Systems that manage a very large number of fine-grained objects with substantial shared state. |
|----------|--------|
| **What** | Shares common (intrinsic) state across many objects to drastically reduce memory consumption, while keeping unique (extrinsic) state external. |
| **When** | When an application creates millions of objects that share most of their data, and the memory cost of storing redundant copies is prohibitive. |
| **Where**| Text renderers (glyph objects sharing font/style), game engines (tree/particle types shared across thousands of instances), GUI toolkits, caching and interning systems. |
| **Why**  | Turns O(n) memory for n objects into O(k) for k unique states plus O(n) for lightweight references, making large-scale object populations feasible. |
| **How**  | Split object state into intrinsic (shared, immutable) and extrinsic (unique, supplied by the client). Store intrinsic state in flyweight objects managed by a factory that ensures sharing. Clients pass extrinsic state as method arguments at call time. |

The Flyweight pattern reduces memory consumption by sharing immutable, repeated state across many objects rather than duplicating it in each one. The key insight is splitting an object's data into **intrinsic state** (constant data shared among many instances — e.g., a tree species' name, color, and texture) and **extrinsic state** (data unique to each instance — e.g., a particular tree's x,y coordinates). The intrinsic state lives in a flyweight object; the extrinsic state is stored externally and passed to the flyweight when needed.

A **flyweight factory** manages the pool of shared flyweight objects. When a client requests a flyweight with certain intrinsic data, the factory checks its cache: if a matching flyweight exists, it returns it; otherwise, it creates one, caches it, and returns it. This ensures that no matter how many trees appear in a forest, only one flyweight exists per unique species.

Flyweight is most impactful when the number of objects is large and the ratio of shared to unique state is high. If each object's data is mostly unique, there is little to share and the pattern adds complexity without meaningful savings. The pattern also requires intrinsic state to be immutable — if shared state changes, every object referencing it is affected. Modern languages provide built-in flyweight mechanisms: string interning, symbol tables, and `Rc`/`Arc` shared pointers all embody the same principle.

<a id="271-paradigm-fit"></a>

#### 2.7.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — immutable values are shared by default; persistent data structures and interning are inherent flyweights. |
| Data-Oriented | **Natural fit** — SoA layouts naturally separate shared columns from per-instance columns; indices into shared tables are flyweight references. |
| OOP | **Natural fit** — flyweight factory + shared immutable objects is the canonical GoF formulation. |
| Procedural | **Workable** — shared lookup tables indexed by ID; each instance stores an index rather than a copy. |
| Reactive | **Adapts well** — shared reference data (`shareReplay`, interned config streams) avoids duplicating constant data across subscribers. |

<a id="272-benefits"></a>

#### 2.7.2. Benefits

- Dramatically reduces memory usage when many objects share most of their state.
- The flyweight factory ensures identity-based sharing — the same intrinsic data is never duplicated.
- Intrinsic immutability simplifies concurrency: shared flyweights require no synchronization.

<a id="273-trade-offs"></a>

#### 2.7.3. Trade-offs

- Splits state into intrinsic and extrinsic, spreading what was a single object across two locations and increasing code complexity.
- CPU cost increases because extrinsic state must be supplied or looked up on every method call rather than stored locally.
- Identifying the correct split between intrinsic and extrinsic state requires careful analysis; a wrong split yields little benefit or breaks encapsulation.

<a id="274-examples"></a>

#### 2.7.4. Examples

##### Rust

`Rc` provides reference-counted sharing of `TreeType` flyweights without cloning the data.

**Implementation**

```rust
use std::collections::HashMap;
use std::rc::Rc;

struct TreeType {
    name: String,
    color: String,
    texture: String,
}

impl TreeType {
    fn draw(&self, x: f64, y: f64) {
        println!(
            "Draw '{}' (color={}, texture={}) at ({x},{y})",
            self.name, self.color, self.texture
        );
    }
}

struct TreeFactory {
    cache: HashMap<String, Rc<TreeType>>,
}

impl TreeFactory {
    fn new() -> Self {
        TreeFactory { cache: HashMap::new() }
    }

    fn get_tree_type(&mut self, name: &str, color: &str, texture: &str) -> Rc<TreeType> {
        let key = format!("{name}_{color}_{texture}");
        Rc::clone(self.cache.entry(key).or_insert_with(|| {
            Rc::new(TreeType {
                name: name.to_string(),
                color: color.to_string(),
                texture: texture.to_string(),
            })
        }))
    }

    fn unique_types(&self) -> usize {
        self.cache.len()
    }
}

struct Tree {
    x: f64,
    y: f64,
    tree_type: Rc<TreeType>,
}

impl Tree {
    fn draw(&self) {
        self.tree_type.draw(self.x, self.y);
    }
}
```

**Usage**

```rust
let mut factory = TreeFactory::new();
let trees = vec![
    Tree { x: 1.0, y: 2.0, tree_type: factory.get_tree_type("Oak", "green", "rough") },
    Tree { x: 5.0, y: 3.0, tree_type: factory.get_tree_type("Oak", "green", "rough") },
    Tree { x: 8.0, y: 1.0, tree_type: factory.get_tree_type("Pine", "dark_green", "smooth") },
];
println!("Unique types: {}", factory.unique_types());
for tree in &trees {
    tree.draw();
}
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public class TreeType
{
    public string Name { get; }
    public string Color { get; }
    public string Texture { get; }

    public TreeType(string name, string color, string texture)
        => (Name, Color, Texture) = (name, color, texture);

    public void Draw(double x, double y) =>
        Console.WriteLine($"Draw '{Name}' (color={Color}, texture={Texture}) at ({x},{y})");
}

public class TreeFactory
{
    private readonly Dictionary<string, TreeType> _cache = new();

    public TreeType GetTreeType(string name, string color, string texture)
    {
        string key = $"{name}_{color}_{texture}";
        if (!_cache.TryGetValue(key, out var treeType))
        {
            treeType = new TreeType(name, color, texture);
            _cache[key] = treeType;
        }
        return treeType;
    }

    public int UniqueTypes => _cache.Count;
}

public class Tree
{
    public double X { get; }
    public double Y { get; }
    public TreeType TreeType { get; }

    public Tree(double x, double y, TreeType treeType) => (X, Y, TreeType) = (x, y, treeType);
    public void Draw() => TreeType.Draw(X, Y);
}
```

**Usage**

```csharp
var factory = new TreeFactory();
var trees = new List<Tree>
{
    new(1, 2, factory.GetTreeType("Oak", "green", "rough")),
    new(5, 3, factory.GetTreeType("Oak", "green", "rough")),
    new(8, 1, factory.GetTreeType("Pine", "dark_green", "smooth")),
};
Console.WriteLine($"Unique types: {factory.UniqueTypes}");
trees.ForEach(t => t.Draw());
```

##### Python

**Implementation**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class TreeType:
    name: str
    color: str
    texture: str

    def draw(self, x: float, y: float) -> None:
        print(f"Draw '{self.name}' (color={self.color}, texture={self.texture}) at ({x},{y})")


class TreeFactory:
    def __init__(self) -> None:
        self._cache: dict[str, TreeType] = {}

    def get_tree_type(self, name: str, color: str, texture: str) -> TreeType:
        key = f"{name}_{color}_{texture}"
        if key not in self._cache:
            self._cache[key] = TreeType(name, color, texture)
        return self._cache[key]

    @property
    def unique_types(self) -> int:
        return len(self._cache)


class Tree:
    def __init__(self, x: float, y: float, tree_type: TreeType) -> None:
        self.x = x
        self.y = y
        self.tree_type = tree_type

    def draw(self) -> None:
        self.tree_type.draw(self.x, self.y)
```

**Usage**

```python
factory = TreeFactory()
trees = [
    Tree(1, 2, factory.get_tree_type("Oak", "green", "rough")),
    Tree(5, 3, factory.get_tree_type("Oak", "green", "rough")),
    Tree(8, 1, factory.get_tree_type("Pine", "dark_green", "smooth")),
]
print(f"Unique types: {factory.unique_types}")
for tree in trees:
    tree.draw()
```

<a id="3-behavioral"></a>

## 3. Behavioral

Behavioral patterns focus on communication and responsibility between objects, defining how they interact and distribute work.

| Pattern | When to Use |
|---------|-------------|
| [Strategy](#31-strategy) | Selecting between interchangeable algorithms at runtime without conditionals. |
| [Observer](#32-observer) | Notifying multiple objects automatically when one object's state changes. |
| [Command](#33-command) | Encapsulating requests as objects for undo/redo, queuing, and logging. |
| [State](#34-state) | Letting an object change behavior when its internal state changes. |
| [Template Method](#35-template-method) | Defining an algorithm skeleton with customizable steps in subclasses. |
| [Iterator](#36-iterator) | Traversing a collection without exposing its internal representation. |
| [Chain of Responsibility](#37-chain-of-responsibility) | Passing a request along a handler chain until one processes it. |
| [Mediator](#38-mediator) | Centralizing complex inter-object communication through a coordinator. |
| [Memento](#39-memento) | Capturing and restoring an object's state without violating encapsulation. |
| [Visitor](#310-visitor) | Adding operations to a class hierarchy without modifying it. |
| [Interpreter](#311-interpreter) | Defining a grammar and interpreter for a language. |
| [Null Object](#312-null-object) | Providing a do-nothing default object to eliminate null checks. |
| [Dependency Injection](#313-dependency-injection) | Externally supplying dependencies instead of creating them internally. |

<a id="31-strategy"></a>

### 3.1. Strategy

| **Who**  | Clients that need to select an algorithm at runtime without changing the code that uses it. |
|----------|--------|
| **What** | Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it. |
| **When** | When you have multiple variants of an algorithm and want to switch between them at runtime without modifying client code. |
| **Where**| Contexts where different behaviors are needed depending on configuration or user input (sorting, compression, validation, pricing, routing). |
| **Why**  | Eliminates large conditional blocks and promotes the Open/Closed Principle — new strategies are added without modifying existing code. |
| **How**  | Define a strategy interface with a method that performs the algorithm. Implement concrete strategy classes for each variant. A context object holds a reference to the current strategy and delegates work to it; swapping the strategy changes the behavior without modifying the context. |

The Strategy pattern defines a family of interchangeable algorithms, encapsulates each one behind a common interface, and lets the client select which algorithm to use at runtime. Instead of implementing multiple behaviors inline with conditionals (`if`/`else`, `switch`), the client delegates work to a strategy object. Swapping the strategy swaps the behavior — no conditionals, no code changes in the client.

The key participants are the **strategy interface** (the contract all algorithms share), **concrete strategies** (individual algorithm implementations), and the **context** (the object that holds the current strategy and forwards requests to it). The context is agnostic to which concrete strategy it holds; it only depends on the interface.

New algorithms are added by implementing the strategy interface, leaving existing code untouched (Open/Closed Principle). Strategy is a common alternative to subclassing: instead of creating a subclass for each variant, you compose the context with a strategy at runtime.

<a id="311-paradigm-fit"></a>

#### 3.1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — first-class functions and closures are strategies by definition; the pattern is implicit. |
| Data-Oriented | **Workable** — system dispatch selects different processing functions for the same component data. |
| OOP | **Natural fit** — strategy interface with interchangeable concrete implementations. |
| Procedural | **Workable** — function pointers or callback parameters. |
| Reactive | **Natural fit** — swappable operators or stream transformations selected at subscription time. |

<a id="312-benefits"></a>

#### 3.1.2. Benefits

- Eliminates conditional blocks (`if`/`else`, `switch`) — each algorithm is self-contained and independently testable.
- New algorithms are added without modifying existing code (Open/Closed Principle).
- Context and strategies vary independently, promoting composition over inheritance.

<a id="313-trade-offs"></a>

#### 3.1.3. Trade-offs

- Clients must know the available strategies and choose between them — the decision logic moves to the caller.
- One class per algorithm can lead to many small classes for a family of simple variants.
- Adds indirection: behavior is delegated rather than inline, which can obscure straightforward logic when only two variants exist.

<a id="314-examples"></a>

#### 3.1.4. Examples

##### Rust

**Implementation**

```rust
trait SortStrategy {
    fn sort(&self, data: &mut [i32]);
}

struct BubbleSort;
impl SortStrategy for BubbleSort {
    fn sort(&self, data: &mut [i32]) {
        let n = data.len();
        for i in 0..n {
            for j in 0..n - 1 - i {
                if data[j] > data[j + 1] {
                    data.swap(j, j + 1);
                }
            }
        }
    }
}

struct InsertionSort;
impl SortStrategy for InsertionSort {
    fn sort(&self, data: &mut [i32]) {
        for i in 1..data.len() {
            let mut j = i;
            while j > 0 && data[j - 1] > data[j] {
                data.swap(j - 1, j);
                j -= 1;
            }
        }
    }
}

struct Sorter {
    strategy: Box<dyn SortStrategy>,
}

impl Sorter {
    fn new(strategy: Box<dyn SortStrategy>) -> Self {
        Sorter { strategy }
    }

    fn set_strategy(&mut self, strategy: Box<dyn SortStrategy>) {
        self.strategy = strategy;
    }

    fn sort(&self, data: &mut [i32]) {
        self.strategy.sort(data);
    }
}
```

**Usage**

```rust
let mut data = vec![3, 1, 4, 1, 5, 9, 2];
let mut sorter = Sorter::new(Box::new(BubbleSort));
sorter.sort(&mut data);

sorter.set_strategy(Box::new(InsertionSort));
sorter.sort(&mut data);
```

##### C\#

**Implementation**

```csharp
using System;

public interface ISortStrategy
{
    void Sort(int[] data);
}

public class BubbleSort : ISortStrategy
{
    public void Sort(int[] data)
    {
        int n = data.Length;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n - 1 - i; j++)
                if (data[j] > data[j + 1])
                    (data[j], data[j + 1]) = (data[j + 1], data[j]);
    }
}

public class InsertionSort : ISortStrategy
{
    public void Sort(int[] data)
    {
        for (int i = 1; i < data.Length; i++)
        {
            int j = i;
            while (j > 0 && data[j - 1] > data[j])
            {
                (data[j - 1], data[j]) = (data[j], data[j - 1]);
                j--;
            }
        }
    }
}

public class Sorter
{
    private ISortStrategy _strategy;

    public Sorter(ISortStrategy strategy) => _strategy = strategy;
    public void SetStrategy(ISortStrategy strategy) => _strategy = strategy;
    public void Sort(int[] data) => _strategy.Sort(data);
}
```

**Usage**

```csharp
int[] data = { 3, 1, 4, 1, 5, 9, 2 };
var sorter = new Sorter(new BubbleSort());
sorter.Sort(data);

sorter.SetStrategy(new InsertionSort());
sorter.Sort(data);
```

##### Python

In Python, first-class functions can replace the class-based Strategy — the context can accept any `Callable` instead of requiring a strategy interface. The class-based approach is shown here for consistency.

**Implementation**

```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> None: ...

class BubbleSort(SortStrategy):
    def sort(self, data: list[int]) -> None:
        n = len(data)
        for i in range(n):
            for j in range(n - 1 - i):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]

class InsertionSort(SortStrategy):
    def sort(self, data: list[int]) -> None:
        for i in range(1, len(data)):
            j = i
            while j > 0 and data[j - 1] > data[j]:
                data[j - 1], data[j] = data[j], data[j - 1]
                j -= 1

class Sorter:
    def __init__(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        self._strategy = strategy

    def sort(self, data: list[int]) -> None:
        self._strategy.sort(data)
```

**Usage**

```python
data = [3, 1, 4, 1, 5, 9, 2]
sorter = Sorter(BubbleSort())
sorter.sort(data)

sorter.set_strategy(InsertionSort())
sorter.sort(data)
```

<a id="32-observer"></a>

### 3.2. Observer

| **Who**  | Objects that need to be notified of state changes in another object (e.g., UI elements, logging services, cache invalidators). |
|----------|--------|
| **What** | Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. |
| **When** | When a change to one object requires updating others, and you don't want to hard-code those dependencies. |
| **Where**| Event handling systems, MVC/MVVM frameworks, GUI toolkits, reactive streams, and any publish-subscribe scenario. |
| **Why**  | Promotes loose coupling between the subject and observers. They vary independently, and new observers can be added without modifying the subject. |
| **How**  | Define an observer interface with an update method. Define a subject interface with attach, detach, and notify methods. The concrete subject maintains a collection of observers and invokes their update method whenever its state changes. |

The Observer pattern establishes a one-to-many dependency between a **subject** and its **observers**: when the subject's state changes, it automatically notifies every registered observer. Observers subscribe (attach) to the subject and can unsubscribe (detach) at any time, making the relationship fully dynamic. The subject knows its observers only through an abstract interface, so new observer types can be added without modifying the subject.

There are two notification models. In the **push model** (shown below), the subject sends the relevant state data to observers as method arguments — simple but couples observers to the specific data shape. In the **pull model**, the subject sends a minimal notification and observers query back for the data they need — more flexible but requires observers to hold a reference to the subject.

Observer is foundational to event-driven architectures, GUI frameworks (click handlers, data binding), reactive programming (`Observable`/`Subject` in Rx), and messaging systems. The pattern trades simplicity for decoupling: debugging notification chains can be harder because the flow of control is implicit rather than explicit.

<a id="321-paradigm-fit"></a>

#### 3.2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — reactive streams and event combinators express the same idea declaratively. |
| Data-Oriented | **Uncommon** — favors polling and system iteration over push-based notification; change detection is query-based. |
| OOP | **Natural fit** — subject/observer interfaces with dynamic subscription lists. |
| Procedural | **Workable** — callback registration with manual lifecycle management. |
| Reactive | **Natural fit** — Observer is the foundational primitive; `Observable`/`Subject` is the pattern formalized as a first-class construct. |

<a id="322-benefits"></a>

#### 3.2.2. Benefits

- Loose coupling — subject and observers depend only on abstractions, not on each other's concrete types.
- Dynamic subscription: observers can register and unregister at any point during runtime.
- Supports broadcast communication — a single state change notifies all interested parties.

<a id="323-trade-offs"></a>

#### 3.2.3. Trade-offs

- Notification order is generally undefined and may vary between runs or implementations.
- Lapsed listener problem: forgetting to detach an observer can cause memory leaks and phantom updates. Weak references (`weakref` in Python, `WeakReference<T>` in C#) mitigate this by allowing garbage collection of unsubscribed observers.
- Cascading notifications (one observer's update triggers another subject change) create hard-to-debug chains.
- Update cost scales linearly with observer count — each state change invokes every registered observer.

<a id="324-examples"></a>

#### 3.2.4. Examples

##### Rust

In garbage-collected languages, observers are detached by reference identity. Rust's ownership model moves the observer into the subject, making reference-based removal impractical. Using numeric IDs returned by `attach` is a straightforward alternative. For fully decoupled communication, channels (`std::sync::mpsc`) are idiomatic.

**Implementation**

```rust
use std::collections::HashMap;

trait Observer {
    fn update(&mut self, temp: f32, humidity: f32, pressure: f32);
}

struct WeatherStation {
    observers: HashMap<usize, Box<dyn Observer>>,
    next_id: usize,
    temperature: f32,
    humidity: f32,
    pressure: f32,
}

impl WeatherStation {
    fn new() -> Self {
        WeatherStation {
            observers: HashMap::new(),
            next_id: 0,
            temperature: 0.0,
            humidity: 0.0,
            pressure: 0.0,
        }
    }

    fn attach(&mut self, observer: Box<dyn Observer>) -> usize {
        let id = self.next_id;
        self.next_id += 1;
        self.observers.insert(id, observer);
        id
    }

    fn detach(&mut self, id: usize) {
        self.observers.remove(&id);
    }

    fn notify(&mut self) {
        let (t, h, p) = (self.temperature, self.humidity, self.pressure);
        for observer in self.observers.values_mut() {
            observer.update(t, h, p);
        }
    }

    fn set_measurements(&mut self, temp: f32, humidity: f32, pressure: f32) {
        self.temperature = temp;
        self.humidity = humidity;
        self.pressure = pressure;
        self.notify();
    }
}

struct CurrentConditionsDisplay;

impl Observer for CurrentConditionsDisplay {
    fn update(&mut self, temp: f32, humidity: f32, pressure: f32) {
        println!("Current conditions: {temp}°C, {humidity}% humidity, {pressure} hPa");
    }
}

struct StatisticsDisplay {
    max_temp: f32,
    min_temp: f32,
    temp_sum: f32,
    count: u32,
}

impl StatisticsDisplay {
    fn new() -> Self {
        StatisticsDisplay {
            max_temp: f32::MIN,
            min_temp: f32::MAX,
            temp_sum: 0.0,
            count: 0,
        }
    }
}

impl Observer for StatisticsDisplay {
    fn update(&mut self, temp: f32, _humidity: f32, _pressure: f32) {
        self.temp_sum += temp;
        self.count += 1;
        if temp > self.max_temp { self.max_temp = temp; }
        if temp < self.min_temp { self.min_temp = temp; }
        println!(
            "Avg/Max/Min temperature = {:.1}/{:.1}/{:.1}",
            self.temp_sum / self.count as f32, self.max_temp, self.min_temp,
        );
    }
}
```

**Usage**

```rust
let mut station = WeatherStation::new();
let _current_id = station.attach(Box::new(CurrentConditionsDisplay));
let stats_id = station.attach(Box::new(StatisticsDisplay::new()));

station.set_measurements(30.0, 65.0, 1013.25);
station.detach(stats_id);
station.set_measurements(28.0, 70.0, 1012.0);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public interface IObserver
{
    void Update(float temp, float humidity, float pressure);
}

public interface ISubject
{
    void Attach(IObserver observer);
    void Detach(IObserver observer);
    void Notify();
}

public class WeatherStation : ISubject
{
    private readonly List<IObserver> _observers = new();
    private float _temperature;
    private float _humidity;
    private float _pressure;

    public void Attach(IObserver observer) => _observers.Add(observer);
    public void Detach(IObserver observer) => _observers.Remove(observer);

    public void Notify()
    {
        foreach (var observer in _observers.ToList())
            observer.Update(_temperature, _humidity, _pressure);
    }

    public void SetMeasurements(float temperature, float humidity, float pressure)
    {
        _temperature = temperature;
        _humidity = humidity;
        _pressure = pressure;
        Notify();
    }
}

public class CurrentConditionsDisplay : IObserver
{
    public void Update(float temp, float humidity, float pressure)
    {
        Console.WriteLine($"Current conditions: {temp}°C, {humidity}% humidity, {pressure} hPa");
    }
}

public class StatisticsDisplay : IObserver
{
    private float _maxTemp = float.MinValue;
    private float _minTemp = float.MaxValue;
    private float _tempSum;
    private int _count;

    public void Update(float temp, float humidity, float pressure)
    {
        _tempSum += temp;
        _count++;
        if (temp > _maxTemp) _maxTemp = temp;
        if (temp < _minTemp) _minTemp = temp;

        Console.WriteLine($"Avg/Max/Min temperature = {_tempSum / _count:F1}/{_maxTemp:F1}/{_minTemp:F1}");
    }
}
```

**Usage**

```csharp
var station = new WeatherStation();
var currentDisplay = new CurrentConditionsDisplay();
var statsDisplay = new StatisticsDisplay();

station.Attach(currentDisplay);
station.Attach(statsDisplay);
station.SetMeasurements(30f, 65f, 1013.25f);

station.Detach(statsDisplay);
station.SetMeasurements(28f, 70f, 1012.0f);
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, temp: float, humidity: float, pressure: float) -> None: ...

class WeatherStation:
    def __init__(self) -> None:
        self._observers: list[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    def set_measurements(self, temp: float, humidity: float, pressure: float) -> None:
        self._temperature = temp
        self._humidity = humidity
        self._pressure = pressure
        self.notify()

class CurrentConditionsDisplay(Observer):
    def update(self, temp: float, humidity: float, pressure: float) -> None:
        print(f"Current conditions: {temp}°C, {humidity}% humidity, {pressure} hPa")

class StatisticsDisplay(Observer):
    def __init__(self) -> None:
        self._max_temp = float("-inf")
        self._min_temp = float("inf")
        self._temp_sum = 0.0
        self._count = 0

    def update(self, temp: float, humidity: float, pressure: float) -> None:
        self._temp_sum += temp
        self._count += 1
        self._max_temp = max(self._max_temp, temp)
        self._min_temp = min(self._min_temp, temp)
        avg = self._temp_sum / self._count
        print(f"Avg/Max/Min temperature = {avg:.1f}/{self._max_temp:.1f}/{self._min_temp:.1f}")
```

**Usage**

```python
station = WeatherStation()
current_display = CurrentConditionsDisplay()
stats_display = StatisticsDisplay()

station.attach(current_display)
station.attach(stats_display)
station.set_measurements(30.0, 65.0, 1013.25)

station.detach(stats_display)
station.set_measurements(28.0, 70.0, 1012.0)
```

<a id="33-command"></a>

### 3.3. Command

| **Who**  | Systems that need to decouple the issuer of a request from the object that performs it (e.g., GUI toolkits, job schedulers, macro recorders). |
|----------|--------|
| **What** | Encapsulates a request as an object, letting you parameterize clients with different requests, queue or log them, and support undoable operations. |
| **When** | When you need to issue requests without knowing the operation or the receiver at compile time, or when undo/redo, queuing, or logging of operations is required. |
| **Where**| Text editors, transaction systems, task queues, menu actions, remote procedure calls, and anywhere operations must be stored, replayed, or reversed. |
| **Why**  | Decouples the sender from the receiver, enabling flexible scheduling, composition of macro commands, and reversible operations without the invoker knowing any details about the work being performed. |
| **How**  | Define a command interface with an `execute` method (and optionally `undo`). Each concrete command stores a reference to a receiver and the parameters needed to carry out the action. An invoker holds commands and triggers them; for undo, it also maintains a history stack of executed commands. |

The Command pattern turns a request into a stand-alone object that contains everything needed to perform the action: the receiver, the method to call, and any arguments. The invoker — a button, a scheduler, a keystroke handler — holds a command and calls `execute` without knowing what happens behind the interface. This inversion means invokers are completely decoupled from the business logic they trigger.

The key participants are the **Command** interface (declaring `execute` and optionally `undo`), **ConcreteCommand** implementations that bind a receiver to an action, the **Receiver** that performs the actual work, and the **Invoker** that stores and triggers commands. When undo is needed, each concrete command captures enough state before execution to reverse the effect, and the invoker maintains a history stack.

Commands are naturally composable: a **MacroCommand** can hold a list of sub-commands and execute them sequentially, enabling complex multi-step operations to be built from simple primitives. The pattern also supports deferred execution (job queues), logging (serialize the command stream for replay), and transactional semantics (roll back a batch if one command fails).

<a id="331-paradigm-fit"></a>

#### 3.3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — commands are simply closures or data describing actions; undo becomes event sourcing over an immutable log. |
| Data-Oriented | **Adapts well** — commands can be plain data structs processed in batches by a command-processing system. |
| OOP | **Natural fit** — classic GoF pattern with Command interface, concrete commands, invoker, and receiver. |
| Procedural | **Workable** — function pointers paired with argument structs; undo requires explicit state snapshots. |
| Reactive | **Adapts well** — commands map to events in a stream; undo/redo becomes stream rewinding or event replay. |

<a id="332-benefits"></a>

#### 3.3.2. Benefits

- Decouples the object that invokes an operation from the one that knows how to perform it.
- Enables undo/redo by storing executed commands in a history stack with inverse operations. A redo stack (cleared on each new command) completes the model, though the examples below show only undo for brevity.
- Commands can be serialized, queued, logged, and composed into macros, supporting deferred and batch execution.

<a id="333-trade-offs"></a>

#### 3.3.3. Trade-offs

- Introduces a class for every operation, increasing the total number of types in the system.
- Undo state management adds complexity — each command must capture and restore enough context to reverse its effect.
- Indirection between the invoker and the receiver can make the control flow harder to trace during debugging.

<a id="334-examples"></a>

#### 3.3.4. Examples

##### Rust

**Implementation**

```rust
use std::cell::RefCell;
use std::rc::Rc;

type Document = Rc<RefCell<String>>;

trait Command {
    fn execute(&mut self);
    fn undo(&mut self);
}

struct TypeCommand {
    doc: Document,
    text: String,
}

impl TypeCommand {
    fn new(doc: Document, text: &str) -> Self {
        Self { doc, text: text.to_string() }
    }
}

impl Command for TypeCommand {
    fn execute(&mut self) {
        self.doc.borrow_mut().push_str(&self.text);
    }

    fn undo(&mut self) {
        let mut doc = self.doc.borrow_mut();
        let new_len = doc.len() - self.text.len();
        doc.truncate(new_len);
    }
}

struct DeleteCommand {
    doc: Document,
    count: usize,
    deleted: String,
}

impl DeleteCommand {
    fn new(doc: Document, count: usize) -> Self {
        Self { doc, count, deleted: String::new() }
    }
}

impl Command for DeleteCommand {
    fn execute(&mut self) {
        let mut doc = self.doc.borrow_mut();
        let split_at = doc.len().saturating_sub(self.count);
        self.deleted = doc[split_at..].to_string();
        doc.truncate(split_at);
    }

    fn undo(&mut self) {
        self.doc.borrow_mut().push_str(&self.deleted);
    }
}

struct Editor {
    doc: Document,
    history: Vec<Box<dyn Command>>,
}

impl Editor {
    fn new() -> Self {
        Self { doc: Rc::new(RefCell::new(String::new())), history: Vec::new() }
    }

    fn execute(&mut self, mut cmd: Box<dyn Command>) {
        cmd.execute();
        self.history.push(cmd);
    }

    fn undo(&mut self) {
        if let Some(mut cmd) = self.history.pop() {
            cmd.undo();
        }
    }

    fn text(&self) -> String {
        self.doc.borrow().clone()
    }
}
```

**Usage**

```rust
let mut editor = Editor::new();
let doc = editor.doc.clone();

editor.execute(Box::new(TypeCommand::new(doc.clone(), "Hello, ")));
editor.execute(Box::new(TypeCommand::new(doc.clone(), "world!")));
assert_eq!(editor.text(), "Hello, world!");

editor.execute(Box::new(DeleteCommand::new(doc.clone(), 6)));
assert_eq!(editor.text(), "Hello, ");

editor.undo();
assert_eq!(editor.text(), "Hello, world!");
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;
using System.Text;

public interface ICommand
{
    void Execute();
    void Undo();
}

public class TypeCommand : ICommand
{
    private readonly StringBuilder _doc;
    private readonly string _text;

    public TypeCommand(StringBuilder doc, string text)
    {
        _doc = doc;
        _text = text;
    }

    public void Execute() => _doc.Append(_text);
    public void Undo() => _doc.Remove(_doc.Length - _text.Length, _text.Length);
}

public class DeleteCommand : ICommand
{
    private readonly StringBuilder _doc;
    private readonly int _count;
    private string _deleted = "";

    public DeleteCommand(StringBuilder doc, int count)
    {
        _doc = doc;
        _count = count;
    }

    public void Execute()
    {
        int start = Math.Max(0, _doc.Length - _count);
        _deleted = _doc.ToString(start, _doc.Length - start);
        _doc.Remove(start, _doc.Length - start);
    }

    public void Undo() => _doc.Append(_deleted);
}

public class Editor
{
    private readonly StringBuilder _doc = new();
    private readonly Stack<ICommand> _history = new();

    public void Execute(ICommand cmd)
    {
        cmd.Execute();
        _history.Push(cmd);
    }

    public void Undo()
    {
        if (_history.Count > 0)
            _history.Pop().Undo();
    }

    public string Text => _doc.ToString();
    public StringBuilder Document => _doc;
}
```

**Usage**

```csharp
var editor = new Editor();
editor.Execute(new TypeCommand(editor.Document, "Hello, "));
editor.Execute(new TypeCommand(editor.Document, "world!"));
Console.WriteLine(editor.Text); // Hello, world!

editor.Execute(new DeleteCommand(editor.Document, 6));
Console.WriteLine(editor.Text); // Hello, 

editor.Undo();
Console.WriteLine(editor.Text); // Hello, world!
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class TypeCommand(Command):
    def __init__(self, doc: list[str], text: str) -> None:
        self._doc = doc
        self._text = text

    def execute(self) -> None:
        self._doc.append(self._text)

    def undo(self) -> None:
        self._doc.pop()


class DeleteCommand(Command):
    def __init__(self, doc: list[str], count: int) -> None:
        self._doc = doc
        self._count = count
        self._deleted: str = ""

    def execute(self) -> None:
        text = "".join(self._doc)
        self._deleted = text[-self._count:]
        self._doc.clear()
        self._doc.append(text[:-self._count])

    def undo(self) -> None:
        self._doc.append(self._deleted)


class Editor:
    def __init__(self) -> None:
        self.doc: list[str] = []
        self._history: list[Command] = []

    def execute(self, cmd: Command) -> None:
        cmd.execute()
        self._history.append(cmd)

    def undo(self) -> None:
        if self._history:
            self._history.pop().undo()

    @property
    def text(self) -> str:
        return "".join(self.doc)
```

**Usage**

```python
editor = Editor()
editor.execute(TypeCommand(editor.doc, "Hello, "))
editor.execute(TypeCommand(editor.doc, "world!"))
print(editor.text)  # Hello, world!

editor.execute(DeleteCommand(editor.doc, 6))
print(editor.text)  # Hello, 

editor.undo()
print(editor.text)  # Hello, world!
```

<a id="34-state"></a>

### 3.4. State

| **Who**  | Objects whose behavior must change based on internal state (e.g., media players, network connections, document workflows, vending machines). |
|----------|--------|
| **What** | Lets an object alter its behavior when its internal state changes — the object appears to change its class. |
| **When** | When an object's behavior depends on its state and it must change behavior at runtime, especially when large conditional blocks on state have become unmanageable. |
| **Where**| Finite state machines, protocol handlers, UI components with modal behavior, game character states, and workflow engines. |
| **Why**  | Eliminates sprawling `if`/`else` or `switch` blocks on state, encapsulates state-specific behavior in dedicated classes, and makes state transitions explicit and self-documenting. |
| **How**  | Define a state interface with methods for every state-dependent action. Implement a concrete class for each state. The context holds a reference to the current state object and delegates all state-dependent behavior to it. State transitions are performed by swapping the context's state reference — either by the context or by the state objects themselves. |

The State pattern encapsulates state-dependent behavior into separate objects, one per state. A **context** object holds a reference to its current state and delegates behavior to it. When the context's state changes — triggered externally or by the current state itself — the delegate is swapped, and subsequent method calls exhibit completely different behavior without any conditionals in the context.

The key participants are the **State** interface (declaring every action the context delegates), **ConcreteState** classes (each implementing the actions appropriate for that state), and the **Context** (which maintains the current state and forwards requests). State transitions can be managed by the context (centralized) or by the concrete states themselves (distributed), depending on whether transition logic is simple or state-specific.

State is closely related to Strategy — both use composition to delegate behavior — but differs in intent: Strategy selects an algorithm chosen by the client, while State transitions autonomously as part of the object's lifecycle. The pattern is especially valuable when modeling finite state machines: each state class maps directly to a state in the diagram, and transitions become method calls that swap the delegate.

<a id="341-paradigm-fit"></a>

#### 3.4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — state can be a discriminated union with pure transition functions returning the next state. |
| Data-Oriented | **Workable** — state is a tag or enum field on entity data; systems dispatch behavior based on the tag. |
| OOP | **Natural fit** — each state is a class implementing a common interface; the context delegates to the current state object. |
| Procedural | **Workable** — function-pointer tables indexed by state enum, or explicit switch blocks. |
| Reactive | **Adapts well** — state machines can be modeled as `scan`/`reduce` over event streams, emitting new states. |

<a id="342-benefits"></a>

#### 3.4.2. Benefits

- Eliminates large conditional blocks — each state's behavior is isolated in its own class, improving readability.
- Adding new states requires only a new class with no changes to the context or existing states.
- State transitions are explicit and localized, making the state machine easy to visualize and verify.

<a id="343-trade-offs"></a>

#### 3.4.3. Trade-offs

- Increases the number of classes — one per state — which can be excessive for simple state machines.
- Distributed transitions (states deciding the next state) can scatter transition logic, making the overall machine harder to see at a glance.
- State objects that need access to the context's internals may require exposing fields that would otherwise be private.

<a id="344-examples"></a>

#### 3.4.4. Examples

##### Rust

**Implementation**

```rust
trait PlayerState {
    fn play(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState>;
    fn pause(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState>;
    fn stop(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState>;
}

struct Stopped;
struct Playing;
struct Paused;

impl PlayerState for Stopped {
    fn play(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        player.status = "Playing".into();
        Box::new(Playing)
    }

    fn pause(self: Box<Self>, _player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        self
    }

    fn stop(self: Box<Self>, _player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        self
    }
}

impl PlayerState for Playing {
    fn play(self: Box<Self>, _player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        self
    }

    fn pause(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        player.status = "Paused".into();
        Box::new(Paused)
    }

    fn stop(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        player.status = "Stopped".into();
        Box::new(Stopped)
    }
}

impl PlayerState for Paused {
    fn play(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        player.status = "Playing".into();
        Box::new(Playing)
    }

    fn pause(self: Box<Self>, _player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        self
    }

    fn stop(self: Box<Self>, player: &mut MediaPlayer) -> Box<dyn PlayerState> {
        player.status = "Stopped".into();
        Box::new(Stopped)
    }
}

struct MediaPlayer {
    state: Option<Box<dyn PlayerState>>,
    status: String,
}

impl MediaPlayer {
    fn new() -> Self {
        Self { state: Some(Box::new(Stopped)), status: "Stopped".into() }
    }

    fn play(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.play(self));
        }
    }

    fn pause(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.pause(self));
        }
    }

    fn stop(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.stop(self));
        }
    }
}
```

**Usage**

```rust
let mut player = MediaPlayer::new();
assert_eq!(player.status, "Stopped");

player.play();
assert_eq!(player.status, "Playing");

player.pause();
assert_eq!(player.status, "Paused");

player.stop();
assert_eq!(player.status, "Stopped");
```

##### C\#

**Implementation**

```csharp
using System;

public interface IPlayerState
{
    IPlayerState Play(MediaPlayer player);
    IPlayerState Pause(MediaPlayer player);
    IPlayerState Stop(MediaPlayer player);
}

public class StoppedState : IPlayerState
{
    public IPlayerState Play(MediaPlayer player)
    {
        player.Status = "Playing";
        return new PlayingState();
    }

    public IPlayerState Pause(MediaPlayer player) => this;
    public IPlayerState Stop(MediaPlayer player) => this;
}

public class PlayingState : IPlayerState
{
    public IPlayerState Play(MediaPlayer player) => this;

    public IPlayerState Pause(MediaPlayer player)
    {
        player.Status = "Paused";
        return new PausedState();
    }

    public IPlayerState Stop(MediaPlayer player)
    {
        player.Status = "Stopped";
        return new StoppedState();
    }
}

public class PausedState : IPlayerState
{
    public IPlayerState Play(MediaPlayer player)
    {
        player.Status = "Playing";
        return new PlayingState();
    }

    public IPlayerState Pause(MediaPlayer player) => this;

    public IPlayerState Stop(MediaPlayer player)
    {
        player.Status = "Stopped";
        return new StoppedState();
    }
}

public class MediaPlayer
{
    private IPlayerState _state;

    public MediaPlayer()
    {
        _state = new StoppedState();
        Status = "Stopped";
    }

    public string Status { get; set; }

    public void Play() => _state = _state.Play(this);
    public void Pause() => _state = _state.Pause(this);
    public void Stop() => _state = _state.Stop(this);
}
```

**Usage**

```csharp
var player = new MediaPlayer();
Console.WriteLine(player.Status); // Stopped

player.Play();
Console.WriteLine(player.Status); // Playing

player.Pause();
Console.WriteLine(player.Status); // Paused

player.Stop();
Console.WriteLine(player.Status); // Stopped
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class PlayerState(ABC):
    @abstractmethod
    def play(self, player: "MediaPlayer") -> "PlayerState": ...

    @abstractmethod
    def pause(self, player: "MediaPlayer") -> "PlayerState": ...

    @abstractmethod
    def stop(self, player: "MediaPlayer") -> "PlayerState": ...


class Stopped(PlayerState):
    def play(self, player: "MediaPlayer") -> PlayerState:
        player.status = "Playing"
        return Playing()

    def pause(self, player: "MediaPlayer") -> PlayerState:
        return self

    def stop(self, player: "MediaPlayer") -> PlayerState:
        return self


class Playing(PlayerState):
    def play(self, player: "MediaPlayer") -> PlayerState:
        return self

    def pause(self, player: "MediaPlayer") -> PlayerState:
        player.status = "Paused"
        return Paused()

    def stop(self, player: "MediaPlayer") -> PlayerState:
        player.status = "Stopped"
        return Stopped()


class Paused(PlayerState):
    def play(self, player: "MediaPlayer") -> PlayerState:
        player.status = "Playing"
        return Playing()

    def pause(self, player: "MediaPlayer") -> PlayerState:
        return self

    def stop(self, player: "MediaPlayer") -> PlayerState:
        player.status = "Stopped"
        return Stopped()


class MediaPlayer:
    def __init__(self) -> None:
        self._state: PlayerState = Stopped()
        self.status: str = "Stopped"

    def play(self) -> None:
        self._state = self._state.play(self)

    def pause(self) -> None:
        self._state = self._state.pause(self)

    def stop(self) -> None:
        self._state = self._state.stop(self)
```

**Usage**

```python
player = MediaPlayer()
print(player.status)  # Stopped

player.play()
print(player.status)  # Playing

player.pause()
print(player.status)  # Paused

player.stop()
print(player.status)  # Stopped
```

<a id="35-template-method"></a>

### 3.5. Template Method

| **Who**  | Framework and library authors who define algorithmic skeletons that client subclasses customize by overriding specific steps. |
|----------|--------|
| **What** | Defines the skeleton of an algorithm in a base class, deferring specific steps to subclasses without changing the algorithm's overall structure. |
| **When** | When multiple classes share the same algorithmic structure but differ in certain steps, and you want to avoid code duplication while still allowing customization. |
| **Where**| Frameworks, data-processing pipelines, test harnesses (setUp/tearDown), and any scenario where the workflow is fixed but individual steps vary. |
| **Why**  | Maximizes code reuse by placing the invariant parts of an algorithm in one place. Subclasses customize only the steps that vary, enforcing a consistent overall structure. |
| **How**  | Define an abstract base class with a template method that calls a sequence of steps — some concrete (shared logic), some abstract or hook methods (customization points). Subclasses override the abstract/hook methods to provide specific behavior while inheriting the fixed workflow. |

The Template Method pattern captures an algorithm's invariant skeleton in a base-class method that calls a sequence of steps — some implemented by the base class itself, some left abstract for subclasses to fill in. The template method is typically `final` (or non-virtual) so subclasses cannot alter the overall flow; they can only override the designated extension points. In practice, not all languages enforce this — Rust trait default methods and Python methods can be overridden freely. C# can use `sealed` in derived classes, Java uses `final`, and Python offers `@typing.final` as a static-analysis hint.

The key participants are the **AbstractClass**, which defines the template method and declares abstract or hook steps, and the **ConcreteClass**, which overrides those steps to supply specific behavior. Hook methods differ from abstract methods in that they provide a default (often empty) implementation, making the override optional.

Template Method is the inheritance-based counterpart to Strategy: where Strategy delegates an entire algorithm to a composed object, Template Method lets subclasses replace individual steps within a fixed algorithm. The pattern is prevalent in frameworks — any time a framework says "override this method to customize behavior," it is using Template Method. The main tension is its reliance on inheritance, which can lead to deep class hierarchies and tight coupling between base and derived classes.

<a id="351-paradigm-fit"></a>

#### 3.5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — higher-order functions accept step functions as parameters, achieving the same structure without inheritance. |
| Data-Oriented | **Uncommon** — systems process data in pipelines; per-entity behavioral customization via inheritance is rare. |
| OOP | **Natural fit** — abstract base class with a final template method and overridable steps is the canonical form. |
| Procedural | **Workable** — a top-level function accepts function pointers for the customizable steps. |
| Reactive | **Workable** — a fixed pipeline of operators with configurable transformation stages, though composition is more idiomatic. |

<a id="352-benefits"></a>

#### 3.5.2. Benefits

- Maximizes code reuse — the invariant algorithm lives in one place; only varying steps are overridden.
- Enforces a consistent algorithmic structure across all variants, preventing subclasses from accidentally breaking the workflow.
- Hook methods provide optional customization points with sensible defaults, minimizing the burden on subclasses.

<a id="353-trade-offs"></a>

#### 3.5.3. Trade-offs

- Relies on inheritance, which can lead to deep hierarchies and tight coupling between base and derived classes.
- Subclasses must understand the base class's control flow to override steps correctly — a form of fragile base class problem.
- Adding a new step to the template method can require changes across all existing subclasses.

<a id="354-examples"></a>

#### 3.5.4. Examples

##### Rust

Rust lacks traditional inheritance, so the template method is expressed via a trait with a provided method that calls required methods.

**Implementation**

```rust
trait DataParser {
    fn read_data(&self, source: &str) -> String;
    fn process_data(&self, raw: &str) -> String;

    fn format_output(&self, processed: &str) -> String {
        processed.to_string()
    }

    fn parse(&self, source: &str) -> String {
        let raw = self.read_data(source);
        let processed = self.process_data(&raw);
        self.format_output(&processed)
    }
}

struct CsvParser;

impl DataParser for CsvParser {
    fn read_data(&self, source: &str) -> String {
        format!("csv_raw({source})")
    }

    fn process_data(&self, raw: &str) -> String {
        raw.to_uppercase()
    }
}

struct JsonParser;

impl DataParser for JsonParser {
    fn read_data(&self, source: &str) -> String {
        format!("json_raw({source})")
    }

    fn process_data(&self, raw: &str) -> String {
        raw.replace("json_raw", "json_processed")
    }

    fn format_output(&self, processed: &str) -> String {
        format!("{{{processed}}}")
    }
}
```

**Usage**

```rust
let csv = CsvParser;
let result = csv.parse("data.csv");
assert_eq!(result, "CSV_RAW(DATA.CSV)");

let json = JsonParser;
let result = json.parse("data.json");
assert_eq!(result, "{json_processed(data.json)}");
```

##### C\#

**Implementation**

```csharp
using System;

public abstract class DataParser
{
    public string Parse(string source)
    {
        string raw = ReadData(source);
        string processed = ProcessData(raw);
        return FormatOutput(processed);
    }

    protected abstract string ReadData(string source);
    protected abstract string ProcessData(string raw);

    protected virtual string FormatOutput(string processed) => processed;
}

public class CsvParser : DataParser
{
    protected override string ReadData(string source) => $"csv_raw({source})";
    protected override string ProcessData(string raw) => raw.ToUpper();
}

public class JsonParser : DataParser
{
    protected override string ReadData(string source) => $"json_raw({source})";
    protected override string ProcessData(string raw) => raw.Replace("json_raw", "json_processed");
    protected override string FormatOutput(string processed) => $"{{{processed}}}";
}
```

**Usage**

```csharp
DataParser csv = new CsvParser();
Console.WriteLine(csv.Parse("data.csv")); // CSV_RAW(DATA.CSV)

DataParser json = new JsonParser();
Console.WriteLine(json.Parse("data.json")); // {json_processed(data.json)}
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class DataParser(ABC):
    def parse(self, source: str) -> str:
        raw = self.read_data(source)
        processed = self.process_data(raw)
        return self.format_output(processed)

    @abstractmethod
    def read_data(self, source: str) -> str: ...

    @abstractmethod
    def process_data(self, raw: str) -> str: ...

    def format_output(self, processed: str) -> str:
        return processed


class CsvParser(DataParser):
    def read_data(self, source: str) -> str:
        return f"csv_raw({source})"

    def process_data(self, raw: str) -> str:
        return raw.upper()


class JsonParser(DataParser):
    def read_data(self, source: str) -> str:
        return f"json_raw({source})"

    def process_data(self, raw: str) -> str:
        return raw.replace("json_raw", "json_processed")

    def format_output(self, processed: str) -> str:
        return f"{{{processed}}}"
```

**Usage**

```python
csv = CsvParser()
print(csv.parse("data.csv"))  # CSV_RAW(DATA.CSV)

json = JsonParser()
print(json.parse("data.json"))  # {json_processed(data.json)}
```

<a id="36-iterator"></a>

### 3.6. Iterator

| **Who**  | Any code that needs to traverse a collection without depending on its internal structure (arrays, trees, graphs, lazy sequences). |
|----------|--------|
| **What** | Provides a standard way to access elements of a collection sequentially without exposing its underlying representation. |
| **When** | When you need to traverse a collection uniformly regardless of its data structure, or when you want to support multiple simultaneous traversals and lazy evaluation. |
| **Where**| Collection libraries, database cursors, file-system walkers, paginated API results, and stream processing pipelines. |
| **Why**  | Decouples traversal logic from collection internals, enables polymorphic iteration over heterogeneous data structures, and supports lazy evaluation where elements are produced on demand. |
| **How**  | Define an iterator interface with a method that returns the next element (and signals completion). The collection exposes a factory method that returns a fresh iterator. Clients consume elements through the iterator interface without knowing whether the backing store is an array, linked list, tree, or generator. |

The Iterator pattern provides a uniform protocol for sequentially accessing the elements of a collection without revealing its internal representation. The client asks the collection for an iterator, then repeatedly calls a `next` method until the sequence is exhausted. Because the client depends only on the iterator interface, the same loop can traverse an array, a linked list, a tree, or a lazily computed stream.

The key participants are the **Iterator** interface (typically a single `next` method returning the next element or a completion signal) and the **Aggregate** (or **Collection**), which creates iterators for itself. Most modern languages have elevated Iterator from a design pattern to a language-level protocol: Python's `__iter__`/`__next__`, Rust's `IntoIterator`/`Iterator`, C#'s `IEnumerable<T>`/`IEnumerator<T>`, and JavaScript's `Symbol.iterator`.

Because iterators decouple production from consumption, they naturally support lazy evaluation — elements can be computed or fetched on demand rather than materialized upfront. Iterator combinators (`map`, `filter`, `take`, `zip`) compose into pipelines that process data without intermediate allocations, which is why Rust and Python lean heavily on iterator chains for data transformation.

<a id="361-paradigm-fit"></a>

#### 3.6.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — lazy lists, generators, and fold/map/filter are iterators in spirit; the pattern is foundational. |
| Data-Oriented | **Adapts well** — iterating over contiguous data arrays is the primary access pattern; custom iterators can expose SoA views. |
| OOP | **Natural fit** — iterator interface with `hasNext`/`next` methods; collections provide factory methods for iterators. |
| Procedural | **Workable** — index-based loops or opaque cursor structs advanced by a `next` function. |
| Reactive | **Adapts well** — push-based streams are the dual of pull-based iterators; conversion between the two is well-defined. |

<a id="362-benefits"></a>

#### 3.6.2. Benefits

- Decouples traversal logic from collection internals, letting both evolve independently.
- Supports multiple simultaneous traversals over the same collection with independent iterator instances.
- Enables lazy evaluation — elements are produced on demand, avoiding unnecessary computation or memory allocation.

<a id="363-trade-offs"></a>

#### 3.6.3. Trade-offs

- Simple collections (plain arrays) gain little from a dedicated iterator; the abstraction adds overhead without clear benefit.
- External iterators expose traversal state that can become stale if the collection is mutated mid-iteration.
- Custom iterators for complex structures (graphs, trees) can be difficult to implement correctly, especially when the traversal must be resumable.

<a id="364-examples"></a>

#### 3.6.4. Examples

##### Rust

Rust's `Iterator` trait is the standard protocol; implementing `next` grants access to the full combinator chain.

**Implementation**

```rust
struct RangeIter {
    current: i64,
    end: i64,
    step: i64,
}

impl RangeIter {
    fn new(start: i64, end: i64, step: i64) -> Self {
        Self { current: start, end, step }
    }
}

impl Iterator for RangeIter {
    type Item = i64;

    fn next(&mut self) -> Option<Self::Item> {
        if (self.step > 0 && self.current >= self.end)
            || (self.step < 0 && self.current <= self.end)
        {
            return None;
        }
        let value = self.current;
        self.current += self.step;
        Some(value)
    }
}
```

**Usage**

```rust
let values: Vec<i64> = RangeIter::new(0, 10, 3).collect();
assert_eq!(values, vec![0, 3, 6, 9]);

let sum: i64 = RangeIter::new(1, 6, 1).filter(|x| x % 2 == 0).sum();
assert_eq!(sum, 6);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections;
using System.Collections.Generic;

public class RangeIterator : IEnumerable<long>
{
    private readonly long _start;
    private readonly long _end;
    private readonly long _step;

    public RangeIterator(long start, long end, long step)
    {
        _start = start;
        _end = end;
        _step = step;
    }

    public IEnumerator<long> GetEnumerator()
    {
        for (long i = _start; _step > 0 ? i < _end : i > _end; i += _step)
            yield return i;
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
```

**Usage**

```csharp
using System.Linq;

var range = new RangeIterator(0, 10, 3);
Console.WriteLine(string.Join(", ", range)); // 0, 3, 6, 9

long sum = new RangeIterator(1, 6, 1).Where(x => x % 2 == 0).Sum();
Console.WriteLine(sum); // 6
```

##### Python

Python's iterator protocol (`__iter__`/`__next__`) integrates directly with `for` loops and comprehensions.

**Implementation**

```python
from collections.abc import Iterator


class RangeIter(Iterator[int]):
    def __init__(self, start: int, end: int, step: int = 1) -> None:
        self._current = start
        self._end = end
        self._step = step

    def __next__(self) -> int:
        if (self._step > 0 and self._current >= self._end) or \
           (self._step < 0 and self._current <= self._end):
            raise StopIteration
        value = self._current
        self._current += self._step
        return value

    def __iter__(self) -> "RangeIter":
        return self
```

**Usage**

```python
values = list(RangeIter(0, 10, 3))
print(values)  # [0, 3, 6, 9]

total = sum(x for x in RangeIter(1, 6) if x % 2 == 0)
print(total)  # 6
```

<a id="37-chain-of-responsibility"></a>

### 3.7. Chain of Responsibility

| **Who**  | Systems where a request must pass through multiple processors, each deciding whether to handle it or forward it (e.g., middleware stacks, event propagation, approval workflows). |
|----------|--------|
| **What** | Passes a request along a chain of handlers, decoupling the sender from the receivers by giving more than one object a chance to handle the request. |
| **When** | When multiple objects may handle a request and the handler isn't known in advance, or when you want to assemble a processing pipeline dynamically at runtime. |
| **Where**| HTTP middleware stacks, GUI event bubbling, logging filter chains, validation pipelines, and authorization layers. |
| **Why**  | Decouples request senders from receivers, allows dynamic assembly of processing chains, and follows the Single Responsibility Principle — each handler addresses one concern. |
| **How**  | Define a handler interface with a method to process the request and a reference to the next handler. Each concrete handler either processes the request and/or forwards it to the next handler. The client sends the request to the first handler in the chain without needing to know which handler will ultimately process it. |

The Chain of Responsibility pattern organizes handlers into a linked sequence. A request enters at the head and travels along the chain; each handler inspects it and either processes it, passes it to the next handler, or does both. The sender does not know — or care — which handler ultimately deals with the request, achieving loose coupling between the sender and the processing logic.

The key participants are the **Handler** interface (declaring a method to handle the request and a way to set the next handler), **ConcreteHandlers** (each implementing specific processing logic), and the **Client** (which assembles the chain and submits requests to its head). There are two common variants: the *pure* variant, where exactly one handler processes the request and the chain stops; and the *pipeline* variant (common in middleware), where every handler processes the request and forwards it onward.

Chain of Responsibility is the backbone of HTTP middleware frameworks (Express, ASP.NET, Actix-web): each middleware function receives the request and a `next` callback, optionally transforms the request or response, and decides whether to continue the chain. The pattern makes it trivial to reorder, add, or remove handlers without touching the others, but debugging long chains can be challenging because the processing path is determined at runtime.

<a id="371-paradigm-fit"></a>

#### 3.7.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — function composition or a list of functions folded over the request; each function decides whether to short-circuit. |
| Data-Oriented | **Workable** — pipeline stages can be systems that process request data sequentially through component tables. |
| OOP | **Natural fit** — handler interface with a `next` reference; each concrete handler in the chain implements the interface. |
| Procedural | **Workable** — a list of function pointers iterated in sequence, each receiving the request and a continue flag. |
| Reactive | **Adapts well** — operators in a stream pipeline are a natural chain; `filter`, `map`, and `takeWhile` model handler decisions. |

<a id="372-benefits"></a>

#### 3.7.2. Benefits

- Decouples the sender from all receivers — the client sends the request without knowing which handler will process it.
- Handlers can be added, removed, or reordered at runtime without modifying existing handlers or the client.
- Each handler addresses a single concern, promoting the Single Responsibility Principle and clean separation of cross-cutting logic.

<a id="373-trade-offs"></a>

#### 3.7.3. Trade-offs

- No guarantee of handling — if no handler in the chain processes the request, it falls through silently unless a catch-all is added.
- Long chains can be difficult to debug because the processing path is assembled at runtime and not visible in static code analysis.
- Performance can degrade with many handlers if every request must traverse the entire chain even when early termination is rare.

<a id="374-examples"></a>

#### 3.7.4. Examples

##### Rust

**Implementation**

```rust
type Request = String;
type Response = String;

trait Handler {
    fn set_next(&mut self, next: Box<dyn Handler>);
    fn handle(&self, request: &Request) -> Response;
}

struct AuthHandler {
    next: Option<Box<dyn Handler>>,
}

impl AuthHandler {
    fn new() -> Self {
        Self { next: None }
    }
}

impl Handler for AuthHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }

    fn handle(&self, request: &Request) -> Response {
        if !request.contains("auth:valid") {
            return "401 Unauthorized".into();
        }
        match &self.next {
            Some(next) => next.handle(request),
            None => "200 OK".into(),
        }
    }
}

struct LoggingHandler {
    next: Option<Box<dyn Handler>>,
}

impl LoggingHandler {
    fn new() -> Self {
        Self { next: None }
    }
}

impl Handler for LoggingHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }

    fn handle(&self, request: &Request) -> Response {
        println!("[LOG] Processing: {request}");
        match &self.next {
            Some(next) => next.handle(request),
            None => "200 OK".into(),
        }
    }
}

struct ValidationHandler {
    next: Option<Box<dyn Handler>>,
}

impl ValidationHandler {
    fn new() -> Self {
        Self { next: None }
    }
}

impl Handler for ValidationHandler {
    fn set_next(&mut self, next: Box<dyn Handler>) {
        self.next = Some(next);
    }

    fn handle(&self, request: &Request) -> Response {
        if request.contains("body:empty") {
            return "400 Bad Request".into();
        }
        match &self.next {
            Some(next) => next.handle(request),
            None => "200 OK".into(),
        }
    }
}
```

**Usage**

```rust
let validation = ValidationHandler::new();

let mut logging = LoggingHandler::new();
logging.set_next(Box::new(validation));

let mut auth = AuthHandler::new();
auth.set_next(Box::new(logging));

let response = auth.handle(&"auth:valid body:present".into());
assert_eq!(response, "200 OK");

let response = auth.handle(&"auth:missing".into());
assert_eq!(response, "401 Unauthorized");

let response = auth.handle(&"auth:valid body:empty".into());
assert_eq!(response, "400 Bad Request");
```

##### C\#

**Implementation**

```csharp
using System;

public abstract class HttpHandler
{
    private HttpHandler? _next;

    public HttpHandler SetNext(HttpHandler next)
    {
        _next = next;
        return next;
    }

    public virtual string Handle(string request)
    {
        return _next?.Handle(request) ?? "200 OK";
    }
}

public class AuthHandler : HttpHandler
{
    public override string Handle(string request)
    {
        if (!request.Contains("auth:valid"))
            return "401 Unauthorized";
        return base.Handle(request);
    }
}

public class LoggingHandler : HttpHandler
{
    public override string Handle(string request)
    {
        Console.WriteLine($"[LOG] Processing: {request}");
        return base.Handle(request);
    }
}

public class ValidationHandler : HttpHandler
{
    public override string Handle(string request)
    {
        if (request.Contains("body:empty"))
            return "400 Bad Request";
        return base.Handle(request);
    }
}
```

**Usage**

```csharp
var auth = new AuthHandler();
var logging = new LoggingHandler();
var validation = new ValidationHandler();

auth.SetNext(logging).SetNext(validation);

Console.WriteLine(auth.Handle("auth:valid body:present")); // 200 OK
Console.WriteLine(auth.Handle("auth:missing"));            // 401 Unauthorized
Console.WriteLine(auth.Handle("auth:valid body:empty"));   // 400 Bad Request
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Handler(ABC):
    def __init__(self) -> None:
        self._next: Handler | None = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler

    @abstractmethod
    def handle(self, request: str) -> str: ...

    def forward(self, request: str) -> str:
        if self._next:
            return self._next.handle(request)
        return "200 OK"


class AuthHandler(Handler):
    def handle(self, request: str) -> str:
        if "auth:valid" not in request:
            return "401 Unauthorized"
        return self.forward(request)


class LoggingHandler(Handler):
    def handle(self, request: str) -> str:
        print(f"[LOG] Processing: {request}")
        return self.forward(request)


class ValidationHandler(Handler):
    def handle(self, request: str) -> str:
        if "body:empty" in request:
            return "400 Bad Request"
        return self.forward(request)
```

**Usage**

```python
auth = AuthHandler()
logging = LoggingHandler()
validation = ValidationHandler()

auth.set_next(logging).set_next(validation)

print(auth.handle("auth:valid body:present"))  # 200 OK
print(auth.handle("auth:missing"))             # 401 Unauthorized
print(auth.handle("auth:valid body:empty"))    # 400 Bad Request
```

<a id="38-mediator"></a>

### 3.8. Mediator

| **Who**  | Objects that communicate through complex many-to-many relationships (UI components, services, subsystems). |
|----------|--------|
| **What** | Defines an object that encapsulates how a set of objects interact, promoting loose coupling by keeping objects from referring to each other explicitly. |
| **When** | When a set of objects communicate in well-defined but complex ways, and the resulting interdependencies are unstructured and hard to understand. |
| **Where**| Chat systems, air traffic control, form validation (fields that enable/disable based on other fields), dialog boxes with interdependent widgets. |
| **Why**  | Reduces the number of direct connections between objects from O(n²) to O(n), centralizes interaction logic, and makes it easier to change interaction behavior independently from the participants. |
| **How**  | Define a mediator interface with a notification method. Colleagues hold a reference to the mediator instead of to each other. When a colleague's state changes, it notifies the mediator, which coordinates the response by calling methods on the appropriate colleagues. |

The Mediator pattern replaces direct communication between a group of objects with indirect communication through a central coordinator. Instead of each object knowing about (and calling methods on) every other object it interacts with, each object knows only about the mediator. When something noteworthy happens, the object tells the mediator, and the mediator decides which other objects need to respond and how. This converts a tangled web of N×(N−1) relationships into N spokes radiating from one hub.

The key participants are the **Mediator** interface (declares the notification method), the **ConcreteMediator** (implements the coordination logic and holds references to all colleagues), and the **Colleagues** (objects that interact through the mediator rather than directly). Colleagues are unaware of each other; their only dependency is the mediator interface.

The main risk is that the mediator itself can become a "god object" — a single class that knows too much and does too much. If the coordination logic grows complex, consider splitting it into sub-mediators or using event-based mediation. Mediator is closely related to Observer (the mediator often observes its colleagues) and to Facade (both centralize communication, but Facade simplifies a subsystem's interface while Mediator manages peer-to-peer interaction).

<a id="381-paradigm-fit"></a>

#### 3.8.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — a central dispatch function routes messages between participants; event buses model the same idea functionally. |
| Data-Oriented | **Workable** — a coordination system reads multiple component tables and writes updates, acting as a mediator between data groups. |
| OOP | **Natural fit** — mediator interface with concrete implementations that coordinate colleague objects. |
| Procedural | **Workable** — a central function or module receives notifications and dispatches calls to relevant subsystems. |
| Reactive | **Natural fit** — a central subject/bus merges streams from multiple sources and routes events to subscribers. |

<a id="382-benefits"></a>

#### 3.8.2. Benefits

- Reduces coupling between communicating objects — each colleague depends only on the mediator, not on every other colleague.
- Centralizes interaction logic in one place, making complex coordination easier to understand and modify.
- Adding new colleagues requires updating the mediator, not every existing colleague.

<a id="383-trade-offs"></a>

#### 3.8.3. Trade-offs

- The mediator can become a monolithic god object if too much logic accumulates in it.
- Adds a layer of indirection — tracing the flow from one colleague to another requires reading through the mediator.
- Single point of failure: all interaction passes through the mediator, so a bug there affects the entire group.

<a id="384-examples"></a>

#### 3.8.4. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

trait Mediator {
    fn send_message(&mut self, sender: &str, message: &str);
}

struct ChatRoom {
    users: HashMap<String, Vec<String>>,
}

impl ChatRoom {
    fn new() -> Self {
        ChatRoom {
            users: HashMap::new(),
        }
    }

    fn add_user(&mut self, name: &str) {
        self.users.entry(name.to_string()).or_default();
    }
}

impl Mediator for ChatRoom {
    fn send_message(&mut self, sender: &str, message: &str) {
        let keys: Vec<String> = self.users.keys().cloned().collect();
        for user in &keys {
            if user != sender {
                self.users
                    .get_mut(user)
                    .unwrap()
                    .push(format!("[{sender}]: {message}"));
            }
        }
    }
}
```

**Usage**

```rust
let mut room = ChatRoom::new();
room.add_user("Alice");
room.add_user("Bob");
room.add_user("Carol");

room.send_message("Alice", "Hello everyone!");
room.send_message("Bob", "Hey Alice!");

let bob_inbox = &room.users["Bob"];
assert_eq!(bob_inbox, &vec!["[Alice]: Hello everyone!".to_string()]);

let carol_inbox = &room.users["Carol"];
assert_eq!(carol_inbox.len(), 2);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public interface IChatMediator
{
    void SendMessage(string sender, string message);
    void AddUser(User user);
}

public class User
{
    public string Name { get; }
    public List<string> Inbox { get; } = new();
    private readonly IChatMediator _mediator;

    public User(string name, IChatMediator mediator)
    {
        Name = name;
        _mediator = mediator;
    }

    public void Send(string message) => _mediator.SendMessage(Name, message);

    public void Receive(string sender, string message) =>
        Inbox.Add($"[{sender}]: {message}");
}

public class ChatRoom : IChatMediator
{
    private readonly List<User> _users = new();

    public void AddUser(User user) => _users.Add(user);

    public void SendMessage(string sender, string message)
    {
        foreach (var user in _users)
        {
            if (user.Name != sender)
                user.Receive(sender, message);
        }
    }
}
```

**Usage**

```csharp
var room = new ChatRoom();
var alice = new User("Alice", room);
var bob = new User("Bob", room);
var carol = new User("Carol", room);

room.AddUser(alice);
room.AddUser(bob);
room.AddUser(carol);

alice.Send("Hello everyone!");
bob.Send("Hey Alice!");

Console.WriteLine(string.Join(", ", bob.Inbox));
Console.WriteLine(string.Join(", ", carol.Inbox));
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, sender: str, message: str) -> None: ...

    @abstractmethod
    def add_user(self, user: "User") -> None: ...


class User:
    def __init__(self, name: str, mediator: ChatMediator) -> None:
        self.name = name
        self.inbox: list[str] = []
        self._mediator = mediator

    def send(self, message: str) -> None:
        self._mediator.send_message(self.name, message)

    def receive(self, sender: str, message: str) -> None:
        self.inbox.append(f"[{sender}]: {message}")


class ChatRoom(ChatMediator):
    def __init__(self) -> None:
        self._users: list[User] = []

    def add_user(self, user: User) -> None:
        self._users.append(user)

    def send_message(self, sender: str, message: str) -> None:
        for user in self._users:
            if user.name != sender:
                user.receive(sender, message)
```

**Usage**

```python
room = ChatRoom()
alice = User("Alice", room)
bob = User("Bob", room)
carol = User("Carol", room)

room.add_user(alice)
room.add_user(bob)
room.add_user(carol)

alice.send("Hello everyone!")
bob.send("Hey Alice!")

print(bob.inbox)   # ['[Alice]: Hello everyone!']
print(carol.inbox)  # ['[Alice]: Hello everyone!', '[Bob]: Hey Alice!']
```

<a id="39-memento"></a>

### 3.9. Memento

| **Who**  | Objects whose internal state needs to be saved and restored (text editors, games, transaction systems). |
|----------|--------|
| **What** | Captures and externalizes an object's internal state so it can be restored later, without violating encapsulation. |
| **When** | When you need undo/redo functionality, checkpoints, or the ability to roll back to a previous state. |
| **Where**| Text editors (undo history), games (save/load), database transactions (rollback), workflow engines (step revert). |
| **Why**  | Preserves encapsulation — external objects can store and restore state without knowing the originator's internal structure. |
| **How**  | The originator creates a memento object containing a snapshot of its state. A caretaker stores the memento without examining its contents. To restore, the caretaker passes the memento back to the originator. |

The Memento pattern captures an object's internal state as an opaque token — the memento — that can be stored externally and used later to restore the object to that exact state. The originator is the only participant that can create and read mementos; external code (the caretaker) holds and manages them but never inspects their contents. This preserves encapsulation: the originator's internals are not exposed to the outside world.

The three participants are the **Originator** (the object whose state is being saved — it creates mementos and restores from them), the **Memento** (an immutable snapshot of the originator's state), and the **Caretaker** (manages a collection of mementos, typically as a stack for undo or a list for history). The caretaker has no knowledge of what the memento contains; it simply stores and retrieves it.

In practice, the memento can be a simple data class, a serialized blob, or even a closure that captures state. For large objects, incremental or diff-based mementos can reduce memory usage. Languages with inner-class or friend access (C#'s `internal`, C++ `friend`) can enforce the "only the originator reads the memento" rule at compile time; in others, convention enforces it.

<a id="391-paradigm-fit"></a>

#### 3.9.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — immutable values make every prior state a natural memento; persistent data structures preserve previous versions automatically. |
| Data-Oriented | **Workable** — snapshots of component arrays can be stored and swapped back in, though bulk-copying data tables can be expensive. |
| OOP | **Natural fit** — originator creates opaque memento objects; caretaker manages them without breaking encapsulation. |
| Procedural | **Workable** — struct copies or serialized snapshots stored in an array serve as mementos. |
| Reactive | **Adapts well** — state replay (e.g., `BehaviorSubject` history or event-sourced streams) achieves the same goal within a reactive pipeline. |

<a id="392-benefits"></a>

#### 3.9.2. Benefits

- Preserves encapsulation — the originator's internal structure is not exposed to the caretaker or any other external object.
- Undo/redo becomes straightforward: push mementos onto a stack and pop to restore.
- Mementos are immutable snapshots, safe to store, serialize, or transmit.

<a id="393-trade-offs"></a>

#### 3.9.3. Trade-offs

- Memory cost can grow quickly if the originator's state is large and snapshots are taken frequently.
- The originator must expose a way to produce and consume mementos, which can be awkward to design if the state is complex.
- The caretaker must manage memento lifecycle (when to discard old mementos) to avoid unbounded memory growth.

<a id="394-examples"></a>

#### 3.9.4. Examples

##### Rust

**Implementation**

```rust
#[derive(Clone)]
struct EditorMemento {
    content: String,
    cursor: usize,
}

struct TextEditor {
    content: String,
    cursor: usize,
}

impl TextEditor {
    fn new() -> Self {
        TextEditor {
            content: String::new(),
            cursor: 0,
        }
    }

    fn type_text(&mut self, text: &str) {
        self.content.insert_str(self.cursor, text);
        self.cursor += text.len();
    }

    fn save(&self) -> EditorMemento {
        EditorMemento {
            content: self.content.clone(),
            cursor: self.cursor,
        }
    }

    fn restore(&mut self, memento: &EditorMemento) {
        self.content = memento.content.clone();
        self.cursor = memento.cursor;
    }
}

struct History {
    snapshots: Vec<EditorMemento>,
}

impl History {
    fn new() -> Self {
        History { snapshots: Vec::new() }
    }

    fn push(&mut self, memento: EditorMemento) {
        self.snapshots.push(memento);
    }

    fn pop(&mut self) -> Option<EditorMemento> {
        self.snapshots.pop()
    }
}
```

**Usage**

```rust
let mut editor = TextEditor::new();
let mut history = History::new();

history.push(editor.save());
editor.type_text("Hello");

history.push(editor.save());
editor.type_text(", world!");

assert_eq!(editor.content, "Hello, world!");

let snapshot = history.pop().unwrap();
editor.restore(&snapshot);
assert_eq!(editor.content, "Hello");

let snapshot = history.pop().unwrap();
editor.restore(&snapshot);
assert_eq!(editor.content, "");
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public class EditorMemento
{
    public string Content { get; }
    public int Cursor { get; }

    internal EditorMemento(string content, int cursor)
    {
        Content = content;
        Cursor = cursor;
    }
}

public class TextEditor
{
    private string _content = "";
    private int _cursor;

    public string Content => _content;

    public void TypeText(string text)
    {
        _content = _content.Insert(_cursor, text);
        _cursor += text.Length;
    }

    public EditorMemento Save() => new(_content, _cursor);

    public void Restore(EditorMemento memento)
    {
        _content = memento.Content;
        _cursor = memento.Cursor;
    }
}

public class History
{
    private readonly Stack<EditorMemento> _snapshots = new();

    public void Push(EditorMemento memento) => _snapshots.Push(memento);
    public EditorMemento? Pop() => _snapshots.Count > 0 ? _snapshots.Pop() : null;
}
```

**Usage**

```csharp
var editor = new TextEditor();
var history = new History();

history.Push(editor.Save());
editor.TypeText("Hello");

history.Push(editor.Save());
editor.TypeText(", world!");

Console.WriteLine(editor.Content); // "Hello, world!"

editor.Restore(history.Pop()!);
Console.WriteLine(editor.Content); // "Hello"

editor.Restore(history.Pop()!);
Console.WriteLine(editor.Content); // ""
```

##### Python

**Implementation**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class EditorMemento:
    content: str
    cursor: int


class TextEditor:
    def __init__(self) -> None:
        self._content = ""
        self._cursor = 0

    @property
    def content(self) -> str:
        return self._content

    def type_text(self, text: str) -> None:
        self._content = (
            self._content[: self._cursor] + text + self._content[self._cursor :]
        )
        self._cursor += len(text)

    def save(self) -> EditorMemento:
        return EditorMemento(content=self._content, cursor=self._cursor)

    def restore(self, memento: EditorMemento) -> None:
        self._content = memento.content
        self._cursor = memento.cursor


class History:
    def __init__(self) -> None:
        self._snapshots: list[EditorMemento] = []

    def push(self, memento: EditorMemento) -> None:
        self._snapshots.append(memento)

    def pop(self) -> EditorMemento | None:
        return self._snapshots.pop() if self._snapshots else None
```

**Usage**

```python
editor = TextEditor()
history = History()

history.push(editor.save())
editor.type_text("Hello")

history.push(editor.save())
editor.type_text(", world!")

print(editor.content)  # "Hello, world!"

memento = history.pop()
assert memento is not None
editor.restore(memento)
print(editor.content)  # "Hello"

memento = history.pop()
assert memento is not None
editor.restore(memento)
print(editor.content)  # ""
```

<a id="310-visitor"></a>

### 3.10. Visitor

| **Who**  | Systems with a stable set of element types that need to support many evolving operations (compilers, document processors, scene graphs). |
|----------|--------|
| **What** | Separates an algorithm from the object structure it operates on, letting you add new operations without modifying the structure's classes. |
| **When** | When you frequently need to add new operations over a fixed set of element types, and modifying those types for every new operation is impractical. |
| **Where**| Abstract syntax trees (evaluate, pretty-print, optimize), document models (render, export, validate), UI component trees (layout, paint, accessibility audit). |
| **Why**  | Consolidates related behavior into a single visitor class rather than scattering it across every element type. New operations are added by writing a new visitor, not by touching existing elements. |
| **How**  | Define a Visitor interface with a `visit` method per element type. Each element implements an `accept(visitor)` method that calls `visitor.visit_X(self)` — this double dispatch routes to the correct visitor method based on the element's concrete type. |

The Visitor pattern uses **double dispatch** to let an external object (the visitor) define new operations over a family of element types without modifying those types. Each element implements an `accept` method that calls back into the visitor with `self`, routing to the visitor method specific to that element's type. This two-step dispatch — element calls visitor, visitor handles the specific element — resolves the correct operation at runtime without casts or type checks.

The key participants are the **Visitor** interface (declares a `visit` method for each concrete element type), **ConcreteVisitors** (implement the operations — each visitor is one complete operation across all elements), the **Element** interface (declares `accept(visitor)`), and **ConcreteElements** (implement `accept` by calling the corresponding visit method). A structure (e.g., a tree) traverses its elements, calling `accept` on each.

Visitor's fundamental trade-off is the opposite of subclassing: adding new operations is easy (write a new visitor), but adding new element types is hard (every existing visitor must be updated). This makes Visitor ideal for stable hierarchies with evolving operations (AST nodes, document elements), and a poor fit for structures where new types are added frequently.

<a id="3101-paradigm-fit"></a>

#### 3.10.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — pattern matching over algebraic data types (sum types) replaces double dispatch; each match arm is a "visit" method. |
| Data-Oriented | **Adapts well** — operations process arrays of each component type in bulk; the "visitor" is the system that iterates over typed tables. |
| OOP | **Natural fit** — canonical double-dispatch pattern with visitor and element interfaces. |
| Procedural | **Workable** — a switch/case on a type tag achieves the same dispatch, though it scatters less cleanly than a visitor object. |
| Reactive | **Workable** — streams can map elements through transform functions keyed by type, but the pattern's dispatch structure isn't a natural reactive idiom. |

<a id="3102-benefits"></a>

#### 3.10.2. Benefits

- New operations are added by writing a new visitor — no modification to element classes (Open/Closed for operations).
- Related behavior for a single operation is consolidated in one visitor class instead of scattered across element types.
- Visitors can accumulate state as they traverse the structure, enabling complex cross-element computations.

<a id="3103-trade-offs"></a>

#### 3.10.3. Trade-offs

- Adding a new element type requires updating every existing visitor — the pattern is closed for new types.
- Double dispatch adds indirection that can be confusing for developers unfamiliar with the pattern.
- Visitors may need access to element internals, which can weaken encapsulation if elements must expose state they would otherwise keep private.

<a id="3104-examples"></a>

#### 3.10.4. Examples

##### Rust

Rust's enums with pattern matching provide a native alternative to double dispatch. The trait-based approach is shown for consistency with the classical pattern. The fixed `f64` return type means non-evaluating visitors (like `Printer`) must return a dummy value; an associated type (`type Output;`) on the trait would allow each visitor to choose its return type.

**Implementation**

```rust
trait ExprVisitor {
    fn visit_number(&mut self, value: f64) -> f64;
    fn visit_binary(&mut self, left: &Expr, op: char, right: &Expr) -> f64;
}

enum Expr {
    Number(f64),
    Binary(Box<Expr>, char, Box<Expr>),
}

impl Expr {
    fn accept(&self, visitor: &mut dyn ExprVisitor) -> f64 {
        match self {
            Expr::Number(v) => visitor.visit_number(*v),
            Expr::Binary(l, op, r) => visitor.visit_binary(l, *op, r),
        }
    }
}

struct Evaluator;

impl ExprVisitor for Evaluator {
    fn visit_number(&mut self, value: f64) -> f64 {
        value
    }

    fn visit_binary(&mut self, left: &Expr, op: char, right: &Expr) -> f64 {
        let l = left.accept(self);
        let r = right.accept(self);
        match op {
            '+' => l + r,
            '-' => l - r,
            '*' => l * r,
            '/' => l / r,
            _ => panic!("unknown operator: {op}"),
        }
    }
}

struct Printer;

impl ExprVisitor for Printer {
    fn visit_number(&mut self, value: f64) -> f64 {
        print!("{value}");
        0.0
    }

    fn visit_binary(&mut self, left: &Expr, op: char, right: &Expr) -> f64 {
        print!("(");
        left.accept(self);
        print!(" {op} ");
        right.accept(self);
        print!(")");
        0.0
    }
}
```

**Usage**

```rust
let expr = Expr::Binary(
    Box::new(Expr::Number(3.0)),
    '+',
    Box::new(Expr::Binary(
        Box::new(Expr::Number(4.0)),
        '*',
        Box::new(Expr::Number(5.0)),
    )),
);

let result = expr.accept(&mut Evaluator);
assert_eq!(result, 23.0);

expr.accept(&mut Printer); // prints: (3 + (4 * 5))
```

##### C\#

**Implementation**

```csharp
using System;

public interface IExprVisitor<T>
{
    T VisitNumber(NumberExpr expr);
    T VisitBinary(BinaryExpr expr);
}

public abstract class Expr
{
    public abstract T Accept<T>(IExprVisitor<T> visitor);
}

public class NumberExpr : Expr
{
    public double Value { get; }
    public NumberExpr(double value) => Value = value;
    public override T Accept<T>(IExprVisitor<T> visitor) => visitor.VisitNumber(this);
}

public class BinaryExpr : Expr
{
    public Expr Left { get; }
    public char Op { get; }
    public Expr Right { get; }

    public BinaryExpr(Expr left, char op, Expr right)
    {
        Left = left;
        Op = op;
        Right = right;
    }

    public override T Accept<T>(IExprVisitor<T> visitor) => visitor.VisitBinary(this);
}

public class Evaluator : IExprVisitor<double>
{
    public double VisitNumber(NumberExpr expr) => expr.Value;

    public double VisitBinary(BinaryExpr expr)
    {
        double l = expr.Left.Accept(this);
        double r = expr.Right.Accept(this);
        return expr.Op switch
        {
            '+' => l + r,
            '-' => l - r,
            '*' => l * r,
            '/' => l / r,
            _ => throw new InvalidOperationException($"Unknown operator: {expr.Op}")
        };
    }
}

public class Printer : IExprVisitor<string>
{
    public string VisitNumber(NumberExpr expr) => expr.Value.ToString();

    public string VisitBinary(BinaryExpr expr)
    {
        string l = expr.Left.Accept(this);
        string r = expr.Right.Accept(this);
        return $"({l} {expr.Op} {r})";
    }
}
```

**Usage**

```csharp
Expr expr = new BinaryExpr(
    new NumberExpr(3),
    '+',
    new BinaryExpr(new NumberExpr(4), '*', new NumberExpr(5))
);

var result = expr.Accept(new Evaluator());
Console.WriteLine(result); // 23

var text = expr.Accept(new Printer());
Console.WriteLine(text); // (3 + (4 * 5))
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod
from typing import Any


class ExprVisitor(ABC):
    @abstractmethod
    def visit_number(self, value: float) -> Any: ...

    @abstractmethod
    def visit_binary(self, left: "Expr", op: str, right: "Expr") -> Any: ...


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any: ...


class NumberExpr(Expr):
    def __init__(self, value: float) -> None:
        self.value = value

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_number(self.value)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, op: str, right: Expr) -> None:
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_binary(self.left, self.op, self.right)


class Evaluator(ExprVisitor):
    def visit_number(self, value: float) -> float:
        return value

    def visit_binary(self, left: Expr, op: str, right: Expr) -> float:
        l = left.accept(self)
        r = right.accept(self)
        match op:
            case "+": return l + r
            case "-": return l - r
            case "*": return l * r
            case "/": return l / r
            case _: raise ValueError(f"unknown operator: {op}")


class Printer(ExprVisitor):
    def visit_number(self, value: float) -> str:
        return str(value)

    def visit_binary(self, left: Expr, op: str, right: Expr) -> str:
        l = left.accept(self)
        r = right.accept(self)
        return f"({l} {op} {r})"
```

**Usage**

```python
expr = BinaryExpr(
    NumberExpr(3),
    "+",
    BinaryExpr(NumberExpr(4), "*", NumberExpr(5)),
)

result = expr.accept(Evaluator())
print(result)  # 23.0

text = expr.accept(Printer())
print(text)  # (3.0 + (4.0 * 5.0))
```

<a id="311-interpreter"></a>

### 3.11. Interpreter

| **Who**  | Systems that need to evaluate or process sentences in a defined language (rule engines, query parsers, DSL evaluators). |
|----------|--------|
| **What** | Defines a representation for a grammar and an interpreter that uses the representation to evaluate sentences in the language. |
| **When** | When a problem occurs repeatedly and can be expressed as sentences in a simple language, and an interpreter for that language is a practical solution. |
| **Where**| Regular expression engines, SQL parsers, rule-based configuration systems, mathematical expression evaluators, template engines. |
| **Why**  | Provides a structured way to evaluate language constructs by mapping each grammar rule to a class, making the grammar explicit, extensible, and easy to modify. |
| **How**  | Define an abstract expression class with an `interpret` method. Create terminal expression classes (for literals and variables) and nonterminal expression classes (for grammar rules that combine other expressions). Build expression trees that mirror the grammar, and evaluate them by calling `interpret` recursively. |

The Interpreter pattern maps a grammar's rules directly to a class hierarchy. Each rule becomes a class: **terminal expressions** represent atomic elements of the language (literals, variables), and **nonterminal expressions** represent composite rules that combine sub-expressions (and, or, sequence). An expression tree built from these classes mirrors the parse tree of a sentence, and evaluating the tree is a recursive walk that calls `interpret` on each node.

The key participants are the **AbstractExpression** (declares the `interpret` method), **TerminalExpression** (implements interpret for leaf symbols — constants, variables), **NonterminalExpression** (implements interpret by combining results of child expressions), and the **Context** (holds global information the interpreter needs, such as variable bindings). The client constructs the expression tree (often using a parser) and then calls `interpret` on the root.

Interpreter works well for small, simple grammars where the overhead of a full parser generator is unjustified. For complex grammars, the class explosion (one class per rule) becomes unmanageable, and tools like parser combinators, ANTLR, or hand-written recursive-descent parsers are preferred. The pattern is closely related to Composite (the expression tree is a composite structure) and Visitor (an external visitor can replace the `interpret` method to add new operations over the grammar).

<a id="3111-domain-context"></a>

#### 3.11.1. Domain Context

Primarily relevant in language tooling, DSLs, rule engines, and compilers. Rarely encountered in general application code that doesn't need to parse or evaluate expressions.

<a id="3112-paradigm-fit"></a>

#### 3.11.2. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — algebraic data types for the AST and recursive functions for interpretation; pattern matching replaces the class hierarchy. |
| Data-Oriented | **Uncommon** — expression trees are pointer-heavy and recursive, which conflicts with flat, cache-friendly data layouts. |
| OOP | **Natural fit** — each grammar rule maps to a class with a polymorphic `interpret` method. |
| Procedural | **Workable** — tagged unions with a switch-based evaluator achieve the same result without a class hierarchy. |
| Reactive | **Uncommon** — expression evaluation is typically a synchronous tree walk, not a stream-based process. |

<a id="3113-benefits"></a>

#### 3.11.3. Benefits

- Grammar is explicit in the class structure — each rule is a self-contained, testable class.
- Easy to extend with new expressions by adding new classes without modifying existing ones.
- Expression trees can be composed, reused, and transformed programmatically.

<a id="3114-trade-offs"></a>

#### 3.11.4. Trade-offs

- One class per grammar rule leads to class explosion for complex grammars.
- Recursive interpretation can be slow for large expression trees compared to compiled or bytecode-based evaluation.
- Building the expression tree typically requires a separate parser, adding complexity.

<a id="3115-examples"></a>

#### 3.11.5. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

type Context = HashMap<String, bool>;

trait BoolExpr {
    fn interpret(&self, ctx: &Context) -> bool;
}

struct Constant(bool);

impl BoolExpr for Constant {
    fn interpret(&self, _ctx: &Context) -> bool {
        self.0
    }
}

struct Variable(String);

impl BoolExpr for Variable {
    fn interpret(&self, ctx: &Context) -> bool {
        *ctx.get(&self.0).unwrap_or(&false)
    }
}

struct And {
    left: Box<dyn BoolExpr>,
    right: Box<dyn BoolExpr>,
}

impl BoolExpr for And {
    fn interpret(&self, ctx: &Context) -> bool {
        self.left.interpret(ctx) && self.right.interpret(ctx)
    }
}

struct Or {
    left: Box<dyn BoolExpr>,
    right: Box<dyn BoolExpr>,
}

impl BoolExpr for Or {
    fn interpret(&self, ctx: &Context) -> bool {
        self.left.interpret(ctx) || self.right.interpret(ctx)
    }
}

struct Not {
    operand: Box<dyn BoolExpr>,
}

impl BoolExpr for Not {
    fn interpret(&self, ctx: &Context) -> bool {
        !self.operand.interpret(ctx)
    }
}
```

**Usage**

```rust
let expr: Box<dyn BoolExpr> = Box::new(Or {
    left: Box::new(And {
        left: Box::new(Variable("x".into())),
        right: Box::new(Variable("y".into())),
    }),
    right: Box::new(Not {
        operand: Box::new(Variable("z".into())),
    }),
});

let mut ctx = HashMap::new();
ctx.insert("x".into(), true);
ctx.insert("y".into(), false);
ctx.insert("z".into(), false);

assert!(expr.interpret(&ctx)); // (x AND y) OR (NOT z) = (false) OR (true) = true
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public interface IBoolExpr
{
    bool Interpret(Dictionary<string, bool> context);
}

public class Constant : IBoolExpr
{
    private readonly bool _value;
    public Constant(bool value) => _value = value;
    public bool Interpret(Dictionary<string, bool> context) => _value;
}

public class Variable : IBoolExpr
{
    private readonly string _name;
    public Variable(string name) => _name = name;

    public bool Interpret(Dictionary<string, bool> context) =>
        context.TryGetValue(_name, out var val) && val;
}

public class And : IBoolExpr
{
    private readonly IBoolExpr _left, _right;
    public And(IBoolExpr left, IBoolExpr right) { _left = left; _right = right; }
    public bool Interpret(Dictionary<string, bool> context) =>
        _left.Interpret(context) && _right.Interpret(context);
}

public class Or : IBoolExpr
{
    private readonly IBoolExpr _left, _right;
    public Or(IBoolExpr left, IBoolExpr right) { _left = left; _right = right; }
    public bool Interpret(Dictionary<string, bool> context) =>
        _left.Interpret(context) || _right.Interpret(context);
}

public class Not : IBoolExpr
{
    private readonly IBoolExpr _operand;
    public Not(IBoolExpr operand) => _operand = operand;
    public bool Interpret(Dictionary<string, bool> context) =>
        !_operand.Interpret(context);
}
```

**Usage**

```csharp
IBoolExpr expr = new Or(
    new And(new Variable("x"), new Variable("y")),
    new Not(new Variable("z"))
);

var ctx = new Dictionary<string, bool>
{
    ["x"] = true,
    ["y"] = false,
    ["z"] = false
};

Console.WriteLine(expr.Interpret(ctx)); // True: (x AND y) OR (NOT z)
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class BoolExpr(ABC):
    @abstractmethod
    def interpret(self, context: dict[str, bool]) -> bool: ...


class Constant(BoolExpr):
    def __init__(self, value: bool) -> None:
        self._value = value

    def interpret(self, context: dict[str, bool]) -> bool:
        return self._value


class Variable(BoolExpr):
    def __init__(self, name: str) -> None:
        self._name = name

    def interpret(self, context: dict[str, bool]) -> bool:
        return context.get(self._name, False)


class And(BoolExpr):
    def __init__(self, left: BoolExpr, right: BoolExpr) -> None:
        self._left = left
        self._right = right

    def interpret(self, context: dict[str, bool]) -> bool:
        return self._left.interpret(context) and self._right.interpret(context)


class Or(BoolExpr):
    def __init__(self, left: BoolExpr, right: BoolExpr) -> None:
        self._left = left
        self._right = right

    def interpret(self, context: dict[str, bool]) -> bool:
        return self._left.interpret(context) or self._right.interpret(context)


class Not(BoolExpr):
    def __init__(self, operand: BoolExpr) -> None:
        self._operand = operand

    def interpret(self, context: dict[str, bool]) -> bool:
        return not self._operand.interpret(context)
```

**Usage**

```python
expr = Or(
    And(Variable("x"), Variable("y")),
    Not(Variable("z")),
)

ctx = {"x": True, "y": False, "z": False}
print(expr.interpret(ctx))  # True: (x AND y) OR (NOT z)
```

<a id="312-null-object"></a>

### 3.12. Null Object

| **Who**  | Any client code that would otherwise need null checks before invoking an object's methods. |
|----------|--------|
| **What** | Provides a do-nothing implementation of an interface, replacing `null` references with a real object that conforms to the expected contract but performs no action. |
| **When** | When default "do nothing" behavior is preferable to scattering null checks throughout the codebase. |
| **Where**| Logging (NullLogger), event handling (no-op handlers), default strategies, optional dependencies that may not be configured. |
| **Why**  | Eliminates defensive null checks, reduces NullPointerException/NullReferenceException risks, and simplifies client code by guaranteeing the collaborator is always a valid object. |
| **How**  | Define an abstract object (interface/base class). Implement a "real" version that performs useful work and a "null" version that implements the same interface with no-op methods. Clients always receive an object — never null — so they call methods unconditionally. |

The Null Object pattern replaces the absence of an object (`null`, `None`, `nil`) with a concrete object that does nothing. The null object implements the same interface as the "real" object, so client code never needs to check whether a collaborator exists before calling its methods. Every method on the null object is a no-op: it returns sensible defaults (empty strings, zero, empty collections) and performs no side effects.

The key participants are the **AbstractObject** (the interface or base class that defines the contract), the **RealObject** (the implementation that does actual work), and the **NullObject** (the implementation that conforms to the contract but does nothing). The client depends on the abstract interface and is unaware of which implementation it holds. Factory methods or dependency injection supply the null object when no real implementation is available.

Null Object is different from Optional/Maybe types, which make the absence of a value explicit and force the caller to handle it. Null Object hides the absence by providing a valid stand-in — this is its strength (simple client code) and its risk (silent failures if the null object masks a genuine configuration error). Use Null Object when "do nothing" is genuinely correct default behavior, not when the absence of a dependency indicates a bug.

<a id="3121-paradigm-fit"></a>

#### 3.12.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — `Option`/`Maybe` with `map`/`getOrElse` or identity functions serve the same purpose; the pattern is implicit in monadic handling. |
| Data-Oriented | **Workable** — default-valued components or sentinel rows in tables replace the concept of a null entity. |
| OOP | **Natural fit** — a concrete class implementing the interface with no-op methods is the canonical form. |
| Procedural | **Workable** — a no-op function or struct with zeroed fields serves as the null stand-in. |
| Reactive | **Adapts well** — `EMPTY` observables or no-op subscribers represent the absence of a real producer/consumer. |

<a id="3122-benefits"></a>

#### 3.12.2. Benefits

- Eliminates pervasive null checks — client code calls methods unconditionally, reducing boilerplate and NullPointerException risk.
- Simplifies client logic by guaranteeing that every collaborator is a valid, callable object.
- Null objects are trivially testable and can serve as safe defaults in dependency injection.

<a id="3123-trade-offs"></a>

#### 3.12.3. Trade-offs

- Silent no-ops can mask configuration errors — if a real dependency was expected but a null object was supplied, failures go undetected.
- Every interface change requires updating the null object alongside the real implementations.
- Can obscure program flow: debugging is harder when "nothing happens" without any explicit indication of why.

<a id="3124-examples"></a>

#### 3.12.4. Examples

##### Rust

Rust's `Option` type and trait defaults provide idiomatic alternatives, but the Null Object pattern is useful when a trait object must always be present.

**Implementation**

```rust
trait Logger {
    fn info(&self, message: &str);
    fn error(&self, message: &str);
}

struct ConsoleLogger;

impl Logger for ConsoleLogger {
    fn info(&self, message: &str) {
        println!("[INFO] {message}");
    }

    fn error(&self, message: &str) {
        eprintln!("[ERROR] {message}");
    }
}

struct NullLogger;

impl Logger for NullLogger {
    fn info(&self, _message: &str) {}
    fn error(&self, _message: &str) {}
}

struct OrderService {
    logger: Box<dyn Logger>,
}

impl OrderService {
    fn new(logger: Box<dyn Logger>) -> Self {
        OrderService { logger }
    }

    fn place_order(&self, item: &str) {
        self.logger.info(&format!("Placing order for {item}"));
        println!("Order placed: {item}");
        self.logger.info(&format!("Order for {item} completed"));
    }
}
```

**Usage**

```rust
let service = OrderService::new(Box::new(ConsoleLogger));
service.place_order("Widget"); // logs to console

let quiet_service = OrderService::new(Box::new(NullLogger));
quiet_service.place_order("Gadget"); // no logging output
```

##### C\#

**Implementation**

```csharp
using System;

public interface ILogger
{
    void Info(string message);
    void Error(string message);
}

public class ConsoleLogger : ILogger
{
    public void Info(string message) => Console.WriteLine($"[INFO] {message}");
    public void Error(string message) => Console.Error.WriteLine($"[ERROR] {message}");
}

public class NullLogger : ILogger
{
    public void Info(string message) { }
    public void Error(string message) { }
}

public class OrderService
{
    private readonly ILogger _logger;

    public OrderService(ILogger? logger = null) => _logger = logger ?? new NullLogger();

    public void PlaceOrder(string item)
    {
        _logger.Info($"Placing order for {item}");
        Console.WriteLine($"Order placed: {item}");
        _logger.Info($"Order for {item} completed");
    }
}
```

**Usage**

```csharp
var service = new OrderService(new ConsoleLogger());
service.PlaceOrder("Widget"); // logs to console

var quietService = new OrderService();
quietService.PlaceOrder("Gadget"); // no logging output
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def info(self, message: str) -> None: ...

    @abstractmethod
    def error(self, message: str) -> None: ...


class ConsoleLogger(Logger):
    def info(self, message: str) -> None:
        print(f"[INFO] {message}")

    def error(self, message: str) -> None:
        print(f"[ERROR] {message}")


class NullLogger(Logger):
    def info(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass


class OrderService:
    def __init__(self, logger: Logger | None = None) -> None:
        self._logger: Logger = logger if logger is not None else NullLogger()

    def place_order(self, item: str) -> None:
        self._logger.info(f"Placing order for {item}")
        print(f"Order placed: {item}")
        self._logger.info(f"Order for {item} completed")
```

**Usage**

```python
service = OrderService(ConsoleLogger())
service.place_order("Widget")  # logs to console

quiet_service = OrderService()
quiet_service.place_order("Gadget")  # no logging output
```

<a id="313-dependency-injection"></a>

### 3.13. Dependency Injection

| **Who**  | Any class or module that depends on external services, repositories, or collaborators. |
|----------|--------|
| **What** | Externally supplies an object's dependencies rather than having the object create or locate them internally. |
| **When** | When you want to decouple a class from the concrete implementations of its dependencies, enabling testability, flexibility, and adherence to the Dependency Inversion Principle. |
| **Where**| Service layers, controllers, repositories, any component that depends on infrastructure (databases, APIs, file systems, loggers). |
| **Why**  | Makes classes easier to test (inject mocks), easier to reconfigure (swap implementations), and easier to reason about (explicit dependency graph). |
| **How**  | Accept dependencies through the constructor (constructor injection — the most common form), setter methods (setter injection), or an interface the class implements to receive its dependencies (interface injection). An external assembler — manual composition root or IoC container — wires the object graph. |

Dependency Injection (DI) inverts the flow of dependency creation: instead of a class constructing or locating its collaborators internally, an external entity supplies them. The class declares what it needs (typically through constructor parameters or interface contracts), and the assembler provides the concrete implementations. This makes the dependency graph explicit — every dependency is visible in the constructor signature — and ensures that classes depend on abstractions, not on concrete types.

The three forms are **constructor injection** (dependencies passed as constructor arguments — the most common and recommended form because it makes dependencies mandatory and immutable), **setter injection** (dependencies set via properties or methods — useful for optional dependencies), and **interface injection** (the class implements an interface that exposes a setter, allowing the injector to supply the dependency). In practice, constructor injection covers the vast majority of use cases.

DI is not the same as a DI container or IoC framework — those are tools that automate the wiring, but DI itself is a plain design principle. Manual DI (commonly called "pure DI") works perfectly: a composition root at the application's entry point constructs the object graph explicitly. Containers add value in large applications where the graph is deep and cross-cutting concerns (lifecycle management, scoping) justify the framework overhead.

The examples below show constructor injection — the most common form. **Setter injection** (assigning dependencies via properties after construction) is useful for optional dependencies that have sensible defaults, but makes the dependency graph harder to reason about since objects can exist in a partially configured state.

<a id="3131-paradigm-fit"></a>

#### 3.13.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — passing dependencies as function arguments (or via reader monads / partial application) is idiomatic; every higher-order function is a form of DI. |
| Data-Oriented | **Adapts well** — systems receive their data sources and configuration externally; the ECS world object is itself an injected context. |
| OOP | **Natural fit** — constructor injection with interfaces is the canonical form; IoC containers automate the wiring. |
| Procedural | **Workable** — passing struct pointers or function pointers to procedures achieves the same decoupling. |
| Reactive | **Adapts well** — services and data sources are injected into stream pipelines as external dependencies; Angular's DI system is a prominent example. |

<a id="3132-benefits"></a>

#### 3.13.2. Benefits

- Explicit dependency graph — every dependency is visible in the constructor, eliminating hidden coupling.
- Testability — injecting mocks, stubs, or fakes replaces real dependencies without modifying the class under test.
- Flexibility — swapping implementations (e.g., switching payment gateways, swapping a cache backend) requires changing only the composition root.

<a id="3133-trade-offs"></a>

#### 3.13.3. Trade-offs

- Constructor parameter lists can grow long in deeply dependent classes, signaling a need to refactor responsibilities.
- Indirection increases — the reader must trace through the composition root or container configuration to understand which concrete types are wired.
- IoC containers add framework complexity, magic (auto-resolution, convention-based binding), and potential runtime errors if bindings are misconfigured.

<a id="3134-examples"></a>

#### 3.13.4. Examples

##### Rust

Rust uses trait objects or generics for DI. Generics (monomorphization) are preferred for performance; trait objects provide runtime flexibility.

**Implementation**

```rust
trait PaymentGateway {
    fn charge(&self, amount: f64) -> Result<String, String>;
}

struct StripeGateway;

impl PaymentGateway for StripeGateway {
    fn charge(&self, amount: f64) -> Result<String, String> {
        Ok(format!("Stripe charged ${amount:.2}"))
    }
}

struct MockGateway {
    should_fail: bool,
}

impl PaymentGateway for MockGateway {
    fn charge(&self, amount: f64) -> Result<String, String> {
        if self.should_fail {
            Err("Payment declined".into())
        } else {
            Ok(format!("Mock charged ${amount:.2}"))
        }
    }
}

struct OrderService<G: PaymentGateway> {
    gateway: G,
}

impl<G: PaymentGateway> OrderService<G> {
    fn new(gateway: G) -> Self {
        OrderService { gateway }
    }

    fn place_order(&self, item: &str, price: f64) -> Result<String, String> {
        self.gateway.charge(price)?;
        Ok(format!("Order placed: {item}"))
    }
}
```

**Usage**

```rust
let service = OrderService::new(StripeGateway);
println!("{}", service.place_order("Widget", 29.99).unwrap());

let test_service = OrderService::new(MockGateway { should_fail: false });
assert!(test_service.place_order("Gadget", 9.99).is_ok());

let failing_service = OrderService::new(MockGateway { should_fail: true });
assert!(failing_service.place_order("Gadget", 9.99).is_err());
```

##### C\#

**Implementation**

```csharp
using System;

public interface IPaymentGateway
{
    string Charge(decimal amount);
}

public class StripeGateway : IPaymentGateway
{
    public string Charge(decimal amount) => $"Stripe charged ${amount:F2}";
}

public class MockGateway : IPaymentGateway
{
    public bool ShouldFail { get; set; }

    public string Charge(decimal amount) =>
        ShouldFail
            ? throw new InvalidOperationException("Payment declined")
            : $"Mock charged ${amount:F2}";
}

public class OrderService
{
    private readonly IPaymentGateway _gateway;

    public OrderService(IPaymentGateway gateway) => _gateway = gateway;

    public string PlaceOrder(string item, decimal price)
    {
        var receipt = _gateway.Charge(price);
        return $"Order placed: {item} — {receipt}";
    }
}
```

**Usage**

```csharp
var service = new OrderService(new StripeGateway());
Console.WriteLine(service.PlaceOrder("Widget", 29.99m));

var testService = new OrderService(new MockGateway { ShouldFail = false });
Console.WriteLine(testService.PlaceOrder("Gadget", 9.99m));
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> str: ...


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> str:
        return f"Stripe charged ${amount:.2f}"


class MockGateway(PaymentGateway):
    def __init__(self, *, should_fail: bool = False) -> None:
        self._should_fail = should_fail

    def charge(self, amount: float) -> str:
        if self._should_fail:
            raise RuntimeError("Payment declined")
        return f"Mock charged ${amount:.2f}"


class OrderService:
    def __init__(self, gateway: PaymentGateway) -> None:
        self._gateway = gateway

    def place_order(self, item: str, price: float) -> str:
        self._gateway.charge(price)
        return f"Order placed: {item}"
```

**Usage**

```python
service = OrderService(StripeGateway())
print(service.place_order("Widget", 29.99))

test_service = OrderService(MockGateway(should_fail=False))
print(test_service.place_order("Gadget", 9.99))

failing_service = OrderService(MockGateway(should_fail=True))
try:
    failing_service.place_order("Gadget", 9.99)
except RuntimeError as e:
    print(e)  # Payment declined
```

<a id="4-architectural"></a>

## 4. Architectural

Architectural patterns address system-level concerns — how components, services, and data flows are organized across application boundaries. Unlike creational, structural, and behavioral patterns which operate at the object level, architectural patterns shape the overall topology and communication style of a system.

| Pattern | When to Use |
|---------|-------------|
| [Repository](#41-repository) | Abstracting data access behind a collection-like interface. |
| [Unit of Work](#42-unit-of-work) | Coordinating multiple data changes as a single atomic transaction. |
| [CQRS](#43-cqrs) | Optimizing reads and writes independently in systems with asymmetric loads. |
| [Event Sourcing](#44-event-sourcing) | Storing state as an append-only sequence of domain events for audit and replay. |
| [Circuit Breaker](#45-circuit-breaker) | Preventing cascading failures by short-circuiting calls to unhealthy services. |
| [Saga](#46-saga) | Managing distributed transactions across multiple services with compensating rollbacks. |
| [Specification](#47-specification) | Composing reusable business rules as combinable boolean predicates. |

<a id="41-repository"></a>

### 4.1. Repository

| **Who**  | Applications with persistent data storage that need to decouple domain logic from data access mechanics. |
|----------|--------|
| **What** | Mediates between domain logic and data access, providing a collection-like interface over a data store. |
| **When** | When domain code should remain ignorant of how and where data is persisted — databases, file systems, APIs, or in-memory stores. |
| **Where**| Between the domain/service layer and the persistence layer in layered or hexagonal architectures. |
| **Why**  | Isolates persistence concerns so domain logic can be tested, reasoned about, and evolved without coupling to a specific storage technology. |
| **How**  | Define a repository interface with collection-style methods (get, add, remove, find). Implement a concrete repository that translates those calls into storage-specific operations (SQL queries, API calls, file I/O). Domain code depends only on the interface. |

The Repository pattern introduces an abstraction layer between domain logic and data access. It exposes a collection-like interface — `get`, `add`, `remove`, `find` — that lets domain code treat persistent storage as if it were an in-memory collection. The concrete repository translates these high-level operations into storage-specific calls (SQL queries, HTTP requests, file operations), keeping persistence details out of the domain layer entirely.

The key participants are the **repository interface** (the contract domain code depends on), the **concrete repository** (the implementation bound to a specific storage technology), and the **domain entity** (the object being persisted and retrieved). In hexagonal architecture, the repository interface lives in the domain layer while the concrete implementation lives in the infrastructure layer, making the dependency point inward.

Repository is often paired with Unit of Work to coordinate multi-entity transactions. A common pitfall is "repository bloat" — accumulating dozens of query methods. This can be mitigated by combining Repository with Specification (for composable queries) or by keeping repositories focused on aggregate roots rather than every entity.

<a id="411-domain-context"></a>

#### 4.1.1. Domain Context

Primarily relevant in applications with persistent data storage (databases, file systems, external APIs). Rarely encountered in stateless utilities, CLI tools, or applications without a data layer.

<a id="412-system-fit"></a>

#### 4.1.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — centralizes data access behind clean interfaces within a single deployable. |
| Microservices | **Natural fit** — each service owns its repository, enforcing bounded-context data isolation. |
| Serverless | **Adapts well** — repository instances are short-lived but still decouple handler logic from storage. |
| Event-Driven | **Adapts well** — repositories persist aggregates while events flow through separate channels. |

<a id="413-benefits"></a>

#### 4.1.3. Benefits

- Decouples domain logic from storage technology — switching from PostgreSQL to DynamoDB requires only a new concrete repository.
- Enables unit testing of domain logic with in-memory or mock repositories, eliminating database dependencies in tests.
- Centralizes data access logic, making query optimizations and caching strategies easier to apply consistently.

<a id="414-trade-offs"></a>

#### 4.1.4. Trade-offs

- Adds an abstraction layer that may be unnecessary for simple CRUD applications with no domain logic.
- Repository interfaces can bloat with query methods; discipline is needed to keep them focused on aggregate roots.
- Leaky abstractions emerge when storage-specific concepts (pagination cursors, query hints) bleed into the interface.

<a id="415-examples"></a>

#### 4.1.5. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

pub trait UserRepository {
    fn find_by_id(&self, id: u64) -> Option<&User>;
    fn find_by_email(&self, email: &str) -> Option<&User>;
    fn add(&mut self, user: User);
    fn remove(&mut self, id: u64) -> bool;
}

#[derive(Debug, Clone)]
pub struct User {
    pub id: u64,
    pub name: String,
    pub email: String,
}

pub struct InMemoryUserRepository {
    store: HashMap<u64, User>,
}

impl InMemoryUserRepository {
    pub fn new() -> Self {
        InMemoryUserRepository { store: HashMap::new() }
    }
}

impl UserRepository for InMemoryUserRepository {
    fn find_by_id(&self, id: u64) -> Option<&User> {
        self.store.get(&id)
    }

    fn find_by_email(&self, email: &str) -> Option<&User> {
        self.store.values().find(|u| u.email == email)
    }

    fn add(&mut self, user: User) {
        self.store.insert(user.id, user);
    }

    fn remove(&mut self, id: u64) -> bool {
        self.store.remove(&id).is_some()
    }
}
```

**Usage**

```rust
let mut repo = InMemoryUserRepository::new();
repo.add(User { id: 1, name: "Alice".into(), email: "alice@example.com".into() });

if let Some(user) = repo.find_by_email("alice@example.com") {
    println!("Found: {} (id={})", user.name, user.id);
}

repo.remove(1);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public record User(long Id, string Name, string Email);

public interface IUserRepository
{
    User? FindById(long id);
    User? FindByEmail(string email);
    void Add(User user);
    bool Remove(long id);
}

public class InMemoryUserRepository : IUserRepository
{
    private readonly Dictionary<long, User> _store = new();

    public User? FindById(long id) =>
        _store.GetValueOrDefault(id);

    public User? FindByEmail(string email) =>
        _store.Values.FirstOrDefault(u => u.Email == email);

    public void Add(User user) =>
        _store[user.Id] = user;

    public bool Remove(long id) =>
        _store.Remove(id);
}
```

**Usage**

```csharp
IUserRepository repo = new InMemoryUserRepository();
repo.Add(new User(1, "Alice", "alice@example.com"));

var user = repo.FindByEmail("alice@example.com");
if (user is not null)
    Console.WriteLine($"Found: {user.Name} (id={user.Id})");

repo.Remove(1);
```

##### Python

**Implementation**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, id: int) -> User | None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def add(self, user: User) -> None: ...

    @abstractmethod
    def remove(self, id: int) -> bool: ...

class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._store: dict[int, User] = {}

    def find_by_id(self, id: int) -> User | None:
        return self._store.get(id)

    def find_by_email(self, email: str) -> User | None:
        return next((u for u in self._store.values() if u.email == email), None)

    def add(self, user: User) -> None:
        self._store[user.id] = user

    def remove(self, id: int) -> bool:
        return self._store.pop(id, None) is not None
```

**Usage**

```python
repo: UserRepository = InMemoryUserRepository()
repo.add(User(id=1, name="Alice", email="alice@example.com"))

user = repo.find_by_email("alice@example.com")
if user:
    print(f"Found: {user.name} (id={user.id})")

repo.remove(1)
```

<a id="42-unit-of-work"></a>

### 4.2. Unit of Work

| **Who**  | Applications performing multiple related data modifications that must succeed or fail together. |
|----------|--------|
| **What** | Tracks changes to objects during a business transaction and coordinates writing them out as a single atomic operation. |
| **When** | When multiple entities are created, updated, or deleted within a single business operation and consistency requires all-or-nothing semantics. |
| **Where**| Between the service/application layer and the repository layer, wrapping a database transaction or equivalent atomic boundary. |
| **Why**  | Prevents partial writes that leave data in an inconsistent state, reduces redundant database round-trips by batching changes, and centralizes transaction management. |
| **How**  | Create a Unit of Work that tracks new, modified, and removed entities. Repositories register changes with the UoW rather than writing directly. A `commit` method flushes all tracked changes in a single transaction; `rollback` discards them. |

The Unit of Work pattern maintains a list of objects affected by a business transaction and coordinates the writing out of changes as a single atomic operation. Rather than each repository call immediately hitting the database, changes are registered with the Unit of Work — new entities, dirty (modified) entities, and removed entities — and flushed together when `commit` is called. If anything fails, the entire batch is rolled back.

The key participants are the **Unit of Work** itself (which tracks the change set and owns the transaction), the **repositories** (which are accessed through or managed by the UoW), and the **domain entities** (whose lifecycle changes are being tracked). In many ORM frameworks (Entity Framework's `DbContext`, SQLAlchemy's `Session`, Hibernate's `Session`), the Unit of Work is built into the framework — you are using it whether you name it or not.

The pattern reduces the number of database round-trips (one batched write instead of many individual ones), ensures atomicity without requiring the caller to manage transactions manually, and prevents the inconsistency that arises when some writes succeed and others fail within a single business operation. A closely related concept is the **Identity Map**, which ensures each entity is loaded only once per UoW scope — preventing duplicate in-memory instances from diverging. Most ORM frameworks bundle an Identity Map into their UoW implementation.

<a id="421-domain-context"></a>

#### 4.2.1. Domain Context

Primarily relevant in applications performing multiple related data modifications that must succeed or fail together. Uncommon in read-heavy or single-write applications where atomic batching adds no value.

<a id="422-system-fit"></a>

#### 4.2.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — wraps a single database transaction spanning multiple repositories. |
| Microservices | **Workable** — limited to each service's local database; cross-service atomicity requires Saga instead. |
| Serverless | **Workable** — short function lifetimes suit small units of work, but connection pooling needs care. |
| Event-Driven | **Adapts well** — commit can atomically persist changes and publish domain events (transactional outbox). |

<a id="423-benefits"></a>

#### 4.2.3. Benefits

- Guarantees atomicity — all changes within a business operation succeed or fail together.
- Reduces database round-trips by batching inserts, updates, and deletes into a single flush.
- Centralizes transaction management, removing explicit begin/commit/rollback calls from service code.

<a id="424-trade-offs"></a>

#### 4.2.4. Trade-offs

- Adds complexity to track entity states (new, dirty, removed) and detect changes.
- Long-lived units of work can hold database locks or accumulate large change sets, increasing conflict risk.
- Implicit change tracking can surprise developers when modifications are flushed at unexpected times.

<a id="425-examples"></a>

#### 4.2.5. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct Entity {
    pub id: u64,
    pub name: String,
}

pub struct UnitOfWork {
    new_entities: Vec<Entity>,
    dirty_entities: HashMap<u64, Entity>,
    removed_ids: Vec<u64>,
}

impl UnitOfWork {
    pub fn new() -> Self {
        UnitOfWork {
            new_entities: Vec::new(),
            dirty_entities: HashMap::new(),
            removed_ids: Vec::new(),
        }
    }

    pub fn register_new(&mut self, entity: Entity) {
        self.new_entities.push(entity);
    }

    pub fn register_dirty(&mut self, entity: Entity) {
        self.dirty_entities.insert(entity.id, entity);
    }

    pub fn register_removed(&mut self, id: u64) {
        self.removed_ids.push(id);
    }

    pub fn commit(&mut self) {
        println!("BEGIN TRANSACTION");
        for e in &self.new_entities {
            println!("  INSERT: {:?}", e);
        }
        for e in self.dirty_entities.values() {
            println!("  UPDATE: {:?}", e);
        }
        for id in &self.removed_ids {
            println!("  DELETE: id={}", id);
        }
        println!("COMMIT");

        self.new_entities.clear();
        self.dirty_entities.clear();
        self.removed_ids.clear();
    }

    pub fn rollback(&mut self) {
        self.new_entities.clear();
        self.dirty_entities.clear();
        self.removed_ids.clear();
    }
}
```

**Usage**

```rust
let mut uow = UnitOfWork::new();
uow.register_new(Entity { id: 1, name: "Alice".into() });
uow.register_new(Entity { id: 2, name: "Bob".into() });
uow.register_dirty(Entity { id: 1, name: "Alice Updated".into() });
uow.register_removed(3);
uow.commit();
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public record Entity(long Id, string Name);

public class UnitOfWork
{
    private readonly List<Entity> _newEntities = new();
    private readonly Dictionary<long, Entity> _dirtyEntities = new();
    private readonly List<long> _removedIds = new();

    public void RegisterNew(Entity entity) => _newEntities.Add(entity);
    public void RegisterDirty(Entity entity) => _dirtyEntities[entity.Id] = entity;
    public void RegisterRemoved(long id) => _removedIds.Add(id);

    public void Commit()
    {
        Console.WriteLine("BEGIN TRANSACTION");
        foreach (var e in _newEntities)
            Console.WriteLine($"  INSERT: {e}");
        foreach (var e in _dirtyEntities.Values)
            Console.WriteLine($"  UPDATE: {e}");
        foreach (var id in _removedIds)
            Console.WriteLine($"  DELETE: id={id}");
        Console.WriteLine("COMMIT");

        _newEntities.Clear();
        _dirtyEntities.Clear();
        _removedIds.Clear();
    }

    public void Rollback()
    {
        _newEntities.Clear();
        _dirtyEntities.Clear();
        _removedIds.Clear();
    }
}
```

**Usage**

```csharp
var uow = new UnitOfWork();
uow.RegisterNew(new Entity(1, "Alice"));
uow.RegisterNew(new Entity(2, "Bob"));
uow.RegisterDirty(new Entity(1, "Alice Updated"));
uow.RegisterRemoved(3);
uow.Commit();
```

##### Python

**Implementation**

```python
from dataclasses import dataclass

@dataclass
class Entity:
    id: int
    name: str

class UnitOfWork:
    def __init__(self) -> None:
        self._new: list[Entity] = []
        self._dirty: dict[int, Entity] = {}
        self._removed: list[int] = []

    def register_new(self, entity: Entity) -> None:
        self._new.append(entity)

    def register_dirty(self, entity: Entity) -> None:
        self._dirty[entity.id] = entity

    def register_removed(self, id: int) -> None:
        self._removed.append(id)

    def commit(self) -> None:
        print("BEGIN TRANSACTION")
        for e in self._new:
            print(f"  INSERT: {e}")
        for e in self._dirty.values():
            print(f"  UPDATE: {e}")
        for id in self._removed:
            print(f"  DELETE: id={id}")
        print("COMMIT")
        self._new.clear()
        self._dirty.clear()
        self._removed.clear()

    def rollback(self) -> None:
        self._new.clear()
        self._dirty.clear()
        self._removed.clear()
```

**Usage**

```python
uow = UnitOfWork()
uow.register_new(Entity(id=1, name="Alice"))
uow.register_new(Entity(id=2, name="Bob"))
uow.register_dirty(Entity(id=1, name="Alice Updated"))
uow.register_removed(3)
uow.commit()
```

<a id="43-cqrs"></a>

### 4.3. CQRS

| **Who**  | Systems with asymmetric read/write loads or complex domain models that benefit from independent optimization. |
|----------|--------|
| **What** | Separates read and write models so each can be optimized independently — commands mutate state, queries read it. |
| **When** | When read and write workloads have different performance, scaling, or structural requirements, and a single model cannot serve both well. |
| **Where**| Between the application layer and the data layer, often in conjunction with Event Sourcing or domain-driven design. |
| **Why**  | Eliminates the tension between a normalized write model (optimized for consistency) and a denormalized read model (optimized for query performance). |
| **How**  | Define separate command and query models. Commands pass through handlers that validate and mutate the write store. Queries pass through handlers that read from a denormalized read store. A synchronization mechanism (events, projections, or materialized views) keeps the read model up to date. |

CQRS (Command Query Responsibility Segregation) splits an application's data model into two: a **command model** optimized for writes and a **query model** optimized for reads. Commands represent intentions to change state — they are validated, processed, and applied to the write store. Queries retrieve data from a separate read store that is structured for fast, flexible reads (denormalized tables, materialized views, search indices). The two stores are synchronized through events, projections, or database-level replication.

The key participants are **commands** (data structures representing write intentions), **command handlers** (which validate and execute commands against the write model), **queries** (data structures representing read requests), **query handlers** (which fetch from the read model), and the **synchronization layer** (which projects write-side changes into the read model). In simpler forms, the two "models" can be different query paths in the same database rather than physically separate stores.

CQRS adds significant structural complexity and is overkill for simple CRUD applications. It shines in systems where reads vastly outnumber writes (or vice versa), where the read shape differs dramatically from the write shape, or where independent scaling of read and write workloads is required. It pairs naturally with Event Sourcing, where the event log serves as the write model and projections build the read model.

<a id="431-domain-context"></a>

#### 4.3.1. Domain Context

Primarily relevant in systems with asymmetric read/write loads or complex domain models where a single model cannot efficiently serve both reads and writes. Overkill for simple CRUD applications with balanced read/write patterns and straightforward data shapes.

<a id="432-system-fit"></a>

#### 4.3.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Adapts well** — separate read/write paths within a single deployable, often sharing the same database. |
| Microservices | **Natural fit** — read and write sides can be independent services scaled separately. |
| Serverless | **Adapts well** — command and query handlers map naturally to separate functions with independent scaling. |
| Event-Driven | **Natural fit** — events bridge the write and read models; projections consume events to build read stores. |

<a id="433-benefits"></a>

#### 4.3.3. Benefits

- Independent optimization — the write model can be normalized for consistency while the read model is denormalized for performance.
- Read and write workloads scale independently, each provisioned for its actual load.
- Simplifies complex domains by letting each side model only the concerns it handles.

<a id="434-trade-offs"></a>

#### 4.3.4. Trade-offs

- Eventual consistency between write and read models requires the application and users to tolerate stale reads.
- Doubles the number of models, handlers, and synchronization code — significant structural overhead.
- Debugging requires tracing through command handlers, events, and projections rather than a single code path.

<a id="435-examples"></a>

#### 4.3.5. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

pub struct Product {
    pub sku: String,
    pub name: String,
    pub quantity: i32,
}

pub enum InventoryCommand {
    Restock { sku: String, amount: i32 },
    Sell { sku: String, amount: i32 },
}

#[derive(Debug, Clone)]
pub struct ProductView {
    pub sku: String,
    pub name: String,
    pub quantity: i32,
    pub available: bool,
}

pub struct WriteStore {
    products: HashMap<String, Product>,
}

impl WriteStore {
    pub fn new() -> Self {
        WriteStore { products: HashMap::new() }
    }

    pub fn add_product(&mut self, product: Product) {
        self.products.insert(product.sku.clone(), product);
    }

    pub fn handle(&mut self, cmd: InventoryCommand) -> Result<(), String> {
        match cmd {
            InventoryCommand::Restock { sku, amount } => {
                let p = self.products.get_mut(&sku).ok_or("Product not found")?;
                p.quantity += amount;
                Ok(())
            }
            InventoryCommand::Sell { sku, amount } => {
                let p = self.products.get_mut(&sku).ok_or("Product not found")?;
                if p.quantity < amount {
                    return Err("Insufficient stock".into());
                }
                p.quantity -= amount;
                Ok(())
            }
        }
    }

    pub fn project(&self) -> ReadStore {
        let views = self.products.values().map(|p| {
            let view = ProductView {
                sku: p.sku.clone(),
                name: p.name.clone(),
                quantity: p.quantity,
                available: p.quantity > 0,
            };
            (p.sku.clone(), view)
        }).collect();
        ReadStore { views }
    }
}

pub struct ReadStore {
    views: HashMap<String, ProductView>,
}

impl ReadStore {
    pub fn find_by_sku(&self, sku: &str) -> Option<&ProductView> {
        self.views.get(sku)
    }

    pub fn find_available(&self) -> Vec<&ProductView> {
        self.views.values().filter(|v| v.available).collect()
    }
}
```

**Usage**

```rust
let mut write = WriteStore::new();
write.add_product(Product { sku: "W-001".into(), name: "Widget".into(), quantity: 100 });
write.handle(InventoryCommand::Sell { sku: "W-001".into(), amount: 30 }).unwrap();

let read = write.project();
let view = read.find_by_sku("W-001").unwrap();
println!("{}: {} in stock (available: {})", view.name, view.quantity, view.available);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public record RestockCommand(string Sku, int Amount);
public record SellCommand(string Sku, int Amount);

public class Product
{
    public string Sku { get; set; } = "";
    public string Name { get; set; } = "";
    public int Quantity { get; set; }
}

public record ProductView(string Sku, string Name, int Quantity, bool Available);

public class WriteStore
{
    private readonly Dictionary<string, Product> _products = new();

    public void AddProduct(Product product) => _products[product.Sku] = product;

    public void Handle(RestockCommand cmd)
    {
        var p = _products[cmd.Sku];
        p.Quantity += cmd.Amount;
    }

    public void Handle(SellCommand cmd)
    {
        var p = _products[cmd.Sku];
        if (p.Quantity < cmd.Amount)
            throw new InvalidOperationException("Insufficient stock");
        p.Quantity -= cmd.Amount;
    }

    public ReadStore Project() =>
        new(_products.Values.ToDictionary(
            p => p.Sku,
            p => new ProductView(p.Sku, p.Name, p.Quantity, p.Quantity > 0)));
}

public class ReadStore
{
    private readonly Dictionary<string, ProductView> _views;

    public ReadStore(Dictionary<string, ProductView> views) => _views = views;

    public ProductView? FindBySku(string sku) =>
        _views.GetValueOrDefault(sku);

    public IEnumerable<ProductView> FindAvailable() =>
        _views.Values.Where(v => v.Available);
}
```

**Usage**

```csharp
var write = new WriteStore();
write.AddProduct(new Product { Sku = "W-001", Name = "Widget", Quantity = 100 });
write.Handle(new SellCommand("W-001", 30));

var read = write.Project();
var view = read.FindBySku("W-001")!;
Console.WriteLine($"{view.Name}: {view.Quantity} in stock (available: {view.Available})");
```

##### Python

**Implementation**

```python
from dataclasses import dataclass

@dataclass
class Product:
    sku: str
    name: str
    quantity: int

@dataclass(frozen=True)
class ProductView:
    sku: str
    name: str
    quantity: int
    available: bool

class WriteStore:
    def __init__(self) -> None:
        self._products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self._products[product.sku] = product

    def restock(self, sku: str, amount: int) -> None:
        self._products[sku].quantity += amount

    def sell(self, sku: str, amount: int) -> None:
        p = self._products[sku]
        if p.quantity < amount:
            raise ValueError("Insufficient stock")
        p.quantity -= amount

    def project(self) -> "ReadStore":
        views = {
            p.sku: ProductView(sku=p.sku, name=p.name, quantity=p.quantity, available=p.quantity > 0)
            for p in self._products.values()
        }
        return ReadStore(views)

class ReadStore:
    def __init__(self, views: dict[str, ProductView]) -> None:
        self._views = views

    def find_by_sku(self, sku: str) -> ProductView | None:
        return self._views.get(sku)

    def find_available(self) -> list[ProductView]:
        return [v for v in self._views.values() if v.available]
```

**Usage**

```python
write = WriteStore()
write.add_product(Product(sku="W-001", name="Widget", quantity=100))
write.sell("W-001", 30)

read = write.project()
view = read.find_by_sku("W-001")
if view:
    print(f"{view.name}: {view.quantity} in stock (available: {view.available})")
```

<a id="44-event-sourcing"></a>

### 4.4. Event Sourcing

| **Who**  | Systems that require a complete audit trail, temporal queries, or the ability to replay history to rebuild state. |
|----------|--------|
| **What** | Stores state as an append-only sequence of domain events rather than mutable current-state snapshots. |
| **When** | When you need full traceability of every state change, the ability to reconstruct past states, or when domain events are first-class concepts in the business. |
| **Where**| Financial systems, audit-heavy applications, collaborative editing, and domains where "how we got here" matters as much as "where we are." |
| **Why**  | Preserves the complete history of state changes, enabling audit trails, temporal queries, debugging by replay, and retroactive correction of bugs by reprocessing events. |
| **How**  | Define domain events for every meaningful state change. Persist events to an append-only event store. Rebuild aggregate state by replaying its event stream from the beginning (or from a snapshot). Use projections to build read-optimized views from the event stream. |

Event Sourcing replaces mutable state snapshots with an append-only log of domain events. Instead of storing "the account balance is $500," the system stores the sequence of events that produced that balance: `Deposited($1000)`, `Withdrawn($300)`, `Withdrawn($200)`. Current state is reconstructed by replaying the event stream from the beginning — or from a periodic snapshot to bound replay time.

The key participants are **domain events** (immutable records of something that happened), the **event store** (append-only persistence for event streams, keyed by aggregate ID), **aggregates** (rebuilt by folding events into state), and **projections** (read-side consumers that build denormalized views from the event stream). Snapshots are an optimization: a serialized aggregate state captured at a known event version, allowing replay to start from the snapshot instead of event zero.

Event Sourcing provides a complete audit trail by construction, supports temporal queries ("what was the balance last Tuesday?"), and enables debugging by replaying production event streams locally. The trade-offs are significant: event schema evolution requires careful versioning, eventual-consistency semantics apply to projections, and the mental model is fundamentally different from CRUD — making it a poor fit for simple applications without audit or replay requirements.

The examples below use floating-point types for monetary amounts for simplicity. Production financial systems should use exact decimal types (`Decimal` in C#/Python, or a fixed-point library in Rust) to avoid rounding errors.

<a id="441-domain-context"></a>

#### 4.4.1. Domain Context

Primarily relevant in audit-heavy systems, financial applications, and domains requiring temporal queries or event replay. Adds significant complexity to simple CRUD applications where only current state matters.

<a id="442-system-fit"></a>

#### 4.4.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Workable** — event store and projections can coexist in one process, but replay and projection logic add complexity. |
| Microservices | **Adapts well** — each service owns its event stream; events serve as the integration contract between services. |
| Serverless | **Workable** — functions can append events and trigger projections, but replay across cold starts needs care. |
| Event-Driven | **Natural fit** — events are the native communication primitive; the event store is the system's source of truth. |

<a id="443-benefits"></a>

#### 4.4.3. Benefits

- Complete audit trail by construction — every state change is recorded as an immutable event.
- Temporal queries are trivial: replay events up to any point in time to reconstruct past states.
- Enables bug fixes by correcting projection logic and reprocessing the event stream, without losing data.

<a id="444-trade-offs"></a>

#### 4.4.4. Trade-offs

- Event schema evolution is hard — renaming or restructuring events requires versioning and upcasting strategies.
- Rebuilding state from long event streams is slow without snapshotting, adding implementation complexity.
- Fundamentally different mental model from CRUD; steep learning curve for teams unfamiliar with the approach.

<a id="445-examples"></a>

#### 4.4.5. Examples

##### Rust

**Implementation**

```rust
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub enum AccountEvent {
    Opened { owner: String },
    Deposited { amount: f64 },
    Withdrawn { amount: f64 },
}

#[derive(Debug)]
pub struct BankAccount {
    pub owner: String,
    pub balance: f64,
    pub version: usize,
}

impl BankAccount {
    pub fn replay(events: &[AccountEvent]) -> Self {
        let mut account = BankAccount {
            owner: String::new(),
            balance: 0.0,
            version: 0,
        };
        for event in events {
            account.apply(event);
        }
        account
    }

    fn apply(&mut self, event: &AccountEvent) {
        match event {
            AccountEvent::Opened { owner } => self.owner = owner.clone(),
            AccountEvent::Deposited { amount } => self.balance += amount,
            AccountEvent::Withdrawn { amount } => self.balance -= amount,
        }
        self.version += 1;
    }
}

pub struct EventStore {
    streams: HashMap<String, Vec<AccountEvent>>,
}

impl EventStore {
    pub fn new() -> Self {
        EventStore { streams: HashMap::new() }
    }

    pub fn append(&mut self, stream_id: &str, event: AccountEvent) {
        self.streams.entry(stream_id.to_string()).or_default().push(event);
    }

    pub fn load(&self, stream_id: &str) -> &[AccountEvent] {
        self.streams.get(stream_id).map(|v| v.as_slice()).unwrap_or(&[])
    }
}
```

**Usage**

```rust
let mut store = EventStore::new();
store.append("acc-1", AccountEvent::Opened { owner: "Alice".into() });
store.append("acc-1", AccountEvent::Deposited { amount: 1000.0 });
store.append("acc-1", AccountEvent::Withdrawn { amount: 200.0 });

let account = BankAccount::replay(store.load("acc-1"));
println!("{}: balance = {:.2} (v{})", account.owner, account.balance, account.version);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public abstract record AccountEvent;
public record AccountOpened(string Owner) : AccountEvent;
public record Deposited(double Amount) : AccountEvent;
public record Withdrawn(double Amount) : AccountEvent;

public class BankAccount
{
    public string Owner { get; private set; } = "";
    public double Balance { get; private set; }
    public int Version { get; private set; }

    public static BankAccount Replay(IEnumerable<AccountEvent> events)
    {
        var account = new BankAccount();
        foreach (var e in events)
            account.Apply(e);
        return account;
    }

    private void Apply(AccountEvent e)
    {
        switch (e)
        {
            case AccountOpened opened: Owner = opened.Owner; break;
            case Deposited deposited: Balance += deposited.Amount; break;
            case Withdrawn withdrawn: Balance -= withdrawn.Amount; break;
        }
        Version++;
    }
}

public class EventStore
{
    private readonly Dictionary<string, List<AccountEvent>> _streams = new();

    public void Append(string streamId, AccountEvent e)
    {
        if (!_streams.ContainsKey(streamId))
            _streams[streamId] = new List<AccountEvent>();
        _streams[streamId].Add(e);
    }

    public IReadOnlyList<AccountEvent> Load(string streamId) =>
        _streams.TryGetValue(streamId, out var events) ? events : Array.Empty<AccountEvent>();
}
```

**Usage**

```csharp
var store = new EventStore();
store.Append("acc-1", new AccountOpened("Alice"));
store.Append("acc-1", new Deposited(1000.0));
store.Append("acc-1", new Withdrawn(200.0));

var account = BankAccount.Replay(store.Load("acc-1"));
Console.WriteLine($"{account.Owner}: balance = {account.Balance:F2} (v{account.Version})");
```

##### Python

**Implementation**

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class AccountOpened:
    owner: str

@dataclass(frozen=True)
class Deposited:
    amount: float

@dataclass(frozen=True)
class Withdrawn:
    amount: float

AccountEvent = AccountOpened | Deposited | Withdrawn

@dataclass
class BankAccount:
    owner: str = ""
    balance: float = 0.0
    version: int = 0

    @classmethod
    def replay(cls, events: list[AccountEvent]) -> "BankAccount":
        account = cls()
        for event in events:
            account._apply(event)
        return account

    def _apply(self, event: AccountEvent) -> None:
        match event:
            case AccountOpened(owner=owner):
                self.owner = owner
            case Deposited(amount=amount):
                self.balance += amount
            case Withdrawn(amount=amount):
                self.balance -= amount
        self.version += 1

class EventStore:
    def __init__(self) -> None:
        self._streams: dict[str, list[AccountEvent]] = {}

    def append(self, stream_id: str, event: AccountEvent) -> None:
        self._streams.setdefault(stream_id, []).append(event)

    def load(self, stream_id: str) -> list[AccountEvent]:
        return list(self._streams.get(stream_id, []))
```

**Usage**

```python
store = EventStore()
store.append("acc-1", AccountOpened(owner="Alice"))
store.append("acc-1", Deposited(amount=1000.0))
store.append("acc-1", Withdrawn(amount=200.0))

account = BankAccount.replay(store.load("acc-1"))
print(f"{account.owner}: balance = {account.balance:.2f} (v{account.version})")
```

<a id="45-circuit-breaker"></a>

### 4.5. Circuit Breaker

| **Who**  | Distributed systems making remote calls to services that can fail, hang, or become unresponsive. |
|----------|--------|
| **What** | Detects failures in remote calls and short-circuits subsequent calls to prevent cascading failure, allowing the failing service time to recover. |
| **When** | When remote calls (HTTP, gRPC, database) can fail or time out, and repeated retries would overwhelm the failing service or exhaust the caller's resources. |
| **Where**| Between any client and a remote dependency — service-to-service calls, database connections, third-party API integrations. |
| **Why**  | Prevents cascading failures where one unhealthy dependency takes down the entire system by consuming all threads, connections, or memory with pending retries. |
| **How**  | Wrap remote calls in a circuit breaker that tracks failures. After a threshold of consecutive failures, the breaker opens and immediately rejects calls (fail-fast). After a timeout, it enters half-open state and allows a probe call through — if it succeeds, the breaker closes; if it fails, it reopens. |

The Circuit Breaker pattern wraps remote calls with a stateful proxy that monitors failures and short-circuits calls when a dependency is unhealthy. It operates in three states: **Closed** (normal operation — calls pass through and failures are counted), **Open** (the failure threshold has been exceeded — all calls are immediately rejected without contacting the remote service), and **Half-Open** (a recovery timeout has elapsed — one probe call is allowed through to test whether the service has recovered).

The key participants are the **circuit breaker** (the stateful wrapper), the **protected call** (the remote operation being wrapped), and the **state machine** (Closed → Open → Half-Open → Closed/Open). Configuration parameters include the failure threshold (how many failures trigger opening), the recovery timeout (how long to wait before probing), and optionally a success threshold in half-open state (how many consecutive successes are required to fully close).

Circuit Breaker is essential in microservice architectures where a single unhealthy service can cascade into system-wide failure. It complements retries (which handle transient failures) by stopping retries entirely when the failure is persistent. The pattern trades some successful calls (rejected during open state) for system stability — an unavailable feature is better than a crashed system. In production, circuit breakers also serve as observability signals — state transitions, rejection counts, and probe results indicate which dependencies are unhealthy, feeding dashboards and alerting systems.

The examples below transition from Half-Open to Closed on a single successful probe. Production implementations often require a configurable **success threshold** — N consecutive successes in Half-Open before fully closing — to avoid re-closing prematurely on a single lucky call.

<a id="451-domain-context"></a>

#### 4.5.1. Domain Context

Primarily relevant in distributed systems and microservice architectures where remote calls can fail or hang. Rarely encountered in single-process applications without external dependencies.

<a id="452-system-fit"></a>

#### 4.5.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Uncommon** — useful only if the monolith calls external services; internal calls don't need circuit breaking. |
| Microservices | **Natural fit** — essential for resilient inter-service communication. |
| Serverless | **Workable** — useful for external API calls, but per-invocation state requires shared storage for the breaker state. |
| Event-Driven | **Adapts well** — protects event consumers from unhealthy downstream processors or external services. |

<a id="453-benefits"></a>

#### 4.5.3. Benefits

- Prevents cascading failures — a single unhealthy dependency cannot exhaust the caller's resources.
- Fail-fast behavior frees threads and connections immediately instead of blocking on doomed calls.
- Gives the failing service time to recover by stopping traffic during the open state.

<a id="454-trade-offs"></a>

#### 4.5.4. Trade-offs

- Legitimate requests are rejected during the open state, even if the remote service has partially recovered.
- Tuning thresholds and timeouts requires production traffic analysis; poor defaults cause premature tripping or delayed detection.
- Adds state management complexity, especially when shared across multiple instances (distributed circuit breaker state).

<a id="455-examples"></a>

#### 4.5.5. Examples

##### Rust

**Implementation**

```rust
use std::time::{Duration, Instant};

#[derive(Debug, PartialEq)]
pub enum State {
    Closed,
    Open,
    HalfOpen,
}

pub struct CircuitBreaker {
    failure_threshold: u32,
    recovery_timeout: Duration,
    failure_count: u32,
    state: State,
    last_failure_time: Option<Instant>,
}

impl CircuitBreaker {
    pub fn new(failure_threshold: u32, recovery_timeout: Duration) -> Self {
        CircuitBreaker {
            failure_threshold,
            recovery_timeout,
            failure_count: 0,
            state: State::Closed,
            last_failure_time: None,
        }
    }

    pub fn call<F, T, E>(&mut self, action: F) -> Result<T, String>
    where
        F: FnOnce() -> Result<T, E>,
        E: std::fmt::Display,
    {
        match self.state {
            State::Open => {
                if self.last_failure_time.unwrap().elapsed() >= self.recovery_timeout {
                    self.state = State::HalfOpen;
                } else {
                    return Err("Circuit is open".into());
                }
            }
            _ => {}
        }

        match action() {
            Ok(value) => {
                self.on_success();
                Ok(value)
            }
            Err(e) => {
                self.on_failure();
                Err(format!("Call failed: {e}"))
            }
        }
    }

    fn on_success(&mut self) {
        self.failure_count = 0;
        self.state = State::Closed;
    }

    fn on_failure(&mut self) {
        self.failure_count += 1;
        self.last_failure_time = Some(Instant::now());
        if self.failure_count >= self.failure_threshold {
            self.state = State::Open;
        }
    }

    pub fn state(&self) -> &State {
        &self.state
    }
}
```

**Usage**

```rust
let mut breaker = CircuitBreaker::new(3, Duration::from_secs(10));

for _ in 0..4 {
    let result = breaker.call(|| Err::<(), &str>("connection refused"));
    println!("Result: {:?}, State: {:?}", result, breaker.state());
}

let result = breaker.call(|| Ok::<&str, &str>("success"));
println!("While open: {:?}", result);
```

##### C\#

**Implementation**

```csharp
using System;

public enum CircuitState { Closed, Open, HalfOpen }

public class CircuitBreaker
{
    private readonly int _failureThreshold;
    private readonly TimeSpan _recoveryTimeout;
    private int _failureCount;
    private DateTime? _lastFailureTime;

    public CircuitState State { get; private set; } = CircuitState.Closed;

    public CircuitBreaker(int failureThreshold, TimeSpan recoveryTimeout)
    {
        _failureThreshold = failureThreshold;
        _recoveryTimeout = recoveryTimeout;
    }

    public T Call<T>(Func<T> action)
    {
        if (State == CircuitState.Open)
        {
            if (DateTime.UtcNow - _lastFailureTime >= _recoveryTimeout)
                State = CircuitState.HalfOpen;
            else
                throw new InvalidOperationException("Circuit is open");
        }

        try
        {
            T result = action();
            OnSuccess();
            return result;
        }
        catch (Exception)
        {
            OnFailure();
            throw;
        }
    }

    private void OnSuccess()
    {
        _failureCount = 0;
        State = CircuitState.Closed;
    }

    private void OnFailure()
    {
        _failureCount++;
        _lastFailureTime = DateTime.UtcNow;
        if (_failureCount >= _failureThreshold)
            State = CircuitState.Open;
    }
}
```

**Usage**

```csharp
var breaker = new CircuitBreaker(3, TimeSpan.FromSeconds(10));

for (int i = 0; i < 4; i++)
{
    try
    {
        breaker.Call<string>(() => throw new Exception("connection refused"));
    }
    catch (Exception ex)
    {
        Console.WriteLine($"Error: {ex.Message}, State: {breaker.State}");
    }
}
```

##### Python

**Implementation**

```python
import time
from enum import Enum, auto
from typing import Callable, TypeVar

T = TypeVar("T")

class State(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class CircuitOpenError(Exception):
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold: int, recovery_timeout: float) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self.state = State.CLOSED

    def call(self, action: Callable[[], T]) -> T:
        if self.state == State.OPEN:
            if self._last_failure_time and (time.monotonic() - self._last_failure_time) >= self.recovery_timeout:
                self.state = State.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = action()
        except Exception:
            self._on_failure()
            raise
        else:
            self._on_success()
            return result

    def _on_success(self) -> None:
        self._failure_count = 0
        self.state = State.CLOSED

    def _on_failure(self) -> None:
        self._failure_count += 1
        self._last_failure_time = time.monotonic()
        if self._failure_count >= self.failure_threshold:
            self.state = State.OPEN
```

**Usage**

```python
def failing_call():
    raise ConnectionError("refused")

breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10.0)

for _ in range(4):
    try:
        breaker.call(failing_call)
    except (ConnectionError, CircuitOpenError) as e:
        print(f"Error: {e}, State: {breaker.state}")
```

<a id="46-saga"></a>

### 4.6. Saga

| **Who**  | Distributed systems where a business process spans multiple services, each with its own database. |
|----------|--------|
| **What** | Manages long-running distributed transactions as a sequence of local transactions, each with a compensating action for rollback. |
| **When** | When a business operation spans multiple services and traditional ACID transactions are not possible across service boundaries. |
| **Where**| E-commerce order flows, booking systems, payment processing, and any multi-service workflow requiring consistency guarantees. |
| **Why**  | Achieves eventual consistency across services without distributed locks or two-phase commit, which are fragile and scale poorly. |
| **How**  | Define the saga as a sequence of steps, each consisting of a local transaction and a compensating transaction. In orchestration, a central coordinator drives the steps; in choreography, each service emits events that trigger the next step. On failure, compensating transactions are executed in reverse order. |

The Saga pattern coordinates distributed transactions by breaking them into a sequence of local transactions, each scoped to a single service. Every step has a corresponding **compensating action** that semantically undoes its effect. If step N fails, the saga executes compensations for steps N-1 through 1 in reverse order, restoring the system to a consistent state without requiring distributed locks.

There are two orchestration styles. In **choreography**, each service publishes domain events upon completing its step; downstream services listen and react, forming an implicit chain. In **orchestration**, a central saga coordinator explicitly drives the sequence — telling each service what to do and handling the compensation flow on failure. Orchestration is easier to reason about and debug; choreography avoids a single point of coordination but can produce complex, hard-to-trace event chains.

Sagas provide eventual consistency rather than immediate consistency. Between steps, the system is in a partially completed state that other operations may observe. This requires careful design of compensating actions (they must be idempotent and handle partial states) and tolerance for intermediate inconsistency in the business domain. In production, the orchestrator's state (which steps have completed, which compensations are pending) must be **persisted** so that if the process crashes mid-saga, recovery can resume compensation from the last known checkpoint rather than leaving the system in an irrecoverable partial state.

<a id="461-domain-context"></a>

#### 4.6.1. Domain Context

Primarily relevant in distributed systems where a business process spans multiple services. Unnecessary in monolithic applications with single-database ACID transactions, where a simple Unit of Work suffices.

<a id="462-system-fit"></a>

#### 4.6.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Uncommon** — a single database transaction handles atomicity; sagas add needless complexity. |
| Microservices | **Natural fit** — the canonical solution for cross-service transactions without distributed locks. |
| Serverless | **Adapts well** — step functions or durable workflows (AWS Step Functions, Azure Durable Functions) implement the orchestrator. |
| Event-Driven | **Natural fit** — choreography sagas are event-driven by definition; events trigger steps and compensations. |

<a id="463-benefits"></a>

#### 4.6.3. Benefits

- Achieves cross-service consistency without distributed locks or two-phase commit.
- Each service retains full autonomy over its local database and transactions.
- Compensating actions provide a structured rollback mechanism that handles partial failures gracefully.

<a id="464-trade-offs"></a>

#### 4.6.4. Trade-offs

- Eventual consistency means intermediate states are visible to other operations during saga execution.
- Compensating actions must be idempotent and carefully designed — some operations (sending an email, charging a card) are difficult to "undo."
- Debugging failures across a multi-step, multi-service saga is significantly harder than debugging a single transaction.

<a id="465-examples"></a>

#### 4.6.5. Examples

##### Rust

The orchestration variant is shown: a central `SagaOrchestrator` drives the steps and rolls back on failure.

**Implementation**

```rust
pub trait SagaStep {
    fn execute(&self) -> Result<(), String>;
    fn compensate(&self) -> Result<(), String>;
    fn name(&self) -> &str;
}

pub struct SagaOrchestrator {
    steps: Vec<Box<dyn SagaStep>>,
}

impl SagaOrchestrator {
    pub fn new(steps: Vec<Box<dyn SagaStep>>) -> Self {
        SagaOrchestrator { steps }
    }

    pub fn execute(&self) -> Result<(), String> {
        let mut completed: Vec<usize> = Vec::new();

        for (i, step) in self.steps.iter().enumerate() {
            println!("Executing: {}", step.name());
            if let Err(e) = step.execute() {
                println!("Failed at {}: {e}. Compensating...", step.name());
                for &j in completed.iter().rev() {
                    println!("  Compensating: {}", self.steps[j].name());
                    let _ = self.steps[j].compensate();
                }
                return Err(e);
            }
            completed.push(i);
        }
        Ok(())
    }
}

struct CreateOrder;
impl SagaStep for CreateOrder {
    fn execute(&self) -> Result<(), String> { println!("  Order created"); Ok(()) }
    fn compensate(&self) -> Result<(), String> { println!("  Order cancelled"); Ok(()) }
    fn name(&self) -> &str { "CreateOrder" }
}

struct ReserveInventory;
impl SagaStep for ReserveInventory {
    fn execute(&self) -> Result<(), String> { println!("  Inventory reserved"); Ok(()) }
    fn compensate(&self) -> Result<(), String> { println!("  Inventory released"); Ok(()) }
    fn name(&self) -> &str { "ReserveInventory" }
}

struct ChargePayment { should_fail: bool }
impl SagaStep for ChargePayment {
    fn execute(&self) -> Result<(), String> {
        if self.should_fail { Err("Payment declined".into()) }
        else { println!("  Payment charged"); Ok(()) }
    }
    fn compensate(&self) -> Result<(), String> { println!("  Payment refunded"); Ok(()) }
    fn name(&self) -> &str { "ChargePayment" }
}
```

**Usage**

```rust
let saga = SagaOrchestrator::new(vec![
    Box::new(CreateOrder),
    Box::new(ReserveInventory),
    Box::new(ChargePayment { should_fail: true }),
]);
let result = saga.execute();
println!("Saga result: {:?}", result);
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;

public interface ISagaStep
{
    string Name { get; }
    void Execute();
    void Compensate();
}

public class SagaOrchestrator
{
    private readonly List<ISagaStep> _steps;

    public SagaOrchestrator(List<ISagaStep> steps) => _steps = steps;

    public void Execute()
    {
        var completed = new Stack<ISagaStep>();
        foreach (var step in _steps)
        {
            Console.WriteLine($"Executing: {step.Name}");
            try
            {
                step.Execute();
                completed.Push(step);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed at {step.Name}: {ex.Message}. Compensating...");
                while (completed.Count > 0)
                {
                    var s = completed.Pop();
                    Console.WriteLine($"  Compensating: {s.Name}");
                    s.Compensate();
                }
                throw;
            }
        }
    }
}

public class CreateOrderStep : ISagaStep
{
    public string Name => "CreateOrder";
    public void Execute() => Console.WriteLine("  Order created");
    public void Compensate() => Console.WriteLine("  Order cancelled");
}

public class ReserveInventoryStep : ISagaStep
{
    public string Name => "ReserveInventory";
    public void Execute() => Console.WriteLine("  Inventory reserved");
    public void Compensate() => Console.WriteLine("  Inventory released");
}

public class ChargePaymentStep : ISagaStep
{
    private readonly bool _shouldFail;
    public ChargePaymentStep(bool shouldFail) => _shouldFail = shouldFail;
    public string Name => "ChargePayment";

    public void Execute()
    {
        if (_shouldFail) throw new InvalidOperationException("Payment declined");
        Console.WriteLine("  Payment charged");
    }

    public void Compensate() => Console.WriteLine("  Payment refunded");
}
```

**Usage**

```csharp
var saga = new SagaOrchestrator(new List<ISagaStep>
{
    new CreateOrderStep(),
    new ReserveInventoryStep(),
    new ChargePaymentStep(shouldFail: true),
});

try { saga.Execute(); }
catch (Exception ex) { Console.WriteLine($"Saga failed: {ex.Message}"); }
```

##### Python

The orchestration variant is shown: a central `SagaOrchestrator` drives the steps and rolls back on failure.

**Implementation**

```python
from abc import ABC, abstractmethod

class SagaStep(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def compensate(self) -> None: ...

class SagaOrchestrator:
    def __init__(self, steps: list[SagaStep]) -> None:
        self._steps = steps

    def execute(self) -> None:
        completed: list[SagaStep] = []
        for step in self._steps:
            print(f"Executing: {step.name}")
            try:
                step.execute()
                completed.append(step)
            except Exception as e:
                print(f"Failed at {step.name}: {e}. Compensating...")
                for s in reversed(completed):
                    print(f"  Compensating: {s.name}")
                    s.compensate()
                raise

class CreateOrder(SagaStep):
    name = "CreateOrder"
    def execute(self) -> None: print("  Order created")
    def compensate(self) -> None: print("  Order cancelled")

class ReserveInventory(SagaStep):
    name = "ReserveInventory"
    def execute(self) -> None: print("  Inventory reserved")
    def compensate(self) -> None: print("  Inventory released")

class ChargePayment(SagaStep):
    name = "ChargePayment"
    def __init__(self, should_fail: bool = False) -> None:
        self._should_fail = should_fail

    def execute(self) -> None:
        if self._should_fail:
            raise RuntimeError("Payment declined")
        print("  Payment charged")

    def compensate(self) -> None:
        print("  Payment refunded")
```

**Usage**

```python
saga = SagaOrchestrator([
    CreateOrder(),
    ReserveInventory(),
    ChargePayment(should_fail=True),
])
try:
    saga.execute()
except RuntimeError as e:
    print(f"Saga failed: {e}")
```

<a id="47-specification"></a>

### 4.7. Specification

| **Who**  | Domain-driven applications that need to compose complex filtering, validation, or selection rules dynamically. |
|----------|--------|
| **What** | Encapsulates a business rule as a reusable, composable boolean predicate that can be combined with AND, OR, NOT. |
| **When** | When business rules for filtering, validation, or selection are complex, overlap across use cases, and need to be composed at runtime rather than hard-coded. |
| **Where**| Repository queries, domain validation, authorization checks, and business rule engines where predicates must be combined dynamically. |
| **Why**  | Extracts business rules from domain objects and services into standalone, testable, reusable units that can be composed without modifying existing code. |
| **How**  | Define a specification interface with an `is_satisfied_by` method. Implement concrete specifications for individual rules. Provide composite specifications (And, Or, Not) that combine specifications using logical operators. Clients compose specifications at runtime to express complex queries or validation rules. |

The Specification pattern encapsulates a business rule as a first-class object with a single method — `is_satisfied_by(candidate)` — that returns a boolean. Individual specifications are simple predicates: "price is under $50," "category is electronics," "item is in stock." The power comes from **composition**: specifications can be combined with `And`, `Or`, and `Not` to build arbitrarily complex boolean expressions without modifying any existing specification.

The key participants are the **specification interface** (declares `is_satisfied_by` and composition methods), **concrete specifications** (individual business rules), and **composite specifications** (`AndSpecification`, `OrSpecification`, `NotSpecification` — each wrapping one or two inner specifications). Some implementations add operator overloads (`&`, `|`, `~`) for more readable composition.

Specification is especially valuable in domain-driven design where the same business rules appear in different contexts — filtering a repository query, validating an entity, or determining eligibility. Each rule is tested in isolation, and new rules are added without touching existing code. The trade-off is verbosity: simple cases that would be a one-line lambda become a class hierarchy. Use Specification when rules are reused, composed dynamically, or complex enough to warrant the abstraction.

<a id="471-domain-context"></a>

#### 4.7.1. Domain Context

Primarily relevant in domain-driven design and business rule engines where complex filtering, validation, or selection logic must be composed dynamically. Less common in applications with simple, static query logic that a single predicate or SQL clause can express.

<a id="472-system-fit"></a>

#### 4.7.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — specifications compose queries and validation rules within a single domain layer. |
| Microservices | **Adapts well** — each service defines specifications for its bounded context; serializable specs can cross service boundaries. |
| Serverless | **Workable** — specifications work within function logic but the composable class hierarchy may be heavier than inline predicates. |
| Event-Driven | **Adapts well** — specifications filter or route events, determining which consumers should process which messages. |

<a id="473-benefits"></a>

#### 4.7.3. Benefits

- Business rules are reusable, testable units — each specification can be validated independently.
- Complex predicates are built by composition rather than modification, adhering to the Open/Closed Principle.
- The same specification can serve multiple purposes: repository filtering, entity validation, and UI display logic.

<a id="474-trade-offs"></a>

#### 4.7.4. Trade-offs

- Class proliferation — each business rule becomes its own specification class, which is verbose for simple predicates.
- Translating in-memory specifications into efficient database queries (e.g., SQL WHERE clauses) requires additional infrastructure.
- Deeply nested composite specifications can be hard to debug when `is_satisfied_by` returns an unexpected result.

<a id="475-examples"></a>

#### 4.7.5. Examples

##### Rust

**Implementation**

```rust
pub trait Specification<T> {
    fn is_satisfied_by(&self, item: &T) -> bool;

    fn and(self, other: impl Specification<T> + 'static) -> Box<dyn Specification<T>>
    where
        Self: Sized + 'static,
    {
        Box::new(AndSpec(Box::new(self), Box::new(other)))
    }

    fn or(self, other: impl Specification<T> + 'static) -> Box<dyn Specification<T>>
    where
        Self: Sized + 'static,
    {
        Box::new(OrSpec(Box::new(self), Box::new(other)))
    }

    fn not(self) -> Box<dyn Specification<T>>
    where
        Self: Sized + 'static,
    {
        Box::new(NotSpec(Box::new(self)))
    }
}

struct AndSpec<T>(Box<dyn Specification<T>>, Box<dyn Specification<T>>);
impl<T> Specification<T> for AndSpec<T> {
    fn is_satisfied_by(&self, item: &T) -> bool {
        self.0.is_satisfied_by(item) && self.1.is_satisfied_by(item)
    }
}

struct OrSpec<T>(Box<dyn Specification<T>>, Box<dyn Specification<T>>);
impl<T> Specification<T> for OrSpec<T> {
    fn is_satisfied_by(&self, item: &T) -> bool {
        self.0.is_satisfied_by(item) || self.1.is_satisfied_by(item)
    }
}

struct NotSpec<T>(Box<dyn Specification<T>>);
impl<T> Specification<T> for NotSpec<T> {
    fn is_satisfied_by(&self, item: &T) -> bool {
        !self.0.is_satisfied_by(item)
    }
}

impl<T> Specification<T> for Box<dyn Specification<T>> {
    fn is_satisfied_by(&self, item: &T) -> bool {
        (**self).is_satisfied_by(item)
    }
}

pub struct Product {
    pub name: String,
    pub price: f64,
    pub category: String,
    pub in_stock: bool,
}

pub struct PriceBelow(pub f64);
impl Specification<Product> for PriceBelow {
    fn is_satisfied_by(&self, item: &Product) -> bool {
        item.price < self.0
    }
}

pub struct InCategory(pub String);
impl Specification<Product> for InCategory {
    fn is_satisfied_by(&self, item: &Product) -> bool {
        item.category == self.0
    }
}

pub struct InStock;
impl Specification<Product> for InStock {
    fn is_satisfied_by(&self, item: &Product) -> bool {
        item.in_stock
    }
}
```

**Usage**

```rust
let products = vec![
    Product { name: "Keyboard".into(), price: 45.0, category: "Electronics".into(), in_stock: true },
    Product { name: "Monitor".into(), price: 300.0, category: "Electronics".into(), in_stock: true },
    Product { name: "Pen".into(), price: 2.0, category: "Office".into(), in_stock: false },
];

let spec = PriceBelow(100.0)
    .and(InCategory("Electronics".into()))
    .and(InStock);

let matches: Vec<_> = products.iter().filter(|p| spec.is_satisfied_by(p)).collect();
for p in matches {
    println!("{}: ${:.2}", p.name, p.price);
}
```

##### C\#

**Implementation**

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

public abstract class Specification<T>
{
    public abstract bool IsSatisfiedBy(T item);

    public Specification<T> And(Specification<T> other) => new AndSpec<T>(this, other);
    public Specification<T> Or(Specification<T> other) => new OrSpec<T>(this, other);
    public Specification<T> Not() => new NotSpec<T>(this);
}

public class AndSpec<T> : Specification<T>
{
    private readonly Specification<T> _left, _right;
    public AndSpec(Specification<T> left, Specification<T> right) { _left = left; _right = right; }
    public override bool IsSatisfiedBy(T item) => _left.IsSatisfiedBy(item) && _right.IsSatisfiedBy(item);
}

public class OrSpec<T> : Specification<T>
{
    private readonly Specification<T> _left, _right;
    public OrSpec(Specification<T> left, Specification<T> right) { _left = left; _right = right; }
    public override bool IsSatisfiedBy(T item) => _left.IsSatisfiedBy(item) || _right.IsSatisfiedBy(item);
}

public class NotSpec<T> : Specification<T>
{
    private readonly Specification<T> _inner;
    public NotSpec(Specification<T> inner) => _inner = inner;
    public override bool IsSatisfiedBy(T item) => !_inner.IsSatisfiedBy(item);
}

public record Product(string Name, double Price, string Category, bool InStock);

public class PriceBelow : Specification<Product>
{
    private readonly double _max;
    public PriceBelow(double max) => _max = max;
    public override bool IsSatisfiedBy(Product item) => item.Price < _max;
}

public class InCategory : Specification<Product>
{
    private readonly string _category;
    public InCategory(string category) => _category = category;
    public override bool IsSatisfiedBy(Product item) => item.Category == _category;
}

public class InStock : Specification<Product>
{
    public override bool IsSatisfiedBy(Product item) => item.InStock;
}
```

**Usage**

```csharp
var products = new List<Product>
{
    new("Keyboard", 45.0, "Electronics", true),
    new("Monitor", 300.0, "Electronics", true),
    new("Pen", 2.0, "Office", false),
};

var spec = new PriceBelow(100.0).And(new InCategory("Electronics")).And(new InStock());

foreach (var p in products.Where(p => spec.IsSatisfiedBy(p)))
    Console.WriteLine($"{p.Name}: ${p.Price:F2}");
```

##### Python

Python's operator overloading (`__and__`, `__or__`, `__invert__`) enables natural composition syntax using `&`, `|`, and `~`.

**Implementation**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")

class Specification(ABC, Generic[T]):
    @abstractmethod
    def is_satisfied_by(self, item: T) -> bool: ...

    def __and__(self, other: "Specification[T]") -> "Specification[T]":
        return _AndSpec(self, other)

    def __or__(self, other: "Specification[T]") -> "Specification[T]":
        return _OrSpec(self, other)

    def __invert__(self) -> "Specification[T]":
        return _NotSpec(self)

class _AndSpec(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left, self._right = left, right

    def is_satisfied_by(self, item: T) -> bool:
        return self._left.is_satisfied_by(item) and self._right.is_satisfied_by(item)

class _OrSpec(Specification[T]):
    def __init__(self, left: Specification[T], right: Specification[T]) -> None:
        self._left, self._right = left, right

    def is_satisfied_by(self, item: T) -> bool:
        return self._left.is_satisfied_by(item) or self._right.is_satisfied_by(item)

class _NotSpec(Specification[T]):
    def __init__(self, inner: Specification[T]) -> None:
        self._inner = inner

    def is_satisfied_by(self, item: T) -> bool:
        return not self._inner.is_satisfied_by(item)

@dataclass
class Product:
    name: str
    price: float
    category: str
    in_stock: bool

class PriceBelow(Specification[Product]):
    def __init__(self, max_price: float) -> None:
        self._max = max_price

    def is_satisfied_by(self, item: Product) -> bool:
        return item.price < self._max

class InCategory(Specification[Product]):
    def __init__(self, category: str) -> None:
        self._category = category

    def is_satisfied_by(self, item: Product) -> bool:
        return item.category == self._category

class InStock(Specification[Product]):
    def is_satisfied_by(self, item: Product) -> bool:
        return item.in_stock
```

**Usage**

```python
products = [
    Product("Keyboard", 45.0, "Electronics", True),
    Product("Monitor", 300.0, "Electronics", True),
    Product("Pen", 2.0, "Office", False),
]

spec = PriceBelow(100.0) & InCategory("Electronics") & InStock()

for p in filter(spec.is_satisfied_by, products):
    print(f"{p.name}: ${p.price:.2f}")
```
