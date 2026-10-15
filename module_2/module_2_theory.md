# Module 2: Fault Tolerance and Security in Distributed Systems

---

## Part A: Fault Tolerance & Consistency

---

### 1. Fault Classification

#### What is a fault, exactly?

A **fault** is anything that causes a system to deviate from its intended behavior. In a single computer, a fault is usually obvious — the program crashes, or the screen freezes. In a distributed system, faults are sneakier: one node can misbehave while the rest of the system carries on, and from the outside you might not even be able to tell *which* node is at fault, or whether it's at fault at all.

> **Simple analogy:** Imagine a group project with five teammates spread across different cities, coordinating only by text message. If one teammate suddenly goes silent, is it because their phone died (easy to reason about — they're just gone), or because they're still texting, but now sending wrong, contradictory information on purpose or by mistake (much harder to reason about — you have to figure out *who* to trust)? Distributed systems have to plan for both.

#### Crash Faults

A **crash fault** is the "polite" failure: a node simply stops. It doesn't respond, it doesn't send corrupted data, it doesn't lie — it's just gone, the way a teammate whose phone died is just gone. Once you detect it's gone (usually via a timeout — "I haven't heard from it in N seconds"), you know exactly what you're dealing with: a node is unavailable, full stop.

This is the easiest class of fault to tolerate, because the failure mode is simple and honest. Most of the fault-tolerance techniques in this module — replication, checkpoint-restart, job migration — are primarily built to survive crash faults.

#### Byzantine Faults

A **Byzantine fault** is the dangerous one: a node keeps participating, but behaves **arbitrarily or maliciously** — sending different (possibly contradictory) information to different parts of the system, or data that's subtly wrong rather than obviously broken. The name comes from the **Byzantine Generals Problem**, a thought experiment from a 1982 paper by Leslie Lamport, Robert Shostak, and Marshall Pease:

> Several generals, each commanding part of the Byzantine army, surround an enemy city. They can only communicate by messenger, and they must unanimously decide: attack, or retreat. If even one general is a traitor, they can send "attack" to some generals and "retreat" to others — enough to make the loyal generals attack piecemeal and lose, purely through deliberately inconsistent messaging. The hard question the paper asks: how many loyal generals does it take to reach agreement despite some number of traitors?

The headline result: with simple messaging, you need **more than 3× the number of traitors** in total participants to guarantee agreement — i.e., to tolerate *f* Byzantine nodes, you need at least *3f + 1* total nodes. That's expensive, which is exactly why Byzantine fault tolerance (BFT) is only used where it's really warranted.

| | Crash Fault | Byzantine Fault |
|---|---|---|
| **Behavior** | Stops responding entirely | Keeps responding, but with wrong/contradictory data |
| **Detectability** | Easy — timeout tells you | Hard — the node *looks* alive |
| **Cause** | Hardware failure, crash, network drop | Bug, corruption, or a malicious/compromised node |
| **Tolerance cost** | Cheap (e.g., 2f+1 nodes to survive f crashes) | Expensive (3f+1 nodes to survive f Byzantine nodes) |

#### 📖 Case Study: Bitcoin as Byzantine Fault Tolerance at Planetary Scale

Bitcoin's entire security model is a practical answer to the Byzantine Generals Problem, just rebranded: thousands of anonymous nodes ("miners") need to agree on one shared transaction history, even though some of them may be actively lying to double-spend coins. Its "proof-of-work" consensus mechanism makes lying *computationally expensive* rather than relying on trust — a direct, real-world instance of Byzantine agreement that most students will have already heard of without knowing it has a name in distributed systems theory.

#### 🔐 Security Perspective

A compromised node is, almost by definition, a Byzantine node — it's still "alive" and responding, but under an attacker's control it can now lie, forge data, or selectively target specific peers. This is exactly why security-critical distributed systems (blockchains, some banking infrastructure, aircraft flight-control systems) are built with explicit Byzantine fault tolerance, even at significant extra cost, while an ordinary web backend usually only bothers to tolerate crash faults.

---

### 2. Fault Tolerance Approaches

There are two fundamentally different philosophies for dealing with faults: **act before they happen** (proactive), or **recover after they happen** (reactive). Real systems almost always use a mix of both.

#### Proactive: Self-Healing

A self-healing system continuously monitors its own health and automatically corrects problems *before* they become outages — restarting a misbehaving process, replacing a node whose health checks are failing, or rebalancing load away from a struggling component. Kubernetes doing this for you (restarting a crashed container pod without a human ever being paged) is the most common real-world example students will have access to.

#### Proactive: Pre-emptive Migration

Instead of waiting for a node to fail, the system **moves work away from a node that looks like it's about to fail** — rising error rates, degrading hardware signals (disk SMART errors, rising temperatures), or a scheduled maintenance window. The job relocates to healthy hardware before anything actually breaks.

#### Proactive: System Rejuvenation

Some faults don't come from a sudden event at all — they come from **slow decay**, like a memory leak that gradually eats available RAM until the system eventually crashes (a phenomenon called "software aging"). System rejuvenation means periodically and deliberately restarting a component — on a schedule, before it degrades — to reset that slow drift back to a clean state. It sounds almost too simple to be "real" fault tolerance, but scheduled restarts are genuinely used in production systems for exactly this reason.

#### Reactive: Checkpoint-Restart

A **checkpoint** is a saved snapshot of a running process's state — memory, variables, progress — taken periodically while it runs. If the process then crashes, instead of starting the whole computation over from scratch, the system **restarts it from the most recent checkpoint**. This is standard practice for long-running scientific/batch computations (think: a simulation that takes 10 hours — you really don't want to lose 9 hours of progress to one crash 10 minutes before the end).

