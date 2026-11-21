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

## Beginner Projects

Three runnable projects apply this module's ideas, at increasing scope. They live in the repository-level [`Projects/`](../Projects/) folder so course projects remain separate from module theory.

**[Mini Hypervisor Simulator](../Projects/project_mini_hypervisor/README.md)** — Module 3 only. A single Python program that models one physical host's vCPU/memory pool and the full VM lifecycle (create, start, pause, resume, stop, delete), including overcommitment, templates, and utilization reporting. No networking, security, Docker, or cloud account required — just this module's concepts, interactively, in one class session.

**[Secure Cloud VM Manager](../Projects/project_secure_cloud_manager/README.md)** — Modules 1–3 combined. Runs as a real TCP client and server (two terminals on one machine): a client logs in, then asks the server to create/list/delete VMs. It layers Module 1's networked client-server protocol and lock-protected concurrency, Module 2's authentication, role-based authorization, and HMAC-signed audit log, on top of this module's VM resource pool and capacity checks. Use this once Modules 1 and 2 have also been covered — it's the integrative, capstone-style version.

**[Secure Cloud VM Manager — Docker version](../Projects/project_secure_cloud_manager_docker/README.md)** — the exact same application as above, but the server and each client run in *separate Docker containers* connected by a private Compose network, so a client reaches the server by service name (`cloud-server`) instead of `localhost`. This is the one to reach for when you specifically want Module 3's virtual networking (and the fact that it's a real network hop, not just your laptop) to be visible — at the cost of needing Docker installed.

In short: start with the Mini Hypervisor Simulator right after this module's theory; move to the Secure Cloud VM Manager (plain or Docker) later, as a bigger exercise once students have also seen Modules 1 and 2.

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
