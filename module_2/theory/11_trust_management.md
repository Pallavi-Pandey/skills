*Module 2 · Part B: Security in Distributed Systems*

# 11. Trust Management

## Deciding whom to believe

In a distributed system, you very often have to grant some level of access to a party you've never directly verified yourself — a new node joining a cluster, a third-party service calling your API, a software update from a vendor. **Trust management** is the set of mechanisms for deciding, and continuously re-evaluating, how much to trust each party.

> **Simple analogy:** You've never met the new tenant who wants to rent your flat. You trust them because their employer vouches for their income, a previous landlord vouches for their behavior, and a government ID vouches for their name. You trust each of those vouchers more than you could ever verify the tenant directly — and if any one of them lied, your whole decision is wrong.

## Trust through authorities: PKI

The classic model is **PKI (Public Key Infrastructure)**: a hierarchy of trusted Certificate Authorities that vouch for identities, which is what makes TLS certificates ([topic 9](09_secure_communication_protocols.md)) actually meaningful — you trust a server's certificate because you trust the CA that issued it, not because you personally verified that server.

The hierarchy is a **chain of trust**. Your operating system and browser ship with a list of more than a hundred **root CAs**. A root signs the certificate of an **intermediate CA**, and the intermediate signs the certificate of the website. Your browser checks each signature up the chain until it reaches a root it already trusts.

PKI also needs a way to take trust back. If a server's private key is stolen, its certificate must be **revoked** before it expires, using **certificate revocation lists (CRLs)** or the **Online Certificate Status Protocol (OCSP)**. In practice, revocation checking is unreliable, which is one reason certificates are now issued with short lifetimes (Let's Encrypt certificates have lasted only 90 days, and lifetimes across the industry are being cut further) — a stolen certificate soon expires on its own.

The weakness of PKI is that *any* trusted CA can issue a certificate for *any* domain. In 2011, attackers broke into **DigiNotar**, a Dutch CA, and issued themselves a valid certificate for `*.google.com`, which was used to intercept the Gmail traffic of hundreds of thousands of users in Iran. Browsers removed DigiNotar from their trusted lists and the company went bankrupt within weeks. A direct response was **Certificate Transparency**: every certificate a CA issues must now be published in public, append-only logs, so a domain owner like Google can spot a certificate they never requested.

## Trust without a central authority

Not every system has, or wants, a central authority:

- **Web of trust** — used by PGP email encryption. Instead of a CA, users sign each other's keys: "I've met this person and this is their key." You trust a key if enough people you already trust have signed it.
- **Reputation-based trust** — used in peer-to-peer networks and marketplaces. Each party's trustworthiness is estimated from its past behavior, as reported by others (seller ratings on an online marketplace, or a peer that keeps delivering corrupt file pieces being dropped by other peers). Reputation systems must defend against **Sybil attacks** ([topic 5](05_threats.md)): fake identities giving each other glowing reviews.
- **Trust on first use** — used by SSH ([topic 9](09_secure_communication_protocols.md)). Trust whatever key you see the first time, and alert if it ever changes.

## Zero Trust

A newer, increasingly dominant model is **Zero Trust**: instead of assuming anything inside your network perimeter is automatically trustworthy (the old "castle and moat" model — hard shell, soft interior), Zero Trust assumes **no implicit trust at all**, anywhere, and re-verifies identity and authorization on every single request, regardless of whether it came from "inside" or "outside" the network. In practice, it combines mutual TLS between every service ([topic 9](09_secure_communication_protocols.md)), short-lived credentials ([topic 6](06_authentication.md)), fine-grained access control on every request ([topic 10](10_access_control.md)), and a check of the requesting device's health.

Google's **BeyondCorp** program, started after the 2009 "Operation Aurora" attacks in which intruders moved freely around its internal network, is the best-known early example: Google employees reach internal applications the same way from the office or a café, and being on the office network grants nothing extra.

## Case Study: The SolarWinds Supply Chain Attack (2020)

Attackers compromised SolarWinds' software build system and inserted malicious code into a legitimate, digitally signed update for its Orion network-monitoring product. The update was then installed — trusted, because it was signed and came from a known vendor — by roughly 18,000 organizations, including US government agencies. This is a **trust management failure at its most severe**: the entire system of "we trust signed updates from known vendors" was turned into the attack vector itself, precisely because downstream organizations had no mechanism to question that trust once it was established.

The signature was genuine. It proved the update came from SolarWinds — not that SolarWinds' build system was uncompromised. Responses since then include **reproducible builds** (anyone can rebuild the software from source and check they get the identical file), **software bills of materials** (a published list of every component inside a piece of software), and frameworks such as **SLSA** for proving how and where software was built.

## Discussion Prompt

Your organization runs a monitoring tool, like SolarWinds Orion, that needs administrator access to every server in order to do its job. You can't simply stop trusting the vendor. What could you do to limit the damage if the vendor were compromised? Things to consider: least privilege for the tool itself ([topic 7](07_authorization.md)), restricting which network destinations it can talk to, delaying updates and testing them first, and monitoring the tool's own behavior ([topic 13](13_auditing_and_monitoring.md)) — in Zero Trust terms, treating even trusted software as something to keep verifying.

---

← [10. Access Control](10_access_control.md) · [Contents](README.md) · [12. Privacy Preserving](12_privacy_preserving.md) →
