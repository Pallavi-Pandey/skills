*Module 2 · Part B: Security in Distributed Systems*

# 5. Threats

## What is a threat?

A **threat** is anything that could cause harm to the CIA triad. A **vulnerability** is a weakness that a threat can exploit, and an **attack** is a threat actually being carried out against a vulnerability. Distributed systems introduce threat categories that simply don't exist on a single standalone machine, because there's now a network in between every component — and in security, you have to assume someone hostile can see and touch that network.

> **Simple analogy:** On a single computer, components talk to each other like people in the same room. In a distributed system, they talk by passing notes through a crowded hallway full of strangers. Any stranger can read a note, swap it for a different one, hand it in twice, or claim to be the person who wrote it.

## The attacker model

Security researchers often start from the **Dolev-Yao model**: assume the attacker *is* the network. They can read every message, delete it, delay it, replay it, or inject new messages of their own. The only thing they can't do is break the underlying cryptography. If a protocol is safe against that attacker, it's safe against weaker ones too. This is a deliberately pessimistic assumption — and it's the right one, because public Wi-Fi, compromised routers, and malicious insiders all make it close to reality.

## Network threats

- **Eavesdropping** — silently reading traffic in transit (breaks Confidentiality).
- **Tampering** — modifying data or messages in transit (breaks Integrity).
- **Spoofing** — pretending to be a different, trusted node or user, e.g. by forging a source IP address or using stolen credentials.
- **Replay attacks** — capturing a legitimate message and resending it later to trigger the same effect again (e.g., resending a captured "transfer 100 rupees" request ten times). Note that encryption alone doesn't stop this: the attacker doesn't need to read the message, only copy it.
- **Man-in-the-middle (MITM)** — an attacker secretly sits between two communicating parties, able to eavesdrop and tamper at will, while both sides believe they're talking directly to each other.
- **Denial of Service (DoS/DDoS)** — overwhelming a system with traffic or requests until legitimate users can't get through (breaks Availability). A *distributed* DoS uses thousands of machines at once, so blocking one source address doesn't help.

## Threats specific to distributed systems

- **Sybil attack** — one attacker creates many fake identities to gain outsized influence. In a peer-to-peer network or any system that decides things by vote, a thousand fake nodes can outvote the honest ones. This is the security version of the Byzantine Generals Problem from [topic 1](01_fault_classification.md): the 3f + 1 bound only helps if the attacker can't cheaply create extra generals.
- **Eclipse attack** — the attacker surrounds a single victim node with nodes they control, so everything it learns about the rest of the network is filtered through the attacker.
- **Insider threat** — a legitimate user or administrator abuses their access. Firewalls are no help here: the attacker is already inside.
- **Supply chain attack** — instead of attacking the system directly, the attacker compromises a library, build tool, or vendor update that the system trusts (see SolarWinds in [topic 11](11_trust_management.md)).

## Each threat and its defense

| Threat | CIA leg hit | Main defense | Covered in |
|---|---|---|---|
| Eavesdropping | Confidentiality | Encryption in transit | [8](08_encryption.md), [9](09_secure_communication_protocols.md) |
| Tampering | Integrity | MACs, digital signatures | [8](08_encryption.md) |
| Spoofing | Authenticity | Strong authentication, certificates | [6](06_authentication.md), [11](11_trust_management.md) |
| Replay | Integrity | Nonces, timestamps, sequence numbers | below |
| MITM | Confidentiality, Integrity | Authenticated key exchange (TLS with certificate checks) | [9](09_secure_communication_protocols.md) |
| DoS / DDoS | Availability | Rate limiting, replication, traffic filtering | [2](02_fault_tolerance_approaches.md) |
| Sybil | Integrity of decisions | Make identities costly (proof-of-work, admission control) | [1](01_fault_classification.md) |
| Insider | All three | Least privilege, auditing | [7](07_authorization.md), [13](13_auditing_and_monitoring.md) |

## Example: stopping a replay attack

The standard fix is to make every message unique and short-lived: attach a random **nonce** (a number used once) and a timestamp, protect the whole thing with a keyed hash (an HMAC, explained in [topic 8](08_encryption.md)), and have the receiver reject anything old or anything it has already seen.

```python
import hmac, hashlib, time, secrets

KEY = b"key-shared-by-client-and-server"
seen_nonces = set()

def sign(message):
    nonce = secrets.token_hex(8)
    timestamp = int(time.time())
    payload = f"{message}|{nonce}|{timestamp}".encode()
    tag = hmac.new(KEY, payload, hashlib.sha256).hexdigest()
    return {"message": message, "nonce": nonce, "timestamp": timestamp, "tag": tag}

def verify(packet):
    payload = f"{packet['message']}|{packet['nonce']}|{packet['timestamp']}".encode()
    expected = hmac.new(KEY, payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, packet["tag"]):
        return "rejected: tampered"
    if abs(time.time() - packet["timestamp"]) > 30:
        return "rejected: too old"
    if packet["nonce"] in seen_nonces:
        return "rejected: replay"
    seen_nonces.add(packet["nonce"])
    return "accepted"

packet = sign("transfer 100 to account 4417")
print(verify(packet))   # accepted
print(verify(packet))   # rejected: replay
```

Notice the timestamp check depends on the client's and server's clocks roughly agreeing — another place where the lack of a common physical clock (from Module 1) turns out to be a security concern.

## STRIDE: a checklist for finding threats

A useful mental model, from Microsoft's threat-modeling framework **STRIDE**, is that almost every attack falls into one of six categories. Each one is the opposite of a property you want:

| Threat | Violates |
|---|---|
| **S**poofing | Authenticity |
| **T**ampering | Integrity |
| **R**epudiation (denying you did something) | Non-repudiation |
| **I**nformation disclosure | Confidentiality |
| **D**enial of service | Availability |
| **E**levation of privilege | Authorization |

To use it, draw the components of a system and the arrows between them, then ask all six questions about every component and every arrow.

## Case Study: The GitHub DDoS Attack (2018)

In February 2018, GitHub was hit with about 1.35 terabits per second of traffic — at the time, the largest DDoS ever recorded. The attackers didn't need a huge botnet. They used **amplification**: they sent small requests to tens of thousands of publicly exposed memcached servers (a caching system meant to run only on private networks), with the source address *spoofed* to be GitHub's. Each server replied to GitHub with a response up to around 50,000 times larger than the request. GitHub's DDoS protection provider detected the attack and filtered the traffic, and the site was back within about ten minutes.

Two threats from this page combined into one attack: spoofing made the servers send their replies to the victim, and misconfigured infrastructure belonging to someone else multiplied the attack's size.

## Discussion Prompt

Take the multi-client chat server from Module 1, [Lab 04](../../module_1/labs/lab_04_client_server/). Apply all six STRIDE questions to it. Can a client pretend to be another user? Can anyone on the network read the messages? Can one client crash the server or stop others from chatting? Can a client later deny having sent something? Which of these could you fix with what you'll learn in topics 6 to 9?

---

← [4. The CIA Triad](04_the_cia_triad.md) · [Contents](README.md) · [6. Authentication](06_authentication.md) →
