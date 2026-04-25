# Ch 11: Bytecode

## Table of Contents

- [1. The Problem](#1-the-problem)
- [2. The Pattern](#2-the-pattern)
- [3. When to Use It](#3-when-to-use-it)
- [4. Building the VM](#4-building-the-vm)
- [5. Design Decisions](#5-design-decisions)
- [6. Keep in Mind](#6-keep-in-mind)

## 1. The Problem

- **Games need lots of tweakable behavior** — spells, AI, scripts all need frequent iteration, shipping patches, and sometimes modding. Encoding them in C++ means every change requires an engineer, a recompile, and a patch to the executable
- **Shipping hard-coded behavior is dangerous** — modders need the compiler and source, and a buggy mod can crash other players' machines. Behavior defined this way has full trust over the engine
- **The goal: behavior as data** — spells should live in separate files, loaded and "executed" by the engine, physically separate from the executable and safely sandboxed
- **Interpreter GoF is the obvious alternative, but too slow** — represent code as a tree of little expression objects (numbers, operators) that evaluate themselves recursively. Elegant, but a sprawling fractal of tiny objects: heavy memory use, pointer chasing murders the data cache, and virtual calls trash the instruction cache. Ruby used it for 15 years before switching to bytecode at 1.9
- **Machine code is the other extreme** — dense, linear, low-level, blazing fast. But letting users supply raw machine code is a security nightmare, and many platforms (consoles, iOS) forbid executing loaded or generated machine code at runtime
- **Bytecode is the compromise** — define a synthetic instruction set, ship an emulator (a **virtual machine**, or VM) for it. Dense and linear like machine code, but handled entirely by the game so it can be sandboxed

## 2. The Pattern

- **An instruction set defines the low-level operations** that can be performed
- **A series of instructions is encoded as a sequence of bytes**
- **A virtual machine executes these instructions one at a time**, using a **stack** for intermediate values
- **Complex high-level behavior is defined by combining instructions**
- **"Virtual machine" and "interpreter" are synonymous** in programming language circles — Nystrom uses "pattern" to disambiguate the GoF Interpreter

## 3. When to Use It

- **Use when you have a lot of behavior to define** and the engine's implementation language isn't a good fit because:
  - it's too low-level, making it tedious or error-prone
  - iteration takes too long (slow compile times, tooling friction)
  - it has too much trust — you need to sandbox the behavior from the rest of the codebase
- **Not for performance-critical code** — bytecode is slower than native. Don't use it inside your inner render loop
- **This is the most complex pattern in the book** — don't reach for it lightly

## 4. Building the VM

- **Start by designing an API** — what functions would spells call if written directly in C++? (`setHealth`, `playSound`, `spawnParticles`). The bytecode is a data-driven translation of that API
- **Each instruction is a byte** — a simple enum of opcodes. A spell is an array of these bytes — hence "bytecode". One byte is enough for the JVM and .NET CLR; it's enough for you
- **The interpreter is a loop over a switch statement** — read byte, dispatch to the right case, advance. "Bytecode and VMs" sound intimidating but amount to a stack, a loop, and a switch
- **Add parameters via a stack machine** — instructions pop their operands from an internal value stack and push results back. Forth, PostScript, and Factor expose this model directly to the user
- **A LITERAL instruction embeds its value in the byte stream** — the next byte after the opcode is read as a number and pushed onto the stack. That's how constants get in
- **Composition via a stack is surprisingly powerful** — with `GET_*`, `SET_*`, `LITERAL`, and arithmetic ops (`ADD`, `DIVIDE`, etc.), you can evaluate deeply nested expressions. The stack handles operator precedence implicitly — each "remember" is a push, each "recall" is a pop
- **Sandboxing falls out of the design** — the bytecode can only do what its instructions allow. Stack size is bounded, and execution time can be capped by counting instructions in the interpreter loop. Without loops, bytecode isn't Turing-complete, which is often a feature

## 5. Design Decisions

### 5.1. How do instructions access the stack?

| | Stack-based | Register-based |
|---|---|---|
| Instruction size | Small (often one byte) | Larger (Lua uses 32 bits) |
| Instruction count | More (explicit stack shuffling) | Fewer (one instruction does more) |
| Code generation | Simpler | Harder |
| Example | JVM, .NET, Wren | Lua 5.1+ |

- **Register-based VMs still have a stack** — the difference is instructions read inputs from arbitrary stack offsets encoded in the bytecode, rather than implicitly from the top
- **Recommendation: stack-based** — simpler to implement and simpler to generate code for. Lua's performance reputation depends on more than just register vs. stack

### 5.2. What instructions do you have?

- **External primitives** — reach out of the VM into the engine (play sound, spawn particles). Without these, the VM can only burn cycles
- **Internal primitives** — literals, arithmetic, comparison, stack juggling
- **Control flow** — a jump instruction just modifies the bytecode index. That's a goto, and all higher-level control flow builds on it
- **Abstraction / callable procedures** — add a second **return stack**. A "call" pushes the current index onto it and jumps; a "return" pops and jumps back

### 5.3. How are values represented?

| Representation | Pros | Cons |
|---|---|---|
| Single datatype | Simple, no type tagging | Can't handle multiple types without pain |
| Tagged variant (enum + union) | Runtime type checks, standard for dynamic languages | Extra memory per value |
| Untagged union | Compact, fast — used by statically typed langs and Forth | Unsafe; malicious bytecode can misinterpret |
| Interface / polymorphism | Open-ended, OOP-clean | Verbose, heap-allocated per value, virtual call cost |

- **Recommendation** — stick with one datatype if you can. Otherwise use a tagged variant. That's what nearly every language interpreter does
- **Statically typed bytecode is still unsafe** — malicious users can hand-craft bytecode bypassing your compiler. The JVM does bytecode verification on load for this reason

### 5.4. How is the bytecode generated?

- **You need a front-end** — authoring in raw bytecode defeats the purpose of moving to a higher level
- **Text-based language** — requires defining syntax (harder than it looks), writing a parser (easy; hand-rolled recursive descent or ANTLR/Bison), and handling syntax errors gracefully. Non-technical users tend to hate plaintext
- **Graphical authoring tool** — clicking, dragging, menus. Can prevent invalid programs by construction instead of reporting errors after the fact. Less portable across OSes due to UI framework choices
- **Error handling is critical** — treat user mistakes as part of the creative process, not a personality flaw. Features like undo help users be more creative

## 6. Keep in Mind

- **Little languages grow like vines** — everyone says "don't worry, it will be tiny", then it ad-hoc accretes into a full language with the architectural elegance of a shanty town. See: every templating language ever. Keep a short leash, or commit to building a real language deliberately
- **You'll miss your debugger** — stepping through the VM in a debugger shows you what the VM is doing, not what the bytecode is doing. Plan to build your own inspection tooling; if your game is moddable, that tooling ships
- **See also** — pairs naturally with the **Interpreter GoF pattern**: the tool that generates bytecode typically walks an internal tree of expression objects, emitting instructions as it recurses. Lua is the most widely used scripting language in games (register-based). Kismet is UnrealEd's graphical scripting. Wren is Nystrom's own stack-based bytecode interpreter
