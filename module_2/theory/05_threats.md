*Module 2 · Part B: Security in Distributed Systems*

# 5. Threats

A **threat** is anything that could cause harm to the CIA triad. Distributed systems introduce threat categories that simply don't exist on a single standalone machine, because there's now a network in between every component:

- **Eavesdropping** — silently reading traffic in transit (breaks Confidentiality).
- **Tampering** — modifying data or messages in transit (breaks Integrity).
- **Spoofing** — pretending to be a different, trusted node or user.
- **Replay attacks** — capturing a legitimate message and resending it later to trigger the same effect again (e.g., resending a captured "transfer $100" request).
- **Denial of Service (DoS/DDoS)** — overwhelming a system with traffic or requests until legitimate users can't get through (breaks Availability).
- **Man-in-the-middle (MITM)** — an attacker secretly sits between two communicating parties, able to eavesdrop and tamper at will, while both sides believe they're talking directly to each other.

A useful mental model (from Microsoft's threat-modeling framework, **STRIDE**) is that almost every distributed-systems attack is one of: **S**poofing, **T**ampering, **R**epudiation (denying you did something), **I**nformation disclosure, **D**enial of service, or **E**levation of privilege.

---

← [4. The CIA Triad](04_the_cia_triad.md) · [Contents](README.md) · [6. Authentication](06_authentication.md) →
