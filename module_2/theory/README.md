# Module 2 Theory: Fault Tolerance and Security in Distributed Systems

One file per topic. Read them in order, or jump to a single topic — each one ends with links to the previous and next topic.

---

## Part A: Fault Tolerance & Consistency

1. [Fault Classification](01_fault_classification.md)
2. [Fault Tolerance Approaches](02_fault_tolerance_approaches.md)
3. [Consistency](03_consistency.md)

---

## Part B: Security in Distributed Systems

Distributed systems multiply the number of machines, networks, and operators involved in getting work done — and every one of those is a potential point of attack. This part covers the vocabulary and mechanisms used to reason about, and defend, a distributed system.

4. [The CIA Triad](04_the_cia_triad.md)
5. [Threats](05_threats.md)
6. [Authentication](06_authentication.md)
7. [Authorization](07_authorization.md)
8. [Encryption](08_encryption.md)
9. [Secure Communication Protocols](09_secure_communication_protocols.md)
10. [Access Control](10_access_control.md)
11. [Trust Management](11_trust_management.md)
12. [Privacy Preserving](12_privacy_preserving.md)
13. [Auditing and Monitoring](13_auditing_and_monitoring.md)

---

## Summary Table: All Topics at a Glance

| # | Topic | One-line takeaway |
|---|---|---|
| 1 | [Fault Classification](01_fault_classification.md) | Crash faults are honest failures; Byzantine faults actively lie |
| 2 | [Fault Tolerance Approaches](02_fault_tolerance_approaches.md) | Proactive = act before it breaks; Reactive = recover after it breaks |
| 3 | [Consistency / CAP](03_consistency.md) | During a network partition, pick Consistency or Availability — not both |
| 4 | [CIA Triad](04_the_cia_triad.md) | Confidentiality, Integrity, Availability — the three things security protects |
| 5 | [Threats](05_threats.md) | Network threats plus Sybil, insider, and supply chain attacks; STRIDE as a checklist |
| 6 | [Authentication](06_authentication.md) | Proving *who you are*, once, then carrying a credential (Kerberos, tokens, mTLS) |
| 7 | [Authorization](07_authorization.md) | Deciding *what you're allowed to do*: least privilege, delegation, no confused deputies |
| 8 | [Encryption](08_encryption.md) | Symmetric + asymmetric for confidentiality; MACs and signatures for integrity |
| 9 | [Secure Communication Protocols](09_secure_communication_protocols.md) | TLS combines authentication + encryption + integrity in one handshake |
| 10 | [Access Control](10_access_control.md) | Enforcing authorization on every path (ACLs, capabilities, DAC, MAC, RBAC, ABAC) |
| 11 | [Trust Management](11_trust_management.md) | Deciding how much to trust a party you can't personally verify (PKI, reputation, Zero Trust) |
| 12 | [Privacy Preserving](12_privacy_preserving.md) | Limiting what even authorized parties can learn about individuals |
| 13 | [Auditing and Monitoring](13_auditing_and_monitoring.md) | Detecting failures fast, and actually acting on what you detect |
