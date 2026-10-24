*Module 5 · Part A: Fundamental Architectures*

# 2. Dynamic Scalability and Elastic Resource Capacity

**Scalability** is the ability to handle more work by adding resources. **Vertical scaling** makes one instance larger; **horizontal scaling** adds instances. **Elasticity** adds the time dimension: capacity automatically grows and shrinks to track demand.

An elastic design needs a metric, threshold, provisioning mechanism, health check, and scale-in policy. CPU percentage alone is often weak; queue length, request latency, and business throughput may better represent demand.

| Design choice | Strength | Limitation |
|---|---|---|
| Vertical scaling | Simple application model | Has a hardware limit and may require restart |
| Horizontal scaling | Better resilience and large scale | Needs statelessness or shared state design |
| Elastic scaling | Reduces idle cost | Reacts too slowly if startup is long |

---

## Design for scale-out

Horizontal scaling is simplest when instances are stateless. Store sessions in a shared service, keep uploaded files in object storage, and use a database or queue for durable shared state. If every request must reach one instance because its memory holds important state, an autoscaler cannot safely replace it.

## Autoscaling control loop

An autoscaler observes a metric, compares it to a target, chooses an instance count, and waits for new capacity to become healthy. A scale-out cooldown avoids creating instances for a brief spike; a scale-in delay avoids removing capacity before demand falls. Poor thresholds cause oscillation: add instances, remove them, then immediately add them again.

Load tests should include startup time, dependency limits, and failure behavior, not only throughput. A service may scale from ten to one hundred web instances but still fail because its database connection limit remains fixed.

← [1. Workload Distribution](01_workload_distribution_and_pooling.md) · [Contents](README.md) · [3. Load Balancing and Bursting](03_load_balancing_and_cloud_bursting.md) →
