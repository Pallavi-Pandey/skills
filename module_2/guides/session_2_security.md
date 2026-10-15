# Session 2 Guide: Security in Distributed Systems

Covers `module_2_theory.md` §4–13. This guide is for pacing and facilitation — the actual content students need is already written out in the theory doc; use this for what to emphasize live, what to put on the board, and how to run each discussion.

---

## Opening (~5 min)

Open with the §4 observation that Availability is in both the CIA triad *and* CAP — don't let this slide by as a footnote. Explicitly tell the room: "everything we covered last session about fault tolerance was already one-third of today's topic." This reframes Session 2 as a continuation, not a context switch, and makes the §13 closing payoff (fault detection and intrusion detection are the same mechanism) land as a planned arc rather than a surprise.

## 4. CIA Triad (~10 min)

- Run the discussion prompt from §4 (the three incidents: leaked passwords / tampered transfer / DDoS) as a live poll before revealing the mapped answers — let students argue, especially about incidents that arguably hit more than one leg at once.

## 5. Threats (~10 min)

- Don't just list the threat categories — for each one, ask "what would this look like concretely, on a system you've actually used?" (e.g., "what's a replay attack on something you use daily?" → replaying a captured login request).
- STRIDE is worth mentioning by name even briefly — some students will encounter it again in security certifications or other courses, and the acronym gives them a retrieval hook.

## 6. Authentication (~10 min)

- **Case study:** Mirai botnet. The "~60 default passwords" detail is the hook — it's deliberately almost absurdly simple, which is the point: catastrophic failures often come from skipping something basic, not from a sophisticated attack.

## 7. Authorization (~10 min)

- Lead with the discussion prompt (the support tool that lets any agent view any customer's data) *before* defining least privilege formally — let the room propose fixes first, then name the principle they just reinvented.
- Explicitly distinguish this from Authentication (§6) again here — "logged in" vs. "allowed to" is a distinction students will keep blurring for the rest of the course if it's not drilled now.

## 8. Encryption (~15 min)

- Symmetric vs. asymmetric is the one piece of this session closest to "mechanics" rather than pure judgment — take the extra time, most students haven't seen this clearly explained before.
- Be explicit about the "use both together" punchline before moving to TLS in §9 — otherwise §9's handshake will feel like it's introducing a third, new thing instead of combining two things they just learned.
- **Case study:** Equifax. Emphasize the encryption-at-rest vs. in-transit distinction using this case specifically — the breach itself wasn't an encryption failure, but the *impact* was massively worsened by one.

## 9. Secure Communication Protocols (~10 min)

- Frame the TLS handshake explicitly as "everything from the last 20 minutes, in one real protocol you use every day" — walk through the 3 steps in §9 and have students name which earlier concept (§6, §8, CIA's Integrity leg) each step maps to, rather than presenting it as new material.

## 10. Access Control (~10 min)

- DAC/MAC/RBAC: don't just define them — ask students to name a system they've used that fits each model (Google Docs sharing = DAC; a classified government system = MAC; most workplace software = RBAC). RBAC deserves the most time since it's what they'll actually encounter professionally.

## 11. Trust Management (~15 min)

- **Case study:** SolarWinds. This is the heaviest case study in the module — budget real time for it. The key point to land explicitly: this wasn't a weak-encryption or weak-authentication failure, it was a failure of the *trust model itself* ("signed + from a known vendor" being treated as sufficient, with no mechanism to question it).
- Introduce Zero Trust as the industry's direct response to exactly this kind of failure — the "castle and moat vs. verify every request" framing works well as a closing image for this topic.

## 12. Privacy Preserving (~10 min)

- **Case study:** Cambridge Analytica. Explicitly contrast this with Equifax (§8) and SolarWinds (§11): no one "broke in" here — the harm came from data flowing exactly where the rules technically allowed. This distinction (security failure vs. privacy failure) is subtle and worth dwelling on.
- Differential privacy is the most mathematically abstract item in the whole module — a plain-language pass ("add just enough random noise that any one person's data can't be reliably extracted back out, but the overall pattern survives") is enough; this isn't the place for the underlying math.

## 13. Auditing and Monitoring (~15 min, deliberately the longest close)

- **Case study:** Target breach. Land hard on the specific detail: the alerts fired correctly. This is the single most important takeaway of the entire security section — detection without response is close to worthless, and it's an organizational failure mode, not a technical one.
- Finish with the explicit Part A ↔ Part B connection from the theory doc's closing section: a fault detector and an intrusion detector are the same kind of system, just watching for different kinds of misbehavior. Revisit whatever the room guessed in Session 1's wrap-up and confirm/correct it now.

## Wrap-up (~5 min)

Close the whole module by asking: *of everything covered across both sessions, which single failure (Equifax, Mirai, SolarWinds, Target, Amazon's cart problem) do you think was most preventable, and what one change would have stopped it?* This is a genuinely good exam/assignment question too, not just a discussion closer.
