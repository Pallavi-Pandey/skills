*Module 2 · Part B: Security in Distributed Systems*

# 4. The CIA Triad

## Three goals behind almost every security decision

Almost everything in security can be organized under three goals, together called the **CIA Triad**. Whenever you look at a security mechanism — a password, a firewall rule, an encrypted disk, a backup — you can ask "which of these three is it protecting?", and the answer is almost always one (or more) of them.

> **Simple analogy:** Think of a sealed letter sent through the post. **Confidentiality** is the envelope: nobody along the way can read what's inside. **Integrity** is the wax seal: if anyone opens and changes the letter, the broken seal gives it away. **Availability** is the postal service itself: the best envelope and seal in the world are useless if the letter never arrives.

## Confidentiality

**Confidentiality** means only authorized parties can read the data. It's broken by eavesdropping on network traffic, by a stolen database, or by an employee looking at records they have no business seeing.

In a distributed system, data is copied and moved far more than on a single machine: it travels between services, sits in replicas on several nodes, ends up in caches, backups, and log files. Every one of those copies is a place confidentiality can fail. The main tools are **encryption** ([topic 8](08_encryption.md)) and **access control** ([topic 10](10_access_control.md)).

## Integrity

**Integrity** means data can't be modified — accidentally or deliberately — without that modification being detected. It's broken by an attacker tampering with a message in transit, by a man-in-the-middle, or by silent corruption on a disk.

Note the wording: integrity is mostly about *detecting* changes, not physically preventing them. You can't stop someone with access to the network cable from flipping bits; what you can do is make sure the receiver notices and rejects the altered message. The main tools are **hashes, message authentication codes, and digital signatures** ([topic 8](08_encryption.md)).

## Availability

**Availability** means the system is accessible to legitimate users when they need it. It's broken by denial-of-service attacks, by ransomware that locks up files, and by ordinary outages.

Notice that **Availability is also one of the three CAP guarantees** from [topic 3](03_consistency.md) — fault tolerance and security are not separate disciplines here, they overlap directly. A well-executed denial-of-service attack and an unplanned network partition can look, from the system's point of view, like the exact same problem: "some nodes can't be reached right now." Everything in Part A — replication, migration, checkpointing — is, from a security point of view, availability engineering.

## Beyond the triad: Authenticity and Non-repudiation

Two more properties come up constantly in distributed systems, and some textbooks add them to the list:

- **Authenticity** — the data really came from who it claims to come from. A message with perfect integrity is still useless if it was perfectly sent by an attacker pretending to be your bank.
- **Non-repudiation** — the sender can't later deny having sent it. If a node signs "I approved this transaction" with a key only it holds, it can't later claim "that wasn't me." This matters for audit trails ([topic 13](13_auditing_and_monitoring.md)) and for any system where parties don't fully trust each other.

## The three goals pull against each other

The triad is not three boxes you tick independently — strengthening one often weakens another:

| Choice | Strengthens | Can weaken |
|---|---|---|
| Encrypt everything with keys held in one place | Confidentiality | Availability (lose the key server, lose all the data) |
| Keep many replicas across regions | Availability | Confidentiality (more copies to protect and to leak) |
| Require MFA and re-checks on every request | Confidentiality, Integrity | Availability (legitimate users locked out when the MFA service is down) |
| Lock an account after 5 failed logins | Confidentiality | Availability (an attacker can lock out real users on purpose) |

Real security design is mostly about choosing which of these tradeoffs is acceptable for a given piece of data.

## Case Study: Colonial Pipeline (2021)

Colonial Pipeline carries a large share of the fuel used on the US East Coast. In May 2021, attackers from the DarkSide ransomware group got into its IT network using the password of an old VPN account that had no multi-factor authentication. They stole data (Confidentiality) and encrypted business systems (Availability). The fuel pipeline's control systems were not directly hit — but because the company could no longer reliably bill and track fuel deliveries, it shut the pipeline down itself for several days, causing fuel shortages and panic buying across several states. The company paid a ransom of about 4.4 million US dollars.

The lesson: a single weak point in authentication led to a Confidentiality breach and an Availability failure at once, and the Availability impact — felt by millions of people who never touched the company's systems — was far larger than the data theft.

## Discussion Prompt

For each incident below, which leg (or legs) of the CIA triad failed?

1. A hacked database of customer emails and passwords is published online.
2. An attacker changes the destination account number of a bank transfer while it is in transit.
3. A botnet floods a company's website with fake traffic until it falls over.
4. Ransomware encrypts a hospital's patient records, and the attackers threaten to publish them unless paid.

Things to consider: the first three map fairly cleanly to one leg each (Confidentiality, Integrity, Availability). The fourth hits Availability and Confidentiality together — and many real incidents are like that, which is why defending only one leg is rarely enough.

---

← [3. Consistency](03_consistency.md) · [Contents](README.md) · [5. Threats](05_threats.md) →
