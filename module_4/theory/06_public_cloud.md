*Module 4 · Part B: Service Deployment Models*

# 6. Public Cloud

A **public cloud** is operated by a third-party provider and offered to many customers over shared infrastructure. Tenants receive logically isolated resources, self-service APIs, elastic capacity, and consumption-based pricing.

Public cloud is well suited to variable workloads, rapid experimentation, global delivery, and services that benefit from a large provider ecosystem. Multi-tenancy does not mean data is public: isolation, encryption, identity controls, and contractual obligations separate customers. But customers must understand regional availability, compliance obligations, egress cost, and the shared-responsibility boundary.

## Discussion prompt

Is public cloud automatically less secure than an on-premises data center? Not necessarily. Major providers can invest heavily in physical and platform security; many incidents instead stem from customers exposing storage, credentials, or management interfaces.

---

## Governance essentials

Public-cloud accounts need guardrails from day one: MFA for privileged identities, separate environments, budgets and cost alerts, centrally logged API activity, approved regions, and restrictive defaults for public network access. Governance should be automated policy, not a spreadsheet reviewed after deployment.

## Regions and exit planning

Providers divide infrastructure into geographic regions and isolated availability zones. Replicas across zones can tolerate a facility failure, while multiple regions can help with regional outages or data-residency needs. Distance also adds latency and cost, so multi-region design needs explicit recovery requirements.

Public cloud can introduce dependence on one provider's APIs and identity system. Keep data exportable, document critical dependencies, and decide which components need portable interfaces. Portability is a spectrum; forcing every workload to be provider-neutral can cost more than the risk it avoids.

← [5. XaaS](05_xaas.md) · [Contents](README.md) · [7. Private Cloud](07_private_cloud.md) →
