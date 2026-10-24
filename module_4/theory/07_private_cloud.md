*Module 4 · Part B: Service Deployment Models*

# 7. Private Cloud

A **private cloud** provides cloud-style resource pooling, automation, and self-service for one organization. It may run in that organization's facilities or be hosted by a third party, but the infrastructure is dedicated to one tenant.

Private cloud can help with strict data residency, specialized hardware, predictable workloads, or legacy integration. It does not automatically mean lower cost or better security: the organization must fund capacity for peaks, operate the platform, patch the control plane, and maintain disaster recovery.

| Benefit | Cost |
|---|---|
| More control over location, hardware, and policy | Less elasticity and more operational responsibility |
| Easier integration with internal systems | Capacity may sit idle |

---

## Private cloud is an operating model

Simply owning servers is not private cloud. A private cloud normally offers a self-service portal/API, pooled resources, measured usage, automated provisioning, and standardized templates. Without these, it is traditional infrastructure operated manually; cloud benefits require automation and a capable operations team.

## Capacity and security

Private-cloud capacity must be bought before demand arrives. Plan for normal demand, growth, maintenance headroom, and failures, then decide safe CPU, memory, and storage overcommitment. Dedicated infrastructure can simplify some compliance boundaries, but it does not make weak identity, unpatched control planes, or missing backups safe. The organization owns more of the security stack and must operate it continuously.

← [6. Public Cloud](06_public_cloud.md) · [Contents](README.md) · [8. Hybrid and Community Cloud](08_hybrid_and_community_cloud.md) →
