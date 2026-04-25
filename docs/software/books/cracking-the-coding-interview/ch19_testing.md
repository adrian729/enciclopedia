# Ch 19: Testing

## Table of Contents

- [1. Framing](#1-framing)
- [2. What the interviewer is looking for](#2-what-the-interviewer-is-looking-for)
- [3. Testing a real-world object](#3-testing-a-real-world-object)
- [4. Testing a piece of software](#4-testing-a-piece-of-software)
- [5. Testing a function](#5-testing-a-function)
- [6. Troubleshooting questions](#6-troubleshooting-questions)

## 1. Framing

- **Testing is a software-engineer task** — even non-test candidates get testing questions; Testing / SDET roles get more.
- **Four question categories** — (1) test a real-world object (like a pen), (2) test a piece of software, (3) write test code for a function, (4) troubleshoot an existing issue.
- **Assume abuse** — never assume the input or the user will "play nice"; plan for abuse.

## 2. What the interviewer is looking for

Surface-level, yes, they want a reasonable list of test cases — but interviewers also evaluate four deeper qualities.

| Quality | What it means |
|---------|---------------|
| **Big Picture Understanding** | Grasp what the software is *really* about; prioritize critical tests (e.g., e-commerce payments and double-charge prevention over image placement). |
| **Knowing How the Pieces Fit Together** | Test the product's integration into its ecosystem (e.g., Google Spreadsheets with Gmail, plug-ins, other components). |
| **Organization** | Break the problem into categories (e.g., Taking Photos, Image Management, Settings) rather than rattling off random cases. |
| **Practicality** | Produce test plans that are feasible and realistic — "reinstall the software" is not a real plan. |

## 3. Testing a real-world object

Example: **how would you test a paperclip?** Walk through five steps.

1. **Who will use it? And why?** — discuss with the interviewer; user could be teachers (holding papers) or artists (bending into animals), or both. This shapes everything else.
2. **What are the use cases?** — list them; for a paperclip, the use case may simply be fastening paper non-destructively. Other products may have multiple use cases (e.g., send/receive content, write/erase).
3. **What are the bounds of use?** — e.g., holds up to 30 sheets without permanent damage, 30–50 with minimal bending. Include environmental factors (hot: 90–110 °F; extreme cold).
4. **What are the stress / failure conditions?** — no product is fail-proof; discuss when failure is acceptable and what failure should look like (e.g., a laundry machine should handle at least 30 shirts or pants; 30–45 pieces may result in minor failure such as inadequate cleaning; >45 pieces, extreme failure might be acceptable — but extreme failure should mean the machine never turns on the water, not a flood or fire).
5. **How would you perform the testing?** — define "normal" usage, decide between manual and automated, possibly automate long-duration usage (e.g., a chair's 5-year stress test).

## 4. Testing a piece of software

Very similar to testing a real-world object, but with more emphasis on *how* testing is performed.

- **Manual vs. Automated Testing** — automation is ideal but rarely fully feasible; some checks are too qualitative for computers (e.g., whether content counts as pornography). Humans may also catch issues no one thought to test.
- **Black Box Testing vs. White Box Testing** — black box tests the software as-is; white box has programmatic access to individual functions. White box is more powerful; automating black-box testing is possible but harder.

The six-step approach for testing software:

1. **Black Box or White Box?** — confirm with the interviewer early (may be both).
2. **Who will use it? And why?** — identify target users and edge users (e.g., for parental-control software: parents, children, and "guests" who neither implement nor receive blocking).
3. **What are the use cases?** — enumerate per user role; this is a conversation with the interviewer, not a unilateral decision.
4. **What are the bounds of use?** — pin down vague terms (e.g., "blocked": just the illegal page or the whole site? whitelist/blacklist or learning? acceptable false-positive rate?).
5. **Stress / failure conditions** — failure must not crash the computer; define what graceful failure looks like (e.g., permit a blocked site with a parent password override).
6. **Test cases & how to perform them** — from steps 3–4, decide which parts use manual vs. automated, black box vs. white box. Approach the case list in a **structured manner** (by components) — not a random brain-dump.

## 5. Testing a function

Often the easiest category — typically limited to validating input and output. Still worth discussing assumptions with the interviewer.

Example: testing `sort(int[] array)`.

### 5.1. Step 1 — define the test cases

Cover four kinds of input:

- **The normal case** — typical inputs. Remember subtleties (e.g., sorting may partition, so odd-length and even-length arrays both belong in the list).
- **The extremes** — empty array, single-element array, very large array.
- **Nulls and "illegal" input** — how should the function behave? (e.g., a Fibonacci function tested with negative `n`.)
- **Strange input** — already sorted, reverse-sorted, etc.

### 5.2. Step 2 — define the expected result

- Usually the correct output, but also validate side effects — e.g., if `sort` returns a new sorted copy, confirm the original array is untouched.

### 5.3. Step 3 — write test code

Straightforward once cases and expected results are defined:

```java
void testAddThreeSorted() {
    MyList list = new MyList();
    list.addThreeSorted(3, 1, 2); // Adds 3 items in sorted order
    assertEquals(list.getElement(0), 1);
    assertEquals(list.getElement(1), 2);
    assertEquals(list.getElement(2), 3);
}
```

## 6. Troubleshooting questions

Example: **you are on the Google Chrome team and get a bug report that Chrome crashes on launch. What do you do?** "Reinstall the software" is the unrealistic answer — the goal is to understand what is *really* happening so developers can fix it for all users.

### 6.1. Step 1 — understand the scenario

Ask questions:

- How long has the user been experiencing the issue?
- What version of the browser? What OS?
- Does it happen consistently? How often? When?
- Is there an error report that launches?

### 6.2. Step 2 — break down the problem

Turn the scenario into testable units — e.g., the Chrome launch flow:

1. Go to Windows Start menu
2. Click on Chrome icon
3. Browser instance starts
4. Browser loads settings
5. Browser issues HTTP request for homepage
6. Browser gets HTTP response
7. Browser parses webpage
8. Browser displays content

A strong tester iterates through these elements to isolate where the failure occurs.

### 6.3. Step 3 — create specific, manageable tests

- Each component needs realistic instructions — things the user can do, or that you can reproduce yourself on your own machine.
- In the real world you cannot give customers steps they cannot or will not perform.
