*Module 2 · Part B: Security in Distributed Systems*

# 12. Privacy Preserving

Privacy is related to Confidentiality, but it's a distinct concern: Confidentiality is about *stopping unauthorized parties* from seeing data, while Privacy is about limiting what even *authorized* parties collect, retain, and do with personal data in the first place. Key techniques:

- **Data minimization** — only collect the data you actually need, so there's less to protect (and less to lose) in the first place.
- **Anonymization / pseudonymization** — strip or replace identifying details so data can still be useful (e.g., for analytics) without being traceable back to a specific person.
- **Differential privacy** — a mathematical technique for adding carefully calibrated statistical "noise" to query results or datasets, so aggregate patterns remain useful while no individual's specific data can be reliably reverse-engineered out of it. (Apple and the US Census Bureau both use this in production.)

## Case Study: Cambridge Analytica (2018)

Cambridge Analytica obtained Facebook data on roughly 87 million users — not primarily through a technical hack, but through permissive data-sharing policies that let a third-party app collect data on users' *friends* who had never consented to or even known about that app. This wasn't a Confidentiality failure in the traditional sense (no one "broke in"); it was a Privacy failure — data flowed exactly where the system's rules technically allowed it to, and those rules themselves were the problem.

---

← [11. Trust Management](11_trust_management.md) · [Contents](README.md) · [13. Auditing and Monitoring](13_auditing_and_monitoring.md) →
