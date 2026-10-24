*Module 3 · Part A: Virtualization and Resource Management*

# 5. Storage Management

## Virtual disks are files or volumes with a contract

A VM usually sees a virtual disk; the hypervisor maps it to a file, logical volume, or networked block device. This decouples a VM from a particular drive and enables snapshots, cloning, thin provisioning, and migration.

| Technique | Benefit | Caution |
|---|---|---|
| **Thin provisioning** | Allocate physical blocks only when written | Apparent capacity can exceed real capacity |
| **Snapshot** | Point-in-time copy using changed blocks | Long chains can slow I/O and consume space |
| **Clone/template** | Fast duplicate deployment | Patch base images and manage drift |
| **Replication** | Survives device/site failure | Requires consistency and recovery planning |

## I/O performance and durability

Storage performance has throughput, latency, and IOPS dimensions. A database may need low, predictable latency more than large sequential throughput. Write caching can improve speed but must honor flush/barrier requests; otherwise a power failure can acknowledge data that never reached durable media.

## Security perspective

Deleting a virtual disk entry does not necessarily erase its blocks. Use encryption at rest with managed keys, secure disposal procedures, access-controlled snapshots/backups, and audit trails. A snapshot is often a complete copy of secrets and deserves the same protection as the live VM.

---

← [4. Memory Management](04_memory_management.md) · [Contents](README.md) · [6. VLAN and VPN](06_vlan_and_vpn.md) →
