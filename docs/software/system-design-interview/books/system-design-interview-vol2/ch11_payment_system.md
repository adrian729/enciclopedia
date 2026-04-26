# Ch 11: Payment System

## Table of Contents

- [1. Problem and Scope](#1-problem-and-scope)
- [2. Pay-in Flow](#2-pay-in-flow)
- [3. Pay-out Flow](#3-pay-out-flow)
- [4. Data Model and Ledger](#4-data-model-and-ledger)
- [5. PSP Integration](#5-psp-integration)
- [6. Reconciliation](#6-reconciliation)
- [7. Reliability: Retries and Failures](#7-reliability-retries-and-failures)
- [8. Exactly-Once via Idempotency](#8-exactly-once-via-idempotency)
- [9. Consistency](#9-consistency)
- [10. Security](#10-security)

## 1. Problem and Scope

- **Payment system** — backend that settles financial transactions between buyers, sellers, and intermediaries; per Wikipedia, "any system used to settle financial transactions through the transfer of monetary value."
- **Functional requirements** — pay-in (collect money from customers on behalf of sellers) and pay-out (disburse money to sellers).
- **Non-functional requirements** — reliability, fault tolerance for failed payments, asynchronous reconciliation between internal services and external providers.
- **Scope simplifications** — credit-card payments only, single currency, third-party payment processors handle card data (no direct PCI DSS storage), e-commerce backend like Amazon.com.
- **Scale** — 1M transactions/day → ~10 TPS; the design challenge is correctness, not throughput.

## 2. Pay-in Flow

- **Money path** — buyer's card → e-commerce bank account (custodian) → after delivery and fees, seller's bank account.
- **Components** — Payment Service (orchestrator + risk check), Payment Executor (per-order execution), PSP, Card Schemes (Visa, MasterCard, Discover), Ledger (financial record), Wallet (merchant balance).
- **Risk check** — AML/CFT compliance and fraud screening, typically delegated to a specialized third party.
- **Payment event vs payment order** — one checkout (event) can produce multiple orders (e.g., multi-seller cart); each order is executed separately by the payment executor.

### Step-by-step

1. User clicks "place order" → payment event reaches Payment Service.
2. Service persists the event, splits into payment orders, calls executor per order.
3. Executor persists the order and calls the PSP.
4. On PSP success, Payment Service updates Wallet (seller balance), then Ledger (debit/credit entries).
5. When all orders for a `checkout_id` succeed, `is_payment_done = TRUE`.

## 3. Pay-out Flow

- **Mirror of pay-in** — same component shape, but instead of moving buyer-card → e-commerce account, a third-party payable provider (e.g., **Tipalti**) moves e-commerce account → seller account.
- **Trigger** — fulfillment milestones (e.g., delivery confirmation) plus regulatory and bookkeeping checks before disbursement.

## 4. Data Model and Ledger

- **Storage choice criteria** — proven stability (5+ years at large financial firms), rich tooling, mature DBA hiring market; ACID-compliant relational DBs preferred over NoSQL/NewSQL.
- **`payment_event` table** — `checkout_id PK`, `buyer_info`, `seller_info`, `credit_card_info`, `is_payment_done`.
- **`payment_order` table** — `payment_order_id PK`, `buyer_account`, `amount`, `currency`, `checkout_id FK`, `payment_order_status`, `ledger_updated`, `wallet_updated`.
- **Status state machine** — `NOT_STARTED` → `EXECUTING` → `SUCCESS` or `FAILED`; a scheduled job alerts on orders stuck in `EXECUTING`.
- **`amount` is a string, not double** — doubles cause precision/serialization rounding errors; values can be huge (Japan's GDP ≈ 5×10¹⁴ yen) or tiny (1 satoshi = 10⁻⁸ BTC). Parse to numeric only at the display/calculation boundary.
- **Double-entry ledger** — every transaction posts to two accounts with equal magnitude: debit one, credit the other. Sum across all entries must equal 0 — "one cent lost means someone else gains a cent." Provides end-to-end traceability (Square's engineering blog cited).
- **Hosted payment page** — companies avoid PCI DSS scope by embedding a PSP-hosted iframe/widget (or SDK page on mobile); card data goes directly to the PSP, never touches the merchant backend.

## 5. PSP Integration

- **Two integration models** — (1) API integration if the company stores sensitive card data itself (rare, expensive PCI compliance); (2) hosted page where PSP captures and stores card data — the common choice.
- **Hosted-page flow** — payment service registers the order with PSP using a UUID nonce; PSP returns a token; service stores token and renders the hosted page; PSP processes payment and redirects browser to a redirect URL with status appended; PSP separately notifies the service via a registered webhook.
- **Token = PSP-side idempotency key** — the nonce maps 1:1 to a token, which uniquely identifies the registration and prevents duplicate registration if the user retries.
- **Redirect URL vs webhook** — redirect URL takes the browser back to the merchant's status page; webhook is a server-to-server callback for asynchronous status updates.
- **Long-running payments** — PSP risk review or 3D Secure can stall a request for hours/days; PSP returns "pending," then either pushes via webhook or requires the merchant to poll.

## 6. Reconciliation

- **Definition** — periodic comparison of state across related services to verify they agree; "the last line of defense" because async messages aren't guaranteed to deliver.
- **Settlement file** — PSPs and banks send nightly files containing the day's transactions and end-of-day balance; reconciliation parses and diffs against the ledger.
- **Internal use** — also used to detect drift between internal services (e.g., ledger ↔ wallet).
- **Mismatch buckets** — (1) classifiable + auto-fixable (write a script); (2) classifiable but not cost-effective to automate (finance team fixes from a job queue); (3) unclassifiable (special queue, manual investigation).

## 7. Reliability: Retries and Failures

- **Append-only payment-state log** — persist every state transition so any failure can resume from the last known state and decide retry vs refund.
- **Retry queue** — transient failures (network, timeouts) are routed here for automatic re-execution by the payment system.
- **Dead letter queue** — messages exceeding the retry threshold; held for engineering investigation rather than silent loss. Uber's payment system (cited) uses Kafka for both queues.
- **Non-retryable errors** — invalid input etc. → stored in DB for review, not retried.

### Retry strategies

| Strategy | Behavior |
|---|---|
| Immediate retry | Resend right away |
| Fixed interval | Wait constant time between attempts |
| Incremental interval | Linearly increasing waits |
| Exponential backoff | Double the wait each attempt (1s, 2s, 4s, …) |
| Cancel | Permanent failure — stop trying |

- **Default guidance** — exponential backoff for network-class failures; provide `Retry-After` header so clients pace themselves; aggressive retries cause cascading overload.

## 8. Exactly-Once via Idempotency

- **Decomposition** — exactly-once = at-least-once (via retry) + at-most-once (via idempotency).
- **Double-payment scenarios** — (1) user double-clicks "pay"; (2) PSP succeeded but the response was lost in transit, user retries.
- **Idempotency key** — client-generated UUID sent in HTTP header `<idempotency-key: key_value>`; for e-commerce the shopping-cart ID just before checkout is a natural choice. Pattern recommended by Stripe and PayPal.
- **DB-enforced idempotency** — primary-key unique constraint on the idempotency key; first insert wins, duplicate inserts fail and the system returns the original status.
- **Concurrent duplicates** — multiple in-flight requests with the same key → only one is processed, others receive `429 Too Many Requests`.
- **PSP-side idempotency** — the nonce → token mapping makes the PSP recognize duplicate retries and replay the prior result rather than charging again.

## 9. Consistency

- **Stateful actors** — payment service, ledger, wallet, PSP, plus DB replicas; any inter-service link can fail and produce divergence.
- **Internal consistency** — exactly-once processing is the foundational guarantee.
- **Internal ↔ external** — combine idempotency on retries with reconciliation; never assume the external system is correct.
- **Replica lag options** — (1) read and write only from the primary (simple, but replicas waste capacity); (2) keep replicas synchronously in agreement via Paxos or Raft, or use consensus-based stores like YugabyteDB or CockroachDB.

### Synchronous vs asynchronous internal communication

| Property | Synchronous (HTTP) | Asynchronous (queue/Kafka) |
|---|---|---|
| Performance | Limited by slowest hop | Decoupled, buffered |
| Failure isolation | Cascading | Contained per consumer |
| Coupling | Sender knows receiver | Loose |
| Scaling | Hard without buffer | Natural |
| Complexity | Simple | Higher (eventual consistency) |

- **Single vs multiple receivers** — shared queue (message removed after one consumer reads) suits single-receiver work like payment execution; Kafka topics (multiple consumers, message retained) suit fanout to analytics, billing, notifications.
- **Recommendation** — async fits large-scale payment systems with many third-party dependencies, despite the eventual-consistency complexity.

## 10. Security

| Threat | Mitigation |
|---|---|
| Eavesdropping | HTTPS |
| Data tampering | Encryption + integrity monitoring |
| Man-in-the-middle | SSL with certificate pinning |
| Stored passwords | Salted hashing |
| Data loss | Multi-region replication + snapshots |
| DDoS | Rate limiting + firewall |
| Card theft | **Tokenization** — store opaque tokens, never raw PAN |
| PCI compliance | PCI DSS for any org handling branded cards |
| Fraud | Address verification, CVV, behavioral analysis |

- **Other operational topics** — monitoring (e.g., per-method acceptance rate), alerting on-call, debugging tools (transaction status, PSP records, processing history), currency exchange for international users, region-specific payment methods, cash payment handling (Uber and Airbnb engineering blogs cited for India and Brazil), Apple Pay / Google Pay integration.
