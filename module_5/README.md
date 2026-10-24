# Module 5: Cloud Computing Architecture

> **Format:** Theory-led, architecture-focused — patterns, trade-offs, reliability properties, and operational reasoning.
> **Builds on:** Modules 3 and 4: virtual infrastructure plus cloud service/deployment choices.

This module examines the architecture patterns that make a cloud platform scalable, elastic, resilient, and maintainable. The same capabilities that improve availability can also create new operational and security dependencies, so every pattern is considered with its trade-offs.

## Repository Structure

```
module_5/
├── README.md
├── agenda.md
└── theory/
    ├── README.md
    ├── 01_workload_distribution_and_pooling.md
    ├── 02_scalability_and_elasticity.md
    ├── 03_load_balancing_and_cloud_bursting.md
    ├── 04_elastic_storage_and_redundancy.md
    ├── 05_hypervisor_clustering_and_virtual_servers.md
    ├── 06_relocation_zero_downtime_and_balancing.md
    ├── 07_reservation_and_failure_recovery.md
    ├── 08_provisioning_and_storage_workloads.md
    ├── 09_direct_io_and_lun_access.md
    ├── 10_data_normalization_and_tiering.md
    ├── 11_elastic_networks_and_virtual_switches.md
    ├── 12_multipath_access_and_persistent_networks.md
    └── 13_redundant_connections_and_storage_maintenance.md
```

## Learning Outcomes

After this module, students should be able to:

1. Explain the architectural patterns behind workload distribution, pooling, scalability, and elasticity.
2. Evaluate high-availability patterns such as clustering, load balancing, relocation, and failure recovery.
3. Reason about storage, networking, and direct-access designs for performance and resilience.
4. Identify the operational and security trade-offs of advanced cloud architectures.
