*Module 2 · Part B: Security in Distributed Systems*

# 13. Auditing and Monitoring

## Detecting what prevention missed

Every mechanism above is about *prevention* — but prevention eventually fails, somewhere, for someone. **Auditing and monitoring** is the discipline of **detecting** that failure as fast as possible, and having a reliable record of what happened.

> **Simple analogy:** Locks on a bank's doors are prevention. The security cameras are monitoring: someone watching the screens can react while a break-in is happening. The recorded footage and the sign-in book at the vault are auditing: after the fact, they answer exactly who went where, and when.

- **Logging** — recording security-relevant events (logins, access attempts, permission changes) as they happen.
- **Monitoring / SIEM (Security Information and Event Management)** — continuously analyzing those logs, often in real time, to spot suspicious patterns (e.g., one account logging in from two countries five minutes apart).
- **Auditing** — a more deliberate, often periodic review of logs and access records, frequently required for regulatory compliance, to answer the question "who accessed what, and was that appropriate?" after the fact.

## What to log

A useful security log entry answers *who* did *what*, to *which* resource, *when*, from *where*, and *whether it succeeded*. Typical events: logins and failed logins, permission changes, access to sensitive data, administrator actions, and changes to the logging configuration itself (an attacker's favourite first step is to turn the logs off). Equally important is what *not* to log: passwords, full card numbers, and access tokens end up in log files surprisingly often, turning the logs themselves into a target.

## Logging in a distributed system

On one machine, the log is one file. In a distributed system, a single user action can touch dozens of services on dozens of machines, which creates three problems:

- **Collection** — logs are scattered across every node. They're shipped as they're written to a **central log store** (tools such as the ELK stack or Splunk), both so they can be searched together and so a compromised node can't quietly delete its own history.
- **Ordering** — to reconstruct an attack, you need to know which event happened first, but every machine has its own clock and they drift apart (the "no common physical clock" problem from Module 1). Servers keep clocks synced with NTP, and logs record time in one standard timezone (UTC).
- **Correlation** — to follow one request through many services, the first service attaches a unique **request ID** (also called a correlation or trace ID) that every later service includes in its log lines.

## Protecting the logs

An attacker who gets in will try to erase their tracks, so logs need integrity protection ([topic 4](04_the_cia_triad.md)). Besides shipping them off the machine immediately and storing them in write-once storage, a common technique is a **hash chain**: each entry includes the hash of the entry before it, so changing or deleting any old entry breaks every hash after it.

```python
import hashlib, json

log = []

def append(event):
    prev_hash = log[-1]["hash"] if log else "0" * 64
    body = json.dumps(event, sort_keys=True)
    entry_hash = hashlib.sha256((prev_hash + body).encode()).hexdigest()
    log.append({"event": event, "prev": prev_hash, "hash": entry_hash})

def verify_log():
    prev_hash = "0" * 64
    for entry in log:
        body = json.dumps(entry["event"], sort_keys=True)
        expected = hashlib.sha256((prev_hash + body).encode()).hexdigest()
        if entry["prev"] != prev_hash or entry["hash"] != expected:
            return False
        prev_hash = entry["hash"]
    return True

append({"user": "asha", "action": "login", "node": "auth-1"})
append({"user": "asha", "action": "delete", "resource": "report.pdf"})
print(verify_log())                 # True
log[1]["event"]["action"] = "read"  # attacker tries to hide the delete
print(verify_log())                 # False
```

On its own, an attacker with full control could recompute the whole chain. The defense is to regularly copy the latest hash somewhere the attacker can't reach — another server, or a separate team's system. It's the same idea behind blockchains ([topic 1](01_fault_classification.md)) and Certificate Transparency logs ([topic 11](11_trust_management.md)).

## Intrusion detection

An **Intrusion Detection System (IDS)** watches network traffic (a network IDS) or activity on a single machine (a host IDS) for signs of attack. There are two approaches:

| Approach | How it works | Good at | Weak at |
|---|---|---|---|
| **Signature-based** | Matches known attack patterns, like antivirus | Known attacks, few false alarms | Anything new |
| **Anomaly-based** | Learns what "normal" looks like and flags deviations | New and unknown attacks | Many false alarms |

An **Intrusion Prevention System (IPS)** goes a step further and blocks suspicious traffic automatically instead of only raising an alert.

The biggest practical problem is **alert fatigue**. A system that raises thousands of alerts a day, mostly false alarms, trains the people watching it to ignore alerts — including the real one.

## Case Study: The Target Breach (2013)

Attackers first got into Target's network using credentials stolen from a heating and air-conditioning contractor, then installed malware on the store checkout terminals. Target's security monitoring systems **did** detect that malware during the attack — the alerts fired, correctly, and were forwarded to the security team. The failure was organizational, not technical: the alerts were seen and not acted on in time, and the breach eventually exposed roughly 40 million customers' credit card data. This is one of the most cited lessons in this entire topic: monitoring that nobody actually responds to provides close to zero real protection. Detection and response have to be treated as one system, not two separate boxes to check.

## Tying it back to Part A

A monitoring system that detects a compromised node is, functionally, doing the same job as a crash-fault detector from [topic 1](01_fault_classification.md) — both are asking "is this node behaving the way it's supposed to?" and triggering a response when the answer is no. The difference is just *what kind* of misbehavior you're watching for: Part A's fault tolerance mainly watches for nodes that have gone silent or degraded; Part B's security monitoring mainly watches for nodes that have been taken over by someone else. By the end of this module, it should be clear these were never really two separate subjects — they're the same discipline (keeping a system trustworthy despite components you can't fully control) viewed from two different angles.

---

← [12. Privacy Preserving](12_privacy_preserving.md) · [Contents](README.md)
