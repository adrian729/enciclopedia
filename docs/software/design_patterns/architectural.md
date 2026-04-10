# Architectural

## Table of Contents

- [1. Repository](#1-repository)
  - [1.1. Domain Context](#11-domain-context)
  - [1.2. System Fit](#12-system-fit)
  - [1.3. Benefits](#13-benefits)
  - [1.4. Trade-offs](#14-trade-offs)
  - [1.5. Examples](#15-examples)
- [2. Unit of Work](#2-unit-of-work)
  - [2.1. Domain Context](#21-domain-context)
  - [2.2. System Fit](#22-system-fit)
  - [2.3. Benefits](#23-benefits)
  - [2.4. Trade-offs](#24-trade-offs)
  - [2.5. Examples](#25-examples)
- [3. CQRS](#3-cqrs)
  - [3.1. Domain Context](#31-domain-context)
  - [3.2. System Fit](#32-system-fit)
  - [3.3. Benefits](#33-benefits)
  - [3.4. Trade-offs](#34-trade-offs)
  - [3.5. Examples](#35-examples)
- [4. Event Sourcing](#4-event-sourcing)
  - [4.1. Domain Context](#41-domain-context)
  - [4.2. System Fit](#42-system-fit)
  - [4.3. Benefits](#43-benefits)
  - [4.4. Trade-offs](#44-trade-offs)
  - [4.5. Examples](#45-examples)
- [5. Circuit Breaker](#5-circuit-breaker)
  - [5.1. Domain Context](#51-domain-context)
  - [5.2. System Fit](#52-system-fit)
  - [5.3. Benefits](#53-benefits)
  - [5.4. Trade-offs](#54-trade-offs)
  - [5.5. Examples](#55-examples)
- [6. Saga](#6-saga)
  - [6.1. Domain Context](#61-domain-context)
  - [6.2. System Fit](#62-system-fit)
  - [6.3. Benefits](#63-benefits)
  - [6.4. Trade-offs](#64-trade-offs)
  - [6.5. Examples](#65-examples)
- [7. Specification](#7-specification)
  - [7.1. Domain Context](#71-domain-context)
  - [7.2. System Fit](#72-system-fit)
  - [7.3. Benefits](#73-benefits)
  - [7.4. Trade-offs](#74-trade-offs)
  - [7.5. Examples](#75-examples)

Architectural patterns address system-level concerns — how components, services, and data flows are organized across application boundaries. Unlike creational, structural, and behavioral patterns which operate at the object level, architectural patterns shape the overall topology and communication style of a system.

| Pattern | When to Use |
|---------|-------------|
| [Repository](#1-repository) | Abstracting data access behind a collection-like interface. |
| [Unit of Work](#2-unit-of-work) | Coordinating multiple data changes as a single atomic transaction. |
| [CQRS](#3-cqrs) | Optimizing reads and writes independently in systems with asymmetric loads. |
| [Event Sourcing](#4-event-sourcing) | Storing state as an append-only sequence of domain events for audit and replay. |
| [Circuit Breaker](#5-circuit-breaker) | Preventing cascading failures by short-circuiting calls to unhealthy services. |
| [Saga](#6-saga) | Managing distributed transactions across multiple services with compensating rollbacks. |
| [Specification](#7-specification) | Composing reusable business rules as combinable boolean predicates. |

## 1. Repository

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

### 1.1. Domain Context

Primarily relevant in applications with persistent data storage (databases, file systems, external APIs). Rarely encountered in stateless utilities, CLI tools, or applications without a data layer.

### 1.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — centralizes data access behind clean interfaces within a single deployable. |
| Microservices | **Natural fit** — each service owns its repository, enforcing bounded-context data isolation. |
| Serverless | **Adapts well** — repository instances are short-lived but still decouple handler logic from storage. |
| Event-Driven | **Adapts well** — repositories persist aggregates while events flow through separate channels. |

### 1.3. Benefits

- Decouples domain logic from storage technology — switching from PostgreSQL to DynamoDB requires only a new concrete repository.
- Enables unit testing of domain logic with in-memory or mock repositories, eliminating database dependencies in tests.
- Centralizes data access logic, making query optimizations and caching strategies easier to apply consistently.

### 1.4. Trade-offs

- Adds an abstraction layer that may be unnecessary for simple CRUD applications with no domain logic.
- Repository interfaces can bloat with query methods; discipline is needed to keep them focused on aggregate roots.
- Leaky abstractions emerge when storage-specific concepts (pagination cursors, query hints) bleed into the interface.

### 1.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 2. Unit of Work

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

### 2.1. Domain Context

Primarily relevant in applications performing multiple related data modifications that must succeed or fail together. Uncommon in read-heavy or single-write applications where atomic batching adds no value.

### 2.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — wraps a single database transaction spanning multiple repositories. |
| Microservices | **Workable** — limited to each service's local database; cross-service atomicity requires Saga instead. |
| Serverless | **Workable** — short function lifetimes suit small units of work, but connection pooling needs care. |
| Event-Driven | **Adapts well** — commit can atomically persist changes and publish domain events (transactional outbox). |

### 2.3. Benefits

- Guarantees atomicity — all changes within a business operation succeed or fail together.
- Reduces database round-trips by batching inserts, updates, and deletes into a single flush.
- Centralizes transaction management, removing explicit begin/commit/rollback calls from service code.

### 2.4. Trade-offs

- Adds complexity to track entity states (new, dirty, removed) and detect changes.
- Long-lived units of work can hold database locks or accumulate large change sets, increasing conflict risk.
- Implicit change tracking can surprise developers when modifications are flushed at unexpected times.

### 2.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 3. CQRS

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

### 3.1. Domain Context

Primarily relevant in systems with asymmetric read/write loads or complex domain models where a single model cannot efficiently serve both reads and writes. Overkill for simple CRUD applications with balanced read/write patterns and straightforward data shapes.

### 3.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Adapts well** — separate read/write paths within a single deployable, often sharing the same database. |
| Microservices | **Natural fit** — read and write sides can be independent services scaled separately. |
| Serverless | **Adapts well** — command and query handlers map naturally to separate functions with independent scaling. |
| Event-Driven | **Natural fit** — events bridge the write and read models; projections consume events to build read stores. |

### 3.3. Benefits

- Independent optimization — the write model can be normalized for consistency while the read model is denormalized for performance.
- Read and write workloads scale independently, each provisioned for its actual load.
- Simplifies complex domains by letting each side model only the concerns it handles.

### 3.4. Trade-offs

- Eventual consistency between write and read models requires the application and users to tolerate stale reads.
- Doubles the number of models, handlers, and synchronization code — significant structural overhead.
- Debugging requires tracing through command handlers, events, and projections rather than a single code path.

### 3.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 4. Event Sourcing

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

### 4.1. Domain Context

Primarily relevant in audit-heavy systems, financial applications, and domains requiring temporal queries or event replay. Adds significant complexity to simple CRUD applications where only current state matters.

### 4.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Workable** — event store and projections can coexist in one process, but replay and projection logic add complexity. |
| Microservices | **Adapts well** — each service owns its event stream; events serve as the integration contract between services. |
| Serverless | **Workable** — functions can append events and trigger projections, but replay across cold starts needs care. |
| Event-Driven | **Natural fit** — events are the native communication primitive; the event store is the system's source of truth. |

### 4.3. Benefits

- Complete audit trail by construction — every state change is recorded as an immutable event.
- Temporal queries are trivial: replay events up to any point in time to reconstruct past states.
- Enables bug fixes by correcting projection logic and reprocessing the event stream, without losing data.

### 4.4. Trade-offs

- Event schema evolution is hard — renaming or restructuring events requires versioning and upcasting strategies.
- Rebuilding state from long event streams is slow without snapshotting, adding implementation complexity.
- Fundamentally different mental model from CRUD; steep learning curve for teams unfamiliar with the approach.

### 4.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 5. Circuit Breaker

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

### 5.1. Domain Context

Primarily relevant in distributed systems and microservice architectures where remote calls can fail or hang. Rarely encountered in single-process applications without external dependencies.

### 5.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Uncommon** — useful only if the monolith calls external services; internal calls don't need circuit breaking. |
| Microservices | **Natural fit** — essential for resilient inter-service communication. |
| Serverless | **Workable** — useful for external API calls, but per-invocation state requires shared storage for the breaker state. |
| Event-Driven | **Adapts well** — protects event consumers from unhealthy downstream processors or external services. |

### 5.3. Benefits

- Prevents cascading failures — a single unhealthy dependency cannot exhaust the caller's resources.
- Fail-fast behavior frees threads and connections immediately instead of blocking on doomed calls.
- Gives the failing service time to recover by stopping traffic during the open state.

### 5.4. Trade-offs

- Legitimate requests are rejected during the open state, even if the remote service has partially recovered.
- Tuning thresholds and timeouts requires production traffic analysis; poor defaults cause premature tripping or delayed detection.
- Adds state management complexity, especially when shared across multiple instances (distributed circuit breaker state).

### 5.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 6. Saga

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

### 6.1. Domain Context

Primarily relevant in distributed systems where a business process spans multiple services. Unnecessary in monolithic applications with single-database ACID transactions, where a simple Unit of Work suffices.

### 6.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Uncommon** — a single database transaction handles atomicity; sagas add needless complexity. |
| Microservices | **Natural fit** — the canonical solution for cross-service transactions without distributed locks. |
| Serverless | **Adapts well** — step functions or durable workflows (AWS Step Functions, Azure Durable Functions) implement the orchestrator. |
| Event-Driven | **Natural fit** — choreography sagas are event-driven by definition; events trigger steps and compensations. |

### 6.3. Benefits

- Achieves cross-service consistency without distributed locks or two-phase commit.
- Each service retains full autonomy over its local database and transactions.
- Compensating actions provide a structured rollback mechanism that handles partial failures gracefully.

### 6.4. Trade-offs

- Eventual consistency means intermediate states are visible to other operations during saga execution.
- Compensating actions must be idempotent and carefully designed — some operations (sending an email, charging a card) are difficult to "undo."
- Debugging failures across a multi-step, multi-service saga is significantly harder than debugging a single transaction.

### 6.5. Examples

#### Rust

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

#### C\#

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

#### Python

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

## 7. Specification

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

### 7.1. Domain Context

Primarily relevant in domain-driven design and business rule engines where complex filtering, validation, or selection logic must be composed dynamically. Less common in applications with simple, static query logic that a single predicate or SQL clause can express.

### 7.2. System Fit

| Architecture | Compatibility |
|--------------|---------------|
| Monolith | **Natural fit** — specifications compose queries and validation rules within a single domain layer. |
| Microservices | **Adapts well** — each service defines specifications for its bounded context; serializable specs can cross service boundaries. |
| Serverless | **Workable** — specifications work within function logic but the composable class hierarchy may be heavier than inline predicates. |
| Event-Driven | **Adapts well** — specifications filter or route events, determining which consumers should process which messages. |

### 7.3. Benefits

- Business rules are reusable, testable units — each specification can be validated independently.
- Complex predicates are built by composition rather than modification, adhering to the Open/Closed Principle.
- The same specification can serve multiple purposes: repository filtering, entity validation, and UI display logic.

### 7.4. Trade-offs

- Class proliferation — each business rule becomes its own specification class, which is verbose for simple predicates.
- Translating in-memory specifications into efficient database queries (e.g., SQL WHERE clauses) requires additional infrastructure.
- Deeply nested composite specifications can be hard to debug when `is_satisfied_by` returns an unexpected result.

### 7.5. Examples

#### Rust

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

#### C\#

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

#### Python

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
