# Design Patterns

## Table of Contents
- [1. Creational](#1-creational)
  - [1.1. Singleton](#11-singleton)
    - [1.1.1. Examples](#111-examples)
  - [1.2. Builder](#12-builder)
    - [1.2.1. Examples](#121-examples)
  - [1.3. Factory](#13-factory)
    - [1.3.1. Examples](#131-examples)
- [2. Structural](#2-structural)
  - [2.1. Facade](#21-facade)
    - [2.1.1. Examples](#211-examples)
  - [2.2. Adapter](#22-adapter)
    - [2.2.1. Examples](#221-examples)
- [3. Behavioral](#3-behavioral)
  - [3.1. Strategy](#31-strategy)
    - [3.1.1. Examples](#311-examples)
  - [3.2. Observer](#32-observer)
    - [3.2.1. Examples](#321-examples)

<a id="1-creational"></a>

## 1. Creational

Creational patterns abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

| Pattern | When to Use |
|---------|-------------|
| [Singleton](#11-singleton) | A shared resource needs exactly one instance with global access. |
| [Builder](#12-builder) | Constructing complex objects with many optional or ordered parameters. |
| [Factory](#13-factory) | Creating objects without specifying the exact class; letting subclasses decide. |

<a id="11-singleton"></a>

### 1.1. Singleton

| | |
|----------|--------|
| **Who**  | Applications that need a single shared instance (e.g., configuration managers, logging services, connection pools). |
| **What** | Ensures a class has exactly one instance and provides a global point of access to it. |
| **When** | When exactly one object is needed to coordinate access to a shared resource, and uncontrolled instantiation would cause inconsistency or waste. |
| **Where**| Infrastructure or service layers where a single point of control is required (logging, caching, configuration, thread pools). |
| **Why**  | Prevents multiple instances that could lead to inconsistent state, duplicated resource usage, or conflicting behavior. |
| **How**  | Make the constructor private, store the instance in a static field, and expose a static method or property that returns the instance — creating it lazily on first access with appropriate thread-safety guarantees. |

The Singleton pattern restricts a class to exactly one instance and provides a global access point to it. The class itself manages its own lifecycle: it hides its constructor so no external code can call `new`, stores the single instance in a static field, and exposes a static method or property that returns that instance — lazily creating it on first access.

Thread safety is the primary implementation concern. In a concurrent environment, two threads could simultaneously detect that the instance does not yet exist and each create one. Solutions include language-level lazy primitives (C# `Lazy<T>`, Java `enum` singletons), double-checked locking, or static initialization guarantees provided by the runtime.

Singleton is sometimes considered an anti-pattern because it introduces hidden global state, makes unit testing harder (shared state leaks between tests), and obscures dependencies. Prefer dependency injection when possible, and reserve Singleton for genuinely shared, stateless, or infrastructure-level resources (loggers, configuration, connection pools).

<a id="111-examples"></a>

#### 1.1.1. Examples

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

A Python module is itself a singleton — its top-level state is initialized once and shared across all imports. When class-level singleton semantics are needed, override `__new__`.

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

| | |
|----------|--------|
| **Who**  | Clients that need to construct complex objects with many optional or conditional parameters. |
| **What** | Separates the construction of a complex object from its representation, allowing the same construction process to create different representations. |
| **When** | When an object has many optional fields, when construction involves multiple steps in a specific order, or when a constructor would need too many parameters to remain readable. |
| **Where**| Commonly used in APIs that configure objects (HTTP clients, query builders, UI component configuration, domain object assembly). |
| **Why**  | Eliminates telescoping constructors, makes construction self-documenting through named methods, and enables validation at build time rather than after the fact. |
| **How**  | Create a separate builder object with fields matching the target's configurable options. Provide setter methods that return the builder for method chaining. A terminal build method validates the accumulated state and produces the finished object, returning an error if required fields are missing. |

The Builder pattern separates the construction of a complex object from its final representation. Instead of passing every parameter to a single constructor call — leading to long, unreadable argument lists (telescoping constructors) — the client configures the object step by step through a dedicated builder. Each setter method records one piece of configuration and returns the builder itself so calls can be chained. A terminal `build` method validates the accumulated state and produces the finished object, failing explicitly if required fields are missing.

The key participants are the **product** (the complex object being built), the **builder** (the mutable intermediate that accumulates configuration), and optionally a **director** (a reusable recipe that drives the builder through a fixed sequence of steps). In practice, most modern uses skip the director and let the client drive the builder directly.

Builder is especially valuable when objects have many optional fields, construction invariants that must hold at creation time, or when the same construction process should produce different representations.

<a id="121-examples"></a>

#### 1.2.1. Examples

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

| | |
|----------|--------|
| **Who**  | Clients that need to create objects without specifying the exact class to instantiate. |
| **What** | Defines an interface for creating an object, but lets subclasses (or trait implementors) decide which concrete class to instantiate, deferring creation to them. |
| **When** | When a class cannot anticipate the type of objects it must create, or when you want to isolate client code from concrete product classes. |
| **Where**| Frameworks, plugin systems, and libraries where the concrete classes are determined by configuration, user choice, or extension code. |
| **Why**  | Eliminates hard-coded instantiation of concrete classes. The client interacts solely with the product interface, making it independent of how objects are created and enabling new products without modifying existing code. |
| **How**  | Define a product interface that all created objects share. Define a creator interface with a factory method that returns the product type. Implement concrete creators that override the factory method to return specific products. Clients depend only on the creator and product interfaces. |

The Factory pattern (specifically Factory Method) defines an interface for creating objects but delegates the choice of concrete type to subclasses or implementors. The client programs against the creator's abstract interface and never references concrete product classes directly, so new product variants can be introduced without modifying existing client logic — a direct application of the Open/Closed Principle.

The key participants are the **product interface** (the abstraction all created objects share), **concrete products** (the specific types being created), the **creator interface** (which declares the factory method), and **concrete creators** (which implement the factory method to return a specific product). The client works only with the creator and product interfaces.

A simpler variant — sometimes called Simple Factory — uses a single function with a discriminator (e.g., an enum or string) to decide which concrete type to return. This trades extensibility for convenience: adding a new product requires modifying the factory function rather than adding a new creator class.

<a id="131-examples"></a>

#### 1.3.1. Examples

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

<a id="2-structural"></a>

## 2. Structural

Structural patterns deal with the composition of classes and objects, using inheritance and composition to form larger structures while keeping them flexible and efficient.

| Pattern | When to Use |
|---------|-------------|
| [Facade](#21-facade) | Simplifying access to a complex subsystem through one unified entry point. |
| [Adapter](#22-adapter) | Making an existing class work with an interface it wasn't designed for. |

<a id="21-facade"></a>

### 2.1. Facade

| | |
|----------|--------|
| **Who**  | Clients that need a simple interface to a complex subsystem. |
| **What** | Provides a unified, higher-level interface to a set of interfaces in a subsystem, making the subsystem easier to use. |
| **When** | When a subsystem has many interdependent classes and clients only need a subset of its capabilities, or when you want to layer your architecture with clean entry points. |
| **Where**| Between client code and complex subsystems (e.g., a multimedia framework, a business services layer, OS kernel APIs). |
| **Why**  | Reduces coupling and the learning curve by hiding subsystem complexity behind a single, well-defined interface. Clients are shielded from subsystem changes. |
| **How**  | Create a facade object that composes (owns or references) the subsystem components. Implement methods on the facade that delegate to the appropriate subsystem objects, handling sequencing and data transformation internally. Clients interact only with the facade. |

The Facade pattern provides a single, simplified interface to a complex subsystem of classes. Rather than forcing clients to understand and orchestrate dozens of subsystem objects, the facade wraps that complexity behind one or a few straightforward methods. The client calls the facade; the facade coordinates the subsystem internally — sequencing calls, translating data, and managing dependencies between subsystem components.

The key participants are the **facade** (the simplified entry point), the **subsystem classes** (the complex internals being wrapped), and the **client** (which interacts only with the facade). Importantly, the facade does not prevent advanced clients from accessing subsystem classes directly when finer control is needed.

Facade promotes loose coupling between the client and the subsystem, reduces the learning curve for new developers, and provides a natural boundary for layering an architecture. It is not about adding new functionality — it is about simplifying access to existing functionality.

<a id="211-examples"></a>

#### 2.1.1. Examples

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

| | |
|----------|--------|
| **Who**  | Clients that need to use an existing class whose interface does not match the one they require. |
| **What** | Converts the interface of an existing class into another interface clients expect, letting incompatible classes work together. |
| **When** | When you want to reuse an existing class but its interface does not match what your code requires, and modifying the class is impossible or undesirable. |
| **Where**| Wrappers around third-party libraries, legacy code, or external APIs that must conform to your application's interface contracts. |
| **Why**  | Avoids modifying existing code (which may be impossible, risky, or a third-party dependency) while still enabling it to integrate with new code through a compatible interface. |
| **How**  | Create an adapter that holds a reference to the adaptee. Implement the target interface on the adapter, delegating each method to the corresponding adaptee method with any necessary translation of data or signatures. |

The Adapter pattern converts the interface of an existing class into the interface that clients expect, allowing classes with incompatible interfaces to collaborate without modifying their source code. The adapter acts as a translator: it wraps the existing class (the **adaptee**), implements the interface the client requires (the **target**), and maps each target method to the corresponding adaptee method — performing any necessary data transformation along the way.

There are two variants. An **object adapter** uses composition: it holds a reference to the adaptee and delegates calls to it. A **class adapter** uses multiple inheritance to combine the target and adaptee interfaces (possible in languages like C++, but not in single-inheritance languages like Java, C#, or Rust). The object adapter is far more common because it works in any language and allows adapting the adaptee's subclasses as well.

Adapter is especially useful when integrating third-party libraries, legacy systems, or external APIs whose interfaces you cannot change but need to conform to your application's contracts.

<a id="221-examples"></a>

#### 2.2.1. Examples

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

<a id="3-behavioral"></a>

## 3. Behavioral

Behavioral patterns focus on communication and responsibility between objects, defining how they interact and distribute work.

| Pattern | When to Use |
|---------|-------------|
| [Strategy](#31-strategy) | Selecting between interchangeable algorithms at runtime without conditionals. |
| [Observer](#32-observer) | Notifying multiple objects automatically when one object's state changes. |

<a id="31-strategy"></a>

### 3.1. Strategy

| | |
|----------|--------|
| **Who**  | Clients that need to select an algorithm at runtime without changing the code that uses it. |
| **What** | Defines a family of algorithms, encapsulates each one, and makes them interchangeable. Strategy lets the algorithm vary independently from clients that use it. |
| **When** | When you have multiple variants of an algorithm and want to switch between them at runtime without modifying client code. |
| **Where**| Contexts where different behaviors are needed depending on configuration or user input (sorting, compression, validation, pricing, routing). |
| **Why**  | Eliminates large conditional blocks and promotes the Open/Closed Principle — new strategies are added without modifying existing code. |
| **How**  | Define a strategy interface with a method that performs the algorithm. Implement concrete strategy classes for each variant. A context object holds a reference to the current strategy and delegates work to it; swapping the strategy changes the behavior without modifying the context. |

The Strategy pattern defines a family of interchangeable algorithms, encapsulates each one behind a common interface, and lets the client select which algorithm to use at runtime. Instead of implementing multiple behaviors inline with conditionals (`if`/`else`, `switch`), the client delegates work to a strategy object. Swapping the strategy swaps the behavior — no conditionals, no code changes in the client.

The key participants are the **strategy interface** (the contract all algorithms share), **concrete strategies** (individual algorithm implementations), and the **context** (the object that holds the current strategy and forwards requests to it). The context is agnostic to which concrete strategy it holds; it only depends on the interface.

New algorithms are added by implementing the strategy interface, leaving existing code untouched (Open/Closed Principle). Strategy is a common alternative to subclassing: instead of creating a subclass for each variant, you compose the context with a strategy at runtime.

<a id="311-examples"></a>

#### 3.1.1. Examples

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

| | |
|----------|--------|
| **Who**  | Objects that need to be notified of state changes in another object (e.g., UI elements, logging services, cache invalidators). |
| **What** | Defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. |
| **When** | When a change to one object requires updating others, and you don't want to hard-code those dependencies. |
| **Where**| Event handling systems, MVC/MVVM frameworks, GUI toolkits, reactive streams, and any publish-subscribe scenario. |
| **Why**  | Promotes loose coupling between the subject and observers. They vary independently, and new observers can be added without modifying the subject. |
| **How**  | Define an observer interface with an update method. Define a subject interface with attach, detach, and notify methods. The concrete subject maintains a collection of observers and invokes their update method whenever its state changes. |

The Observer pattern establishes a one-to-many dependency between a **subject** and its **observers**: when the subject's state changes, it automatically notifies every registered observer. Observers subscribe (attach) to the subject and can unsubscribe (detach) at any time, making the relationship fully dynamic. The subject knows its observers only through an abstract interface, so new observer types can be added without modifying the subject.

There are two notification models. In the **push model** (shown below), the subject sends the relevant state data to observers as method arguments — simple but couples observers to the specific data shape. In the **pull model**, the subject sends a minimal notification and observers query back for the data they need — more flexible but requires observers to hold a reference to the subject.

Observer is foundational to event-driven architectures, GUI frameworks (click handlers, data binding), reactive programming (`Observable`/`Subject` in Rx), and messaging systems. The pattern trades simplicity for decoupling: debugging notification chains can be harder because the flow of control is implicit rather than explicit.

<a id="321-examples"></a>

#### 3.2.1. Examples

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
        foreach (var observer in _observers)
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
