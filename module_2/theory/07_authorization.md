*Module 2 · Part B: Security in Distributed Systems*

# 7. Authorization

**Authorization answers the question "now that I know who you are, what are you allowed to do?"** — this is a distinct step that happens *after* authentication, and it's a common mistake to conflate the two. Being logged in (authenticated) doesn't mean you should be able to do everything the system can do.

The foundational principle here is **least privilege**: every user, process, and service should have the minimum set of permissions needed to do its job, and nothing more — so that if that identity is ever compromised, the damage it can do is limited by design, not by luck.

## Discussion Prompt

A company's customer-support tool lets any support agent view *any* customer's full account details, including payment info, "just in case they need it." Using the least-privilege principle, how would you redesign this access model? (Push toward: scope access to only the customer the agent is actively assigned to, time-limit that access, and log every access — a preview of Access Control and Auditing, both coming up next.)

---

← [6. Authentication](06_authentication.md) · [Contents](README.md) · [8. Encryption](08_encryption.md) →
