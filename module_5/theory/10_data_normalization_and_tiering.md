*Module 5 · Part C: Specialized Architectures*

# 10. Dynamic Data Normalization and Tiering

**Dynamic data normalization** standardizes data representation or layout so data from different sources can be managed consistently. In storage architectures it can reduce duplication and make policy-based placement easier.

**Vertical tiering** moves data between performance/cost tiers, such as NVMe/SSD, standard disks, and archive storage. **Cross-storage-device tiering** moves data between devices; **intra-storage-device tiering** reorganizes data within one storage system. Frequently used (“hot”) data belongs on faster tiers, while older (“cold”) data can use economical capacity.

Tiering is a policy decision: classification, access patterns, latency targets, compliance, and recovery time must be known. Never tier data away solely because it looks idle if legal retention or recovery requirements demand rapid access.

---

## Lifecycle policies

A policy might keep recent transactions on a high-performance tier, move records not read for 90 days to a standard tier, and archive data after one year. Such rules should be observable and reversible. Test archive retrieval before an incident; low storage price is not useful if restoration takes too long.

## Classification first

Tiering must honor data classification. An archive may be cheaper but unsuitable for regulated data if encryption, retention locks, or regional residency are absent. Classify data by sensitivity, expected access pattern, legal retention, and required recovery time before an automated lifecycle rule moves it.

← [9. Direct I/O and LUN Access](09_direct_io_and_lun_access.md) · [Contents](README.md) · [11. Elastic Networks and Virtual Switches](11_elastic_networks_and_virtual_switches.md) →
