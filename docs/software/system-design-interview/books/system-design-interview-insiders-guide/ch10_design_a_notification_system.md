# Ch 10: Design a Notification System

## Table of Contents

- [1. Requirements and Scale](#1-requirements-and-scale)
- [2. Notification Types](#2-notification-types)
- [3. Contact Info Gathering](#3-contact-info-gathering)
- [4. Initial Design and Its Problems](#4-initial-design-and-its-problems)
- [5. Improved High-Level Design](#5-improved-high-level-design)
- [6. End-to-End Sending Flow](#6-end-to-end-sending-flow)
- [7. Reliability](#7-reliability)
- [8. Notification Templates](#8-notification-templates)
- [9. Notification Settings](#9-notification-settings)
- [10. Rate Limiting](#10-rate-limiting)
- [11. Retry Mechanism](#11-retry-mechanism)
- [12. Security](#12-security)
- [13. Monitoring and Event Tracking](#13-monitoring-and-event-tracking)
- [14. Wrap Up](#14-wrap-up)

## 1. Requirements and Scale

- **Three formats** — mobile push notification, SMS message, and email; the system must support all three
- **Soft real-time** — deliver as soon as possible; slight delay acceptable under high workload
- **Devices** — iOS, Android, laptop/desktop
- **Triggers** — client applications and server-side scheduled jobs
- **Opt-out** — users who opt out must stop receiving notifications
- **Volume target** — 10M push notifications/day, 1M SMS/day, 5M emails/day

## 2. Notification Types

- **iOS push** — three components: a **provider** that builds requests with a **device token** (unique per-device identifier) and **payload** (JSON dictionary), **APNS** (Apple Push Notification Service) which propagates to devices, and the iOS device itself
- **Android push** — same pattern as iOS but uses **Firebase Cloud Messaging (FCM)** instead of APNS
- **SMS** — typically delegated to commercial third-party services like Twilio or Nexmo
- **Email** — companies can set up their own email servers, but most use commercial services like Sendgrid or Mailchimp for better delivery rate and data analytics

## 3. Contact Info Gathering

- **Collection point** — when a user installs the app or signs up, API servers capture and persist contact info (email, phone, device tokens)
- **Schema** — emails and phone numbers live in the **user table**; device tokens live in a separate **device table** because one user can have multiple devices, so a single push can fan out to all of them

## 4. Initial Design and Its Problems

- **Setup** — services 1..N → single notification server → third-party services (APNS, FCM, SMS, Email) → user devices
- **SPOF** — a single notification server is a single point of failure
- **Hard to scale** — DB, cache, and notification logic in one server can't scale independently
- **Performance bottleneck** — building HTML pages and waiting on third-party responses overloads one box at peak

## 5. Improved High-Level Design

- **Move database and cache out** — notification servers become stateless and scalable
- **Horizontal scaling** — multiple notification servers behind autoscaling
- **Message queues for decoupling** — one **distinct queue per notification type** so an outage in one third-party service (e.g., FCM) doesn't block the others
- **Notification servers** — expose APIs (internal/verified-client only to prevent spam), validate emails/phone numbers, fetch render data from cache/DB, and push notification events onto the right queue
- **Cache** — user info, device info, and notification templates
- **DB** — users, notifications, settings
- **Workers** — pull notification events from queues and dispatch to the corresponding third-party service

## 6. End-to-End Sending Flow

1. A service calls the notification servers' API
2. Servers fetch user info, device token, and settings from cache/DB
3. The notification event is routed to the queue matching its type (e.g., iOS PN queue)
4. Workers pull events from the queue
5. Workers send to the third-party service
6. The third-party service delivers to the user device

## 7. Reliability

- **No data loss** — notifications can be delayed or reordered, but never lost; achieved by persisting events in a **notification log database** and retrying on failure
- **Exactly-once?** — not guaranteed in distributed systems; the system reduces duplicates with a **dedupe mechanism** keyed on event ID — first arrival is processed, subsequent arrivals with the same ID are discarded

## 8. Notification Templates

- **Why** — millions of notifications/day share similar formats; building each from scratch is wasteful
- **What it is** — a preformatted notification with parameter slots for content, styling, tracking links
- **Benefits** — consistent format across channels, fewer formatting errors, faster authoring
- **Example body** — `You dreamed of it. We dared it. [ITEM NAME] is back — only until [DATE].` with CTA `Order Now. Or, Save My [ITEM NAME]`

## 9. Notification Settings

- **Why** — users get overwhelmed by volume, so apps offer fine-grained per-channel control
- **Schema** — `user_id` (bigInt), `channel` (push/email/SMS), `opt_in` (boolean)
- **Enforcement** — check opt-in for the relevant channel before sending any notification

## 10. Rate Limiting

- **Frequency cap** — limit how many notifications a user can receive
- **Why it matters** — if you send too often, receivers could turn off notifications completely

## 11. Retry Mechanism

- **On failure** — third-party send failure puts the event back on the message queue for retry
- **Persistent failure** — after repeated retries, alert developers

## 12. Security

- **appKey / appSecret** — iOS and Android push notification APIs are gated by an appKey/appSecret pair, so only authenticated/verified clients can submit notifications

## 13. Monitoring and Event Tracking

- **Queue depth** — total queued notifications is the key health metric; large backlog means workers can't keep up and more workers must be added to avoid delivery delay
- **Event tracking** — analytics service captures metrics like **open rate**, **click rate**, and **engagement**, which are important for understanding customer behaviors

## 14. Wrap Up

- **Reliability** — robust retry mechanism minimizes failure rate
- **Security** — appKey/appSecret pair restricts senders to verified clients
- **Tracking and monitoring** — instrumented at every stage of the flow
- **Respect user settings** — always check opt-in before sending
- **Rate limiting** — frequency capping prevents user fatigue
