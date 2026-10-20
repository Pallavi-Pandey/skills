*Module 2 · Part A: Fault Tolerance & Consistency*

# 1. Fault Classification

## What is a fault, exactly?

A **fault** is anything that causes a system to deviate from its intended behavior. In a single computer, a fault is usually obvious — the program crashes, or the screen freezes. In a distributed system, faults are sneakier: one node can misbehave while the rest of the system carries on, and from the outside you might not even be able to tell *which* node is at fault, or whether it's at fault at all.

> **Simple analogy:** Imagine a group project with five teammates spread across different cities, coordinating only by text message. If one teammate suddenly goes silent, is it because their phone died (easy to reason about — they're just gone), or because they're still texting, but now sending wrong, contradictory information on purpose or by mistake (much harder to reason about — you have to figure out *who* to trust)? Distributed systems have to plan for both.

## Crash Faults

A **crash fault** is the "polite" failure: a node simply stops. It doesn't respond, it doesn't send corrupted data, it doesn't lie — it's just gone, the way a teammate whose phone died is just gone. Once you detect it's gone (usually via a timeout — "I haven't heard from it in N seconds"), you know exactly what you're dealing with: a node is unavailable, full stop.

This is the easiest class of fault to tolerate, because the failure mode is simple and honest. Most of the fault-tolerance techniques in this module — replication, checkpoint-restart, job migration — are primarily built to survive crash faults.

## Byzantine Faults

A **Byzantine fault** is the dangerous one: a node keeps participating, but behaves **arbitrarily or maliciously** — sending different (possibly contradictory) information to different parts of the system, or data that's subtly wrong rather than obviously broken. The name comes from the **Byzantine Generals Problem**, a thought experiment from a 1982 paper by Leslie Lamport, Robert Shostak, and Marshall Pease:

> Several generals, each commanding part of the Byzantine army, surround an enemy city. They can only communicate by messenger, and they must unanimously decide: attack, or retreat. If even one general is a traitor, they can send "attack" to some generals and "retreat" to others — enough to make the loyal generals attack piecemeal and lose, purely through deliberately inconsistent messaging. The hard question the paper asks: how many loyal generals does it take to reach agreement despite some number of traitors?

The headline result: with simple messaging, you need **more than 3× the number of traitors** in total participants to guarantee agreement — i.e., to tolerate *f* Byzantine nodes, you need at least *3f + 1* total nodes. That's expensive, which is exactly why Byzantine fault tolerance (BFT) is only used where it's really warranted.

| | Crash Fault | Byzantine Fault |
|---|---|---|
| **Behavior** | Stops responding entirely | Keeps responding, but with wrong/contradictory data |
| **Detectability** | Easy — timeout tells you | Hard — the node *looks* alive |
| **Cause** | Hardware failure, crash, network drop | Bug, corruption, or a malicious/compromised node |
| **Tolerance cost** | Cheap (e.g., 2f+1 nodes to survive f crashes) | Expensive (3f+1 nodes to survive f Byzantine nodes) |

## Case Study: Bitcoin as Byzantine Fault Tolerance at Planetary Scale

Bitcoin's entire security model is a practical answer to the Byzantine Generals Problem, just rebranded: thousands of anonymous nodes ("miners") need to agree on one shared transaction history, even though some of them may be actively lying to double-spend coins. Its "proof-of-work" consensus mechanism makes lying *computationally expensive* rather than relying on trust — a direct, real-world instance of Byzantine agreement that most students will have already heard of without knowing it has a name in distributed systems theory.

## Security Perspective

A compromised node is, almost by definition, a Byzantine node — it's still "alive" and responding, but under an attacker's control it can now lie, forge data, or selectively target specific peers. This is exactly why security-critical distributed systems (blockchains, some banking infrastructure, aircraft flight-control systems) are built with explicit Byzantine fault tolerance, even at significant extra cost, while an ordinary web backend usually only bothers to tolerate crash faults.

---

← [Contents](README.md) · [Contents](README.md) · [2. Fault Tolerance Approaches](02_fault_tolerance_approaches.md) →