#### Reactive: Job Migration

Similar to pre-emptive migration, but *after* a failure rather than before it: when a node dies mid-job, the system picks up that job (often from its last checkpoint) and relocates it to a different, healthy node, rather than waiting for the original node to come back.

#### Reactive: Replication

Instead of relying on one copy of data or one instance of a service, **keep multiple identical copies running on different nodes**, so that if one fails, the others are already there and ready — no restart, no migration delay, just an immediate failover (or, in many designs, the other replicas were serving traffic the whole time anyway). This is the single most widely used fault-tolerance technique in real distributed systems, and it reappears constantly throughout the rest of this module, especially in the Consistency section below — because the moment you have multiple copies of the same data, you have to decide how to keep them in agreement.

#### 📖 Case Study: Netflix's Chaos Monkey

Netflix famously built a tool, **Chaos Monkey**, that randomly kills production servers — on purpose, during business hours — specifically to force every team to build self-healing, replicated systems rather than systems that merely *hope* nothing fails. It's proactive fault tolerance taken to its logical extreme: instead of waiting to discover your fault tolerance doesn't actually work during a real outage, you manufacture small controlled outages constantly, so you find out immediately — a practice now broadly called "chaos engineering."

#### 🔐 Security Perspective

Checkpointing and replication both multiply the number of places sensitive data physically exists — a checkpoint file saved to disk is a new copy of memory contents (which might include secrets like session tokens or decrypted data) sitting on a filesystem; a replica is a full additional copy of a database, in a different place, that also needs to be secured, patched, and access-controlled. Fault tolerance and the "reduce your attack surface" principle are often in direct tension, which is one reason security and fault tolerance get taught together in this module instead of separately.

---

### 3. Consistency

#### The Consistency Spectrum

Once you have multiple replicas of the same data (from the previous section), a new question appears: when one replica is updated, how quickly — and how reliably — do the others reflect that update? This isn't a single yes/no property; it's a **spectrum**:

- **Strong consistency** — every read, from any replica, always reflects the most recent write. The system behaves as if there's really only one copy of the data, even though there are many. Easiest to reason about, hardest (slowest, most coordination-heavy) to actually build.
- **Eventual consistency** — after a write, replicas are allowed to temporarily disagree, but given enough time with no new writes, they will all converge to the same value. Much easier to make fast and available, but callers have to accept that a read *might* return stale data.
- **Everything in between** — causal consistency, read-your-own-writes, session consistency, and more: various compromises that give stronger guarantees than pure eventual consistency without paying the full cost of strong consistency.

