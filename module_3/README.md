# Module 3: Virtualization and Cloud Computing

> **Format:** Theory-led, discussion-driven — short explanations, architecture sketches, trade-offs, and case studies rather than platform-specific labs.
> **Audience:** M.Tech Cyber Security students.
> **Builds on:** Modules 1 and 2: distributed-system communication, failures, security, and resource trade-offs.

Virtualization is the layer that lets one physical machine safely act like many independent computers. Cloud computing turns that capability into an on-demand service: resources can be requested, pooled, measured, and released through an API. This module explains both the machinery beneath a cloud and the models used to reason about it.

## Repository Structure

```
module_3/
├── README.md
├── agenda.md                         ← Original syllabus
└── theory/                           ← One self-contained topic per file
    ├── README.md
    ├── 01_virtualization_basics.md
    ├── 02_hardware_abstraction_and_vmm.md
    ├── 03_cpu_management.md
    ├── 04_memory_management.md
    ├── 05_storage_management.md
    ├── 06_vlan_and_vpn.md
    ├── 07_sdn_and_nfv.md
    ├── 08_overlay_networks.md
    ├── 09_vm_resource_and_state_models.md
    ├── 10_vm_allocation_and_template_models.md
    ├── 11_vm_performance_and_security_models.md
    ├── 12_vm_lifecycle_persistence_and_migration.md
    ├── 13_cloud_computing_basics.md
    └── 14_cloud_mathematical_models.md
```

## How to Use This Module

Start with [theory/README.md](theory/README.md) and read in order. Topics 1–5 establish the compute, memory, and storage foundations; 6–8 cover virtual networking; 9–12 describe a VM as a managed information object; and 13–14 introduce cloud computing and its capacity/cost models.

## Beginner Project

[Secure Cloud VM Manager](../Projects/project_secure_cloud_manager/README.md) is a small runnable project that combines Module 1's TCP client-server and concurrency patterns with Module 2's authentication, role-based authorization, integrity-protected audit logging, and availability/resource checks. It lives in the repository-level [`Projects/`](../Projects/) folder so course projects remain separate from module theory. It simulates a cloud VM control plane in plain Python; no Docker or cloud account is required.

## Session Breakdown

| Session | Covers | Topic files |
|---|---|---|
| **1: Virtualization foundations** | Hypervisors and management of CPU, memory, and storage | [01](theory/01_virtualization_basics.md)–[05](theory/05_storage_management.md) |
| **2: Virtual networking** | VLANs, VPNs, SDN, NFV, and overlays | [06](theory/06_vlan_and_vpn.md)–[08](theory/08_overlay_networks.md) |
| **3: VM models and cloud** | VM metadata/lifecycle, cloud characteristics, modelling demand and capacity | [09](theory/09_vm_resource_and_state_models.md)–[14](theory/14_cloud_mathematical_models.md) |

## Learning Outcomes

After this module, students should be able to:

1. Explain how hypervisors abstract hardware and isolate virtual machines.
2. Compare CPU, memory, and storage virtualization trade-offs.
3. Design the network building blocks for a tenant-isolated virtual environment.
4. Interpret VM resource, state, allocation, security, persistence, and migration models.
5. Distinguish cloud characteristics from virtualization alone and reason about cloud capacity, utilization, and cost.
