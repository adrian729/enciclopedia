# Ch 20: C and C++

## Table of Contents

- [1. Framing](#1-framing)
- [2. Classes and inheritance](#2-classes-and-inheritance)
- [3. Constructors and destructors](#3-constructors-and-destructors)
- [4. Virtual functions](#4-virtual-functions)
- [5. Virtual destructors](#5-virtual-destructors)
- [6. Default values](#6-default-values)
- [7. Operator overloading](#7-operator-overloading)
- [8. Pointers and references](#8-pointers-and-references)
- [9. Templates](#9-templates)

## 1. Framing

- **A good interviewer won't demand a language you don't profess to know** — if C++ is on your resume, expect to code in it. Not remembering every API is usually fine; most interviewers don't care that much.
- **Study up on basic C++ syntax** so you can approach questions with ease.

## 2. Classes and inheritance

- **C++ classes have similar characteristics to other languages** — the chapter walks through core syntax via a `Person` base class and a `Student : public Person` subclass.
- **All data members and methods are private by default** in C++; introduce the `public:` keyword to change access.
- **Inheritance syntax** — `class Student : public Person { ... };` makes `Student` inherit from `Person`.
- **`#define`** creates a macro (e.g., `#define NAME_SIZE 50`) usable as a compile-time constant (e.g., for `char name[NAME_SIZE]`).
- **Allocated objects must be deleted** — after `Student * p = new Student();`, call `delete p;` to free memory.

## 3. Constructors and destructors

- **Constructor** — automatically called on object creation. If none is defined, the compiler generates a **Default Constructor**.
- **Custom constructor** — `Person(int a) { id = a; }` assigns via the body.
- **Initializer list** — `Person(int a) : id(a) { ... }` assigns the data member *before* the object is created and before the constructor body runs. Particularly useful for **constant fields that can only be assigned a value once**.
- **Destructor** — automatically called on object deletion; cleans up allocated resources. **Cannot take an argument** because destructors are not explicitly called.
- **Destructor syntax** — `~Person() { delete obj; // free any memory allocated within class }`.

## 4. Virtual functions

- **Static binding** — calling `p->aboutMe()` on `Person * p = new Student();` resolves at compile time to `Person::aboutMe`, printing `"I am a person."` rather than the `Student` version.
- **`virtual` keyword** — marking `aboutMe` as `virtual` in `Person` ensures the `Student` implementation is called through a `Person*`, enabling runtime polymorphism.
- **Pure virtual function** — `virtual bool addCourse(string s) = 0;` declares a method with no base-class implementation, forcing subclasses to provide one.
- **Abstract class** — defining a pure virtual function makes the class abstract; it **cannot be instantiated**.
- **When to use pure virtual** — when a common method (e.g., `addCourse`) only makes sense per-subclass (e.g., `Student` vs. `Teacher`), not on the base `Person`.

## 5. Virtual destructors

- **Problem** — with non-virtual destructors, `delete p;` on a `Person* p = new Student();` calls only `~Person()`, leaving `Student`-specific memory uncleaned.
- **Fix** — declare `virtual ~Person()`. Deletion then runs `~Student()` followed by `~Person()`, outputting:
  - `Deleting a student.`
  - `Deleting a person.`

## 6. Default values

- **Functions can specify default values** for parameters — `int func(int a, int b = 3) { ... }` allows `func(4)` or `func(4, 5)`.
- **Placement rule** — all default parameters must be on the **right side** of the function declaration, since there's no other way for the compiler to line up arguments.

## 7. Operator overloading

- **Purpose** — apply operators like `+` to objects that wouldn't otherwise support them (e.g., merging two `BookShelf` objects).
- **Syntax** — `BookShelf BookShelf::operator+(BookShelf &other) { ... }`.

## 8. Pointers and references

- **Pointer** — holds the address of a variable; can perform any operation the variable supports (access, modify).
- **Aliasing** — two pointers can equal each other (`int * q = p;`), so modifying through one changes the value seen through the other since they point to the same address.
- **Pointer size varies by architecture** — 32 bits on a 32-bit machine, 64 bits on a 64-bit machine. Interviewers commonly ask exactly how much space a data structure takes up, so this matters.
- **Reference** — another name (alias) for a pre-existing object; has no memory of its own. `int & b = a; b = 7;` also modifies `a`.
- **Free-standing reference** — can be created by binding to a fresh allocation, e.g., `int & b = 12;` (allocates storage for `12` and makes `b` refer to it).
- **Reference constraints** — unlike pointers, references **cannot be null** and **cannot be reassigned** to another piece of memory.
- **Pointer arithmetic** — `p++` skips ahead by `sizeof(int)` bytes (or the size of the pointed-to type), not one byte. For `int * p = new int[2]; p[0]=0; p[1]=1; p++; cout << *p;` outputs `1`.

## 9. Templates

- **Purpose** — reuse code to apply the same class to different data types (e.g., a list-like structure usable for any element type).
- **Syntax** — `template <class T> class ShiftedList { T* array; ... };`, instantiated as `ShiftedList<int> * list = new ShiftedList<int>(size);`.
- **Example use** — `ShiftedList` holds a `T* array` plus an `offset`, exposes `shiftBy(int n)`, `getAt(int i)`, `setAt(T item, int i)`, with a private `convertIndex` computing `(i - offset) % size` (normalized for negatives).