#### The CAP Theorem

Formulated by Eric Brewer, the CAP theorem states that a distributed system can provide, **at most two** of the following three guarantees **at the same time**, during a network partition:

- **Consistency (C)** — every node sees the same data at the same time.
- **Availability (A)** — every request gets a (non-error) response, even if it might not be the most recent data.
- **Partition Tolerance (P)** — the system keeps working even if network communication between some nodes is lost.

The crucial, often-misunderstood detail: **network partitions are going to happen** — cables get cut, routers fail, cloud regions lose connectivity — so partition tolerance isn't really optional for any system that's actually distributed across multiple machines. CAP, in practice, becomes a choice between **CP** (stay consistent, refuse requests you can't guarantee are correct, sacrifice availability during the partition) and **AP** (stay available, answer every request, accept that some answers might be stale or conflicting, sacrifice strict consistency during the partition).

> **Simple analogy:** Picture two bank branches that can normally sync balances instantly, but the phone line between them just went dead. A customer walks into Branch A and asks to withdraw money. Branch A has two choices: **refuse the withdrawal** until it can confirm with Branch B that the balance is accurate (choosing Consistency over Availability), or **allow it anyway** based on its last known balance, and risk the two branches disagreeing about the account balance once the line comes back (choosing Availability over Consistency). CAP says: during that dead phone line, Branch A *must* pick one of those two — there is no third option where it magically keeps both guarantees perfectly intact.

#### Consistency Models in Practice

Real systems make this choice deliberately, based on what the data is actually for:

| System type | Typical choice | Why |
|---|---|---|
| Traditional relational databases (single-region) | **CP** | A bank balance or an inventory count being wrong is worse than the system briefly refusing requests |
| Amazon DynamoDB, Apache Cassandra | **AP** (tunable) | A shopping cart or a social media "like" count being briefly stale is far less costly than the site going down |
| Google Spanner | Engineered to approximate **CA** using synchronized atomic clocks | An extreme (and famous) engineering effort to narrow the tradeoff — not a loophole in the theorem itself |

#### 📖 Case Study: The Amazon Shopping Cart Problem

Amazon's own engineers published a landmark paper (which led to the creation of DynamoDB) describing a real production problem: their shopping cart service, built on a strongly consistent design, would occasionally become *unavailable* during network blips — meaning customers literally could not add items to their cart, at the exact moment they were trying to buy something. Amazon's conclusion: for a shopping cart specifically, **availability matters more than perfect consistency** — it's far better to let two devices both add items and merge the carts later than to block a sale entirely. This single engineering decision is the direct ancestor of an entire category of "eventually consistent" databases used across the industry today.

#### 🔐 Security Perspective

Consistency choices have real security consequences, not just correctness ones. An eventually-consistent permissions system — e.g., "user X was just revoked access" — might mean a revoked user can still read data for a few seconds (or longer) on a replica that hasn't caught up yet. Security-sensitive state (who's authorized, what a balance is, whether a session is still valid) very often needs to lean toward the **CP** side of the tradeoff specifically *because* staleness there isn't just inconvenient, it's a vulnerability window.

---

## Part B: Security in Distributed Systems

Distributed systems multiply the number of machines, networks, and operators involved in getting work done — and every one of those is a potential point of attack. This part covers the vocabulary and mechanisms used to reason about, and defend, a distributed system.

---

### 4. The CIA Triad

Almost everything in security can be organized under three goals, together called the **CIA Triad**:

- **Confidentiality** — only authorized parties can read the data. (Stopped by: eavesdropping, data breaches.)
- **Integrity** — data can't be modified without detection. (Stopped by: tampering, corruption, man-in-the-middle attacks.)
- **Availability** — the system is accessible to legitimate users when they need it. (Stopped by: denial-of-service, outages.)

Notice that **Availability is also one of the three CAP guarantees** from Part A — fault tolerance and security are not separate disciplines here, they overlap directly. A well-executed denial-of-service attack and an unplanned network partition can look, from the system's point of view, like the exact same problem: "some nodes can't be reached right now." Everything from here on is about defending Confidentiality and Integrity specifically, since Part A already covered Availability in depth.

