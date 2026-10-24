*Module 5 · Part C: Specialized Architectures*

# 9. Direct I/O Access and Direct LUN Access

**Direct I/O access** lets a VM or workload use hardware with fewer virtualization layers, often through device passthrough or SR-IOV. **Direct LUN access** exposes a storage logical unit directly to a workload rather than presenting a conventional virtual disk.

These patterns can reduce latency and increase throughput for databases, high-performance computing, or network appliances. They also reduce portability: live migration, snapshots, simple backup workflows, and multi-tenant isolation may become harder.

Use direct access only after measuring a real bottleneck. The fastest path should still be controlled by least privilege, IOMMU/device isolation, approved drivers, and clear ownership of the storage data.

---

## Decision checklist

Ask whether the latency improvement is measurable, whether backup and disaster-recovery tools support the direct device, and whether the workload can still be migrated or replaced quickly. A direct LUN may suit one database but be inappropriate for short-lived, horizontally scaled application instances.

## Operational ownership

Direct devices blur the usual boundary between the VM administrator and infrastructure team. Record who creates the mapping, who may resize it, how access is revoked, and how data is securely erased. Without clear ownership, a performance optimization can become an untracked path to sensitive storage.

← [8. Provisioning and Storage Workloads](08_provisioning_and_storage_workloads.md) · [Contents](README.md) · [10. Normalization and Tiering](10_data_normalization_and_tiering.md) →
