# NVim

## Table of Contents

- [1. The Language](#1-the-language)
  - [1.1. Fundamentals](#11-fundamentals)
  - [1.2. Text Objects (nouns)](#12-text-objects-nouns)
    - [1.2.1. Modifiers](#121-modifiers)
  - [1.3. Operations (verbs)](#13-operations-verbs)
  - [1.4. Navigation](#14-navigation)
    - [1.4.1. The Jumps](#141-the-jumps)
    - [1.4.2. The Snippers](#142-the-snippers)
  - [1.5. Examples](#15-examples)
- [2. Command Mode (`:`)](#2-command-mode-)
  - [2.1. Search](#21-search)
    - [2.1.1. Search](#211-search)
    - [2.1.2. Search & Replace (`:s`)](#212-search--replace-s)
  - [2.2. File Management (system)](#22-file-management-system)
- [3. Registers (`"`)](#3-registers-)
  - [3.1. Formula](#31-formula)
  - [3.2. Types of Lockers (Registers)](#32-types-of-lockers-registers)
  - [3.3. Check the Lockers (`:reg`)](#33-check-the-lockers-reg)
- [4. Macros](#4-macros)
  - [4.1. Macro Workflow](#41-macro-workflow)

<a id="1-the-language"></a>

## 1. The Language

<a id="11-fundamentals"></a>

### 1.1. Fundamentals

| Key                | Action                | Context                                        |
| :----------------- | :-------------------- | :--------------------------------------------- |
| `h`, `j`, `k`, `l` | Left, Down, Up, Right | Home row – basic movement                      |
| `i`                | Enter Insert mode     |                                                |
| `<Esc>`            | Back to Normal mode   | Returns to the "command" state                 |
| `:`                | Enter Command mode    | Opens prompt at bottom (save/quit/shell, etc.) |
| `u`                | Undo                  |                                                |
| `<C-r>`            | Redo                  |                                                |

<a id="12-text-objects-nouns"></a>

### 1.2. Text Objects (nouns)

To identify `what` to change. Combine with operators.

| Key             | Text Object          | Description                                               |
| :-------------- | :------------------- | :-------------------------------------------------------- |
| `w` / `W`       | word                 | `w`: stops at `.`, `-`, or `_` / `W`: stops at whitespace |
| `s`             | sentence             | A sentence                                                |
| `p`             | paragraph            | A paragraph                                               |
| `t`             | tag                  | A tag (like `<div>` in HTML)                              |
| `b` / `(` / `)` | block (parentheses)  | Inside parentheses `()`                                   |
| `B` / `{` / `}` | block (curly braces) | Inside curly braces `{}`                                  |
| `"`             | double quotes        | Inside double quotes `"`                                  |
| `'`             | single quotes        | Inside single quotes `'`                                  |
| `[` / `]`       | square brackets      | Inside square brackets `[]`                               |

<a id="121-modifiers"></a>

#### 1.2.1. Modifiers

Modifiers let you choose how much of an object is affected by an operator: just the inside (inner) or the whole thing (around).

| Modifier | Description                                               | Example                    |
| :------- | :-------------------------------------------------------- | :------------------------- |
| `i`      | Inner – targets only the content inside the object        | `ciw` = Change Inner Word  |
| `a`      | Around – targets the object plus whitespace or delimiters | `daw` = Delete Around Word |

<a id="13-operations-verbs"></a>

### 1.3. Operations (verbs)

Actions to perform on the nouns.

| Key | Operation       | Description                                             |
| :-- | :-------------- | :------------------------------------------------------ |
| `d` | Delete          | Delete (also cuts to clipboard)                         |
| `c` | Change          | Change (deletes and immediately enters Insert mode)     |
| `y` | Yank            | Yank (copy)                                             |
| `p` | Paste           | Paste after the cursor                                  |
| `v` | Visual mode     | Highlight text in visual mode                           |
| `s` | Substitute      | Delete character under the cursor and enter Insert mode |
| `S` | Substitute line | Delete the whole line and enter Insert mode             |
| `>` | Indent          | Indent                                                  |
| `=` | Auto-format     | Auto-format (very useful in 0.11 with LSP/Tree-sitter)  |

<a id="14-navigation"></a>

### 1.4. Navigation

<a id="141-the-jumps"></a>

#### 1.4.1. The Jumps

| Keys       | Movement / Action              | Nickname (Mnemonic) |
| :--------- | :----------------------------- | :------------------ |
| `l` / `h`  | Move by character              | The Step            |
| `w` / `b`  | Move by word                   | The Stride          |
| `(` / `)`  | Move by sentence               | The Leap            |
| `{` / `}`  | Move by paragraph              | The Flight          |
| `gg` / `G` | Move to start/end of file      | The Teleport        |
| `:[num]`   | Go to line number              | The Elevator        |
| `0`        | Jump to first character        | Absolute Zero       |
| `^`        | Jump to first non-blank char   | First Content       |
| `$`        | Jump to end of line            | The End             |
| `%`        | Jump between matching brackets | The Bridge          |

<a id="142-the-snippers"></a>

#### 1.4.2. The Snippers

| Key | Name      | Action/Direction | Result / Description                            |
| :-- | :-------- | :--------------- | :---------------------------------------------- |
| `f` | Find      | Forward          | `fx` **ON** the next character `x`              |
| `t` | Till      | Forward          | `tx` **BEFORE** the next character `x`          |
| `F` | Find Back | Backward         | `Fx` **ON** the prev character `x`              |
| `T` | Till Back | Backward         | `Tx` **AFTER** the prev character `x`           |
| `;` | Repeat    | Forward          | Repeat the last jump in the same direction.     |
| `,` | Repeat    | Backward         | Repeat the last jump in the opposite direction. |

<a id="15-examples"></a>

### 1.5. Examples

| Command | Action                        | Common Use Case                                                          |
| :------ | :---------------------------- | :----------------------------------------------------------------------- |
| `dap`   | `D`elete `A`round `P`aragraph | Deletes an entire block of code and the blank line after it.             |
| `yip`   | `Y`ank `I`nner `P`aragraph    | Copies just the code inside a block without the surrounding empty lines. |
| `cip`   | `C`hange `I`nner `P`aragraph  | Clears a block of text and starts Insert mode so you can rewrite it.     |
| `vip`   | `V`isual `I`nner `P`aragraph  | Quickly highlights a whole block (e.g., to indent it with `>`).          |
| `dt)`   | `D`elete `T`ill `)`           | Deletes everything inside the parentheses but keeps the bracket itself.  |
| `df)`   | `D`elete `F`ind `)`           | Deletes everything including the bracket.                                |

<a id="2-command-mode-"></a>

## 2. Command Mode (`:`)

<a id="21-search"></a>

### 2.1. Search

<a id="211-search"></a>

#### 2.1.1. Search

| Key | Action                            | Nickname            |
| :-: | :-------------------------------- | :------------------ |
| `/` | Search Forward                    | The Scout           |
| `?` | Search Backward                   | The Reverse Scout   |
| `*` | Search Word Under Cursor Forward  | The Seeker          |
| `#` | Search Word Under Cursor Backward | The Backward Seeker |
| `n` | Next Match                        |                     |
| `N` | Previous Match                    |                     |

<a id="212-search--replace-s"></a>

#### 2.1.2. Search & Replace (`:s`)

`:[range]s/[pattern]/[replacement]/[flags]`

##### range

| Range      | Meaning                                                                                      |
| :--------- | :------------------------------------------------------------------------------------------- |
| (no range) | Only the line the cursor is currently on.                                                    |
| `%`        | The entire file (The most common usage).                                                     |
| `'<,'>`    | The current visual selection (automatically added if you hit `:` while text is highlighted). |
| `.`        | Current line (default).                                                                      |

##### pattern/replacement

word to search for / word to replace it with

##### flags

| Flag | Name          | What it does                                                                                       | Example          |
| :--- | :------------ | :------------------------------------------------------------------------------------------------- | :--------------- |
| g    | Global        | Replaces all occurrences on a line. Without this, Neovim only replaces the first one it finds.     | `:%s/cat/dog/g`  |
| c    | Confirm       | Asks for permission before each replacement. Highly recommended to avoid "oops" moments.           | `:%s/cat/dog/gc` |
| i    | Ignore Case   | Makes the search case-insensitive. Finds "Cat", "CAT", and "cat".                                  | `:%s/cat/dog/gi` |
| I    | Inert Case    | Forces case-sensitivity. (Usually the default, but useful if you've changed your global settings). | `:%s/cat/dog/gI` |
| e    | Error silence | Prevents Neovim from showing an "Error: Pattern not found" message if there are no matches.        | `:%s/cat/dog/ge` |
| n    | Number        | Report only. It tells you how many matches were found but doesn't actually replace anything.       | `:%s/cat/dog/gn` |
| p    | Print         | Prints the last line that was changed.                                                             | `:%s/cat/dog/gp` |

<a id="22-file-management-system"></a>

### 2.2. File Management (system)

| Command         | Description                 |
| :-------------- | :-------------------------- |
| `:w`            | Write (save)                |
| `:q`            | Quit                        |
| `:wq`           | Save and quit               |
| `:q!`           | Quit without saving         |
| `:e <filename>` | Open a new file             |
| `:vsplit`       | Split the screen vertically |

<a id="3-registers-"></a>

## 3. Registers (`"`)

In Neovim, you have 36+ "Registers." Think of them as Lockers or Slots where you can store text.

If you copy (yank) something, it goes into a specific locker. If you delete something, it goes into another. You can even choose which locker to use manually.

<a id="31-formula"></a>

### 3.1. Formula

`"` + `[Register Name]` + `[Action]`

**Examples**
| Command | Action |
| :--------- | :------------------------------ |
| `"ayw` | Yank (copy) word to register a |
| `"ap` | Paste from register a |
| `"bdd` | Delete line to register b |

<a id="32-types-of-lockers-registers"></a>

### 3.2. Types of Lockers (Registers)

| Locker Name   | Type               | How it behaves                                                                               |
| :------------ | :----------------- | :------------------------------------------------------------------------------------------- |
| `"` (default) | The Unnamed        | Your "main" clipboard. Most yanks and deletes go here.                                       |
| `0`           | The Yank Locker    | Stores the last thing you copied (yanked). It doesn't store deletes!                         |
| `1` – `9`     | The History        | Stores your last 9 deletions. `1` is the newest, `9` is the oldest.                          |
| `a` – `z`     | Custom Lockers     | Your personal slots. Neovim never touches these; only you can put things here intentionally. |
| `*` and `+`   | System Clipboard   | Bridge to the outside world (copying between Neovim and other apps like Chrome or Slack).    |
| `_`           | Black Hole         | Anything sent here is deleted forever and not saved anywhere (like /dev/null).               |
| `%`           | Filename Register  | Contains the name of the current file (`%p` to paste the filename).                          |
| `.`           | Last Inserted Text | Contains the last inserted text.                                                             |
| `/`           | Last Search        | Contains the last search pattern.                                                            |

<a id="33-check-the-lockers-reg"></a>

### 3.3. Check the Lockers (`:reg`)

`:reg` will show all registers and what is stored in them

<a id="4-macros"></a>

## 4. Macros

A **Macro** is like a "_Screen Recorder_" for your keystrokes. You record a sequence of actions once, and then you can play it back 10, 100, or 1,000 times.

Macros are stored inside registers.

<a id="41-macro-workflow"></a>

### 4.1. Macro Workflow

| Step   | Key            | Action                                               |
| :----- | :------------- | :--------------------------------------------------- |
| Start  | `q` + [letter] | Start recording into a specific locker (e.g., `qa`). |
| Action | (Do anything)  | Perform your edits, jumps, and searches.             |
| Stop   | `q`            | Stop the recording.                                  |
| Play   | `@` + [letter] | Play the macro stored in that locker.                |
| Repeat | `@@`           | Play the last used macro again.                      |

**Macros should be `repeatable`:**

- **BAD**: Using `llll`, this moves 4 characters, if the next line is shorter it won't work.
- **GOOD**: Using `f(` or `0`.
