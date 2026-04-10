# Structural

## Table of Contents

- [1. Facade](#1-facade)
  - [1.1. Paradigm Fit](#11-paradigm-fit)
  - [1.2. Benefits](#12-benefits)
  - [1.3. Trade-offs](#13-trade-offs)
  - [1.4. Examples](#14-examples)
- [2. Adapter](#2-adapter)
  - [2.1. Paradigm Fit](#21-paradigm-fit)
  - [2.2. Benefits](#22-benefits)
  - [2.3. Trade-offs](#23-trade-offs)
  - [2.4. Examples](#24-examples)
- [3. Decorator](#3-decorator)
  - [3.1. Paradigm Fit](#31-paradigm-fit)
  - [3.2. Benefits](#32-benefits)
  - [3.3. Trade-offs](#33-trade-offs)
  - [3.4. Examples](#34-examples)
- [4. Proxy](#4-proxy)
  - [4.1. Paradigm Fit](#41-paradigm-fit)
  - [4.2. Benefits](#42-benefits)
  - [4.3. Trade-offs](#43-trade-offs)
  - [4.4. Examples](#44-examples)
- [5. Composite](#5-composite)
  - [5.1. Paradigm Fit](#51-paradigm-fit)
  - [5.2. Benefits](#52-benefits)
  - [5.3. Trade-offs](#53-trade-offs)
  - [5.4. Examples](#54-examples)
- [6. Bridge](#6-bridge)
  - [6.1. Paradigm Fit](#61-paradigm-fit)
  - [6.2. Benefits](#62-benefits)
  - [6.3. Trade-offs](#63-trade-offs)
  - [6.4. Examples](#64-examples)
- [7. Flyweight](#7-flyweight)
  - [7.1. Paradigm Fit](#71-paradigm-fit)
  - [7.2. Benefits](#72-benefits)
  - [7.3. Trade-offs](#73-trade-offs)
  - [7.4. Examples](#74-examples)

Structural patterns deal with the composition of classes and objects, using inheritance and composition to form larger structures while keeping them flexible and efficient.

| Pattern | When to Use |
|---------|-------------|
| [Facade](#1-facade) | Simplifying access to a complex subsystem through one unified entry point. |
| [Adapter](#2-adapter) | Making an existing class work with an interface it wasn't designed for. |
| [Decorator](#3-decorator) | Dynamically adding behavior to an object without modifying its class. |
| [Proxy](#4-proxy) | Controlling access to another object for lazy loading, access control, or caching. |
| [Composite](#5-composite) | Treating individual objects and groups uniformly in tree structures. |
| [Bridge](#6-bridge) | Separating abstraction from implementation so both vary independently. |
| [Flyweight](#7-flyweight) | Sharing common state across many fine-grained objects to save memory. |

## 1. Facade

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

### 1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — a module exporting simple functions that compose complex internal operations. |
| Data-Oriented | **Natural fit** — modules that hide cache-friendly data transformations behind a clean query API. |
| OOP | **Natural fit** — facade object wrapping and orchestrating subsystem instances. |
| Procedural | **Natural fit** — wrapper functions that sequence subsystem calls behind a simple API. |
| Reactive | **Natural fit** — exposes simple subscribe/observe entry points over complex internal pipelines. |

### 1.2. Benefits

- Reduces coupling — the client depends on one facade rather than many subsystem classes.
- Lowers the learning curve by exposing only the operations most clients need.
- Provides a natural layering boundary; the subsystem can evolve internally without breaking clients.

### 1.3. Trade-offs

- Risk of becoming a "god object" if the facade accumulates too many responsibilities over time.
- May hide functionality that advanced clients need, forcing them to bypass the facade and couple to the subsystem directly.
- Adds an extra layer of indirection between the client and the actual work.

### 1.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 2. Adapter

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

### 2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — function wrappers and composition translate one signature to another. |
| Data-Oriented | **Workable** — transform functions convert between data layouts (AoS ↔ SoA), but less formalized as a named pattern. |
| OOP | **Natural fit** — wrapper class implementing the target interface, delegating to the adaptee. |
| Procedural | **Workable** — wrapper functions that translate calls and data between interfaces. |
| Reactive | **Natural fit** — operators like `map`/`flatMap` are adapters that translate one stream type to another. |

### 2.2. Benefits

- Enables reuse of existing classes without modifying their source code.
- Isolates translation logic in one place — client code stays clean of conversion details.
- Can adapt entire class hierarchies: an object adapter works with the adaptee and all its subclasses.

### 2.3. Trade-offs

- Adds a wrapper layer with delegation overhead (negligible in most cases, noticeable in hot paths).
- One adapter per incompatible interface can lead to many small wrapper classes.
- If the adaptee's interface changes, the adapter must change too — maintenance coupling shifts rather than disappears.

### 2.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 3. Decorator

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

### 3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — function composition (`f(g(x))`) is decoration; higher-order functions wrap and extend behavior without mutation. |
| Data-Oriented | **Uncommon** — behavior is attached to data pipelines rather than individual objects; component flags or bitmasks replace wrapper layers. |
| OOP | **Natural fit** — classic GoF pattern: shared interface, composition-based wrapping, polymorphic dispatch. |
| Procedural | **Workable** — function pointer chains or wrapper functions provide similar layering, though without polymorphic dispatch. |
| Reactive | **Adapts well** — operators like `map`, `tap`, `retry` are decorators on a stream, each adding behavior around the data flow. |

### 3.2. Benefits

- Extends behavior at runtime without modifying existing code or creating subclass explosions.
- Each decorator is a small, single-responsibility class that is easy to test and reason about.
- Decorators compose freely — any combination and ordering of layers is possible.

### 3.3. Trade-offs

- Deep decorator stacks produce many small objects, making debugging and stack traces harder to follow.
- The order of wrapping matters and is implicit — swapping two decorators can silently change behavior.
- Identity checks (`obj == original`) break because the outermost wrapper is a different object than the original component.

### 3.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 4. Proxy

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

### 4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — lazy evaluation (thunks, `Lazy<T>`) and memoization are functional proxies; access control maps to wrapper functions. |
| Data-Oriented | **Uncommon** — data-oriented designs avoid indirection; proxies add pointer-chasing that hurts cache locality. |
| OOP | **Natural fit** — shared interface with delegating wrapper is the classic formulation. |
| Procedural | **Workable** — guard functions that check conditions before calling the real function; opaque handles act as proxies. |
| Reactive | **Adapts well** — `shareReplay` caches emissions (caching proxy), `defer` delays subscription (virtual proxy), access control operators gate streams. |

### 4.2. Benefits

- Defers costly initialization until the object is actually needed, saving resources in cases where it may never be used.
- Centralizes cross-cutting concerns (logging, caching, access control) without modifying the real subject.
- Transparent to the client — the proxy shares the subject's interface, so no calling code needs to change.

### 4.3. Trade-offs

- Adds an indirection layer that can increase response latency, especially if the proxy performs locking or network calls.
- Lazy initialization introduces first-access latency spikes that can be surprising in latency-sensitive paths.
- The proxy must stay in sync with the real subject's interface — any change to the subject requires a corresponding update.

### 4.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 5. Composite

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

### 5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — algebraic data types (enums with variants) and recursive functions model trees directly; fold/catamorphism traverses the structure. |
| Data-Oriented | **Workable** — trees stored as flat arrays with parent/child indices avoid pointer-chasing; operations iterate linearly over the array. |
| OOP | **Natural fit** — shared interface with polymorphic dispatch makes recursive traversal seamless. |
| Procedural | **Workable** — tree nodes as structs with tagged unions; recursive functions switch on the node type. |
| Reactive | **Adapts well** — composite streams (`merge`, `combineLatest`) unify multiple sources into one, mirroring the part-whole concept. |

### 5.2. Benefits

- Clients treat single objects and compositions uniformly — no conditional branching on type.
- New leaf or composite types can be added without changing client code that operates on the component interface.
- Recursive operations (size, render, search) propagate naturally through the tree with minimal boilerplate.

### 5.3. Trade-offs

- The uniform interface may expose operations on leaves that are meaningless (e.g., `add_child` on a file), requiring no-op or error implementations.
- Deep trees with many small nodes can be expensive to traverse and difficult to debug.
- Enforcing constraints (e.g., "a composite can only hold certain leaf types") is hard when the interface is fully generic.

### 5.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 6. Bridge

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

### 6.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — pass implementation functions (or a record of functions) to the abstraction; higher-order functions bridge the two layers. |
| Data-Oriented | **Workable** — separate data tables for abstraction state and implementation state, joined by an ID; avoids virtual dispatch. |
| OOP | **Natural fit** — two class hierarchies connected by composition, the canonical GoF formulation. |
| Procedural | **Workable** — struct holding a function-pointer table (vtable) for the implementation; abstractions call through the table. |
| Reactive | **Adapts well** — the abstraction emits events; the implementor subscribes and performs platform-specific work, decoupling the stream topology from the effect execution. |

### 6.2. Benefits

- Eliminates M × N subclass explosion — each dimension grows independently.
- Implementation can be swapped or selected at runtime without altering abstraction code.
- Hides implementation details from the client, strengthening encapsulation across the boundary.

### 6.3. Trade-offs

- Adds structural complexity with two parallel hierarchies and an indirection between them.
- The right split point between abstraction and implementation must be identified early; refactoring later is costly.
- Over-engineering risk when only one implementation exists or the two axes are unlikely to vary independently.

### 6.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 7. Flyweight

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

### 7.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — immutable values are shared by default; persistent data structures and interning are inherent flyweights. |
| Data-Oriented | **Natural fit** — SoA layouts naturally separate shared columns from per-instance columns; indices into shared tables are flyweight references. |
| OOP | **Natural fit** — flyweight factory + shared immutable objects is the canonical GoF formulation. |
| Procedural | **Workable** — shared lookup tables indexed by ID; each instance stores an index rather than a copy. |
| Reactive | **Adapts well** — shared reference data (`shareReplay`, interned config streams) avoids duplicating constant data across subscribers. |

### 7.2. Benefits

- Dramatically reduces memory usage when many objects share most of their state.
- The flyweight factory ensures identity-based sharing — the same intrinsic data is never duplicated.
- Intrinsic immutability simplifies concurrency: shared flyweights require no synchronization.

### 7.3. Trade-offs

- Splits state into intrinsic and extrinsic, spreading what was a single object across two locations and increasing code complexity.
- CPU cost increases because extrinsic state must be supplied or looked up on every method call rather than stored locally.
- Identifying the correct split between intrinsic and extrinsic state requires careful analysis; a wrong split yields little benefit or breaks encapsulation.

### 7.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

