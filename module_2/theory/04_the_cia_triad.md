*Module 2 · Part B: Security in Distributed Systems*

# 4. The CIA Triad

Almost everything in security can be organized under three goals, together called the **CIA Triad**:

- **Confidentiality** — only authorized parties can read the data. (Stopped by: eavesdropping, data breaches.)
- **Integrity** — data can't be modified without detection. (Stopped by: tampering, corruption, man-in-the-middle attacks.)
- **Availability** — the system is accessible to legitimate users when they need it. (Stopped by: denial-of-service, outages.)

Notice that **Availability is also one of the three CAP guarantees** from Part A — fault tolerance and security are not separate disciplines here, they overlap directly. A well-executed denial-of-service attack and an unplanned network partition can look, from the system's point of view, like the exact same problem: "some nodes can't be reached right now." Everything from here on is about defending Confidentiality and Integrity specifically, since Part A already covered Availability in depth.

## Discussion Prompt

For each of these real incidents, which leg (or legs) of the CIA triad actually failed: a) a hacked database of customer emails and passwords gets published online, b) an attacker modifies a bank transfer's destination account number in transit, c) a botnet floods a company's website with fake traffic until it falls over? (Answers: a = Confidentiality, b = Integrity, c = Availability — but push students to notice real incidents are often more than one of these at once.)

---

← [3. Consistency](03_consistency.md) · [Contents](README.md) · [5. Threats](05_threats.md) →
