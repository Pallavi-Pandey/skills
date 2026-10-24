*Module 5 · Part C: Specialized Architectures*

# 13. Redundant Physical Connections and Storage Maintenance Windows

**Redundant physical connections for virtual servers** use multiple NICs, switches, links, and paths so one cable, port, or switch failure does not isolate a workload. The logical virtual network must be designed to use those paths correctly; redundant hardware with a shared single point upstream is only partial redundancy.

A **storage maintenance window** is a controlled period for firmware updates, capacity work, repairs, or configuration changes. Mature clouds reduce or hide maintenance disruption through replication, failover, migration, and advance notification — but maintenance still needs a tested plan and a rollback path.

## Final takeaway

Cloud architecture is not a list of features. Each pattern is a deliberate trade: more availability may require more replicas; more performance may reduce portability; more automation increases the importance of safe control planes. Design from workload requirements, failure assumptions, and security boundaries.

---

## Maintenance communication

Even with redundant designs, communicate maintenance windows, affected services, expected behavior, and rollback criteria. Monitor before, during, and after the change. If an operator cannot quickly identify owners, dependencies, and rollback steps, the architecture is not operationally ready.

## Change safety

Use a maintenance checklist: confirm backup/recovery status, verify redundant paths are healthy, capture baselines, make one reversible change at a time, and define the condition that triggers rollback. Post-maintenance verification should include user-facing tests, not only an infrastructure green status.

← [12. Multipath and Persistent Networks](12_multipath_access_and_persistent_networks.md) · [Contents](README.md)
