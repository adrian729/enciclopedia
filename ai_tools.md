# AI Tools

## The Tools

### Cursor

vscode-like editor.

### Claude Code

CLI app.

### OpenAI Codex

Git repo tool (PRs and changes).

### Google Gemini CLI

CLI tool, alternative to Claude Code (and free).

## Context Engineering vs Vibe Coding

Be precise with the context fed to the model. The less it guesses, the less it hallucinates.

- Exact Files
- Error Logs
- Test failures

If it doesn't have context for a thing, it is guessing or hallucinating it.

That doesn't mean to feed the whole project to the model.

- Models use **tokens** - `1 token = ~4 characters`. You pay for it.
- Too much context can be counter-productive instead of helpful.

### The context window

The `context window` is the limited amount of `text/tokens` that an AI model can `process and remember` during an interaction.

It varies between models and can impact performance and complexity.

---

**Chat history**

Most LLMs manage chat history by just sending the entire chat history with each request!!!

### Managing the context window

The main challenge when working with LLMs is to manage the context window.

It is recommended to split the process in several phases:

- Preparation
- Execution
- Verification

It is really important to keep the three of them separate and not try to do them simultaneously.

##### Preparation

`Plan ahead`.

It is really important to brainstorm and think thorough the problem to plan before executing.

###### AI-Generated planning

If using AI for planning, try use several AI models to review and refine the plan.

##### Execution

1. `Break down problems` into smaller and specific tasks.
2. `Be precise`.
   - Write `detailed plans`, writing precise requirements.
     - DON'T: <br> `do auth`
     - DO: <br> `use Auth0 JavaScript SDK to implement a React hook that checks for user authentication and hooks into Google OAuth`
   - `Keep it as short/simple as possible`. Feed only the necessary context: files, error logs, test results.

Anything unnecessary in the context window can contribute to the LLM getting confused, plus you pay per token.

##### Verification

Verify / review the execution result is and behavies as expected.

### Maintenance

- `Keep your house in order: audit everything`.
  <br>
  <br>
  Regularly audit and maintain generated code by: trimming dead code, keeping track of different versions, ensuring consistency between rules across different tools, and being vigilant about potential inconsistencies or errors in the generated code.
  <br>
  <br>
  A good rule of thumb could be to audit the project at the start and end of the day.
  <br>
  <br>
- `Version control`.
  <br>
  <br>
  Use git or other version control tools, commit regularly.

## Cursor

### Modalities

Cursor has three major modalities:

- **Inline Edit** - `Cmd/Ctrl-k` and `Tab` - surgical, in-place code modifications. Takes place directly in the code editor.
- **AI Chat** - `Cmd/Ctrl-l` - opens up a chat window. Similar to ChatGPT with the codebase indexed.
  - Useful for `asking questions` about the codebase and `brainstorming`.
- **The Agent** - `Cmd/Ctrl-i` - enables agentic coding for complex, multi-file tasks. Describe a goal, the agent comes up with a plan and carries it out.

### Context

Cursor will try to load some extra `invisible` context:

- `current file` full content.
- List of `recently viewed files`.
- `Semantic search` of the codebase.
- Current `linter` and `compile` errors.
- Recent `edit history`.

#### Context limitations

The context window is limited, so Cursor will:

- In `Agent Mode` only read a maximum amount of lines from files and/or searches (atm 250 lines of a file, 100 fo a search).
- When using `@codebase`, use a smaller model to try to summarize each file, losing some context.
- Will try to push you to start a new chat to clean up context (Which you should be doing anyways!).

#### Context clues

`Pointing cursor in the right direction.`

- `@Files` and `@Folders` to explicitly include specific files or directories. Why more precise than relying on the AI guessing correctly where to look.
- `@Code` and `@Symbols` to reference specific functions, classes, variables for granular control.
- `@Docs` to point cursor to specific documentation via URL. Cursor will index this content and use it as a primary source of truth, reducing hallucinations and ensuring up-to-date code.
- `@Web` live web search for current information, blog posts, etc, adding the results to the query context.

#### Strategies to manage the context limitations

- Keep files small.
- Use linting rules to prevent large files.
- Manually specify which files and folders to analyze.
- Point to specific documentation URLs.
- Search recent versions information for specific technologies.

### Model Selection

#### Antrhopic

- `FE engineering`
- `UI / UX`
- OK at `code simplification / refactoring`
- OK at `general coding tasks`

##### Sonnet

Smaller.

##### Opus

Big guns. CAN BE VERY EXPENSIVE.

#### Google

- `HUGE context window` (`2M tokens`)
- Writting and cleaning up `documentation`
- `Code reviews`
- `Understanding big codebases`
- OK at `general coding tasks`

##### Gemini Flash

Speed / efficiency.

##### Gemini Pro

High-performance. Thinking.

#### OpenAI GPT Models

- `Deep Architectural Restructuring`
- `Design Patterns`
- `Debugging`
- `Brainstorming` (specially `o3`)
- Less hallucinations for `factual questions`

#### Local Mode

It is possible to host your own models.

- `Privacy`
- NEED VERY GOOD HARDWARE!

### Inline Mode `Cmd/Ctrl-k`

Command K allows users to generate code by highlighting a specific piece of code and asking the AI to perform actions like refactoring, mirroring, or creating similar functions based on the existing code context.

It will use the whole codebase as context, selecting relevant files and context, and use a lighter models that requires less comprehensive understanding of the entire project.

Useful for surgical or small quick refactors or code generation with minimal risk.

### Chat Window: Agent Mode

Add detailed instructions and context (`@Files`, `@Folders`, etc). The agent will use that to update or generate the codebase.

After, you can review the changes and accept, change or reject them.

#### Overview

- Chat History
- Chat TextBox
- Options
  - Switch Agent Mode
    - Agent
    - Plan
    - Debug
    - Ask
  - Select model (or auto)
    - Models can be configured from cursor settings
  - Cycle Agent Count (for multi-model mode)
  - Context Used: good to keep track of the current chat and know when we HAVE TO cleanup.
  - Add Context: files, folders, documentation...
  - Connect to browser
  - Upload image
  - Voice input

---

- `Cmd/Ctrl-N`: new chat.
- `Cmd/Ctrl-C`: halt/stop current thinking process (f.e. if AI gets stuck thinking).
  - If the AI is stuck, better to stop it and provide more specific and detailed feedback.

### AI Rules

Persistent instructions that provide guidelines for how code should be written, such as accessibility requirements, design principles, or coding conventions, without having to repeatedly specify them for each task.

The more specific the rule the better (same as for interacting when giving context to the AI tools).

- Project-level rules
  - Specific to a project.
  - They live in `.cursor/rules`.
  - Can be committed to `git` and shared.
  - Useful to specify preferred frameworks, code style, architectural guidelines...

- User-level rules
  - Apply `globally` to all the projects in the machine.
  - NOT checked into version control.
  - Ideal for individual stylistic decisions.

#### Applying the rules

Several options:

- `always`
- `auto-attached`: you define some globs for the types of files the rule should be applied to.
  - f.e. `**/*.css` for css files.
  - f.e `src/components/` for files inside that directory.
- `agent-requested`: leave it up to the AI to decide if it should apply the rule or not.
- `manually`: you can choose to pull particular rules in your context.

The rules count towards the `context window`! So it's important to include only the relevant ones, specifying when to apply them or not (specifying the file type or directory, requesting them manually when needed, etc).

### Background Agents

...
