# Ch 5.12: Security

## Table of Contents

- [1. Security in the Interview](#1-security-in-the-interview)
- [2. API Security Considerations](#2-api-security-considerations)
- [3. Man in the Middle Attack](#3-man-in-the-middle-attack)
- [4. Authentication](#4-authentication)

## 1. Security in the Interview

- **Rarely a core topic** — security spans physical to software, and a generalist system design interview usually tests knowledge rather than problem-solving because most concepts apply uniformly to any question
- **API security is the exception** — end-user APIs are unique to your specific design, so they're worth calling out
- **Appendix material** — the book defers other security topics to an appendix

## 2. API Security Considerations

- **Assume malicious users** — in the interview, think through the worst thing that could happen against each API and describe mitigations
- **Example abuses** — the book walks through four API signatures with concrete attacks:

| API | Attack to think about |
|---|---|
| `transfer_money(amount, user_id, to_user_id)` | Client sets `user_id` and `to_user_id` to anyone — what validation prevents stealing money? |
| `upload_photo(user, photo_bytes)` | User uploads malicious bytes |
| `request_ride(user, from, to)` | User enters a ride from another continent with no intent of being picked up |
| `place_order(user, item, quantity)` | User enters a huge quantity, or orders an item no longer available |

## 3. Man in the Middle Attack

- **Not unique per design, but expected trivia** — the interviewer may quiz on the concept even though it's not design-specific
- **The attack** — an interceptor on the network path captures request contents (username, password, PII); happens frequently on public wifi since anyone can receive the wifi packets
- **Mitigation: Transport Layer Security (TLS)** — packets are encrypted so the interceptor sees only ciphertext
- **TLS key exchange** — client verifies the server's certificate against a certificate authority, then uses the public key to encrypt data; the server decrypts with its private key
- **Don't memorize the flow** — the interviewer is unlikely to quiz the exact steps; just understand the problem TLS solves

## 4. Authentication

- **Core question** — how does the server know the caller is who they claim to be? If the server trusts anyone, any user can transfer money to themselves, request a ride for themselves, or view personal photos of other people
- **Frame the worst-case user story** — mention what a compromised authentication would let an attacker do in your specific design
- **OAuth and tokens** — the client logs in via a protocol like OAuth and maintains a token that identifies them; the token is passed in subsequent calls so the server can verify identity
- **Token refresh** — the system periodically refreshes the token to limit the blast radius if a token is compromised
