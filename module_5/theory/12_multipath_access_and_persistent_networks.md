*Module 5 · Part C: Specialized Architectures*

# 12. Multipath Resource Access and Persistent Virtual Network Configuration

**Multipath resource access** provides more than one route from a server to a storage or network resource. If one path fails, I/O can continue through another; paths may also share load. Multipath designs need consistent identifiers and careful failover testing so a transient path failure does not corrupt writes.

**Persistent virtual network configuration** preserves a workload's logical connectivity — addresses, segments, policies, and service identity — across restart, migration, or host replacement. It separates application identity from a particular physical switch port.

These patterns make infrastructure less fragile, but stale routes, asymmetric paths, and duplicate configuration can create hard-to-debug outages. Treat network configuration as versioned, reviewed infrastructure code.

---

## Test the failure, not just the design

Redundancy is proven only when a path is removed and the workload continues correctly. Test link loss, switch loss, route withdrawal, and recovery under realistic I/O. Record expected failover time and application behavior so an unnoticed configuration error is not discovered during an outage.

## Configuration recovery

Back up and version-control virtual network definitions, route policies, and access rules. A replacement host should receive the intended network configuration automatically rather than depend on a remembered manual command. Persistent configuration is also valuable for incident investigation because it shows what policy was active at a particular time.

← [11. Elastic Networks and Virtual Switches](11_elastic_networks_and_virtual_switches.md) · [Contents](README.md) · [13. Redundant Connections and Storage Maintenance](13_redundant_connections_and_storage_maintenance.md) →
