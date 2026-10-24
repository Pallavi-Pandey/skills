*Module 3 · Part B: Virtual Networks*

# 7. Software-Defined Networking and Network Function Virtualization

## Make policy programmable

**Software-defined networking (SDN)** separates the **data plane** (forward packets) from the **control plane** (decide where packets should go). A controller can express policy centrally and program switches through APIs, rather than requiring an operator to configure every box independently.

**Network function virtualization (NFV)** implements functions traditionally delivered by appliances — firewall, load balancer, router, intrusion detector — as software workloads, called virtual network functions (VNFs) or cloud-native network functions (CNFs).

| Concept | Question it answers |
|---|---|
| SDN | How should forwarding policy be controlled? |
| NFV | Where/how should network services run? |
| Orchestration | How are service chains deployed, scaled, and healed? |

## Benefits and new failure modes

Central policy makes a virtual network easier to automate and adapt. But central control can become a high-value target or a single point of failure. Controllers need authentication, authorization, redundancy, validated changes, and an auditable separation between tenant policy and infrastructure policy.

## Discussion prompt

If one API change can update firewall rules for thousands of workloads, is that safer than manual configuration? It can be — because desired policy is reviewed and repeatable — but only when the API credentials, change process, and rollback path are as carefully designed as the network itself.

---

← [6. VLAN and VPN](06_vlan_and_vpn.md) · [Contents](README.md) · [8. Overlay Networks](08_overlay_networks.md) →
