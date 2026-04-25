# Ch 5: Information Hiding (and Leakage)

## Table of Contents

- [1. Information Hiding](#1-information-hiding)
- [2. Information Leakage](#2-information-leakage)
- [3. Temporal Decomposition](#3-temporal-decomposition)
- [4. HTTP Server Examples](#4-http-server-examples)
  - [4.1. Too Many Classes](#41-too-many-classes)
  - [4.2. Parameter Handling](#42-parameter-handling)
  - [4.3. Defaults in Responses](#43-defaults-in-responses)
- [5. Information Hiding Within a Class](#5-information-hiding-within-a-class)
- [6. Taking It Too Far](#6-taking-it-too-far)

## 1. Information Hiding

- **Information hiding** — the most important technique for creating deep modules (first described by David Parnas). Each module encapsulates design decisions in its implementation, keeping them invisible to other modules
- **What gets hidden** — data structures, algorithms, lower-level details (e.g., page sizes), and higher-level assumptions (e.g., "most files are small"). Anything related to *how* a mechanism works
- **Two benefits** — (1) simplifies the interface, reducing cognitive load for users of the module; (2) makes the system easier to evolve, since hidden details can change without affecting other modules
- **Private is not the same as hidden** — declaring variables `private` prevents direct access, but exposing them through getters and setters leaks the same information. True information hiding means callers don't need to know about the data at all
- **Partial hiding has value** — if a feature is only needed by a few callers and is accessed through separate methods not visible in the common API, it creates fewer dependencies than information visible to every user

## 2. Information Leakage

- **Information leakage** — a design decision reflected in multiple modules, creating a dependency. Any change to that decision forces changes in all involved modules
- **Interface leakage** — when information appears in a module's interface, it is leaked by definition. Simpler interfaces correlate with better information hiding
- **Back-door leakage** — two modules share knowledge of the same design decision (e.g., a file format) even though neither exposes it in its interface. This is more pernicious because it isn't obvious
- **Remedies** — (1) merge small, closely-tied classes into one, or (2) extract the shared knowledge into a new class with a simple abstraction. The second approach only helps if the new class truly hides the details behind its interface; otherwise you've just traded back-door leakage for interface leakage

> **Red Flag: Information Leakage** — the same knowledge is used in multiple places, such as two different classes that both understand the format of a particular type of file.

## 3. Temporal Decomposition

- **Temporal decomposition** — structuring modules around the time order of operations (e.g., one class to read a file, another to modify it, a third to write it). This is a common cause of information leakage
- **Why it fails** — design decisions (like a file format) often span multiple phases. Splitting by time forces the same knowledge into multiple modules
- **Fix** — combine the mechanisms that share knowledge into a single module. A class that handles both reading and writing a file format keeps that format knowledge in one place

> **Red Flag: Temporal Decomposition** — execution order is reflected in code structure; operations at different times live in different methods or classes. If the same knowledge is used at different points in execution, it gets encoded in multiple places, resulting in information leakage.

- **Design by knowledge, not by time** — when creating modules, focus on what knowledge is needed to perform each task, not the order in which tasks occur

## 4. HTTP Server Examples

### 4.1. Too Many Classes

- **Problem** — students split HTTP request handling into separate classes for reading and parsing. Since you can't read a request without parsing headers (e.g., `Content-Length` determines body length), both classes needed knowledge of the HTTP format
- **Result** — duplicated parsing code, information leakage, and a more complex caller interface (two methods in two classes, called in a specific order)
- **Fix** — merge into a single class that reads and parses in one step. This isolates format knowledge and provides a simpler interface (one method call)
- **General principle** — information hiding can often be improved by making a class slightly larger, either to consolidate related knowledge or to raise the interface level (one method for the whole operation instead of separate methods for each step)

### 4.2. Parameter Handling

- **Good decisions** — students merged URL-line and body parameters into a single collection (callers don't care where parameters came from) and decoded URL encoding internally (callers receive clean values like `"What a cute baby!"` instead of `"What+a+cute+baby%21"`)
- **Shallow mistake** — returning the internal `Map<String, String>` via `getParams()`. This exposes the storage representation, forces callers to do a second lookup, and risks accidental mutation of internal state
- **Deeper alternative** — `getParameter(String name)` and `getIntParameter(String name)`. These hide the internal representation, provide a simpler one-step API, and handle type conversion so callers don't need to do it themselves

### 4.3. Defaults in Responses

- **Good defaults reduce interface complexity** — HTTP response version should be set automatically (it must match the request version, which the library already knows). The `Date` header should default to the current time
- **Defaults as partial information hiding** — in the common case, callers don't even need to know the defaulted item exists. For rare cases, provide a method to override
- **"Do the right thing" without being asked** — the best features are the ones users get without knowing they exist. Java's unbuffered-by-default I/O is a counterexample: buffering is so universally needed that requiring it explicitly is a design flaw

> **Red Flag: Overexposure** — if the API for a commonly used feature forces users to learn about other features that are rarely used, this increases cognitive load on users who don't need the rarely used features.

## 5. Information Hiding Within a Class

- **Applies at every level** — information hiding is not just for public APIs. Design private methods so each one encapsulates some capability and hides it from the rest of the class
- **Minimize variable reach** — reduce the number of places each instance variable is used. Fewer access points means fewer intra-class dependencies and less internal complexity

## 6. Taking It Too Far

- **Don't hide what callers need** — if information is genuinely required outside a module (e.g., configuration parameters that affect performance), it must be exposed in the interface
- **Prefer auto-configuration** — if a module can determine the right settings on its own, that is better than exposing configuration parameters. But when external input is truly necessary, hiding it only creates obscurity
