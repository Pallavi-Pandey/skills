# Session 1 Guide: Fault Tolerance & Consistency

Covers theory topics 1–3 ([`theory/01`](../theory/01_fault_classification.md)–[`03`](../theory/03_consistency.md)). This guide is for pacing and facilitation — the actual content students need is already written out in the topic files; use this for what to emphasize live, what to put on the board, and how to run each discussion.

---

## Opening (~5 min)

Don't start with definitions. Start with the group-project analogy from [topic 1](../theory/01_fault_classification.md): a remote teammate who's gone silent (crash fault) vs. one who's still responding but sending contradictory information (Byzantine fault). Ask the room: *which one would you rather deal with, and why?* Nearly everyone picks "gone silent" instantly, without needing the vocabulary yet — that instinct is the entire lesson of this section, just confirm it with the formal definitions afterward.

## 1. Fault Classification (~20 min)

- Put the crash-vs-Byzantine comparison table from [topic 1](../theory/01_fault_classification.md) on the board as you go, filling it in live rather than presenting it pre-made.
- Walk through the Byzantine Generals Problem as a story, not a formula — the "3f+1" result lands much better once students have already felt, intuitively, why agreement is hard when you can't tell who's lying.
- **Case study:** Bitcoin/Byzantine fault tolerance at scale. Most students will have heard of Bitcoin; few will have connected it to a 1982 distributed-systems paper. That connection is usually the single most memorable moment of this section.
- **Checkpoint question to ask the room:** "Is a slow node a crash fault, a Byzantine fault, or neither?" (Answer: neither, technically — but it's a great trap question, since a sufficiently slow node is often *treated* as crashed via timeout, which is worth surfacing.)

## 2. Fault Tolerance Approaches (~20 min)

- Frame proactive vs. reactive with a concrete pair before naming the six specific techniques: *"Replacing your car's brake pads before they wear out" (proactive) vs. "calling a tow truck after they fail on the highway" (reactive).* Then map Self-Healing/Pre-emptive Migration/System Rejuvenation and Checkpoint-Restart/Job Migration/Replication onto that frame.
- **Case study:** Netflix's Chaos Monkey. This one tends to provoke genuine surprise/pushback ("wait, they do this on purpose, in production?") — let that reaction happen, it's doing the work of making the concept stick.
- Worth a short tangent: ask why System Rejuvenation ("just restart things on a schedule") counts as real engineering rather than a hack. (It's a legitimate answer to software aging/memory leaks — not every fault needs a sophisticated fix.)

## 3. Consistency / CAP Theorem (~25 min — this one runs long, budget for it)

- This is the hardest concept in the session. Use the two-bank-branches-with-a-dead-phone-line analogy from [topic 3](../theory/03_consistency.md) *before* stating CAP formally — students who get the analogy first rarely struggle with the theorem statement afterward; students who get the theorem first often struggle with the analogy as a "proof" rather than an intuition pump.
- Common misconception to address head-on: students often think CAP means "pick any 2 of 3, always." Be explicit that Partition tolerance isn't really a choice for a genuinely distributed system — the real tradeoff that shows up in practice is CP vs. AP, specifically *during* a partition.
- **Case study:** Amazon's shopping cart problem. This is the best bridge from "abstract theorem" to "a company's actual multi-million-dollar engineering decision" — it's worth spending real time on the "why would you ever choose availability over correctness?" framing.
- Close with the [topic 3](../theory/03_consistency.md) security perspective (stale permissions = a vulnerability window) to set up Session 2 — this is a deliberate connective thread, not a throwaway line.

## Wrap-up (~5 min)

Ask the room to summarize, in one sentence each, how Fault Tolerance (Part A) and Security (coming in Session 2) might turn out to be related. Don't correct wrong answers yet — Session 2's closing section ([topic 13](../theory/13_auditing_and_monitoring.md)) will answer this explicitly, and it lands better if they've already guessed at it themselves first.
