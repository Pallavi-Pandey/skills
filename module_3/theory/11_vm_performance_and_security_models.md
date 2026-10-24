*Module 3 · Part C: Information Model for Virtual Machines*

# 11. VM Performance and Security Models

## Measuring the service, not merely the host

A **performance model** defines what is measured, its units, collection interval, baseline, and action thresholds. Useful signals include CPU ready time, memory pressure, disk latency/IOPS, network loss/latency, and application response time. A low host CPU number does not prove a service is healthy.

The **security model** defines identities, trust boundaries, permitted operations, network policy, image provenance, encryption/key ownership, logging, and incident response responsibilities.

| Layer | Performance question | Security question |
|---|---|---|
| Host/hypervisor | Is capacity sufficient? | Is the platform patched and access-controlled? |
| VM | Is the guest resource-starved? | Is the OS hardened and monitored? |
| Network | Is the path congested? | Is only authorized traffic permitted? |
| Application | Is user experience acceptable? | Are data and identities protected? |

## Shared responsibility

In a public IaaS cloud, the provider normally secures the physical facilities and core platform; the customer still secures guest OS configuration, identities, data, and application code. Exact boundaries vary by service, so “the cloud provider handles security” is never a sufficient plan.

## Discussion prompt

Which alert is more actionable: “CPU is 90%” or “checkout p99 latency exceeds its SLO while CPU-ready time rises”? The latter connects infrastructure evidence to a user-facing objective.

---

← [10. Allocation and Template Models](10_vm_allocation_and_template_models.md) · [Contents](README.md) · [12. Lifecycle, Persistence, and Migration](12_vm_lifecycle_persistence_and_migration.md) →
