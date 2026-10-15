# Module 2: Fault Tolerance and Security in Distributed Systems

> **Format:** Theory-led, discussion-driven — analogies, real-world case studies, and discussion prompts rather than hands-on coding labs.
> **Audience:** Same as Module 1 — M.Tech Cyber Security students.
> **Builds on:** Module 1 (especially Lab 01's replication/failure concepts and the CAP-theorem framing already introduced there).

This module covers two topics that turn out to be the same discipline viewed from two angles: **keeping a distributed system working despite components that fail** (Part A), and **keeping it trustworthy despite components that get attacked** (Part B). By the end, a "monitoring system" and a "fault detector" should start to look like the same idea to you — Section 13 makes that connection explicit.

---

## Repository Structure

```
module_2/
├── README.md                          ← You are here
├── agenda.md                          ← Original syllabus
├── module_2_theory.md                 ← The main content: all 13 topics, case studies, analogies
│
└── guides/                            ← Instructor-facing session guides
    ├── session_1_fault_tolerance.md   ← Fault Classification, Fault Tolerance Approaches, Consistency
    └── session_2_security.md          ← CIA Triad through Auditing and Monitoring
```

---

## How to Use This Module

1. Read [`module_2_theory.md`](module_2_theory.md) start to finish, or topic by topic — each of the 13 sections is self-contained enough to teach on its own, but they build on each other (especially within Part A, and within Part B).
2. Each major topic has a **📖 Case Study** or **💭 Discussion Prompt** callout — these are designed to be the centerpiece of a session, not an afterthought. Real incidents (Equifax, Mirai, SolarWinds, the Target breach, Netflix's Chaos Monkey, Amazon's shopping-cart story) make abstract theory memorable, and every one of them is something students can look up and read more about afterward.
3. Use the two session guides in `guides/` for suggested pacing, talking points, and additional discussion angles beyond what's in the theory doc itself.

## Session Breakdown

| Session | Covers | Theory doc sections |
|---|---|---|
| **Session 1: Fault Tolerance & Consistency** | Crash vs Byzantine faults, proactive/reactive fault tolerance, the consistency spectrum, CAP theorem | §1–3 |
| **Session 2: Security** | CIA triad, threats, authentication, authorization, encryption, secure protocols, access control, trust, privacy, auditing | §4–13 |

These are rough pacing guides, not a fixed clock schedule — some topics (CAP theorem, TLS handshakes) reliably need more discussion time than others.

## Why Theory-First for This Module

Module 1 was hands-on because the underlying mechanics (sockets, RPC, mutual exclusion) are things you only really understand by making them fail in front of you. Module 2's topics are different in kind — Byzantine fault tolerance, the CAP theorem, trust management, and most of the security section are primarily about **judgment and tradeoffs**, not mechanics you build yourself from scratch. A case study like the Equifax breach or the Target breach teaches the lesson ("defense in depth," "monitoring without response is nearly useless") more effectively than a toy lab would, and it's the kind of reasoning these students will actually be asked to apply on the job.
