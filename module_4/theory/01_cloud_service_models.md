*Module 4 · Part A: Service Delivery Models*

# 1. Cloud Service Models

## The responsibility stack

A cloud service model describes which layer is operated by the provider and which remains the consumer's responsibility. The layers commonly include physical facilities, networking, servers, virtualization, operating system, runtime, application, and data.

| Model | Consumer mainly manages | Provider mainly manages |
|---|---|---|
| IaaS | OS through application/data | Physical infrastructure and virtualization |
| PaaS | Application and data | Infrastructure, OS, and runtime |
| SaaS | Data, identities, and configuration | The complete application and its platform |

> **Simple analogy:** IaaS is renting an unfurnished apartment; PaaS is renting a serviced kitchen where you cook; SaaS is ordering a prepared meal. More provider service means less operational work, but also less freedom to alter the underlying layers.

## Shared responsibility remains

No model removes all security duties. Even in SaaS, a customer must manage identities, access permissions, data classification, retention, and configuration. A provider may secure the platform, while a customer accidentally exposes documents through a permissive sharing policy.

---

## Choosing deliberately

Start with workload requirements, not provider terminology. A team needing kernel modules or a custom network appliance may require IaaS. A standard web API may prefer PaaS; email or HR commonly fits SaaS. Document who patches, backs up, responds to incidents, and approves access.

## A practical comparison exercise

Consider a college that needs email, a student mobile app, and a research-computing cluster. Email is usually SaaS because the institution needs messaging, not mail-server administration. The mobile app may fit PaaS because the team needs to deploy code quickly. The research cluster may need IaaS because researchers require special libraries and hardware. One organization can use several models; the right choice is per workload.

For every candidate service, ask: what data will it store; who administers identities; how is data backed up/exported; what happens during an outage; what limits apply; and how will costs be monitored? The answers turn a service-model label into an operating plan.

[Contents](README.md) · [2. IaaS](02_iaas.md) →
