*Module 3 · Part A: Virtualization and Resource Management*

# 1. Virtualization Basics

## One computer, many believable computers

**Virtualization** uses software to present a physical resource as one or more logical resources. A single server can therefore run several virtual machines (VMs), each with its own operating system, applications, virtual CPU, memory, disk, and network interface. The guest OS behaves as if it owns a real computer; the host shares the actual hardware underneath.

> **Simple analogy:** A hotel converts one building into many private rooms. Guests have their own key, address, and facilities, even though plumbing, power, and the building structure are shared.

Virtualization is useful because workloads rarely use a whole server continuously. Consolidating them raises utilization, makes isolation and provisioning easier, and allows a VM image to be copied or moved. It also introduces overhead and a larger management/security surface.

| Term | Meaning |
|---|---|
| **Host** | Physical machine providing resources |
| **Guest** | Operating system running inside a VM |
| **VM** | Isolated software-defined computer |
| **Hypervisor** | Software that creates and manages VMs |
| **Container** | Isolated process sharing the host kernel; not a VM |

## Forms of virtualization

- **Server virtualization:** split one server into VMs.
- **Desktop virtualization:** deliver a desktop remotely or as a managed VM.
- **Storage virtualization:** combine physical disks into logical volumes.
- **Network virtualization:** create logical switches, routers, and networks in software.
- **Application/container virtualization:** isolate applications while sharing an OS kernel.

## Security perspective

Isolation is a security promise, not a guarantee. A vulnerable hypervisor, unsafe device passthrough, or misconfigured virtual network can permit **VM escape** or cross-tenant exposure. Strong patching, least privilege for management APIs, and segmentation matter as much as the virtualization technology.

---

[Contents](README.md) · [2. Hardware Abstraction Layer and VMM](02_hardware_abstraction_and_vmm.md) →
