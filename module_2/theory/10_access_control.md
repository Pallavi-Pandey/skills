*Module 2 · Part B: Security in Distributed Systems*

# 10. Access Control

## Enforcing the rules on every request

While Authorization ([topic 7](07_authorization.md)) defines the *policy* ("what is this user allowed to do?"), **Access Control** is the actual *enforcement mechanism* that checks that policy on every single request. A perfect policy that isn't enforced, or is enforced on only some paths into the system, protects nothing.

> **Simple analogy:** A company's policy document says "only finance staff may enter the finance office." That's authorization. The badge reader on the finance office door, which checks every badge every time the door opens, is access control. And if there's a second, unguarded door at the back, the policy is worthless.

## The reference monitor

The classic way to think about enforcement is the **reference monitor**: a component that sits between every subject (a user or process) and every object (a file, record, or API) and decides each access. A trustworthy reference monitor has three properties:

1. **Always invoked** — there is no path to the object that skips the check.
2. **Tamper-proof** — the subject can't modify or disable it.
3. **Small enough to verify** — simple enough that you can convince yourself it's correct.

Most access control bugs are a violation of the first property: some endpoint, some internal API, some background job, or some direct database connection that nobody remembered to put behind the check.

## Access control lists and capabilities

There are two basic ways to record who can access what:

- **Access Control List (ACL)** — attached to each *object*: "report.pdf: asha can read and write, ravi can read." Easy to answer "who can access this file?" — this is how file permissions on Linux and Windows work.
- **Capability** — held by each *subject*: an unforgeable token saying "the holder of this may read report.pdf." Easy to pass along and to check without a central lookup, which suits distributed systems well. Signed access tokens ([topic 6](06_authentication.md)) and pre-signed download links from cloud storage are capabilities. The downside is revocation: once handed out, a capability works for whoever holds it until it expires.

## Access control models

- **DAC (Discretionary Access Control)** — the owner of a resource decides who else can access it (e.g., sharing a Google Doc with specific people). Flexible, but easy to misconfigure, and one careless owner can expose data the organization cares about.
- **MAC (Mandatory Access Control)** — a central authority sets fixed access rules that users can't override, even for their own resources. Common in military and government systems with classification levels. The best-known MAC model, **Bell-LaPadula**, uses two rules: *no read up* (you can't read data above your clearance) and *no write down* (you can't copy secret data into a less secret document, where lower-cleared people could read it). Linux's SELinux applies mandatory rules to processes.
- **RBAC (Role-Based Access Control)** — permissions are attached to *roles* (e.g., "editor," "admin," "viewer"), and users are assigned roles, rather than permissions being granted to individual users one by one. This is by far the most common model in real distributed systems and cloud platforms, because it scales — you manage a handful of roles instead of thousands of individual permission grants.
- **ABAC (Attribute-Based Access Control)** — decisions are made from *attributes* of the user, the resource, and the situation: "a doctor may read a patient record if the doctor is assigned to that patient, during working hours, from a hospital device." Far more expressive than roles, and it can express need-to-know directly, but the rules are harder to understand and audit.

| Model | Who sets the rules | Strength | Weakness |
|---|---|---|---|
| DAC | Each resource owner | Flexible, simple | Easy to overshare |
| MAC | Central authority | Strong, consistent | Rigid |
| RBAC | Administrators, per role | Scales to large organizations | Roles multiply over time ("role explosion") |
| ABAC | Policy authors | Very fine-grained, context-aware | Complex to write and audit |

A minimal RBAC check fits in a few lines:

```python
ROLE_PERMISSIONS = {
    "viewer": {"read"},
    "editor": {"read", "write"},
    "admin":  {"read", "write", "delete", "manage_users"},
}
USER_ROLES = {
    "asha": {"editor"},
    "ravi": {"viewer"},
}

def is_allowed(user, action):
    for role in USER_ROLES.get(user, set()):
        if action in ROLE_PERMISSIONS[role]:
            return True
    return False                      # default deny

print(is_allowed("asha", "write"))    # True
print(is_allowed("ravi", "write"))    # False
print(is_allowed("mallory", "read"))  # False: unknown users get nothing
```

## Where to enforce in a distributed system

In a system of many services, there are several possible places to put the check: at an **API gateway** at the edge, in a **service mesh** sidecar next to each service, or inside each service's own code. The gateway is convenient but only sees the outside of the system; anything that reaches a service another way — from another internal service, a message queue, or a compromised node — skips it. Robust designs check at the edge *and* in each service, so that getting past one layer isn't enough. The service that owns the data is the only one that can reliably answer questions like "does order 1002 belong to this user?"

## Case Study: First American Financial (2019)

First American, one of the largest US title insurance companies, let customers view their documents through links like `.../documentID=000000075`. A security journalist found that changing the number showed *other* customers' documents — bank account numbers, tax records, Social Security numbers — with no login required. About 885 million records going back to 2003 were exposed this way. The system knew which customer each document belonged to; it simply never checked whether the person asking was that customer.

This is called an **insecure direct object reference**, and it is horizontal privilege escalation ([topic 7](07_authorization.md)) in its simplest form. Broken access control of this kind tops the OWASP Top 10 list of the most critical web application security risks (2021 edition).

---

← [9. Secure Communication Protocols](09_secure_communication_protocols.md) · [Contents](README.md) · [11. Trust Management](11_trust_management.md) →
