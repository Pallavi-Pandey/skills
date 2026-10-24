*Module 3 · Part D: Introduction to Cloud Computing*

# 14. Cloud Mathematical Models

## Put the trade-offs into variables

Mathematical models do not predict cloud behavior perfectly. They make assumptions visible and give operators a way to reason about capacity, performance, and cost before an outage or bill forces the issue.

### Capacity and utilization

If a pool has total capacity \(C\) and current demand \(D\), utilization is:

\[
U = D/C
\]

At \(U \approx 1\), small bursts cause queues. Systems therefore keep headroom rather than planning for 100% utilization. If each instance provides service rate \(\mu\) requests/second and arrival rate is \(\lambda\), a stable system needs \(\lambda < n\mu\) for \(n\) equivalent instances.

### Queueing intuition

As utilization rises, waiting time rises nonlinearly. That is why autoscaling on a high but not saturated utilization threshold can be sensible: it needs time to provision new capacity. Latency-based scaling can be even better when the user-visible service-level objective is known.

### Cost model

A simplified hourly cost is:

\[
\text{Cost} = (n \times p_{compute}) + (g_{storage} \times p_{storage}) + (g_{egress} \times p_{egress}) + p_{managed}
\]

where prices reflect the chosen region and pricing plan. The model reminds us that idle VMs, snapshots, and network egress all cost money; exact provider prices are deliberately outside this course material because they change frequently.

## A safe autoscaling rule

Choose a target utilization \(U_t\) below saturation, observe demand over a window, and estimate desired instances as \(n_{desired}=\lceil D/(U_t\mu)\rceil\). Then add cooldowns, minimum/maximum bounds, health checks, and manual review for anomalous spikes. A formula is a control input, not a substitute for reliability engineering.

---

← [13. Cloud Computing Basics](13_cloud_computing_basics.md) · [Contents](README.md)
