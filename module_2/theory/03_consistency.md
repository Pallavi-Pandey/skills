*Module 2 · Part A: Fault Tolerance & Consistency*

# 3. Consistency

## The Consistency Spectrum

Once you have multiple replicas of the same data (from the previous section), a new question appears: when one replica is updated, how quickly — and how reliably — do the others reflect that update? This isn't a single yes/no property; it's a **spectrum**:

- **Strong consistency** — every read, from any replica, always reflects the most recent write. The system behaves as if there's really only one copy of the data, even though there are many. Easiest to reason about, hardest (slowest, most coordination-heavy) to actually build.
- **Eventual consistency** — after a write, replicas are allowed to temporarily disagree, but given enough time with no new writes, they will all converge to the same value. Much easier to make fast and available, but callers have to accept that a read *might* return stale data.
- **Everything in between** — causal consistency, read-your-own-writes, session consistency, and more: various compromises that give stronger guarantees than pure eventual consistency without paying the full cost of strong consistency.

## The CAP Theorem

Formulated by Eric Brewer, the CAP theorem states that a distributed system can provide, **at most two** of the following three guarantees **at the same time**, during a network partition:

- **Consistency (C)** — every node sees the same data at the same time.
- **Availability (A)** — every request gets a (non-error) response, even if it might not be the most recent data.
- **Partition Tolerance (P)** — the system keeps working even if network communication between some nodes is lost.

The crucial, often-misunderstood detail: **network partitions are going to happen** — cables get cut, routers fail, cloud regions lose connectivity — so partition tolerance isn't really optional for any system that's actually distributed across multiple machines. CAP, in practice, becomes a choice between **CP** (stay consistent, refuse requests you can't guarantee are correct, sacrifice availability during the partition) and **AP** (stay available, answer every request, accept that some answers might be stale or conflicting, sacrifice strict consistency during the partition).

> **Simple analogy:** Picture two bank branches that can normally sync balances instantly, but the phone line between them just went dead. A customer walks into Branch A and asks to withdraw money. Branch A has two choices: **refuse the withdrawal** until it can confirm with Branch B that the balance is accurate (choosing Consistency over Availability), or **allow it anyway** based on its last known balance, and risk the two branches disagreeing about the account balance once the line comes back (choosing Availability over Consistency). CAP says: during that dead phone line, Branch A *must* pick one of those two — there is no third option where it magically keeps both guarantees perfectly intact.

## Consistency Models in Practice

Real systems make this choice deliberately, based on what the data is actually for:

| System type | Typical choice | Why |
|---|---|---|
| Traditional relational databases (single-region) | **CP** | A bank balance or an inventory count being wrong is worse than the system briefly refusing requests |
| Amazon DynamoDB, Apache Cassandra | **AP** (tunable) | A shopping cart or a social media "like" count being briefly stale is far less costly than the site going down |
| Google Spanner | Engineered to approximate **CA** using synchronized atomic clocks | An extreme (and famous) engineering effort to narrow the tradeoff — not a loophole in the theorem itself |

## Case Study: The Amazon Shopping Cart Problem

Amazon's own engineers published a landmark paper (which led to the creation of DynamoDB) describing a real production problem: their shopping cart service, built on a strongly consistent design, would occasionally become *unavailable* during network blips — meaning customers literally could not add items to their cart, at the exact moment they were trying to buy something. Amazon's conclusion: for a shopping cart specifically, **availability matters more than perfect consistency** — it's far better to let two devices both add items and merge the carts later than to block a sale entirely. This single engineering decision is the direct ancestor of an entire category of "eventually consistent" databases used across the industry today.

## Security Perspective

Consistency choices have real security consequences, not just correctness ones. An eventually-consistent permissions system — e.g., "user X was just revoked access" — might mean a revoked user can still read data for a few seconds (or longer) on a replica that hasn't caught up yet. Security-sensitive state (who's authorized, what a balance is, whether a session is still valid) very often needs to lean toward the **CP** side of the tradeoff specifically *because* staleness there isn't just inconvenient, it's a vulnerability window.

---

← [2. Fault Tolerance Approaches](02_fault_tolerance_approaches.md) · [Contents](README.md) · [4. The CIA Triad](04_the_cia_triad.md) →
