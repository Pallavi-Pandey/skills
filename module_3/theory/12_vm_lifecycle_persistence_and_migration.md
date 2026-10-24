*Module 3 · Part C: Information Model for Virtual Machines*

# 12. VM Lifecycle, Data Persistence, and Migration Models

## Operate from creation to retirement

The **lifecycle management model** specifies allowed state transitions and who may request them: create, configure, start, stop, suspend, snapshot, resize, migrate, recover, and delete. Automation should make invalid or unsafe transitions difficult.

The **data persistence model** distinguishes ephemeral state (temporary disk/cache that may disappear with an instance) from durable state (managed disks, object storage, backups). Design applications so important data survives replacement of a VM.

## Moving a running VM

**Cold migration** stops a VM, copies/moves it, then starts it elsewhere. **Live migration** copies most memory while the VM runs, briefly pauses it to transfer final changed pages and CPU state, then resumes it on the destination. Shared storage simplifies migration; storage migration must move disk blocks too.

| Benefit | Risk/requirement |
|---|---|
| Host maintenance without a long outage | Compatible CPU/platform and network reachability |
| Load balancing | Memory-heavy workload may dirty pages faster than copying |
| Fault avoidance | Persistent storage and sessions must survive the move |

## Security perspective

Migration traffic and VM snapshots can contain the entire live memory image, including keys and tokens. Encrypt management/migration channels, restrict operators, maintain audit logs, and securely wipe decommissioned hosts and volumes.

---

← [11. Performance and Security Models](11_vm_performance_and_security_models.md) · [Contents](README.md) · [13. Cloud Computing Basics](13_cloud_computing_basics.md) →
