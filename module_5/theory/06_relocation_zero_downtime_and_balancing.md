*Module 5 · Part B: Advanced Architectures*

# 6. Non-Disruptive Relocation, Zero Downtime, and Cloud Balancing

**Non-disruptive service relocation** moves a workload between hosts with little or no visible outage, commonly through VM live migration or application-level rolling replacement. It supports maintenance, power optimization, and proactive failure avoidance.

**Zero downtime** is an availability objective, not a button. It needs redundant instances, compatible data migrations, traffic draining, health checks, rollback, and monitoring. Some changes — especially schema or protocol changes — cannot be safely made without planning for old and new versions to coexist.

**Cloud balancing** extends placement decisions across pools, zones, or clouds. It can improve resilience, but cross-site latency, data gravity, and inconsistent controls can make a multi-cloud design worse than a well-operated single cloud.

---

## Maintenance workflow

A non-disruptive workflow marks a host unschedulable, drains or migrates workloads, verifies it is empty, applies changes, runs health checks, and returns it to the pool. Automating each stage creates an audit trail and avoids starting maintenance while a critical workload still uses the host.

## Deployment versus migration

Live VM migration is useful for infrastructure maintenance, whereas rolling deployments replace application versions gradually. Both need traffic draining and rollback. A database schema change is especially risky: old and new application versions may need to coexist, so the schema must remain compatible until the rollout completes.

← [5. Hypervisor Clustering](05_hypervisor_clustering_and_virtual_servers.md) · [Contents](README.md) · [7. Reservation and Recovery](07_reservation_and_failure_recovery.md) →
