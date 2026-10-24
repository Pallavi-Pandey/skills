*Module 3 · Part A: Virtualization and Resource Management*

# 2. Hardware Abstraction Layer and Virtual Machine Monitor

## The layer between an OS and the machine

A **hardware abstraction layer (HAL)** hides device-specific details behind stable operations: allocate memory, schedule a CPU, write a block, send a packet. Virtualization extends this idea by exposing *virtual* hardware to each guest and mapping it to physical hardware.

The **virtual machine monitor (VMM)**, or **hypervisor**, is the control layer that performs that mapping. It schedules virtual CPUs, translates memory addresses, emulates or safely exposes devices, and enforces isolation.

| Hypervisor type | Where it runs | Typical use |
|---|---|---|
| **Type 1 (bare metal)** | Directly on hardware | Data centers; e.g., ESXi, Hyper-V, Xen/KVM-based hosts |
| **Type 2 (hosted)** | On top of a normal host OS | Development and desktop use; e.g., VirtualBox |

## How the VMM handles privileged work

An OS normally executes privileged instructions to configure hardware. A guest must not directly reconfigure the shared machine. Modern CPUs provide virtualization extensions so sensitive guest operations trap safely to the VMM. The VMM can emulate the request, deny it, or map it to a safe physical operation.

**Paravirtualization** is another approach: a guest is modified to make explicit hypercalls to the hypervisor, often using efficient paravirtual device drivers. In practice, modern platforms commonly combine hardware assistance with paravirtual drivers.

## Case study: live infrastructure maintenance

The VMM makes it possible to move or pause VMs while a physical host is patched. This changes maintenance from “take the application down” to “evacuate workloads, patch, and return capacity.” It is powerful, but only if the control plane, storage, and network are designed for the move.

---

← [1. Virtualization Basics](01_virtualization_basics.md) · [Contents](README.md) · [3. CPU Management](03_cpu_management.md) →
