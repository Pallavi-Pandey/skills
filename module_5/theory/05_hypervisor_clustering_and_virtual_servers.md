*Module 5 · Part B: Advanced Architectures*

# 5. Hypervisor Clustering and Load-Balanced Virtual Server Instances

A **hypervisor cluster** is a coordinated group of hosts sharing management, network, and often storage capabilities. It provides a placement pool for VMs and allows workloads to be moved away from a failed or overloaded host.

**Load-balanced virtual server instances** place several equivalent application VMs behind a load balancer. If one instance fails, the load balancer stops sending it traffic; if demand grows, more instances can be added.

High availability requires eliminating hidden single points of failure: the load balancer, identity provider, storage, DNS, and control plane need appropriate redundancy too. A cluster makes failure recovery possible; it does not by itself guarantee the application is stateless or data-consistent.

---

## Quorum matters

Cluster members need agreement about which hosts are active. A quorum mechanism prevents a network split from letting two sides make conflicting decisions (split brain). Two hosts must not both believe they own the same writable VM disk. Fencing, witness nodes, and tested failover rules matter as much as extra servers.

## Application readiness

Infrastructure failover protects a VM, but an application may still need time to reconnect to a database, rebuild cache, or replay messages. Test the full service path, not only whether a VM starts on another host. A recovery runbook should define who verifies data integrity and how traffic is returned after a failover.

← [4. Elastic Storage](04_elastic_storage_and_redundancy.md) · [Contents](README.md) · [6. Relocation and Zero Downtime](06_relocation_zero_downtime_and_balancing.md) →
