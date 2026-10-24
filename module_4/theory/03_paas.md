*Module 4 · Part A: Service Delivery Models*

# 3. Platform as a Service (PaaS)

**PaaS** supplies a managed application platform: operating system, language runtime, middleware, deployment workflow, and often databases or queues. Developers deploy source code or a packaged application; the platform handles servers, patches, and much of the scaling.

PaaS improves delivery speed because teams focus on code and data rather than machine administration. It can also impose limits on languages, runtime versions, networking, and low-level tuning. These limits are intentional: standardization is what lets the provider operate the platform efficiently.

> **Simple analogy:** PaaS is a commercial kitchen. You bring recipes and ingredients; the building, ovens, cleaning, and utilities are provided under rules you did not design.

## Questions before choosing PaaS

- Does the platform support the required language, version, and libraries?
- Can the application be moved if provider-specific APIs become costly?
- How are secrets, logs, backups, and network access configured?
- What are the scaling and concurrency limits?

---

## Example: a student-facing API

For a course-registration API, IaaS requires the team to build servers, patch an OS, install the runtime, and configure deployment. With PaaS, it supplies the application and configuration while the platform operates the runtime. Authentication, input validation, backups, and database design remain the team's responsibility.

## Twelve-factor habits

PaaS works best when an application keeps configuration outside source code, writes logs to standard output, treats databases as attached resources, and does not depend on local persistent files. These habits improve portability. If an application stores sessions only in one server's memory, automated scaling and replacement become unreliable.

Use a secrets service or protected configuration for passwords and API keys; do not put them in source repositories. Deployment logs, build provenance, and role-based permissions should show who released which version and make rollback possible.

← [2. IaaS](02_iaas.md) · [Contents](README.md) · [4. SaaS](04_saas.md) →
