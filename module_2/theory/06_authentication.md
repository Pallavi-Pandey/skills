*Module 2 · Part B: Security in Distributed Systems*

# 6. Authentication

## Proving who you are

**Authentication answers the question "who are you?"** — proving an identity before any access is granted. In a distributed system, this has to happen over a network, between parties who may never have physically met, which is fundamentally harder than a security guard checking a photo ID in person. And it isn't only people who authenticate: a payment service calling an inventory service has to prove it really is the payment service.

> **Simple analogy:** Checking into a hotel, you show your ID at the front desk once. The desk gives you a key card, and from then on every door in the hotel checks the card, not your ID. Most distributed authentication works exactly like this: prove your identity once to a trusted service, receive a short-lived credential, and present that credential everywhere else.

## Authentication factors

Every authentication method relies on one or more **factors**:

- **Something you know** — a password or PIN.
- **Something you have** — a phone receiving a one-time code, a hardware security key, a smart card.
- **Something you are** — a fingerprint or face scan.

**Multi-factor authentication (MFA)** combines two or more *different* factors, so a stolen password alone isn't enough. (A password plus a security question is still one factor — both are things you know.)

## Storing passwords safely

A server should never store passwords themselves. It stores a **salted, slow hash** of each one: a random salt is added to the password, and the result is run through a function deliberately designed to be slow (bcrypt, scrypt, Argon2, or PBKDF2). At login, the server repeats the same calculation and compares the results.

```python
import hashlib, hmac, os

salt = os.urandom(16)                     # random, different for every user
stored = hashlib.pbkdf2_hmac("sha256", b"correct horse battery staple", salt, 600_000)

# later, at login:
attempt = hashlib.pbkdf2_hmac("sha256", b"correct horse battery staple", salt, 600_000)
print(hmac.compare_digest(stored, attempt))   # True
```

The salt means two users with the same password get different hashes, so an attacker can't crack them all at once with a precomputed table. The 600,000 rounds make each guess slow, so testing billions of candidate passwords against a stolen database becomes impractical.

## Authentication across many machines

Logging in separately to every service would be unusable, and giving every service a copy of every password would be dangerous. Distributed systems instead use a trusted third party that does the checking once and hands out credentials.

**Kerberos** is the classic design, and still what Windows Active Directory networks use today. A central **Key Distribution Center (KDC)** checks your password once and gives you a **ticket-granting ticket**. When you want to use a service, you show that ticket to the KDC and get a **service ticket** for just that one service. Your password is never sent over the network, and services never see it. Tickets expire after a few hours, and because they contain timestamps, Kerberos requires every machine's clock to be closely in sync — another place where distributed time matters.

**Tokens** are the modern web equivalent. After you log in, an identity provider issues a signed token, often a **JWT (JSON Web Token)**: three base64-encoded parts — a header, a payload with claims such as `{"sub": "asha", "role": "editor", "exp": 1767225600}`, and a signature. Any service holding the identity provider's public key can verify the signature on its own, without calling back to a central server — which is exactly why tokens suit distributed systems. Two things to keep in mind: a JWT is *signed, not encrypted*, so anyone holding one can read its contents; and because services don't check back with anyone, a stolen token keeps working until it expires, which is why lifetimes are kept short.

**Single sign-on (SSO)** builds on these ideas: you log in once to an identity provider (your university or company account, or "Sign in with Google") and are trusted by many separate applications. The common protocols are **OpenID Connect**, which handles authentication, built on top of **OAuth 2.0**, which handles delegating access (more in [topic 7](07_authorization.md)).

**Mutual TLS (mTLS)** is how services authenticate *each other*. In ordinary TLS, only the server presents a certificate. In mTLS, the client presents one too, so both sides prove their identity cryptographically before any data flows. Service meshes such as Istio and Linkerd turn this on automatically between every pair of microservices.

| Method | Who authenticates | Credential | Typical use |
|---|---|---|---|
| Password + MFA | Person | Secret + device | Logging in to any account |
| Kerberos | Person or service | Tickets from a KDC | Enterprise networks, Active Directory |
| JWT / OpenID Connect | Person (via an app) | Signed token | Web and mobile apps, SSO |
| Mutual TLS | Service | Certificate | Microservices talking to each other |

## Case Study: The Mirai Botnet

In 2016, the Mirai botnet compromised hundreds of thousands of IoT devices (security cameras, routers) not through some sophisticated exploit, but simply by trying a list of about 60 **default factory username/password combinations** that device owners had never bothered to change. It then used that botnet to launch some of the largest DDoS attacks seen up to that point, including one against the DNS provider Dyn that made sites like Twitter, Netflix, and GitHub unreachable for parts of a day. A single missing authentication discipline — "require users to change the default password" — cascaded into an availability attack on a huge portion of the internet.

## Connection to Part A

Authentication is a natural single point of failure. If every service checks every request against one central login server, an outage of that server takes down everything — exactly the crash-fault problem from [topic 1](01_fault_classification.md). This is one more reason self-verifying tokens are popular: each service can keep authenticating requests even when the identity provider is briefly unreachable. Identity providers themselves are also run with heavy replication ([topic 2](02_fault_tolerance_approaches.md)).

---

← [5. Threats](05_threats.md) · [Contents](README.md) · [7. Authorization](07_authorization.md) →
