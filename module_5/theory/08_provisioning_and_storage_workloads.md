*Module 5 · Part B: Advanced Architectures*

# 8. Bare-Metal/Rapid Provisioning and Storage Workload Management

**Bare-metal provisioning** supplies an entire physical server to one consumer, avoiding hypervisor overhead and giving direct hardware control. It is useful for specialized accelerators, licensing constraints, or strict performance isolation, but starts more slowly than a VM.

**Rapid provisioning** shortens the time from request to usable service through templates, images, infrastructure as code, and automated configuration. Speed without governance is dangerous: templates must be patched, approved, and traceable.

**Storage workload management** matches workload behavior to storage resources. A database needing low-latency random I/O differs from a backup job needing high sequential throughput. Use QoS, tiers, schedules, and monitoring to prevent background work from starving production services.

---

## Image hygiene

Rapid provisioning depends on trustworthy images. Build images automatically, scan packages, remove default accounts and secrets, apply security updates, record provenance, and retire old versions. A fast pipeline that distributes a vulnerable image merely scales the vulnerability faster.

## Storage QoS

Storage quality of service can reserve IOPS for an important database, cap a noisy background task, or schedule backup jobs outside peak hours. Monitor tail latency rather than average latency: a few very slow writes can affect transactions even when the average looks acceptable.

← [7. Reservation and Recovery](07_reservation_and_failure_recovery.md) · [Contents](README.md) · [9. Direct I/O and LUN Access](09_direct_io_and_lun_access.md) →
