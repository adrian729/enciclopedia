# Ch 23: Threads and Locks

## Table of Contents

- [1. Why threads appear in interviews](#1-why-threads-appear-in-interviews)
- [2. Threads in Java](#2-threads-in-java)
- [3. Runnable vs. Thread](#3-runnable-vs-thread)
- [4. Synchronization and locks](#4-synchronization-and-locks)
- [5. Synchronized methods](#5-synchronized-methods)
- [6. Synchronized blocks](#6-synchronized-blocks)
- [7. Locks](#7-locks)
- [8. Deadlocks and deadlock prevention](#8-deadlocks-and-deadlock-prevention)

## 1. Why threads appear in interviews

- **Implementing threaded algorithms is uncommon** at Microsoft, Google, or Amazon interviews unless the team specifically needs that skill.
- **Understanding threads and deadlocks is common** — interviewers at any company may probe general thread knowledge, especially deadlocks.

## 2. Threads in Java

- **Every thread is a `java.lang.Thread` object** — uniquely controls one thread of execution.
- **Main thread** — automatically created to run `main()` when a standalone application starts.
- **Two ways to implement a thread** — implementing `java.lang.Runnable`, or extending `java.lang.Thread`.

### 2.1. Implementing the Runnable interface

```java
public interface Runnable {
    void run();
}
```

Three steps to create and use a thread:

1. **Create a class that implements `Runnable`** — its instance is a `Runnable` object.
2. **Construct a `Thread`** — pass the `Runnable` as the constructor argument.
3. **Invoke `start()`** on the `Thread` object.

### 2.2. Extending the Thread class

- **Override `run()`** — subclass typically overrides `run()` and may call the `Thread` constructor explicitly.
- **Call `start()` directly on the subclass instance** — no wrapping `Thread` object needed.

## 3. Runnable vs. Thread

Two reasons **implementing `Runnable` is often preferable** to extending `Thread`:

- **Single inheritance** — Java does not support multiple inheritance. Extending `Thread` blocks the class from extending any other class; implementing `Runnable` leaves inheritance free.
- **Avoid inheriting `Thread` overhead** — if the class only needs to be runnable, inheriting the full `Thread` machinery is excessive.

## 4. Synchronization and locks

- **Threads in a process share memory** — valuable for data sharing but opens the door to conflicts when two threads modify the same resource simultaneously.
- **Java's `synchronized` keyword and the `lock`** — form the basis for controlling access to shared resources.

## 5. Synchronized methods

- **`synchronized` restricts simultaneous execution on the same object** — can be applied to methods or code blocks.
- **Per-instance locking** — two threads calling a `synchronized` method on *different* `MyObject` instances can run concurrently; on the *same* instance one must wait.
- **Static `synchronized` methods synchronize on the class lock** — two threads cannot simultaneously execute any `static synchronized` methods of the same class, even distinct ones (e.g., `foo` and `bar`).

## 6. Synchronized blocks

```java
public void foo(String name) {
    synchronized(this) {
        ...
    }
}
```

- **Behaves like a synchronized method** — only one thread per `MyObject` instance can execute code inside the block at a time.
- **Finer granularity** — lets you synchronize a subset of a method rather than the whole method.

## 7. Locks

- **Lock (or monitor)** — synchronizes access to a shared resource by associating the resource with the lock. A thread must first acquire the lock; at most one thread holds it at a time.
- **Use case** — a resource is accessed from multiple places but must only be touched by one thread at a time (e.g., an ATM's shared `balance` accessed by `withdraw` and `deposit`).
- **Typical pattern** — `lock.lock()` before the critical section, work inside `try`, `lock.unlock()` after. `ReentrantLock` is the common implementation.

## 8. Deadlocks and deadlock prevention

- **Deadlock** — thread A waits for a lock held by thread B while B waits for a lock held by A (or an equivalent cycle across more threads). Both wait forever.

All **four conditions** must hold for a deadlock to occur:

| # | Condition | Meaning |
|---|-----------|---------|
| 1 | **Mutual Exclusion** | Only one process can access a resource at a time (or access is limited / the resource has limited quantity). |
| 2 | **Hold and Wait** | A process holding resources may request more without releasing what it has. |
| 3 | **No Preemption** | One process cannot forcibly take a resource from another. |
| 4 | **Circular Wait** | Two or more processes form a circular chain, each waiting on the next for a resource. |

- **Prevention removes any one condition** — but most are hard to drop. Condition 1 is often non-negotiable (printers, exclusive resources).
- **Most algorithms target circular wait (#4)** — e.g., imposing a global ordering on lock acquisition so cycles cannot form.
