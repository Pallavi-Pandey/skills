*Module 2 · Part B: Security in Distributed Systems*

# 13. Auditing and Monitoring

Every mechanism above is about *prevention* — but prevention eventually fails, somewhere, for someone. **Auditing and monitoring** is the discipline of **detecting** that failure as fast as possible, and having a reliable record of what happened.

- **Logging** — recording security-relevant events (logins, access attempts, permission changes) as they happen.
- **Monitoring / SIEM (Security Information and Event Management)** — continuously analyzing those logs, often in real time, to spot suspicious patterns (e.g., one account logging in from two countries five minutes apart).
- **Auditing** — a more deliberate, often periodic review of logs and access records, frequently required for regulatory compliance, to answer the question "who accessed what, and was that appropriate?" after the fact.

## Case Study: The Target Breach (2013)

Target's security monitoring systems **did** detect the malware used in a breach that eventually exposed roughly 40 million customers' credit card data — the alerts fired, correctly, during the attack. The failure was organizational, not technical: the alerts were seen and not acted on in time. This is one of the most cited lessons in this entire topic: monitoring that nobody actually responds to provides close to zero real protection. Detection and response have to be treated as one system, not two separate boxes to check.

## Tying it back to Part A

A monitoring system that detects a compromised node is, functionally, doing the same job as a crash-fault detector from [Section 1](01_fault_classification.md) — both are asking "is this node behaving the way it's supposed to?" and triggering a response when the answer is no. The difference is just *what kind* of misbehavior you're watching for: Part A's fault tolerance mainly watches for nodes that have gone silent or degraded; Part B's security monitoring mainly watches for nodes that have been taken over by someone else. By the end of this module, it should be clear these were never really two separate subjects — they're the same discipline (keeping a system trustworthy despite components you can't fully control) viewed from two different angles.

---

← [12. Privacy Preserving](12_privacy_preserving.md) · [Contents](README.md)
