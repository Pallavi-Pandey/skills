*Module 2 · Part B: Security in Distributed Systems*

# 11. Trust Management

In a distributed system, you very often have to grant some level of access to a party you've never directly verified yourself — a new node joining a cluster, a third-party service calling your API. **Trust management** is the set of mechanisms for deciding, and continuously re-evaluating, how much to trust each party.

The classic model is **PKI (Public Key Infrastructure)**: a hierarchy of trusted Certificate Authorities that vouch for identities, which is what makes TLS certificates ([Section 9](09_secure_communication_protocols.md)) actually meaningful — you trust a server's certificate because you trust the CA that issued it, not because you personally verified that server.

A newer, increasingly dominant model is **Zero Trust**: instead of assuming anything inside your network perimeter is automatically trustworthy (the old "castle and moat" model — hard shell, soft interior), Zero Trust assumes **no implicit trust at all**, anywhere, and re-verifies identity and authorization on every single request, regardless of whether it came from "inside" or "outside" the network.

## Case Study: The SolarWinds Supply Chain Attack (2020)

Attackers compromised SolarWinds' software build system and inserted malicious code into a legitimate, digitally-signed software update, which was then installed — trusted, because it was signed and came from a known vendor — by roughly 18,000 organizations, including US government agencies. This is a **trust management failure at its most severe**: the entire system of "we trust signed updates from known vendors" was turned into the attack vector itself, precisely because downstream organizations had no mechanism to question that trust once it was established.

---

← [10. Access Control](10_access_control.md) · [Contents](README.md) · [12. Privacy Preserving](12_privacy_preserving.md) →
