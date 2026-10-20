# Module 2: Fault Tolerance and Security in Distributed Systems

> **Format:** Theory-led, discussion-driven — analogies, real-world case studies, and discussion prompts rather than hands-on coding labs.
> **Audience:** Same as Module 1 — M.Tech Cyber Security students.
> **Builds on:** Module 1 (especially Lab 01's replication/failure concepts and the CAP-theorem framing already introduced there).

This module covers two topics that turn out to be the same discipline viewed from two angles: **keeping a distributed system working despite components that fail** (Part A), and **keeping it trustworthy despite components that get attacked** (Part B). By the end, a "monitoring system" and a "fault detector" should start to look like the same idea to you — [Topic 13](theory/13_auditing_and_monitoring.md) makes that connection explicit.

---

## Repository Structure

```
module_2/
├── README.md                          ← You are here
├── agenda.md                          ← Original syllabus
│
└── theory/                            ← The main content: one file per topic
    ├── README.md                      ← Contents, part intros, summary table
    ├── 01_fault_classification.md
    ├── 02_fault_tolerance_approaches.md
    ├── 03_consistency.md
    ├── 04_the_cia_triad.md
    ├── 05_threats.md
    ├── 06_authentication.md
    ├── 07_authorization.md
    ├── 08_encryption.md
    ├── 09_secure_communication_protocols.md
    ├── 10_access_control.md
    ├── 11_trust_management.md
    ├── 12_privacy_preserving.md
    └── 13_auditing_and_monitoring.md
```

---

## How to Use This Module

1. Start at [`theory/README.md`](theory/README.md) and read the 13 topic files in order, or pick a single topic — each file is self-contained enough to teach on its own, but they build on each other (especially within Part A, and within Part B).
2. Each major topic has a **Case Study** or **Discussion Prompt** callout — these are designed to be the centerpiece of a session, not an afterthought. Real incidents (Equifax, Mirai, SolarWinds, the Target breach, Netflix's Chaos Monkey, Amazon's shopping-cart story) make abstract theory memorable, and every one of them is something students can look up and read more about afterward.

## Session Breakdown

| Session | Covers | Topic files |
|---|---|---|
| **Session 1: Fault Tolerance & Consistency** | Crash vs Byzantine faults, proactive/reactive fault tolerance, the consistency spectrum, CAP theorem | [01](theory/01_fault_classification.md)–[03](theory/03_consistency.md) |
| **Session 2: Security** | CIA triad, threats, authentication, authorization, encryption, secure protocols, access control, trust, privacy, auditing | [04](theory/04_the_cia_triad.md)–[13](theory/13_auditing_and_monitoring.md) |

These are rough pacing guides, not a fixed clock schedule — some topics (CAP theorem, TLS handshakes) reliably need more discussion time than others.

## Why Theory-First for This Module

Module 1 was hands-on because the underlying mechanics (sockets, RPC, mutual exclusion) are things you only really understand by making them fail in front of you. Module 2's topics are different in kind — Byzantine fault tolerance, the CAP theorem, trust management, and most of the security section are primarily about **judgment and tradeoffs**, not mechanics you build yourself from scratch. A case study like the Equifax breach or the Target breach teaches the lesson ("defense in depth," "monitoring without response is nearly useless") more effectively than a toy lab would, and it's the kind of reasoning these students will actually be asked to apply on the job.
