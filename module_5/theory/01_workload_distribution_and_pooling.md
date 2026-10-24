*Module 5 · Part A: Fundamental Architectures*

# 1. Workload Distribution and Resource Pooling

**Workload distribution** assigns incoming work across available compute resources. It prevents one server becoming a bottleneck while others are idle. Distribution can be based on round robin, current connections, measured load, locality, or application-specific rules.

**Resource pooling** groups compute, storage, and network capacity so it can be allocated dynamically to many consumers. Pooling is the architectural basis of multi-tenancy and economies of scale.

> **Simple analogy:** Workload distribution chooses which checkout counter serves the next customer; resource pooling is the supermarket owning a shared set of counters rather than permanently dedicating one to every customer.

Pooling raises utilization, but also creates noisy-neighbour and blast-radius risks. Quotas, reservations, observability, and isolation policies make the pool fair and safe.

---

## Placement policies

A scheduler may pack workloads tightly to free hosts for power saving, or spread them to reduce correlated failure. A three-replica application should use anti-affinity so replicas do not land on one host; a latency-sensitive application and cache may use affinity to remain close. Good placement encodes requirements as policy.

## Measuring fairness and failure domains

Pooling needs measurements: allocated versus used CPU/memory, queue time, storage latency, network saturation, and per-tenant consumption. Quotas cap maximum use, while reservations protect a minimum. Also define the boundary that can fail together: host, rack, zone, or region. Three copies on one host improve little against a host failure, even if a dashboard reports three healthy VMs.

[Contents](README.md) · [2. Scalability and Elasticity](02_scalability_and_elasticity.md) →
