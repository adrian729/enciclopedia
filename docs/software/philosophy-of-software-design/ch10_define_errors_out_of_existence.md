# Ch 10: Define Errors Out Of Existence

## Table of Contents

- [1. Why Exceptions Add Complexity](#1-why-exceptions-add-complexity)
- [2. Too Many Exceptions](#2-too-many-exceptions)
- [3. Define Errors Out of Existence](#3-define-errors-out-of-existence)
- [4. Mask Exceptions](#4-mask-exceptions)
- [5. Exception Aggregation](#5-exception-aggregation)
- [6. Just Crash](#6-just-crash)
- [7. Design Special Cases Out of Existence](#7-design-special-cases-out-of-existence)
- [8. Taking It Too Far](#8-taking-it-too-far)

## 1. Why Exceptions Add Complexity

- **Exceptions are one of the worst sources of complexity** — code that handles special conditions is inherently harder to write than normal-case code, and developers often define exceptions without considering how they will be handled
- **Two hard recovery paths** — when an exception occurs you can either (a) move forward and complete the work despite the error, or (b) abort and unwind partial state changes; both are complicated
- **Exceptions breed exceptions** — recovery actions can trigger secondary exceptions (e.g., resending a "lost" packet that was merely delayed creates duplicates the peer must handle), risking an unending cascade
- **Verbose language support** — try/catch boilerplate often exceeds the normal-case code, obscuring the relationship between error handlers and the code that triggers them
- **Hard to test** — exceptional conditions (I/O errors, network failures) are difficult to reproduce; exception-handling code rarely executes, so bugs hide in it for a long time. Over 90% of catastrophic failures in distributed data-intensive systems were caused by incorrect error handling

## 2. Too Many Exceptions

- **"More errors detected = better" is a trap** — over-defensive coding that throws an exception for anything suspicious creates a proliferation of unnecessary exceptions, each one adding complexity
- **Tcl `unset` example** — Ousterhout defined `unset` to throw an error if the variable doesn't exist; in practice, callers used `unset` to clean up state that might or might not exist, forcing them to wrap every call in a `catch` to ignore the error
- **Throwing is easy, handling is hard** — the complexity cost of an exception lives in the handler, not the throw site; every exception you add potentially propagates up several stack levels, affecting multiple callers' interfaces
- **Classes with lots of exceptions are shallower** — exceptions are part of the interface; more exceptions = more complex interface, less depth
- **Key goal** — reduce the number of places where exceptions must be handled; the rest of the chapter presents four techniques to achieve this

## 3. Define Errors Out of Existence

- **Redefine the operation so the error condition can't occur** — change the API semantics so that what was previously an error is now the normal case
- **Tcl `unset` fix** — redefine `unset` as "ensure the variable no longer exists" instead of "delete the variable"; if the variable is already gone, the work is already done, no error needed
- **Windows vs. Unix file deletion** — Windows throws an error when deleting a file that's open; Unix marks the file for deletion, returns success, and frees the data only after all processes close it. Unix defines away two errors: "file is in use" and "open file was deleted under you"
- **Java `substring`** — throws `IndexOutOfBoundsException` for out-of-range indices, forcing callers to clamp values manually (5-10 lines for what should be 1). A better API: "return the characters (if any) in the given range" handles all edge cases automatically and makes the method deeper. Python slicing already works this way

> **Design Principle: Define Errors Out of Existence** — the best way to eliminate exception handling complexity is to define your APIs so that there are no exceptions to handle. Redefine the semantics so that the normal behavior covers all situations.

- **"But errors catch bugs"** — the error-ful approach may catch some bugs, but it adds complexity that causes other bugs (forgotten checks, boilerplate errors). Overall, the best way to reduce bugs is to make software simpler

## 4. Mask Exceptions

- **Exception masking** — detect and handle an exceptional condition at a low level so higher layers never see it; this is an example of pulling complexity downward
- **TCP example** — TCP masks packet loss by resending lost packets internally; callers see a reliable byte stream and are unaware of drops
- **NFS example** — when the file server is unresponsive, NFS clients silently retry rather than reporting errors to applications. Alternatives (let applications retry, or abort) are worse: retrying is better done once in the NFS layer than in every file-system call in every application, and aborting would cascade into a collapse of the user's working environment
- **Masking works best at low levels** — the low-level method is typically a library used by many callers; masking there eliminates handlers in all of them
- **Result** — deeper classes (simpler interface with fewer exceptions, more functionality via the masking code)

## 5. Exception Aggregation

- **Exception aggregation** — handle many exceptions with a single piece of code instead of writing separate handlers for each one
- **Web server example** — instead of wrapping each `getParameter` call in its own try/catch, let `NoSuchParameter` exceptions propagate up to a single top-level dispatch handler that generates an error response. This handler can also catch other request-level errors (bad syntax, permission denied) since they all result in the same action: send an error response with the message carried in the exception
- **General pattern** — define an exception class that aborts the current request, cleans up state, and continues with the next request; catch it in one place near the top of the request loop. Different subclasses capture different conditions, but one handler covers them all
- **RAMCloud crash recovery** — rather than building separate recovery mechanisms for each error type (corrupted object, lost replica, etc.), RAMCloud "promotes" small errors into server crashes and reuses the single crash-recovery mechanism. This reduces code, and the shared path gets exercised more often, flushing out bugs faster
- **Aggregation works best when exceptions propagate far** — the more stack levels the exception crosses, the more exception sites one handler covers
- **Contrast with masking** — masking catches exceptions low in the stack (near the source); aggregation catches them high (near the top). Both position the handler where it can eliminate the most individual handlers

## 6. Just Crash

- **Some errors aren't worth handling** — for errors that are difficult/impossible to recover from and occur rarely, the simplest response is to print diagnostic information and abort
- **Out-of-memory** — `malloc` returning `NULL` forces every caller to check; most can't do anything useful anyway (if there were freeable memory, it would have been freed already). Better: define a `ckalloc` wrapper that aborts on failure, or rely on C++/Java `new` throwing an exception that should not be caught
- **Other crash-worthy errors** — disk hard errors on open files, failed socket opens, internal data-structure inconsistencies (likely bugs). These are rare enough that aborting doesn't meaningfully affect usability
- **Context matters** — a replicated storage system cannot crash on I/O errors because recovering lost data is its core value proposition; the extra recovery complexity is justified there

## 7. Design Special Cases Out of Existence

- **Same principle extends beyond exceptions** — special cases of any kind (extra `if` statements, state flags) add complexity and breed bugs
- **Text editor selection example** — students introduced a boolean for "selection exists" and added checks throughout the code. Better: the selection always exists but can be empty (start == end). Copying an empty selection inserts 0 bytes; deleting an empty selection regenerates the original line. No special-case code needed
- **Interface vs. implementation** — "no selection" makes sense in the user's mental model, but the internal representation doesn't have to mirror it. An always-present-but-sometimes-empty selection is a simpler implementation

## 8. Taking It Too Far

- **Don't mask exceptions the caller needs** — defining away or masking errors only makes sense when the exception information isn't needed outside the module
- **Counter-example** — a networking module that silently swallowed all network errors made it impossible for applications to detect lost messages or failed peers; those errors were essential for building robust applications
- **The balance** — things that are not important should be hidden (the more the better); things that are important must be exposed, even though they add complexity to the interface
