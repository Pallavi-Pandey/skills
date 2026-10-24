*Module 5 · Part A: Fundamental Architectures*

# 3. Service Load Balancing and Cloud Bursting

A **load balancer** accepts requests and forwards them to healthy service instances. It can operate at network level (Layer 4) or inspect HTTP/application information (Layer 7). Health checks remove failed targets before users repeatedly reach them.

**Cloud bursting** handles a peak by extending a private or primary environment into additional public-cloud capacity. It is attractive for periodic demand, but requires portable workloads, secure network connectivity, compatible data access, and predictable cost.

The hard problem is usually state: a stateless web tier can burst easily, while a database with large sensitive data may not. Design the application to externalize session state and clarify data consistency before promising burst capacity.

---

## Traffic controls

Load balancers can terminate TLS, enforce rate limits, route by URL path, and gradually send a small percentage of traffic to a new version. These controls make them security- and availability-critical. Protect configuration APIs, test health checks, and ensure a health check validates meaningful readiness rather than merely proving a process exists.

## Session and cost decisions

Some applications use sticky sessions so the same user reaches the same instance. This eases legacy migration but weakens balancing and recovery; prefer external session storage so any healthy instance can serve a request. Cloud bursting also needs a threshold that considers cost as well as performance. A short queue may be cheaper to tolerate than launching expensive capacity, while a patient-facing service may justify rapid expansion.

← [2. Scalability and Elasticity](02_scalability_and_elasticity.md) · [Contents](README.md) · [4. Elastic Storage and Redundancy](04_elastic_storage_and_redundancy.md) →
