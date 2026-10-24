*Module 3 · Part A: Virtualization and Resource Management*

# 4. Memory Management

## Translating an address twice

A process uses virtual addresses; its guest OS maps them to guest-physical addresses; the hypervisor maps those to real machine memory. Hardware support such as nested page tables accelerates this second translation while preserving isolation.

The hypervisor may manage memory with:

- **Reservation:** a minimum amount that must be available.
- **Ballooning:** a guest driver allocates guest memory on the hypervisor’s request, making it reclaimable.
- **Transparent page sharing/deduplication:** identical pages may be stored once (often limited because of side-channel concerns).
- **Compression and swapping:** last-resort ways to reclaim host RAM, usually harmful to latency.

## Overcommitment is a promise to manage risk

Allocated VM memory can exceed physical RAM when not every guest actively uses its maximum. Unlike CPU, memory pressure often hurts abruptly: swapping makes applications dramatically slower, and an out-of-memory condition can terminate work.

| Situation | Preferred response |
|---|---|
| Short, mild contention | Ballooning or reclaim unused cache |
| Sustained contention | Move/resize workloads or add RAM |
| Latency-critical database | Reserve memory; avoid swapping/overcommitment |

## Security perspective

Memory must be cleared before being reassigned to another tenant; otherwise a new VM could read old data. Hypervisor escapes and shared-memory side channels are also reasons to patch hosts promptly and limit untrusted co-tenancy.

---

← [3. CPU Management](03_cpu_management.md) · [Contents](README.md) · [5. Storage Management](05_storage_management.md) →
