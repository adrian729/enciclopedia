# Creational

## Table of Contents

- [1. Singleton](#1-singleton)
  - [1.1. Paradigm Fit](#11-paradigm-fit)
  - [1.2. Benefits](#12-benefits)
  - [1.3. Trade-offs](#13-trade-offs)
  - [1.4. Examples](#14-examples)
- [2. Builder](#2-builder)
  - [2.1. Paradigm Fit](#21-paradigm-fit)
  - [2.2. Benefits](#22-benefits)
  - [2.3. Trade-offs](#23-trade-offs)
  - [2.4. Examples](#24-examples)
- [3. Factory](#3-factory)
  - [3.1. Paradigm Fit](#31-paradigm-fit)
  - [3.2. Benefits](#32-benefits)
  - [3.3. Trade-offs](#33-trade-offs)
  - [3.4. Examples](#34-examples)
- [4. Abstract Factory](#4-abstract-factory)
  - [4.1. Paradigm Fit](#41-paradigm-fit)
  - [4.2. Benefits](#42-benefits)
  - [4.3. Trade-offs](#43-trade-offs)
  - [4.4. Examples](#44-examples)
- [5. Prototype](#5-prototype)
  - [5.1. Paradigm Fit](#51-paradigm-fit)
  - [5.2. Benefits](#52-benefits)
  - [5.3. Trade-offs](#53-trade-offs)
  - [5.4. Examples](#54-examples)
- [6. Object Pool](#6-object-pool)
  - [6.1. Domain Context](#61-domain-context)
  - [6.2. Paradigm Fit](#62-paradigm-fit)
  - [6.3. Benefits](#63-benefits)
  - [6.4. Trade-offs](#64-trade-offs)
  - [6.5. Examples](#65-examples)

Creational patterns abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

| Pattern | When to Use |
|---------|-------------|
| [Singleton](#1-singleton) | A shared resource needs exactly one instance with global access. |
| [Builder](#2-builder) | Constructing complex objects with many optional or ordered parameters. |
| [Factory](#3-factory) | Creating objects without specifying the exact class; letting subclasses decide. |
| [Abstract Factory](#4-abstract-factory) | Creating families of related objects without specifying their concrete classes. |
| [Prototype](#5-prototype) | Creating new objects by cloning an existing instance instead of constructing from scratch. |
| [Object Pool](#6-object-pool) | Reusing expensive-to-create objects instead of repeated creation and destruction. |

## 1. Singleton

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

### 1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Uncommon** — global mutable state conflicts with purity; module-level constants or managed effects are preferred. |
| Data-Oriented | **Uncommon** — global state contradicts the "data lives in tables/arrays" model; shared resources are system-level parameters. |
| OOP | **Natural fit** — private constructor and static accessor is the canonical form. |
| Procedural | **Workable** — global variable behind an initialization-guard function. |
| Reactive | **Uncommon** — reactive systems favor injected shared services; `shareReplay`/`BehaviorSubject` serve similar sharing purposes within the stream. |

### 1.2. Benefits

- Guarantees exactly one instance — no accidental duplicates or conflicting copies.
- Lazy initialization defers resource allocation until the instance is actually needed.
- Provides a well-known global access point, simplifying discovery of shared infrastructure.

### 1.3. Trade-offs

- Hidden global state makes dependencies implicit and the call graph harder to reason about.
- Shared mutable state leaks between tests, causing order-dependent failures.
- Tight coupling to the concrete class makes substitution difficult; mocking in tests often requires workarounds.
- Concurrency requires explicit thread-safety measures (locking, `Lazy<T>`, `OnceLock`, etc.).

### 1.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 2. Builder

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

### 2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — pipelines of chained transformations over immutable intermediate values achieve the same goal, though named/default parameters and record update syntax often eliminate the need. |
| Data-Oriented | **Workable** — archetype-builders can batch-initialize component arrays, but per-object ceremony conflicts with bulk-data thinking. |
| OOP | **Natural fit** — mutable builder object with fluent method chaining. |
| Procedural | **Workable** — struct-population helpers, but no fluent chaining. |
| Reactive | **Adapts well** — fluent builder chains mirror operator pipelines; builders can configure stream topologies and subscription options. |

### 2.2. Benefits

- Eliminates telescoping constructors — each step is a named method, making construction self-documenting.
- Enforces invariants at build time rather than relying on post-creation validation.
- The same construction process can produce different representations by swapping builder implementations.
- Method chaining provides a fluent, discoverable API that IDEs can autocomplete.

### 2.3. Trade-offs

- Adds a parallel class (the builder) for every product — more code to maintain.
- Builder fields mirror the product's fields; changes to the product must be reflected in both.
- For simple objects with few required parameters, a plain constructor or factory method is simpler and less ceremony.

### 2.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 3. Factory

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

### 3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — factory functions, closures, and higher-order functions returning values. |
| Data-Oriented | **Adapts well** — archetype factories batch-create entities with the correct component layout in a single allocation pass. |
| OOP | **Natural fit** — polymorphic creation through interfaces and subclass overrides. |
| Procedural | **Workable** — dispatch functions (switch/if) returning concrete structs. |
| Reactive | **Adapts well** — factories produce observables/streams or select concrete operators based on runtime configuration. |

### 3.2. Benefits

- Decouples client code from concrete product classes — clients depend only on the product interface.
- New products can be added by implementing the interfaces, without modifying existing client code (Open/Closed Principle).
- Centralizes creation logic, making it straightforward to enforce constraints, add logging, or swap implementations.

### 3.3. Trade-offs

- Each new product typically requires a new concrete creator class — class proliferation.
- Adds indirection: the reader must trace through the factory to discover which concrete type is created.
- The Simple Factory variant re-introduces modification when adding products, losing the Open/Closed benefit.

### 3.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 4. Abstract Factory

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

### 4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — a record or module of factory functions (one per product kind) serves as the abstract factory; swapping the record swaps the family. |
| Data-Oriented | **Workable** — factory tables can batch-initialize component arrays per family, but the per-object abstraction layer adds indirection that DOD typically avoids. |
| OOP | **Natural fit** — interfaces for both the factory and the products, with polymorphic dispatch selecting the concrete family. |
| Procedural | **Workable** — a struct of function pointers (one per product kind) passed to client code; switching the struct switches the family. |
| Reactive | **Adapts well** — factory-selected streams or operators can produce family-consistent event pipelines; configuration determines which factory feeds the reactive graph. |

### 4.2. Benefits

- Guarantees product compatibility — objects from a single factory are always designed to work together.
- Isolates concrete classes from client code; the client never mentions a specific product implementation.
- Swapping an entire product family requires changing only the concrete factory supplied at the composition root.

### 4.3. Trade-offs

- Adding a new product kind to the family forces changes across every concrete factory — the interface expands, and all implementations must follow.
- Class proliferation: each family multiplies the number of concrete product classes.
- The additional abstraction layer can be overkill when the system only has one product family or when families are unlikely to change.

### 4.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 5. Prototype

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

### 5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — immutable data structures are inherently safe to share; structural sharing makes "cloning" nearly free, and variant creation is a record-update expression. |
| Data-Oriented | **Workable** — bulk-copying rows or component arrays from a template archetype; useful for spawning entities from prefab data, though memcpy semantics require care with referenced data. |
| OOP | **Natural fit** — clone methods on objects, often combined with a prototype registry for runtime variant management. |
| Procedural | **Workable** — struct copy plus manual deep-copy of heap-allocated fields; no polymorphism required if types are known statically. |
| Reactive | **Uncommon** — streams and observables are typically constructed via operators, not cloned; however, snapshot-and-fork of stream state can serve similar purposes. |

### 5.2. Benefits

- Avoids expensive re-initialization — cloning a pre-built object is often faster than constructing one from scratch.
- Eliminates subclass proliferation — new variants are created by cloning and modifying, not by writing new factory classes.
- Decouples the client from concrete product classes — the client only knows the prototype interface.

### 5.3. Trade-offs

- Deep cloning complex object graphs (circular references, file handles, sockets) can be difficult to implement correctly.
- Each concrete prototype must support cloning — retrofitting clone into an existing hierarchy may require touching every class.
- Shallow-copy defaults in many languages silently share mutable state, introducing aliasing bugs when deep copy was intended.

### 5.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 6. Object Pool

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

### 6.1. Domain Context

Object Pool is primarily relevant in infrastructure and server contexts — database connection pools, HTTP client pools, thread pools, and GPU buffer management. It is rarely encountered in simple CLI tools, scripts, or applications where object creation is cheap and the allocation rate is low.

### 6.2. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Workable** — pools are inherently stateful (mutable idle/active sets), which clashes with purity; they can be modeled as managed effects or wrapped behind a functional resource-acquisition API. |
| Data-Oriented | **Natural fit** — pre-allocated arrays of reusable slots map directly to contiguous memory pools; entity/component pools are a core DOD technique. |
| OOP | **Natural fit** — the pool is an object managing a collection, with checkout/return methods and encapsulated lifecycle logic. |
| Procedural | **Adapts well** — a fixed-size array plus an index or free-list; straightforward to implement without objects. |
| Reactive | **Adapts well** — resource acquisition can be modeled as an observable that emits a resource, with disposal triggering return to the pool; backpressure maps naturally to pool exhaustion. |

### 6.3. Benefits

- Amortizes expensive initialization — the cost of creating a connection or thread is paid once, not per request.
- Bounds resource consumption with a fixed maximum pool size, providing natural backpressure.
- Reduces garbage-collection pressure by reusing allocations instead of creating short-lived objects.

### 6.4. Trade-offs

- State leakage between borrowers if the reset mechanism is incomplete — a returned object may carry dirty state.
- Pool sizing requires tuning: too small starves throughput, too large wastes memory and OS resources.
- Added complexity for health-checking (evicting broken resources), idle-timeout eviction, and thread-safe checkout/return.

### 6.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

