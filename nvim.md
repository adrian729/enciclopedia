# NVim

## The Language

### Fundamentals

| Key            | Action                   | Context                                         |
| :------------- | :----------------------- | :----------------------------------------------- |
| `h`, `j`, `k`, `l` | Left, Down, Up, Right| Home row – basic movement                   |
| `i`            | Enter Insert mode        |                                                  |
| `<Esc>`        | Back to Normal mode      | Returns to the "command" state                   |
| `:`            | Enter Command mode       | Opens prompt at bottom (save/quit/shell, etc.)   |
| `u`            | Undo                     |                                                  |
| `<C-r>`        | Redo                     |                                                  |
| `<C-r>`        | Redo                     |                                                  |

### Text Objects (nouns)

To identify `what` to change. Combine with operators.

| Key                | Text Object           | Description                                                     |
| :----------------- | :-------------------- | :-------------------------------------------------------------- |
| `w` / `W`          | word                  | `w`: stops at `.`, `-`, or `_` &nbsp;/&nbsp; `W`: stops at whitespace |
| `s`                | sentence              | A sentence                                                      |
| `p`                | paragraph             | A paragraph                                                     |
| `t`                | tag                   | A tag (like `<div>` in HTML)                                    |
| `b` / `(` / `)`    | block (parentheses)   | Inside parentheses `()`                                         |
| `B` / `{` / `}`    | block (curly braces)  | Inside curly braces `{}`                                        |
| `"`                | double quotes         | Inside double quotes `"`                                        |
| `'`                | single quotes         | Inside single quotes `'`                                        |
| `[` / `]`          | square brackets       | Inside square brackets `[]`                                     |

#### Modifiers

Modifiers let you choose how much of an object is affected by an operator: just the inside (inner) or the whole thing (around).

| Modifier | Description                                                | Example                |
| :------- | :--------------------------------------------------------- | :--------------------- |
| `i`      | Inner – targets only the content inside the object         | `ciw` = Change Inner Word |
| `a`      | Around – targets the object plus whitespace or delimiters  | `daw` = Delete Around Word |

### Operations (verbs)

Actions to perform on the nouns.

| Key   | Operation    | Description                                                    |
| :---- | :----------- | :-------------------------------------------------------------|
| `d`   | Delete       | Delete (also cuts to clipboard)                                |
| `c`   | Change       | Change (deletes and immediately enters Insert mode)            |
| `y`   | Yank         | Yank (copy)                                                    |
| `p`   | Paste        | Paste after the cursor                                         |
| `v`   | Visual mode  | Highlight text in visual mode                                  |
| `s`   | Substitute   | Delete character under the cursor and enter Insert mode        |
| `S`   | Substitute line | Delete the whole line and enter Insert mode                 |
| `>`   | Indent       | Indent                                                         |
| `=`   | Auto-format  | Auto-format (very useful in 0.11 with LSP/Tree-sitter)         |

### Navigation

#### The Jumps

| Keys        | Movement / Action             | Nickname (Mnemonic)      |
| :---------- | :----------------------------| :----------------------- |
| `l` / `h`   | Move by character             | The Step                 |
| `w` / `b`   | Move by word                  | The Stride               |
| `(` / `)`   | Move by sentence              | The Leap                 |
| `{` / `}`   | Move by paragraph             | The Flight               |
| `gg` / `G`  | Move to start/end of file     | The Teleport             |
| `:[num]`    | Go to line number             | The Elevator             |
| `0`         | Jump to first character       | Absolute Zero            |
| `^`         | Jump to first non-blank char  | First Content            |
| `$`         | Jump to end of line           | The End                  |
| `%`         | Jump between matching brackets| The Bridge               |



**The Snippers**

