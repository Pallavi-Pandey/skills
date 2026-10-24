*Module 3 · Part A: Virtualization and Resource Management*

# 3. CPU Management

## Scheduling time, not creating processors

Each VM sees one or more **virtual CPUs (vCPUs)**. The hypervisor maps those vCPUs onto a smaller or larger pool of physical CPU cores by scheduling short time slices. It must balance responsiveness, fairness, priority, and isolation.

> **Simple analogy:** vCPUs are appointments in a shared meeting room. Giving every team a calendar slot does not create more rooms; poor booking can make everyone wait.

Key controls include:

- **Shares/weights:** relative entitlement when CPUs are contested.
- **Reservations:** guaranteed minimum CPU capacity.
- **Limits/quotas:** ceiling on CPU use to protect neighbours.
- **CPU affinity/pinning:** prefer or bind a vCPU to particular core(s), useful for latency-sensitive workloads.

## Overcommitment and its cost

Administrators may allocate more total vCPUs than physical cores because workloads peak at different times. This **overcommitment** improves utilization, but simultaneous demand causes **CPU ready time**: a VM is runnable but waiting for a physical core. Multi-vCPU guests can also suffer **co-scheduling** delays when they need several vCPUs together.

| Goal | Helpful technique | Trade-off |
|---|---|---|
| High consolidation | Moderate overcommitment | Noisy-neighbour risk |
| Predictable latency | Reservation and pinning | Lower flexibility/utilization |
| Fair multi-tenancy | Shares and quotas | Does not guarantee low latency |

## Security perspective

CPU sharing can leak timing information through caches and speculative execution side channels. Cloud providers mitigate these with microcode/OS updates, scheduling controls, and sometimes dedicated hosts. Treat performance isolation and security isolation as related, but distinct, requirements.

---

← [2. HAL and VMM](02_hardware_abstraction_and_vmm.md) · [Contents](README.md) · [4. Memory Management](04_memory_management.md) →
