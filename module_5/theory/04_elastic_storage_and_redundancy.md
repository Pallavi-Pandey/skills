*Module 5 · Part A: Fundamental Architectures*

# 4. Elastic Disk Provisioning and Redundant Storage

**Elastic disk provisioning** lets a volume's capacity or performance be increased without rebuilding an entire system. Thin provisioning allocates physical blocks only when data is written, improving utilization but requiring careful monitoring so the pool does not run out unexpectedly.

**Redundant storage** keeps additional copies or erasure-coded fragments so data survives device, host, or site failures. Redundancy is not a backup: replication may faithfully copy deletion or corruption; backups provide a recoverable earlier point.

| Goal | Pattern |
|---|---|
| Survive a disk failure | RAID, replication, or erasure coding |
| Recover an earlier version | Snapshot and backup retention |
| Serve low latency | Local replicas or performance tiers |

---

## Consistency versus availability

Synchronous replication can reduce data loss but adds latency and may be unavailable during a link failure. Asynchronous replication is faster and more available, but a disaster can lose the latest acknowledged writes. The correct choice follows the application's recovery point objective and recovery time objective.

## Backup design

Backups need their own retention period, access control, encryption, and restore test. A snapshot can be quick, but it may depend on the original storage system; a copy in a separate account or region better protects against a wider failure. Define which data is backed up, how often, where it is stored, and who has authority to restore it.

← [3. Load Balancing and Bursting](03_load_balancing_and_cloud_bursting.md) · [Contents](README.md) · [5. Hypervisor Clustering](05_hypervisor_clustering_and_virtual_servers.md) →