#### 💭 Discussion Prompt

For each of these real incidents, which leg (or legs) of the CIA triad actually failed: a) a hacked database of customer emails and passwords gets published online, b) an attacker modifies a bank transfer's destination account number in transit, c) a botnet floods a company's website with fake traffic until it falls over? (Answers: a = Confidentiality, b = Integrity, c = Availability — but push students to notice real incidents are often more than one of these at once.)

---

### 5. Threats

A **threat** is anything that could cause harm to the CIA triad. Distributed systems introduce threat categories that simply don't exist on a single standalone machine, because there's now a network in between every component:

- **Eavesdropping** — silently reading traffic in transit (breaks Confidentiality).
- **Tampering** — modifying data or messages in transit (breaks Integrity).
- **Spoofing** — pretending to be a different, trusted node or user.
- **Replay attacks** — capturing a legitimate message and resending it later to trigger the same effect again (e.g., resending a captured "transfer $100" request).
- **Denial of Service (DoS/DDoS)** — overwhelming a system with traffic or requests until legitimate users can't get through (breaks Availability).
- **Man-in-the-middle (MITM)** — an attacker secretly sits between two communicating parties, able to eavesdrop and tamper at will, while both sides believe they're talking directly to each other.

A useful mental model (from Microsoft's threat-modeling framework, **STRIDE**) is that almost every distributed-systems attack is one of: **S**poofing, **T**ampering, **R**epudiation (denying you did something), **I**nformation disclosure, **D**enial of service, or **E**levation of privilege.

---

### 6. Authentication

**Authentication answers the question "who are you?"** — proving an identity before any access is granted. In a distributed system, this has to happen over a network, between parties who may never have physically met, which is fundamentally harder than a security guard checking a photo ID in person.

Common mechanisms: passwords (the weakest, most phishable option), multi-factor authentication (MFA — something you know + something you have/are), and certificate-based authentication (a cryptographic proof of identity, covered more in Secure Communication Protocols below).

#### 📖 Case Study: The Mirai Botnet

In 2016, the Mirai botnet compromised hundreds of thousands of IoT devices (security cameras, routers) not through some sophisticated exploit, but simply by trying a list of ~60 **default factory username/password combinations** that device owners had never bothered to change. It then used that botnet to launch one of the largest DDoS attacks in history, taking down major internet services. A single missing authentication discipline — "require users to change the default password" — cascaded into an availability attack on a huge portion of the internet.

---

### 7. Authorization

**Authorization answers the question "now that I know who you are, what are you allowed to do?"** — this is a distinct step that happens *after* authentication, and it's a common mistake to conflate the two. Being logged in (authenticated) doesn't mean you should be able to do everything the system can do.

The foundational principle here is **least privilege**: every user, process, and service should have the minimum set of permissions needed to do its job, and nothing more — so that if that identity is ever compromised, the damage it can do is limited by design, not by luck.

#### 💭 Discussion Prompt

A company's customer-support tool lets any support agent view *any* customer's full account details, including payment info, "just in case they need it." Using the least-privilege principle, how would you redesign this access model? (Push toward: scope access to only the customer the agent is actively assigned to, time-limit that access, and log every access — a preview of Access Control and Auditing, both coming up next.)

---

### 8. Encryption

**Encryption** turns readable data (plaintext) into unreadable data (ciphertext) using a mathematical algorithm and a key, so that anyone who intercepts it without the right key only sees gibberish. There are two fundamentally different families:

- **Symmetric encryption** — the same key both encrypts and decrypts. Fast, but both parties need to somehow already share that key securely (the "key distribution problem").
- **Asymmetric (public-key) encryption** — a mathematically linked key *pair*: a public key (safe to share with anyone, used to encrypt) and a private key (kept secret, used to decrypt). Solves the key-distribution problem, but is computationally much more expensive than symmetric encryption.

In practice, almost every real system uses **both together**: asymmetric encryption to safely exchange a one-time symmetric key, then fast symmetric encryption for the actual bulk of the data — which is exactly what TLS does, covered next.

Two more distinctions worth being precise about: **encryption in transit** (protecting data while it travels across the network — defeats eavesdropping) versus **encryption at rest** (protecting data while it's sitting on a disk somewhere — defeats theft of a stolen hard drive or an unauthorized database copy). A system needs both; having one without the other is a common, serious gap.

#### 📖 Case Study: The Equifax Breach (2017)

Equifax, a major credit bureau, exposed the sensitive personal data of roughly 147 million people. The root cause was a known, already-patched vulnerability in a web framework that Equifax simply hadn't updated — but what made it catastrophic rather than merely bad was that a large amount of the exposed data was stored **unencrypted**. Encryption at rest wouldn't have stopped the initial breach, but it would have made the stolen data largely useless to the attackers. This is a frequently cited case for exactly the "defense in depth" principle: multiple independent security layers, so that one failure doesn't mean total compromise.

---

### 9. Secure Communication Protocols

The most important one to know by name is **TLS (Transport Layer Security)** — the protocol behind the padlock icon in a browser's address bar, and the thing that makes HTTPS secure. At a conceptual level, a TLS handshake does three things before any real data is sent:

1. **Authenticates the server** (and optionally the client) using a digital certificate — a credential issued by a trusted third party (a Certificate Authority) vouching "this public key really does belong to this domain."
2. **Negotiates a shared symmetric key**, using asymmetric encryption just long enough to exchange that key safely (exactly the "use both together" pattern from the Encryption section above).
3. **Switches to fast symmetric encryption** for the actual conversation, which now also includes integrity checks so any tampering in transit gets detected.

This single protocol is a working example of nearly every concept in this security section at once: Authentication (the certificate), Encryption (both kinds), and Integrity protection (part of the CIA triad) — all bundled into the handshake you've been relying on, invisibly, every time you've visited an `https://` website.

---

### 10. Access Control

While Authorization defines the *policy* ("what is this user allowed to do?"), **Access Control** is the actual *enforcement mechanism* that checks that policy on every single request. Three common models:

- **DAC (Discretionary Access Control)** — the owner of a resource decides who else can access it (e.g., sharing a Google Doc with specific people). Flexible, but easy to misconfigure.
- **MAC (Mandatory Access Control)** — a central authority sets fixed access rules that users can't override, even for their own resources (common in military/government systems with classification levels).
- **RBAC (Role-Based Access Control)** — permissions are attached to *roles* (e.g., "editor," "admin," "viewer"), and users are assigned roles, rather than permissions being granted to individual users one by one. This is by far the most common model in real distributed systems and cloud platforms, because it scales — you manage a handful of roles instead of thousands of individual permission grants.

---

### 11. Trust Management

In a distributed system, you very often have to grant some level of access to a party you've never directly verified yourself — a new node joining a cluster, a third-party service calling your API. **Trust management** is the set of mechanisms for deciding, and continuously re-evaluating, how much to trust each party.

The classic model is **PKI (Public Key Infrastructure)**: a hierarchy of trusted Certificate Authorities that vouch for identities, which is what makes TLS certificates (Section 9) actually meaningful — you trust a server's certificate because you trust the CA that issued it, not because you personally verified that server.

A newer, increasingly dominant model is **Zero Trust**: instead of assuming anything inside your network perimeter is automatically trustworthy (the old "castle and moat" model — hard shell, soft interior), Zero Trust assumes **no implicit trust at all**, anywhere, and re-verifies identity and authorization on every single request, regardless of whether it came from "inside" or "outside" the network.

#### 📖 Case Study: The SolarWinds Supply Chain Attack (2020)

Attackers compromised SolarWinds' software build system and inserted malicious code into a legitimate, digitally-signed software update, which was then installed — trusted, because it was signed and came from a known vendor — by roughly 18,000 organizations, including US government agencies. This is a **trust management failure at its most severe**: the entire system of "we trust signed updates from known vendors" was turned into the attack vector itself, precisely because downstream organizations had no mechanism to question that trust once it was established.

---

### 12. Privacy Preserving

Privacy is related to Confidentiality, but it's a distinct concern: Confidentiality is about *stopping unauthorized parties* from seeing data, while Privacy is about limiting what even *authorized* parties collect, retain, and do with personal data in the first place. Key techniques:

- **Data minimization** — only collect the data you actually need, so there's less to protect (and less to lose) in the first place.
- **Anonymization / pseudonymization** — strip or replace identifying details so data can still be useful (e.g., for analytics) without being traceable back to a specific person.
- **Differential privacy** — a mathematical technique for adding carefully calibrated statistical "noise" to query results or datasets, so aggregate patterns remain useful while no individual's specific data can be reliably reverse-engineered out of it. (Apple and the US Census Bureau both use this in production.)

#### 📖 Case Study: Cambridge Analytica (2018)

Cambridge Analytica obtained Facebook data on roughly 87 million users — not primarily through a technical hack, but through permissive data-sharing policies that let a third-party app collect data on users' *friends* who had never consented to or even known about that app. This wasn't a Confidentiality failure in the traditional sense (no one "broke in"); it was a Privacy failure — data flowed exactly where the system's rules technically allowed it to, and those rules themselves were the problem.

---

### 13. Auditing and Monitoring

Every mechanism above is about *prevention* — but prevention eventually fails, somewhere, for someone. **Auditing and monitoring** is the discipline of **detecting** that failure as fast as possible, and having a reliable record of what happened.

- **Logging** — recording security-relevant events (logins, access attempts, permission changes) as they happen.
- **Monitoring / SIEM (Security Information and Event Management)** — continuously analyzing those logs, often in real time, to spot suspicious patterns (e.g., one account logging in from two countries five minutes apart).
- **Auditing** — a more deliberate, often periodic review of logs and access records, frequently required for regulatory compliance, to answer the question "who accessed what, and was that appropriate?" after the fact.

#### 📖 Case Study: The Target Breach (2013)

Target's security monitoring systems **did** detect the malware used in a breach that eventually exposed roughly 40 million customers' credit card data — the alerts fired, correctly, during the attack. The failure was organizational, not technical: the alerts were seen and not acted on in time. This is one of the most cited lessons in this entire topic: monitoring that nobody actually responds to provides close to zero real protection. Detection and response have to be treated as one system, not two separate boxes to check.

#### 🔐 Tying it back to Part A

A monitoring system that detects a compromised node is, functionally, doing the same job as a crash-fault detector from Section 1 — both are asking "is this node behaving the way it's supposed to?" and triggering a response when the answer is no. The difference is just *what kind* of misbehavior you're watching for: Part A's fault tolerance mainly watches for nodes that have gone silent or degraded; Part B's security monitoring mainly watches for nodes that have been taken over by someone else. By the end of this module, it should be clear these were never really two separate subjects — they're the same discipline (keeping a system trustworthy despite components you can't fully control) viewed from two different angles.

---

## Summary Table: All Topics at a Glance

| # | Topic | One-line takeaway |
|---|---|---|
| 1 | Fault Classification | Crash faults are honest failures; Byzantine faults actively lie |
| 2 | Fault Tolerance Approaches | Proactive = act before it breaks; Reactive = recover after it breaks |
| 3 | Consistency / CAP | During a network partition, pick Consistency or Availability — not both |
| 4 | CIA Triad | Confidentiality, Integrity, Availability — the three things security protects |
| 5 | Threats | Eavesdropping, tampering, spoofing, replay, DoS, MITM |
| 6 | Authentication | Proving *who you are* |
| 7 | Authorization | Deciding *what you're allowed to do*, once you're known |
| 8 | Encryption | Symmetric (fast, shared key) + Asymmetric (solves key distribution) |
| 9 | Secure Communication Protocols | TLS combines authentication + encryption + integrity in one handshake |
| 10 | Access Control | The enforcement mechanism behind authorization (DAC, MAC, RBAC) |
| 11 | Trust Management | Deciding how much to trust a party you can't personally verify |
| 12 | Privacy Preserving | Limiting what even authorized parties can learn about individuals |
| 13 | Auditing and Monitoring | Detecting failures fast, and actually acting on what you detect |
