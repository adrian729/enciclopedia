# Behavioral

## Table of Contents

- [1. Strategy](#1-strategy)
  - [1.1. Paradigm Fit](#11-paradigm-fit)
  - [1.2. Benefits](#12-benefits)
  - [1.3. Trade-offs](#13-trade-offs)
  - [1.4. Examples](#14-examples)
- [2. Observer](#2-observer)
  - [2.1. Paradigm Fit](#21-paradigm-fit)
  - [2.2. Benefits](#22-benefits)
  - [2.3. Trade-offs](#23-trade-offs)
  - [2.4. Examples](#24-examples)
- [3. Command](#3-command)
  - [3.1. Paradigm Fit](#31-paradigm-fit)
  - [3.2. Benefits](#32-benefits)
  - [3.3. Trade-offs](#33-trade-offs)
  - [3.4. Examples](#34-examples)
- [4. State](#4-state)
  - [4.1. Paradigm Fit](#41-paradigm-fit)
  - [4.2. Benefits](#42-benefits)
  - [4.3. Trade-offs](#43-trade-offs)
  - [4.4. Examples](#44-examples)
- [5. Template Method](#5-template-method)
  - [5.1. Paradigm Fit](#51-paradigm-fit)
  - [5.2. Benefits](#52-benefits)
  - [5.3. Trade-offs](#53-trade-offs)
  - [5.4. Examples](#54-examples)
- [6. Iterator](#6-iterator)
  - [6.1. Paradigm Fit](#61-paradigm-fit)
  - [6.2. Benefits](#62-benefits)
  - [6.3. Trade-offs](#63-trade-offs)
  - [6.4. Examples](#64-examples)
- [7. Chain of Responsibility](#7-chain-of-responsibility)
  - [7.1. Paradigm Fit](#71-paradigm-fit)
  - [7.2. Benefits](#72-benefits)
  - [7.3. Trade-offs](#73-trade-offs)
  - [7.4. Examples](#74-examples)
- [8. Mediator](#8-mediator)
  - [8.1. Paradigm Fit](#81-paradigm-fit)
  - [8.2. Benefits](#82-benefits)
  - [8.3. Trade-offs](#83-trade-offs)
  - [8.4. Examples](#84-examples)
- [9. Memento](#9-memento)
  - [9.1. Paradigm Fit](#91-paradigm-fit)
  - [9.2. Benefits](#92-benefits)
  - [9.3. Trade-offs](#93-trade-offs)
  - [9.4. Examples](#94-examples)
- [10. Visitor](#10-visitor)
  - [10.1. Paradigm Fit](#101-paradigm-fit)
  - [10.2. Benefits](#102-benefits)
  - [10.3. Trade-offs](#103-trade-offs)
  - [10.4. Examples](#104-examples)
- [11. Interpreter](#11-interpreter)
  - [11.1. Domain Context](#111-domain-context)
  - [11.2. Paradigm Fit](#112-paradigm-fit)
  - [11.3. Benefits](#113-benefits)
  - [11.4. Trade-offs](#114-trade-offs)
  - [11.5. Examples](#115-examples)
- [12. Null Object](#12-null-object)
  - [12.1. Paradigm Fit](#121-paradigm-fit)
  - [12.2. Benefits](#122-benefits)
  - [12.3. Trade-offs](#123-trade-offs)
  - [12.4. Examples](#124-examples)
- [13. Dependency Injection](#13-dependency-injection)
  - [13.1. Paradigm Fit](#131-paradigm-fit)
  - [13.2. Benefits](#132-benefits)
  - [13.3. Trade-offs](#133-trade-offs)
  - [13.4. Examples](#134-examples)

Behavioral patterns focus on communication and responsibility between objects, defining how they interact and distribute work.

| Pattern | When to Use |
|---------|-------------|
| [Strategy](#1-strategy) | Selecting between interchangeable algorithms at runtime without conditionals. |
| [Observer](#2-observer) | Notifying multiple objects automatically when one object's state changes. |
| [Command](#3-command) | Encapsulating requests as objects for undo/redo, queuing, and logging. |
| [State](#4-state) | Letting an object change behavior when its internal state changes. |
| [Template Method](#5-template-method) | Defining an algorithm skeleton with customizable steps in subclasses. |
| [Iterator](#6-iterator) | Traversing a collection without exposing its internal representation. |
| [Chain of Responsibility](#7-chain-of-responsibility) | Passing a request along a handler chain until one processes it. |
| [Mediator](#8-mediator) | Centralizing complex inter-object communication through a coordinator. |
| [Memento](#9-memento) | Capturing and restoring an object's state without violating encapsulation. |
| [Visitor](#10-visitor) | Adding operations to a class hierarchy without modifying it. |
| [Interpreter](#11-interpreter) | Defining a grammar and interpreter for a language. |
| [Null Object](#12-null-object) | Providing a do-nothing default object to eliminate null checks. |
| [Dependency Injection](#13-dependency-injection) | Externally supplying dependencies instead of creating them internally. |

## 1. Strategy

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

### 1.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — first-class functions and closures are strategies by definition; the pattern is implicit. |
| Data-Oriented | **Workable** — system dispatch selects different processing functions for the same component data. |
| OOP | **Natural fit** — strategy interface with interchangeable concrete implementations. |
| Procedural | **Workable** — function pointers or callback parameters. |
| Reactive | **Natural fit** — swappable operators or stream transformations selected at subscription time. |

### 1.2. Benefits

- Eliminates conditional blocks (`if`/`else`, `switch`) — each algorithm is self-contained and independently testable.
- New algorithms are added without modifying existing code (Open/Closed Principle).
- Context and strategies vary independently, promoting composition over inheritance.

### 1.3. Trade-offs

- Clients must know the available strategies and choose between them — the decision logic moves to the caller.
- One class per algorithm can lead to many small classes for a family of simple variants.
- Adds indirection: behavior is delegated rather than inline, which can obscure straightforward logic when only two variants exist.

### 1.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 2. Observer

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

### 2.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — reactive streams and event combinators express the same idea declaratively. |
| Data-Oriented | **Uncommon** — favors polling and system iteration over push-based notification; change detection is query-based. |
| OOP | **Natural fit** — subject/observer interfaces with dynamic subscription lists. |
| Procedural | **Workable** — callback registration with manual lifecycle management. |
| Reactive | **Natural fit** — Observer is the foundational primitive; `Observable`/`Subject` is the pattern formalized as a first-class construct. |

### 2.2. Benefits

- Loose coupling — subject and observers depend only on abstractions, not on each other's concrete types.
- Dynamic subscription: observers can register and unregister at any point during runtime.
- Supports broadcast communication — a single state change notifies all interested parties.

### 2.3. Trade-offs

- Notification order is generally undefined and may vary between runs or implementations.
- Lapsed listener problem: forgetting to detach an observer can cause memory leaks and phantom updates. Weak references (`weakref` in Python, `WeakReference<T>` in C#) mitigate this by allowing garbage collection of unsubscribed observers.
- Cascading notifications (one observer's update triggers another subject change) create hard-to-debug chains.
- Update cost scales linearly with observer count — each state change invokes every registered observer.

### 2.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 3. Command

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

### 3.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — commands are simply closures or data describing actions; undo becomes event sourcing over an immutable log. |
| Data-Oriented | **Adapts well** — commands can be plain data structs processed in batches by a command-processing system. |
| OOP | **Natural fit** — classic GoF pattern with Command interface, concrete commands, invoker, and receiver. |
| Procedural | **Workable** — function pointers paired with argument structs; undo requires explicit state snapshots. |
| Reactive | **Adapts well** — commands map to events in a stream; undo/redo becomes stream rewinding or event replay. |

### 3.2. Benefits

- Decouples the object that invokes an operation from the one that knows how to perform it.
- Enables undo/redo by storing executed commands in a history stack with inverse operations. A redo stack (cleared on each new command) completes the model, though the examples below show only undo for brevity.
- Commands can be serialized, queued, logged, and composed into macros, supporting deferred and batch execution.

### 3.3. Trade-offs

- Introduces a class for every operation, increasing the total number of types in the system.
- Undo state management adds complexity — each command must capture and restore enough context to reverse its effect.
- Indirection between the invoker and the receiver can make the control flow harder to trace during debugging.

### 3.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 4. State

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

### 4.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — state can be a discriminated union with pure transition functions returning the next state. |
| Data-Oriented | **Workable** — state is a tag or enum field on entity data; systems dispatch behavior based on the tag. |
| OOP | **Natural fit** — each state is a class implementing a common interface; the context delegates to the current state object. |
| Procedural | **Workable** — function-pointer tables indexed by state enum, or explicit switch blocks. |
| Reactive | **Adapts well** — state machines can be modeled as `scan`/`reduce` over event streams, emitting new states. |

### 4.2. Benefits

- Eliminates large conditional blocks — each state's behavior is isolated in its own class, improving readability.
- Adding new states requires only a new class with no changes to the context or existing states.
- State transitions are explicit and localized, making the state machine easy to visualize and verify.

### 4.3. Trade-offs

- Increases the number of classes — one per state — which can be excessive for simple state machines.
- Distributed transitions (states deciding the next state) can scatter transition logic, making the overall machine harder to see at a glance.
- State objects that need access to the context's internals may require exposing fields that would otherwise be private.

### 4.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 5. Template Method

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

### 5.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — higher-order functions accept step functions as parameters, achieving the same structure without inheritance. |
| Data-Oriented | **Uncommon** — systems process data in pipelines; per-entity behavioral customization via inheritance is rare. |
| OOP | **Natural fit** — abstract base class with a final template method and overridable steps is the canonical form. |
| Procedural | **Workable** — a top-level function accepts function pointers for the customizable steps. |
| Reactive | **Workable** — a fixed pipeline of operators with configurable transformation stages, though composition is more idiomatic. |

### 5.2. Benefits

- Maximizes code reuse — the invariant algorithm lives in one place; only varying steps are overridden.
- Enforces a consistent algorithmic structure across all variants, preventing subclasses from accidentally breaking the workflow.
- Hook methods provide optional customization points with sensible defaults, minimizing the burden on subclasses.

### 5.3. Trade-offs

- Relies on inheritance, which can lead to deep hierarchies and tight coupling between base and derived classes.
- Subclasses must understand the base class's control flow to override steps correctly — a form of fragile base class problem.
- Adding a new step to the template method can require changes across all existing subclasses.

### 5.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 6. Iterator

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

### 6.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — lazy lists, generators, and fold/map/filter are iterators in spirit; the pattern is foundational. |
| Data-Oriented | **Adapts well** — iterating over contiguous data arrays is the primary access pattern; custom iterators can expose SoA views. |
| OOP | **Natural fit** — iterator interface with `hasNext`/`next` methods; collections provide factory methods for iterators. |
| Procedural | **Workable** — index-based loops or opaque cursor structs advanced by a `next` function. |
| Reactive | **Adapts well** — push-based streams are the dual of pull-based iterators; conversion between the two is well-defined. |

### 6.2. Benefits

- Decouples traversal logic from collection internals, letting both evolve independently.
- Supports multiple simultaneous traversals over the same collection with independent iterator instances.
- Enables lazy evaluation — elements are produced on demand, avoiding unnecessary computation or memory allocation.

### 6.3. Trade-offs

- Simple collections (plain arrays) gain little from a dedicated iterator; the abstraction adds overhead without clear benefit.
- External iterators expose traversal state that can become stale if the collection is mutated mid-iteration.
- Custom iterators for complex structures (graphs, trees) can be difficult to implement correctly, especially when the traversal must be resumable.

### 6.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 7. Chain of Responsibility

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

### 7.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — function composition or a list of functions folded over the request; each function decides whether to short-circuit. |
| Data-Oriented | **Workable** — pipeline stages can be systems that process request data sequentially through component tables. |
| OOP | **Natural fit** — handler interface with a `next` reference; each concrete handler in the chain implements the interface. |
| Procedural | **Workable** — a list of function pointers iterated in sequence, each receiving the request and a continue flag. |
| Reactive | **Adapts well** — operators in a stream pipeline are a natural chain; `filter`, `map`, and `takeWhile` model handler decisions. |

### 7.2. Benefits

- Decouples the sender from all receivers — the client sends the request without knowing which handler will process it.
- Handlers can be added, removed, or reordered at runtime without modifying existing handlers or the client.
- Each handler addresses a single concern, promoting the Single Responsibility Principle and clean separation of cross-cutting logic.

### 7.3. Trade-offs

- No guarantee of handling — if no handler in the chain processes the request, it falls through silently unless a catch-all is added.
- Long chains can be difficult to debug because the processing path is assembled at runtime and not visible in static code analysis.
- Performance can degrade with many handlers if every request must traverse the entire chain even when early termination is rare.

### 7.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 8. Mediator

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

### 8.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — a central dispatch function routes messages between participants; event buses model the same idea functionally. |
| Data-Oriented | **Workable** — a coordination system reads multiple component tables and writes updates, acting as a mediator between data groups. |
| OOP | **Natural fit** — mediator interface with concrete implementations that coordinate colleague objects. |
| Procedural | **Workable** — a central function or module receives notifications and dispatches calls to relevant subsystems. |
| Reactive | **Natural fit** — a central subject/bus merges streams from multiple sources and routes events to subscribers. |

### 8.2. Benefits

- Reduces coupling between communicating objects — each colleague depends only on the mediator, not on every other colleague.
- Centralizes interaction logic in one place, making complex coordination easier to understand and modify.
- Adding new colleagues requires updating the mediator, not every existing colleague.

### 8.3. Trade-offs

- The mediator can become a monolithic god object if too much logic accumulates in it.
- Adds a layer of indirection — tracing the flow from one colleague to another requires reading through the mediator.
- Single point of failure: all interaction passes through the mediator, so a bug there affects the entire group.

### 8.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 9. Memento

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

### 9.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — immutable values make every prior state a natural memento; persistent data structures preserve previous versions automatically. |
| Data-Oriented | **Workable** — snapshots of component arrays can be stored and swapped back in, though bulk-copying data tables can be expensive. |
| OOP | **Natural fit** — originator creates opaque memento objects; caretaker manages them without breaking encapsulation. |
| Procedural | **Workable** — struct copies or serialized snapshots stored in an array serve as mementos. |
| Reactive | **Adapts well** — state replay (e.g., `BehaviorSubject` history or event-sourced streams) achieves the same goal within a reactive pipeline. |

### 9.2. Benefits

- Preserves encapsulation — the originator's internal structure is not exposed to the caretaker or any other external object.
- Undo/redo becomes straightforward: push mementos onto a stack and pop to restore.
- Mementos are immutable snapshots, safe to store, serialize, or transmit.

### 9.3. Trade-offs

- Memory cost can grow quickly if the originator's state is large and snapshots are taken frequently.
- The originator must expose a way to produce and consume mementos, which can be awkward to design if the state is complex.
- The caretaker must manage memento lifecycle (when to discard old mementos) to avoid unbounded memory growth.

### 9.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 10. Visitor

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

### 10.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — pattern matching over algebraic data types (sum types) replaces double dispatch; each match arm is a "visit" method. |
| Data-Oriented | **Adapts well** — operations process arrays of each component type in bulk; the "visitor" is the system that iterates over typed tables. |
| OOP | **Natural fit** — canonical double-dispatch pattern with visitor and element interfaces. |
| Procedural | **Workable** — a switch/case on a type tag achieves the same dispatch, though it scatters less cleanly than a visitor object. |
| Reactive | **Workable** — streams can map elements through transform functions keyed by type, but the pattern's dispatch structure isn't a natural reactive idiom. |

### 10.2. Benefits

- New operations are added by writing a new visitor — no modification to element classes (Open/Closed for operations).
- Related behavior for a single operation is consolidated in one visitor class instead of scattered across element types.
- Visitors can accumulate state as they traverse the structure, enabling complex cross-element computations.

### 10.3. Trade-offs

- Adding a new element type requires updating every existing visitor — the pattern is closed for new types.
- Double dispatch adds indirection that can be confusing for developers unfamiliar with the pattern.
- Visitors may need access to element internals, which can weaken encapsulation if elements must expose state they would otherwise keep private.

### 10.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 11. Interpreter

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

### 11.1. Domain Context

Primarily relevant in language tooling, DSLs, rule engines, and compilers. Rarely encountered in general application code that doesn't need to parse or evaluate expressions.

### 11.2. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — algebraic data types for the AST and recursive functions for interpretation; pattern matching replaces the class hierarchy. |
| Data-Oriented | **Uncommon** — expression trees are pointer-heavy and recursive, which conflicts with flat, cache-friendly data layouts. |
| OOP | **Natural fit** — each grammar rule maps to a class with a polymorphic `interpret` method. |
| Procedural | **Workable** — tagged unions with a switch-based evaluator achieve the same result without a class hierarchy. |
| Reactive | **Uncommon** — expression evaluation is typically a synchronous tree walk, not a stream-based process. |

### 11.3. Benefits

- Grammar is explicit in the class structure — each rule is a self-contained, testable class.
- Easy to extend with new expressions by adding new classes without modifying existing ones.
- Expression trees can be composed, reused, and transformed programmatically.

### 11.4. Trade-offs

- One class per grammar rule leads to class explosion for complex grammars.
- Recursive interpretation can be slow for large expression trees compared to compiled or bytecode-based evaluation.
- Building the expression tree typically requires a separate parser, adding complexity.

### 11.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 12. Null Object

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

### 12.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Adapts well** — `Option`/`Maybe` with `map`/`getOrElse` or identity functions serve the same purpose; the pattern is implicit in monadic handling. |
| Data-Oriented | **Workable** — default-valued components or sentinel rows in tables replace the concept of a null entity. |
| OOP | **Natural fit** — a concrete class implementing the interface with no-op methods is the canonical form. |
| Procedural | **Workable** — a no-op function or struct with zeroed fields serves as the null stand-in. |
| Reactive | **Adapts well** — `EMPTY` observables or no-op subscribers represent the absence of a real producer/consumer. |

### 12.2. Benefits

- Eliminates pervasive null checks — client code calls methods unconditionally, reducing boilerplate and NullPointerException risk.
- Simplifies client logic by guaranteeing that every collaborator is a valid, callable object.
- Null objects are trivially testable and can serve as safe defaults in dependency injection.

### 12.3. Trade-offs

- Silent no-ops can mask configuration errors — if a real dependency was expected but a null object was supplied, failures go undetected.
- Every interface change requires updating the null object alongside the real implementations.
- Can obscure program flow: debugging is harder when "nothing happens" without any explicit indication of why.

### 12.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 13. Dependency Injection

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

### 13.1. Paradigm Fit

| Paradigm | Compatibility |
|----------|---------------|
| FP | **Natural fit** — passing dependencies as function arguments (or via reader monads / partial application) is idiomatic; every higher-order function is a form of DI. |
| Data-Oriented | **Adapts well** — systems receive their data sources and configuration externally; the ECS world object is itself an injected context. |
| OOP | **Natural fit** — constructor injection with interfaces is the canonical form; IoC containers automate the wiring. |
| Procedural | **Workable** — passing struct pointers or function pointers to procedures achieves the same decoupling. |
| Reactive | **Adapts well** — services and data sources are injected into stream pipelines as external dependencies; Angular's DI system is a prominent example. |

### 13.2. Benefits

- Explicit dependency graph — every dependency is visible in the constructor, eliminating hidden coupling.
- Testability — injecting mocks, stubs, or fakes replaces real dependencies without modifying the class under test.
- Flexibility — swapping implementations (e.g., switching payment gateways, swapping a cache backend) requires changing only the composition root.

### 13.3. Trade-offs

- Constructor parameter lists can grow long in deeply dependent classes, signaling a need to refactor responsibilities.
- Indirection increases — the reader must trace through the composition root or container configuration to understand which concrete types are wired.
- IoC containers add framework complexity, magic (auto-resolution, convention-based binding), and potential runtime errors if bindings are misconfigured.

### 13.4. Examples

#### Rust

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

#### C\#

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

#### Python

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