| Key   | Name         | Action/Direction | Result / Description                                              |
| :---- | :----------- | :--------------- | :--------------------------------------------------------------- |
| `f`   | Find         | Forward          | `fx` **ON** the next character `x`              |
| `t`   | Till         | Forward          | `tx` **BEFORE** the next character `x`|
| `F`   | Find Back    | Backward         | `Fx` **ON** the prev character `x`        |
| `T`   | Till Back    | Backward         | `Tx` **AFTER** the prev character `x` |
| `;`   | Repeat       | Forward          | Repeat the last jump in the same direction.                      |
| `,`   | Repeat       | Backward         | Repeat the last jump in the opposite direction.                   |

### Examples

| Command | Action                          | Common Use Case                                                                     |
|:--------|:-------------------------------|:------------------------------------------------------------------------------------|
| `dap`   | `D`elete `A`round `P`aragraph   | Deletes an entire block of code and the blank line after it.                        |
| `yip`   | `Y`ank `I`nner `P`aragraph      | Copies just the code inside a block without the surrounding empty lines.             |
| `cip`   | `C`hange `I`nner `P`aragraph    | Clears a block of text and starts Insert mode so you can rewrite it.                 |
| `vip`   | `V`isual `I`nner `P`aragraph    | Quickly highlights a whole block (e.g., to indent it with `>`).                      |
| `dt)`   | `D`elete `T`ill `)`             | Deletes everything inside the parentheses but keeps the bracket itself.              |
| `df)`   | `D`elete `F`ind `)`             | Deletes everything including the bracket.                                            |

## Command Mode (`:`)

### Search

#### Search

| Key | Action                                | Nickname            |
|:---:|:--------------------------------------|:--------------------|
| `/` | Search Forward                        | The Scout           |
| `?` | Search Backward                       | The Reverse Scout   |
| `*` | Search Word Under Cursor Forward      | The Seeker          |
| `#` | Search Word Under Cursor Backward     | The Backward Seeker |
| `n` | Next Match                            |                     |
| `N` | Previous Match                        |                     |

#### Search & Replace (`:s`)

`:[range]s/[pattern]/[replacement]/[flags]`

##### range

| Range      | Meaning                                                                                     |
| :--------- | :------------------------------------------------------------------------------------------ |
| (no range) | Only the line the cursor is currently on.                                                   |
| `%`        | The entire file (The most common usage).                                                    |
| `'<,'>`    | The current visual selection (automatically added if you hit `:` while text is highlighted).|
| `.`        | Current line (default).                                                                     |

##### pattern/replacement

word to search for / word to replace it with

##### flags

| Flag | Name         | What it does                                                                                      | Example              |
| :--- | :----------- | :------------------------------------------------------------------------------------------------ | :------------------- |
| g    | Global       | Replaces all occurrences on a line. Without this, Neovim only replaces the first one it finds.    | `:%s/cat/dog/g`      |
| c    | Confirm      | Asks for permission before each replacement. Highly recommended to avoid "oops" moments.           | `:%s/cat/dog/gc`     |
| i    | Ignore Case  | Makes the search case-insensitive. Finds "Cat", "CAT", and "cat".                                 | `:%s/cat/dog/gi`     |
| I    | Inert Case   | Forces case-sensitivity. (Usually the default, but useful if you've changed your global settings). | `:%s/cat/dog/gI`     |
| e    | Error silence| Prevents Neovim from showing an "Error: Pattern not found" message if there are no matches. Great for macros. | `:%s/cat/dog/ge`     |
| n    | Number       | Report only. It tells you how many matches were found but doesn't actually replace anything.       | `:%s/cat/dog/gn`     |
| p    | Print        | Prints the last line that was changed.                                                            | `:%s/cat/dog/gp`     |


### File Management (system)

| Command          | Description                    |
| :--------------- | :---------------------------- |
| `:w`             | Write (save)                  |
| `:q`             | Quit                          |
| `:wq`            | Save and quit                 |
| `:q!`            | Quit without saving           |
| `:e <filename>`  | Open a new file               |
| `:vsplit`        | Split the screen vertically   |
