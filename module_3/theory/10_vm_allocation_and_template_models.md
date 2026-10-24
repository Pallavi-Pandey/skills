*Module 3 · Part C: Information Model for Virtual Machines*

# 10. VM Allocation and Template Models

## Placement is a constrained decision

The **allocation model** determines where a VM runs and what it receives. A scheduler considers CPU, RAM, storage/network locality, tenant quotas, hardware requirements, affinity/anti-affinity rules, availability zones, and energy/cost policy.

| Rule | Example purpose |
|---|---|
| **Affinity** | Keep an app and its cache close for latency |
| **Anti-affinity** | Put replicas on different hosts to survive host failure |
| **Reservation** | Guarantee capacity for a critical workload |
| **Quota** | Prevent one tenant exhausting a shared pool |

The **template model** describes a reusable starting point: base OS image, virtual hardware, initialization rules, approved software, and version. Templates make provisioning repeatable and fast.

## Immutable base, mutable configuration

Prefer a small, patched, versioned base image plus startup configuration over hand-modifying every long-lived VM. That makes provenance visible and avoids configuration drift. A template is a supply-chain artifact: record who built it, what packages it contains, and whether it is still supported.

## Case study: autoscaling safely

Autoscaling only works if a newly allocated VM is ready to serve consistently. A current template, health checks, capacity-aware placement, and a rollback mechanism matter more than the command that starts an extra VM.

---

← [9. Resource and State Models](09_vm_resource_and_state_models.md) · [Contents](README.md) · [11. VM Performance and Security Models](11_vm_performance_and_security_models.md) →
