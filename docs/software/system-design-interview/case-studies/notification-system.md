# Notification System

> Xu's Ch 10 only. The interesting design choice is **a distinct queue per channel** so an outage in one third-party (FCM, APNS, Twilio, Sendgrid) doesn't block the others.

## Table of Contents

- [1. Requirements](#1-requirements)
- [2. Channels and Third Parties](#2-channels-and-third-parties)
- [3. Naive vs Improved Architecture](#3-naive-vs-improved-architecture)
- [4. Reliability](#4-reliability)
  - [4.1. Notification Log + Retries](#41-notification-log--retries)
  - [4.2. Dedupe by Event ID](#42-dedupe-by-event-id)
- [5. Templates and Opt-In](#5-templates-and-opt-in)
- [6. Rate Limiting Against User Fatigue](#6-rate-limiting-against-user-fatigue)
- [Sources](#sources)

## 1. Requirements

- Deliver push notifications, SMS, and email.
- High reliability — don't drop notifications.
- Per-user opt-in per channel.
- Rate limit so users don't get spammed and disable the channel.

## 2. Channels and Third Parties

Three categories:

| Channel | Provider |
|---|---|
| Push (iOS) | APNS |
| Push (Android) | FCM |
| SMS | Twilio, Nexmo |
| Email | Sendgrid, Mailchimp |

Each provider has its own API, rate limits, failure modes, and retry semantics. The system has to absorb that heterogeneity.

## 3. Naive vs Improved Architecture

**Naive**: a single notification server fronted by API servers. Drawbacks:

- SPOF — server down = all notifications down.
- Can't scale per-channel (a flood of pushes shouldn't slow email).
- Tight coupling — an FCM outage backs up the queue for all other channels.

**Improved**:

```
API Servers
    ↓
Notification Service (validates, looks up user prefs)
    ↓
Per-channel Message Queues  (one queue each: push iOS, push Android, SMS, email)
    ↓
Per-channel Workers (autoscaled, drain their queue)
    ↓
Third-party Provider (APNS, FCM, Twilio, Sendgrid)
    ↓
Notification Log DB (write outcome)
```

Key moves:

- **DB and cache moved out** of the notification server (no SPOF).
- **Notification servers behind autoscaling** — fleet grows with load.
- **Distinct queue per notification type** — an FCM outage backs up *only* the push-Android queue; SMS, email, and iOS push keep flowing.

See [Queues & Messaging](fundamentals/queues-and-messaging.md) for queue patterns.

## 4. Reliability

### 4.1. Notification Log + Retries

Every send attempt writes to a **notification log database**. The worker reads back failed entries and retries with [exponential backoff](fundamentals/resilience-patterns.md). Permanent failures (invalid token, unsubscribed) are marked as such and not retried.

### 4.2. Dedupe by Event ID

The producer attaches an **event ID** to each notification. The worker checks the log before sending; if the event ID has already succeeded, skip. Approximates exactly-once delivery with the cost of a single DB lookup per send.

## 5. Templates and Opt-In

- **Notification templates** prevent re-formatting from scratch. The service stores `welcome_email`, `password_reset`, etc., and the producer fills in variables.
- **Per-channel opt-in** is enforced before every send. The user prefs DB is consulted; a user who opted out of email but kept push gets only the push.

## 6. Rate Limiting Against User Fatigue

A separate concern from infrastructure rate limiting. Over-notification is the fastest way to make users disable the channel entirely (Android settings → "block notifications from this app"). Per-user, per-channel daily caps prevent that. Unrelated to the [Rate Limiter](case-studies/rate-limiter.md) pattern at the API gateway — this one's about user UX.

## Sources

- [Xu Ch 10: Design a Notification System](software/system-design-interview/books/system-design-interview-insiders-guide/ch10_design_a_notification_system.md)
