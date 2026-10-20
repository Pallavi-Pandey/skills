*Module 2 · Part A: Fault Tolerance & Consistency*

# 2. Fault Tolerance Approaches

There are two fundamentally different philosophies for dealing with faults: **act before they happen** (proactive), or **recover after they happen** (reactive). Real systems almost always use a mix of both.

## Proactive: Self-Healing

A self-healing system continuously monitors its own health and automatically corrects problems *before* they become outages — restarting a misbehaving process, replacing a node whose health checks are failing, or rebalancing load away from a struggling component. Kubernetes doing this for you (restarting a crashed container pod without a human ever being paged) is the most common real-world example students will have access to.

## Proactive: Pre-emptive Migration

Instead of waiting for a node to fail, the system **moves work away from a node that looks like it's about to fail** — rising error rates, degrading hardware signals (disk SMART errors, rising temperatures), or a scheduled maintenance window. The job relocates to healthy hardware before anything actually breaks.

## Proactive: System Rejuvenation

Some faults don't come from a sudden event at all — they come from **slow decay**, like a memory leak that gradually eats available RAM until the system eventually crashes (a phenomenon called "software aging"). System rejuvenation means periodically and deliberately restarting a component — on a schedule, before it degrades — to reset that slow drift back to a clean state. It sounds almost too simple to be "real" fault tolerance, but scheduled restarts are genuinely used in production systems for exactly this reason.

## Reactive: Checkpoint-Restart

A **checkpoint** is a saved snapshot of a running process's state — memory, variables, progress — taken periodically while it runs. If the process then crashes, instead of starting the whole computation over from scratch, the system **restarts it from the most recent checkpoint**. This is standard practice for long-running scientific/batch computations (think: a simulation that takes 10 hours — you really don't want to lose 9 hours of progress to one crash 10 minutes before the end).

## Reactive: Job Migration

Similar to pre-emptive migration, but *after* a failure rather than before it: when a node dies mid-job, the system picks up that job (often from its last checkpoint) and relocates it to a different, healthy node, rather than waiting for the original node to come back.

## Reactive: Replication

Instead of relying on one copy of data or one instance of a service, **keep multiple identical copies running on different nodes**, so that if one fails, the others are already there and ready — no restart, no migration delay, just an immediate failover (or, in many designs, the other replicas were serving traffic the whole time anyway). This is the single most widely used fault-tolerance technique in real distributed systems, and it reappears constantly throughout the rest of this module, especially in the Consistency section below — because the moment you have multiple copies of the same data, you have to decide how to keep them in agreement.

## Case Study: Netflix's Chaos Monkey

Netflix famously built a tool, **Chaos Monkey**, that randomly kills production servers — on purpose, during business hours — specifically to force every team to build self-healing, replicated systems rather than systems that merely *hope* nothing fails. It's proactive fault tolerance taken to its logical extreme: instead of waiting to discover your fault tolerance doesn't actually work during a real outage, you manufacture small controlled outages constantly, so you find out immediately — a practice now broadly called "chaos engineering."

## Security Perspective

Checkpointing and replication both multiply the number of places sensitive data physically exists — a checkpoint file saved to disk is a new copy of memory contents (which might include secrets like session tokens or decrypted data) sitting on a filesystem; a replica is a full additional copy of a database, in a different place, that also needs to be secured, patched, and access-controlled. Fault tolerance and the "reduce your attack surface" principle are often in direct tension, which is one reason security and fault tolerance get taught together in this module instead of separately.

---

← [1. Fault Classification](01_fault_classification.md) · [Contents](README.md) · [3. Consistency](03_consistency.md) →
