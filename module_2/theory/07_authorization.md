*Module 2 · Part B: Security in Distributed Systems*

# 7. Authorization

## What are you allowed to do?

**Authorization answers the question "now that I know who you are, what are you allowed to do?"** — this is a distinct step that happens *after* authentication, and it's a common mistake to conflate the two. Being logged in (authenticated) doesn't mean you should be able to do everything the system can do.

> **Simple analogy:** In the hotel from [topic 6](06_authentication.md), the front desk checking your ID is authentication. Your key card opening room 412 and the gym, but not room 413 or the staff office, is authorization. Two guests can be equally well authenticated and still be allowed into completely different places.

Authorization is the *policy* — the rules about who may do what. [Topic 10](10_access_control.md), Access Control, covers the *mechanisms* that enforce those rules on every request.

## Guiding principles

- **Least privilege** — every user, process, and service should have the minimum set of permissions needed to do its job, and nothing more — so that if that identity is ever compromised, the damage it can do is limited by design, not by luck.
- **Separation of duties** — no single identity should be able to complete a sensitive action alone. The person who requests a large payment shouldn't be the one who approves it; the developer who writes code shouldn't be the only one who can deploy it to production.
- **Need to know** — even within a permitted category of data, access only the specific records your task requires. A doctor can read patient records, but only for patients they are treating.
- **Default deny** — if no rule explicitly allows an action, it's refused. Systems that allow by default and block known-bad actions eventually miss one.

## Privilege escalation

Most authorization attacks are an attempt to get more access than you were given:

- **Vertical escalation** — an ordinary user gains administrator powers, e.g. by calling an admin-only API endpoint the user interface never shows them but the server never checks.
- **Horizontal escalation** — a user gains access to *another user's* data at the same level, e.g. changing `/orders/1001` to `/orders/1002` in a URL and seeing a stranger's order.

Both usually come from the same root mistake: the check was done in the user interface, or not at all, instead of on the server for every request.

## Authorization between services

In a distributed system, most requests don't come straight from a user — they pass through several services. That creates two problems a single machine doesn't have.

**Delegation.** If you let a photo-printing website access your Google Photos, it shouldn't receive your password, and it shouldn't be able to read your email. **OAuth 2.0** solves this: you approve a limited set of **scopes** (for example, "read photos only"), and the website gets an access token that carries only those scopes, expires on its own, and can be revoked without changing your password. When you see "This app wants to: view your profile, read your contacts," you are looking at OAuth scopes.

**The confused deputy.** Suppose a file-conversion service runs with permission to read *every* user's files, so it can do its job. A user asks it to convert `/users/someone_else/salary.pdf`. If the service only checks its own permissions — and not whether the *user who asked* is allowed to read that file — it has been tricked into using its power on the attacker's behalf. The fix is to pass the original user's identity along with each request, and have each service authorize based on who the request is really for, not just who is making the call.

## Case Study: The Capital One Breach (2019)

An attacker found a misconfigured web application firewall running on Capital One's Amazon Web Services infrastructure. By tricking it into making a request to an internal AWS address (a technique called server-side request forgery), the attacker obtained temporary credentials belonging to the firewall's cloud role. That role had far more permission than a firewall needs: it could list and read the company's storage buckets. The result was the exposure of data on roughly 106 million people in the US and Canada, and an 80 million dollar regulatory fine.

The initial bug was real, but it was overly broad authorization that turned one misconfigured component into a massive breach. With least privilege applied, the stolen credentials would have opened almost nothing.

## Discussion Prompt

A company's customer-support tool lets any support agent view *any* customer's full account details, including payment information, "just in case they need it." Using the principles on this page, how would you redesign this access model? Things to consider: scoping access to only the customers an agent is actively assigned to, hiding payment details unless the task needs them, making access expire when the support ticket is closed, and recording every access so it can be reviewed later — a preview of [Access Control](10_access_control.md) and [Auditing](13_auditing_and_monitoring.md).

---

← [6. Authentication](06_authentication.md) · [Contents](README.md) · [8. Encryption](08_encryption.md) →
