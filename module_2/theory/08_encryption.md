*Module 2 · Part B: Security in Distributed Systems*

# 8. Encryption

## Turning data into something only the right party can use

**Encryption** turns readable data (plaintext) into unreadable data (ciphertext) using a mathematical algorithm and a key, so that anyone who intercepts it without the right key only sees gibberish. Encryption protects **Confidentiality**. A closely related set of tools — hashes, MACs, and digital signatures — protects **Integrity** and **Authenticity**. Real systems need both, and they are covered together on this page.

> **Simple analogy:** Symmetric encryption is a locked box where sender and receiver have copies of the same key. Asymmetric encryption is a public post box: anyone can drop a letter in through the slot (the public key), but only the owner has the key that opens it (the private key).

## Symmetric encryption

The same key both encrypts and decrypts. It's fast — modern processors have built-in instructions for **AES**, the standard algorithm, and can encrypt gigabytes per second. The catch is the **key distribution problem**: both parties need to somehow already share that key securely, and you can't just send it across the same network you're trying to protect.

## Asymmetric (public-key) encryption

A mathematically linked key *pair*: a public key (safe to share with anyone, used to encrypt) and a private key (kept secret, used to decrypt). The standard algorithms are **RSA** and **elliptic-curve cryptography (ECC)**. This solves the key distribution problem, but is computationally much more expensive than symmetric encryption — far too slow for bulk data.

A third tool, **Diffie-Hellman key agreement**, lets two parties who have never met each compute the *same* secret key by exchanging only public values over an open network; an eavesdropper who sees every message still can't work out the key.

In practice, almost every real system uses **both together**: public-key techniques to safely agree on a one-time symmetric key, then fast symmetric encryption for the actual bulk of the data — which is exactly what TLS does, covered next in [topic 9](09_secure_communication_protocols.md).

## Hashes, MACs, and digital signatures

Encryption hides data, but it doesn't by itself tell you whether data was changed. That's the job of three related tools:

- **Cryptographic hash** (e.g. SHA-256) — turns any input into a fixed-size fingerprint. Change one character of the input and the fingerprint changes completely. But anyone can compute a hash, so an attacker who changes a message can simply compute a new hash to go with it.
- **MAC (Message Authentication Code)**, most commonly **HMAC** — a hash that also mixes in a secret key. Only someone who has the key can produce a valid tag, so a matching tag proves the message wasn't changed *and* came from someone who holds the key.
- **Digital signature** — the asymmetric version of a MAC. The sender signs with their **private** key; anyone can verify with their **public** key. Because only the sender holds the private key, a signature also gives **non-repudiation** ([topic 4](04_the_cia_triad.md)): the sender can't later deny having signed.

```python
import hashlib, hmac

print(hashlib.sha256(b"transfer 100 to account 4417").hexdigest())
# d7b2ba143d2d0adac753e8858b9dfcc10f1afc0388c83c8aceb8d78889af541c
print(hashlib.sha256(b"transfer 900 to account 4417").hexdigest())
# 7794b69516ec5f4abaa71d2b374da412a9c62b1b1b0e1fd8486a7cef93c63d5f  <- completely different

key = b"key-only-the-two-parties-know"
tag = hmac.new(key, b"transfer 100 to account 4417", hashlib.sha256).hexdigest()
# without the key, an attacker cannot produce a valid tag for a changed message
```

| Tool | Key | Protects | Who can verify |
|---|---|---|---|
| Symmetric encryption (AES) | One shared key | Confidentiality | Anyone with the key |
| Asymmetric encryption (RSA, ECC) | Public / private pair | Confidentiality, key exchange | Private key holder |
| Hash (SHA-256) | None | Detects accidental change only | Anyone |
| MAC (HMAC) | One shared key | Integrity + authenticity | Anyone with the key |
| Digital signature | Public / private pair | Integrity + authenticity + non-repudiation | Anyone with the public key |

## Encryption in transit and at rest

Two more distinctions worth being precise about: **encryption in transit** (protecting data while it travels across the network — defeats eavesdropping) versus **encryption at rest** (protecting data while it's sitting on a disk somewhere — defeats theft of a stolen hard drive or an unauthorized database copy). A distributed system has far more of both than a single machine: every replica, backup, cache, and message queue is data at rest, and every call between services is data in transit. A system needs both kinds of protection; having one without the other is a common, serious gap.

## Key management

Encryption is only as strong as the protection of its keys. A key stored in the same database as the data it protects, or written into source code and pushed to GitHub, makes the encryption close to worthless. Real systems keep keys in a dedicated **key management service** (such as AWS KMS or HashiCorp Vault) or a **hardware security module (HSM)**, rotate them regularly, and use **envelope encryption**: each piece of data is encrypted with its own data key, and those data keys are themselves encrypted by a master key that never leaves the key management service.

## Case Study: The Equifax Breach (2017)

Equifax, a major credit bureau, exposed the sensitive personal data of roughly 147 million people. The root cause was a known, already-patched vulnerability in the Apache Struts web framework that Equifax simply hadn't updated — but what made it catastrophic rather than merely bad was that a large amount of the exposed data was stored **unencrypted**, and attackers also found plaintext credentials that let them reach further databases. The attack also went unnoticed for over two months, partly because an expired certificate on a traffic-inspection device meant encrypted outgoing traffic wasn't being examined. Encryption at rest wouldn't have stopped the initial breach, but it would have made the stolen data far less useful. This is a frequently cited case for the "defense in depth" principle: multiple independent security layers, so that one failure doesn't mean total compromise.

---

← [7. Authorization](07_authorization.md) · [Contents](README.md) · [9. Secure Communication Protocols](09_secure_communication_protocols.md) →
