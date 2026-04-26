# Ch 2: The Sidecar Pattern

## Table of Contents

- [1. Pattern Definition](#1-pattern-definition)
- [2. Use Cases](#2-use-cases)
  - [2.1. Adding HTTPS to a Legacy Service](#21-adding-https-to-a-legacy-service)
  - [2.2. Dynamic Configuration](#22-dynamic-configuration)
  - [2.3. Modular Utility Containers](#23-modular-utility-containers)
  - [2.4. A Simple PaaS](#24-a-simple-paas)
- [3. Designing for Modularity and Reuse](#3-designing-for-modularity-and-reuse)

## 1. Pattern Definition

- **Sidecar pattern** — a single-node pattern of two containers: an *application container* (core logic) and a *sidecar container* that augments or extends it, often without the application container knowing.
- **Application container** — holds the core application logic; the system would not exist without it.
- **Sidecar container** — adds functionality to the application container that would otherwise be hard to add (e.g., to legacy code).
- **Container group** — atomic co-scheduling unit (e.g., Kubernetes `pod`); the sidecar and application share machine, parts of the filesystem, hostname, network, and other namespaces.

## 2. Use Cases

### 2.1. Adding HTTPS to a Legacy Service

- **Problem** — a legacy HTTP-only web service must serve HTTPS, but its old build system no longer functions, making source-level changes painful.
- **Sidecar solution** — bind the legacy app to localhost (127.0.0.1) only, then add an nginx sidecar in the same network namespace that terminates HTTPS on the pod's external IP and proxies plaintext traffic over the loopback adapter.
- **Outcome** — modernizes the legacy app without rebuilding it; security team is satisfied because unencrypted traffic never leaves the container group.

### 2.2. Dynamic Configuration

- **Problem** — many legacy apps read configuration from a file on the filesystem at startup; cloud-native ops want push-based config updates via an API (with rollback, automation).
- **Sidecar solution** — pair the app with a configuration-manager sidecar; both share a directory holding the config file. The sidecar polls the config API, writes changes to the shared file, then signals the app (file watch, `SIGHUP`, or as a last resort `SIGKILL` + orchestrator restart).
- **Effect** — adapts existing apps to dynamic configuration without modifying them.

### 2.3. Modular Utility Containers

- **`topz` example** — instead of forcing every team to link a language-specific `/topz` HTTP plugin into their app, deploy a `topz` sidecar that shares the application container's PID namespace and exposes a consistent web UI of running processes and resource use.
- **Why a sidecar over a library** — a per-language library demands a separate implementation per language and risks inconsistency or gaps when new languages appear; a sidecar can be auto-attached by the orchestrator to every app for uniform tooling.
- **Off-the-rack vs. bespoke tradeoff** — the modular sidecar may be slightly less efficient or less tailored than a hand-rolled library (analogous to off-the-rack vs. bespoke clothing), but for most cases the general-purpose container is the right buy; reach for the handwritten solution only under extreme performance demands.

### 2.4. A Simple PaaS

- **Setup** — main container runs a Node.js server using `nodemon` to auto-reload on file changes; sidecar shares the filesystem and runs `while true; do git pull; sleep 10; done` against a Git repo.
- **Result** — a minimal Git-push-to-deploy PaaS: pushing code triggers the sidecar's pull, which triggers the server's reload — sidecars compose application behavior, not just augment it.

## 3. Designing for Modularity and Reuse

- **Three discipline areas** — to be reusable, sidecars need (1) parameterization, (2) a defined API, (3) documentation.
- **Parameterize like a function** — treat the container as a function whose parameters customize a generic image to a specific deployment (e.g., the SSL sidecar needs a certificate name and a localhost port).
- **Prefer environment variables over command-line args** for passing parameters; consume them inside the container with a small shell script that templates config files or invokes the underlying app.
- **The container's API is everything it touches** — parameters, outbound calls to other services, and inbound HTTP/other interfaces all form the API; treat it like a microservice contract so consumers keep working across versions.
- **Breaking changes can be subtle** — renaming `UPDATE_FREQUENCY` → `UPDATE_PERIOD` is obviously breaking; changing the value's units (seconds → strings like "10m"; or unitless integers from seconds → milliseconds) is also breaking even if it doesn't error, because behavior silently changes (e.g., far higher request load on the config server).
- **Document with Dockerfile directives** — `EXPOSE` for listening ports (with comments), `ENV` for default values of parameters with comments explaining usage, `LABEL` for metadata.
- **Use the Label Schema project taxonomy** — common label names (e.g., `org.label-schema.vendor`, `org.label-schema.version`) let community tools visualize, monitor, and use images without bespoke modification.
