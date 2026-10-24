*Module 5 · Part C: Specialized Architectures*

# 11. Elastic Network Capacity and Load-Balanced Virtual Switches

**Elastic network capacity** changes available bandwidth, connections, or network functions as demand changes. The goal is to avoid a network becoming the fixed bottleneck after compute instances scale out.

A **virtual switch** connects VM interfaces in software and enforces segmentation, forwarding, and often policy. **Load-balanced virtual switches** distribute traffic or forwarding work across switch instances/paths to improve throughput and resilience.

Network elasticity needs observability: track latency, packet loss, retransmissions, connection counts, and saturation. Scaling bandwidth does not fix an application that opens too many connections or a policy that routes traffic through an overloaded inspection point.

---

## Security controls at the switch

Virtual switches can enforce segmentation close to each workload. Security groups, distributed firewalls, and microsegmentation can limit which services communicate even when they share a subnet. Policy must be centrally managed and logged; manual VM-specific rules drift quickly and are difficult to audit.

## Capacity planning

Scaling compute can shift a bottleneck into the network. Estimate east-west traffic between services as well as north-south user traffic, and account for TLS inspection, NAT, firewalls, and backups. A network diagram should show both the desired logical path and the physical/control-plane dependencies that can limit it.

← [10. Normalization and Tiering](10_data_normalization_and_tiering.md) · [Contents](README.md) · [12. Multipath and Persistent Networks](12_multipath_access_and_persistent_networks.md) →
