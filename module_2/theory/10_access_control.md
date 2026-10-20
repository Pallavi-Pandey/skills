*Module 2 · Part B: Security in Distributed Systems*

# 10. Access Control

While Authorization defines the *policy* ("what is this user allowed to do?"), **Access Control** is the actual *enforcement mechanism* that checks that policy on every single request. Three common models:

- **DAC (Discretionary Access Control)** — the owner of a resource decides who else can access it (e.g., sharing a Google Doc with specific people). Flexible, but easy to misconfigure.
- **MAC (Mandatory Access Control)** — a central authority sets fixed access rules that users can't override, even for their own resources (common in military/government systems with classification levels).
- **RBAC (Role-Based Access Control)** — permissions are attached to *roles* (e.g., "editor," "admin," "viewer"), and users are assigned roles, rather than permissions being granted to individual users one by one. This is by far the most common model in real distributed systems and cloud platforms, because it scales — you manage a handful of roles instead of thousands of individual permission grants.

---

← [9. Secure Communication Protocols](09_secure_communication_protocols.md) · [Contents](README.md) · [11. Trust Management](11_trust_management.md) →
