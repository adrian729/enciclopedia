# Design Patterns

## Table of Contents

- [1. Creational](#1-creational)
- [2. Structural](#2-structural)
- [3. Behavioral](#3-behavioral)
- [4. Architectural](#4-architectural)

## 1. Creational

Creational patterns abstract the instantiation process, making systems independent of how their objects are created, composed, and represented.

| Pattern | When to Use |
|---------|-------------|
| [Singleton](software/design_patterns/creational?id=1-singleton) | A shared resource needs exactly one instance with global access. |
| [Builder](software/design_patterns/creational?id=2-builder) | Constructing complex objects with many optional or ordered parameters. |
| [Factory](software/design_patterns/creational?id=3-factory) | Creating objects without specifying the exact class; letting subclasses decide. |
| [Abstract Factory](software/design_patterns/creational?id=4-abstract-factory) | Creating families of related objects without specifying their concrete classes. |
| [Prototype](software/design_patterns/creational?id=5-prototype) | Creating new objects by cloning an existing instance instead of constructing from scratch. |
| [Object Pool](software/design_patterns/creational?id=6-object-pool) | Reusing expensive-to-create objects instead of repeated creation and destruction. |

## 2. Structural

Structural patterns deal with the composition of classes and objects, using inheritance and composition to form larger structures while keeping them flexible and efficient.

| Pattern | When to Use |
|---------|-------------|
| [Facade](software/design_patterns/structural?id=1-facade) | Simplifying access to a complex subsystem through one unified entry point. |
| [Adapter](software/design_patterns/structural?id=2-adapter) | Making an existing class work with an interface it wasn't designed for. |
| [Decorator](software/design_patterns/structural?id=3-decorator) | Dynamically adding behavior to an object without modifying its class. |
| [Proxy](software/design_patterns/structural?id=4-proxy) | Controlling access to another object for lazy loading, access control, or caching. |
| [Composite](software/design_patterns/structural?id=5-composite) | Treating individual objects and groups uniformly in tree structures. |
| [Bridge](software/design_patterns/structural?id=6-bridge) | Separating abstraction from implementation so both vary independently. |
| [Flyweight](software/design_patterns/structural?id=7-flyweight) | Sharing common state across many fine-grained objects to save memory. |

## 3. Behavioral

Behavioral patterns focus on communication and responsibility between objects, defining how they interact and distribute work.

| Pattern | When to Use |
|---------|-------------|
| [Strategy](software/design_patterns/behavioral?id=1-strategy) | Selecting between interchangeable algorithms at runtime without conditionals. |
| [Observer](software/design_patterns/behavioral?id=2-observer) | Notifying multiple objects automatically when one object's state changes. |
| [Command](software/design_patterns/behavioral?id=3-command) | Encapsulating requests as objects for undo/redo, queuing, and logging. |
| [State](software/design_patterns/behavioral?id=4-state) | Letting an object change behavior when its internal state changes. |
| [Template Method](software/design_patterns/behavioral?id=5-template-method) | Defining an algorithm skeleton with customizable steps in subclasses. |
| [Iterator](software/design_patterns/behavioral?id=6-iterator) | Traversing a collection without exposing its internal representation. |
| [Chain of Responsibility](software/design_patterns/behavioral?id=7-chain-of-responsibility) | Passing a request along a handler chain until one processes it. |
| [Mediator](software/design_patterns/behavioral?id=8-mediator) | Centralizing complex inter-object communication through a coordinator. |
| [Memento](software/design_patterns/behavioral?id=9-memento) | Capturing and restoring an object's state without violating encapsulation. |
| [Visitor](software/design_patterns/behavioral?id=10-visitor) | Adding operations to a class hierarchy without modifying it. |
| [Interpreter](software/design_patterns/behavioral?id=11-interpreter) | Defining a grammar and interpreter for a language. |
| [Null Object](software/design_patterns/behavioral?id=12-null-object) | Providing a do-nothing default object to eliminate null checks. |
| [Dependency Injection](software/design_patterns/behavioral?id=13-dependency-injection) | Externally supplying dependencies instead of creating them internally. |

## 4. Architectural

Architectural patterns address system-level concerns — how components, services, and data flows are organized across application boundaries. Unlike creational, structural, and behavioral patterns which operate at the object level, architectural patterns shape the overall topology and communication style of a system.

| Pattern | When to Use |
|---------|-------------|
| [Repository](software/design_patterns/architectural?id=1-repository) | Abstracting data access behind a collection-like interface. |
| [Unit of Work](software/design_patterns/architectural?id=2-unit-of-work) | Coordinating multiple data changes as a single atomic transaction. |
| [CQRS](software/design_patterns/architectural?id=3-cqrs) | Optimizing reads and writes independently in systems with asymmetric loads. |
| [Event Sourcing](software/design_patterns/architectural?id=4-event-sourcing) | Storing state as an append-only sequence of domain events for audit and replay. |
| [Circuit Breaker](software/design_patterns/architectural?id=5-circuit-breaker) | Preventing cascading failures by short-circuiting calls to unhealthy services. |
| [Saga](software/design_patterns/architectural?id=6-saga) | Managing distributed transactions across multiple services with compensating rollbacks. |
| [Specification](software/design_patterns/architectural?id=7-specification) | Composing reusable business rules as combinable boolean predicates. |
