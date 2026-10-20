*Module 2 · Part B: Security in Distributed Systems*

# 8. Encryption

**Encryption** turns readable data (plaintext) into unreadable data (ciphertext) using a mathematical algorithm and a key, so that anyone who intercepts it without the right key only sees gibberish. There are two fundamentally different families:

- **Symmetric encryption** — the same key both encrypts and decrypts. Fast, but both parties need to somehow already share that key securely (the "key distribution problem").
- **Asymmetric (public-key) encryption** — a mathematically linked key *pair*: a public key (safe to share with anyone, used to encrypt) and a private key (kept secret, used to decrypt). Solves the key-distribution problem, but is computationally much more expensive than symmetric encryption.

In practice, almost every real system uses **both together**: asymmetric encryption to safely exchange a one-time symmetric key, then fast symmetric encryption for the actual bulk of the data — which is exactly what TLS does, covered next.

Two more distinctions worth being precise about: **encryption in transit** (protecting data while it travels across the network — defeats eavesdropping) versus **encryption at rest** (protecting data while it's sitting on a disk somewhere — defeats theft of a stolen hard drive or an unauthorized database copy). A system needs both; having one without the other is a common, serious gap.

## Case Study: The Equifax Breach (2017)

Equifax, a major credit bureau, exposed the sensitive personal data of roughly 147 million people. The root cause was a known, already-patched vulnerability in a web framework that Equifax simply hadn't updated — but what made it catastrophic rather than merely bad was that a large amount of the exposed data was stored **unencrypted**. Encryption at rest wouldn't have stopped the initial breach, but it would have made the stolen data largely useless to the attackers. This is a frequently cited case for exactly the "defense in depth" principle: multiple independent security layers, so that one failure doesn't mean total compromise.

---

← [7. Authorization](07_authorization.md) · [Contents](README.md) · [9. Secure Communication Protocols](09_secure_communication_protocols.md) →
