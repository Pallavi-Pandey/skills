*Module 3 · Part C: Information Model for Virtual Machines*

# 9. VM Resource and State Models

## A VM is more than a running guest

An **information model** names the data needed to describe, operate, and govern a VM consistently. It lets an API, scheduler, monitoring system, and administrator discuss the same object without guessing.

The **resource model** describes desired and available capacity: vCPUs, RAM, virtual disks, NICs, accelerators, placement constraints, reservations, and quotas. The **state model** records where a VM is in its operation.

| State | Meaning |
|---|---|
| Provisioning | Resources/image are being prepared |
| Running | Guest is executing |
| Paused/suspended | Execution is stopped; state may be retained |
| Stopped | Guest is off; persistent disks remain |
| Failed/terminated | Instance is unavailable or intentionally removed |

## Desired state versus observed state

Good infrastructure systems track both. The desired state might say “three running web VMs with 2 vCPUs each”; observed state might show one failed. A controller then reconciles the difference. This is the same control-loop idea behind cloud orchestration and Kubernetes.

## Security perspective

VM metadata is sensitive: it reveals topology, IP addresses, attached volumes, image provenance, and often credentials if poorly designed. Treat management-plane read access as privileged, not harmless.

---

← [8. Overlay Networks](08_overlay_networks.md) · [Contents](README.md) · [10. VM Allocation and Template Models](10_vm_allocation_and_template_models.md) →
