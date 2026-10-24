*Module 4 · Part B: Service Deployment Models*

# 8. Hybrid and Community Cloud

A **hybrid cloud** combines two or more distinct environments — commonly private/on-premises infrastructure and public cloud — connected so applications, identities, data, or workloads can interoperate. It is not simply “using two clouds”; it needs deliberate networking, identity, governance, and data-placement design.

A **community cloud** is shared by organizations with common requirements, such as a group of universities, government agencies, or healthcare organizations. It can distribute cost while applying policies tailored to the community.

## The hard part is the boundary

Hybrid designs must decide where authoritative data lives, how identities cross environments, what happens during link failure, and how logs/costs/policies are unified. Use hybrid only when its benefits outweigh that complexity; otherwise a well-designed single environment is usually easier to secure and operate.

---

## Example decision

A hospital might keep its patient-record database in a controlled private environment while using public-cloud capacity for de-identified research analytics. It still needs documented de-identification, encrypted links, least-privilege identities, audit logs, and a rule that prevents raw patient data from reaching analytics.

## Integration patterns

Hybrid applications often connect environments through site-to-site VPNs or private links, federate users through one identity provider, and exchange data by APIs, queues, or controlled replication. Design for link failure: should a public component use cached data, become read-only, or stop safely? A hybrid design with no answer merely moves a single point of failure onto a network connection.

Community clouds also need shared rules for membership, funding, data ownership, incident response, acceptable use, and independent audit. Shared requirements can lower cost, but unclear governance makes a technically sound platform hard to operate.

← [7. Private Cloud](07_private_cloud.md) · [Contents](README.md)
