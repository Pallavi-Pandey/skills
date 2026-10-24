*Module 3 · Part B: Virtual Networks*

# 6. Virtual LANs and Virtual Private Networks

## Logical boundaries on shared infrastructure

A **virtual LAN (VLAN)** splits one physical Ethernet network into separate Layer-2 broadcast domains. Frames carry a VLAN tag (commonly IEEE 802.1Q); ports or virtual switch interfaces are assigned to a VLAN. Devices in different VLANs need a router or firewall policy to communicate.

A **virtual private network (VPN)** creates an encrypted, authenticated tunnel over an untrusted network. A site-to-site VPN connects networks; a remote-access VPN connects a user/device to a private network.

| | VLAN | VPN |
|---|---|---|
| Main purpose | Segmentation | Confidential remote connectivity |
| Typical scope | One local switching domain | Across the Internet/WAN |
| Encryption | No | Yes |
| Main threat addressed | Accidental lateral traffic | Eavesdropping/tampering in transit |

## Do not confuse segmentation with security

VLANs are valuable for limiting broadcasts and separating environments, but a VLAN alone is not a complete security boundary. Misconfigured trunks, vulnerable switches, and permissive inter-VLAN routing can defeat the design. Apply firewall rules, identity-aware access, and logging at the boundary.

> **Simple analogy:** VLANs create rooms in the same building; a VPN creates a locked, protected corridor through public streets to reach that building.

---

← [5. Storage Management](05_storage_management.md) · [Contents](README.md) · [7. SDN and NFV](07_sdn_and_nfv.md) →
