*Module 2 · Part B: Security in Distributed Systems*

# 9. Secure Communication Protocols

The most important one to know by name is **TLS (Transport Layer Security)** — the protocol behind the padlock icon in a browser's address bar, and the thing that makes HTTPS secure. At a conceptual level, a TLS handshake does three things before any real data is sent:

1. **Authenticates the server** (and optionally the client) using a digital certificate — a credential issued by a trusted third party (a Certificate Authority) vouching "this public key really does belong to this domain."
2. **Negotiates a shared symmetric key**, using asymmetric encryption just long enough to exchange that key safely (exactly the "use both together" pattern from the Encryption section above).
3. **Switches to fast symmetric encryption** for the actual conversation, which now also includes integrity checks so any tampering in transit gets detected.

This single protocol is a working example of nearly every concept in this security section at once: Authentication (the certificate), Encryption (both kinds), and Integrity protection (part of the CIA triad) — all bundled into the handshake you've been relying on, invisibly, every time you've visited an `https://` website.

---

← [8. Encryption](08_encryption.md) · [Contents](README.md) · [10. Access Control](10_access_control.md) →
