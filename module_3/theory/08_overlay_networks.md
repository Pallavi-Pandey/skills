*Module 3 · Part B: Virtual Networks*

# 8. Overlay Networks

## A network built on top of another network

An **overlay network** encapsulates one packet inside another so that a logical network can cross an existing IP network (the underlay). Endpoints such as virtual switches add/remove the encapsulation. Technologies such as VXLAN provide many isolated logical segments without requiring every physical switch to understand every tenant network.

> **Simple analogy:** The underlay is the postal system; an overlay is a set of labelled inner envelopes. The post office delivers the outer envelope, while the labels inside decide which private organization receives it.

## Why clouds use overlays

- Tenant networks can use overlapping private IP ranges.
- A workload can retain its logical network while moving hosts.
- Network policy can follow the workload rather than a physical port.
- Operators avoid exhausting the roughly 4,000 VLAN identifiers.

## Trade-offs

Encapsulation adds headers and troubleshooting layers. The underlay must have sufficient MTU and reliable IP reachability; otherwise fragmentation or dropped oversized packets produce mysterious failures. Observability needs to connect an overlay identity to the underlay path.

## Security perspective

An overlay is not automatically encrypted. Encrypt traffic when its path or threat model requires it, authenticate the control plane that distributes endpoint mappings, and enforce policies at workload interfaces to prevent spoofing or unintended lateral movement.

---

← [7. SDN and NFV](07_sdn_and_nfv.md) · [Contents](README.md) · [9. VM Resource and State Models](09_vm_resource_and_state_models.md) →
