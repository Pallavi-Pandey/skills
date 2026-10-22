*Module 2 · Part B: Security in Distributed Systems*

# 12. Privacy Preserving

## Privacy is not the same as confidentiality

Privacy is related to Confidentiality, but it's a distinct concern: Confidentiality is about *stopping unauthorized parties* from seeing data, while Privacy is about limiting what even *authorized* parties collect, retain, and do with personal data in the first place. A system can have perfect confidentiality — no one ever breaks in — and still violate the privacy of every person in it.

> **Simple analogy:** Your doctor is fully authorized to see your medical records, and their filing cabinet is locked (confidentiality). Privacy is the further set of questions: should the clinic have recorded your religion at all? Should it keep your records forever? Should it share them with an insurance company "for research"?

Distributed systems make privacy harder because personal data spreads: it gets replicated across regions, copied into analytics pipelines, cached, logged, and sent to third-party services. Each copy is another place the data can be misused, and deleting a person's data properly means finding all of them.

## Collect less, keep less

- **Data minimization** — only collect the data you actually need, so there's less to protect (and less to lose) in the first place. A delivery app needs your address, not your date of birth.
- **Purpose limitation** — data collected for one purpose (delivering your order) isn't quietly reused for another (selling your shopping habits).
- **Retention limits** — delete data when it's no longer needed. Data that no longer exists can't be leaked.

## Anonymization is harder than it looks

**Pseudonymization** replaces direct identifiers with a code: "Asha Rao" becomes "user 58213." **Anonymization** goes further and tries to make the data impossible to link back to a person at all. The problem is that removing names is almost never enough. Research by Latanya Sweeney found that about 87% of the US population could be uniquely identified by just three facts: ZIP code, date of birth, and gender. Records with no name in them can still be matched against another dataset that does have names.

**k-anonymity** is one attempt at a fix: generalize the data (age 34 becomes "30 to 39", a full postcode becomes its first three digits) until every record is identical to at least *k − 1* others on those identifying fields, so no record points to fewer than *k* people. It helps, but it can still leak information when everyone in a group shares the same sensitive value.

## Privacy-enhancing techniques

- **Differential privacy** — a mathematical technique for adding carefully calibrated statistical "noise" to query results or datasets, so aggregate patterns remain useful while no individual's specific data can be reliably reverse-engineered out of it. The guarantee: the result looks almost the same whether or not any one particular person's data was included. Apple and the US Census Bureau both use this in production.
- **Federated learning** — instead of sending everyone's data to a central server to train a machine learning model, the model is sent to the data. Each phone trains on its own data locally and sends back only the model updates. Google uses this to improve keyboard word predictions without collecting what people type.
- **Secure multi-party computation** — several parties jointly compute a result (for example, "which of us has the highest salary?" or "do our two customer lists overlap?") without any of them revealing their own input to the others.
- **Homomorphic encryption** — allows computation directly on encrypted data: a cloud server can add up encrypted numbers and return an encrypted total, without ever seeing the numbers. Still much slower than ordinary computation, but improving.

| Technique | What it protects | Typical use |
|---|---|---|
| Data minimization | Everything you never collected | Any system design |
| Pseudonymization | Direct identifiers | Internal analytics |
| k-anonymity | Re-identification from combinations of fields | Releasing datasets |
| Differential privacy | Any individual's contribution to a statistic | Census data, usage statistics |
| Federated learning | Raw data never leaves the device | Machine learning on phones |
| Multi-party computation / homomorphic encryption | Inputs during computation | Joint analysis between organizations |

## Privacy law

Privacy is increasingly a legal requirement, not just good practice. The EU's **General Data Protection Regulation (GDPR)**, in force since 2018, and India's **Digital Personal Data Protection Act, 2023** both require a lawful basis or consent for processing personal data, limit use to the stated purpose, and give individuals rights such as correcting or erasing their data. For a distributed system, a "right to erasure" request is an engineering problem: the data must be removed from every replica, cache, backup, and downstream service it reached.

## Case Study: The Netflix Prize (2006–2010)

Netflix released 100 million movie ratings from about 480,000 subscribers for a public competition to improve its recommendation algorithm, with names replaced by random numbers. In 2008, researchers Arvind Narayanan and Vitaly Shmatikov showed that many subscribers could be re-identified by matching the timing and content of their ratings against public reviews on IMDb — sometimes from as few as a handful of ratings. Movie ratings can reveal political views, religion, and sexual orientation. After a lawsuit and a regulatory inquiry, Netflix cancelled a planned second competition.

## Case Study: Cambridge Analytica (2018)

Cambridge Analytica obtained Facebook data on as many as 87 million users — not primarily through a technical hack, but through permissive data-sharing policies that let a third-party app collect data on users' *friends* who had never consented to or even known about that app. This wasn't a Confidentiality failure in the traditional sense (no one "broke in"); it was a Privacy failure — data flowed exactly where the system's rules technically allowed it to, and those rules themselves were the problem.

---

← [11. Trust Management](11_trust_management.md) · [Contents](README.md) · [13. Auditing and Monitoring](13_auditing_and_monitoring.md) →
