*Module 2 · Part B: Security in Distributed Systems*

# 6. Authentication

**Authentication answers the question "who are you?"** — proving an identity before any access is granted. In a distributed system, this has to happen over a network, between parties who may never have physically met, which is fundamentally harder than a security guard checking a photo ID in person.

Common mechanisms: passwords (the weakest, most phishable option), multi-factor authentication (MFA — something you know + something you have/are), and certificate-based authentication (a cryptographic proof of identity, covered more in Secure Communication Protocols below).

## Case Study: The Mirai Botnet

In 2016, the Mirai botnet compromised hundreds of thousands of IoT devices (security cameras, routers) not through some sophisticated exploit, but simply by trying a list of ~60 **default factory username/password combinations** that device owners had never bothered to change. It then used that botnet to launch one of the largest DDoS attacks in history, taking down major internet services. A single missing authentication discipline — "require users to change the default password" — cascaded into an availability attack on a huge portion of the internet.

---

← [5. Threats](05_threats.md) · [Contents](README.md) · [7. Authorization](07_authorization.md) →
