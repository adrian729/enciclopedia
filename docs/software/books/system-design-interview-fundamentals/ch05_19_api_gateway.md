# Ch 5.19: API Gateway

## Table of Contents

- [1. What an API Gateway Is](#1-what-an-api-gateway-is)
- [2. When to Use It in the Interview](#2-when-to-use-it-in-the-interview)

## 1. What an API Gateway Is

- **Entry point for APIs** — forwards a given API call to the appropriate microservice for processing
- **Has its own IP** — callers hit the gateway's IP; it sits in front of the internal microservices
- **Main reverse proxy** — fronts most internal microservices, making it the natural place to centralize cross-cutting concerns

## 2. When to Use It in the Interview

- **Adds clarity with multiple microservices** — drawing an API gateway in the diagram makes the routing between client and many backends easier to follow
- **Natural home for cross-cutting features** — if the interviewer asks for a feature that fronts all backends, the API gateway is a possible place to implement it:
  - **Rate limiting**
  - **IP blocklist**
  - **TLS termination**
