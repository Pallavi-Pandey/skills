*Module 4 · Part A: Service Delivery Models*

# 2. Infrastructure as a Service (IaaS)

**IaaS** delivers virtualized compute, storage, and networking on demand. The consumer creates virtual machines, virtual networks, disks, and load-balancing resources through a console or API. Examples include virtual-machine offerings from major cloud providers.

The attraction is control: a team can choose its OS, install any compatible software, tune network rules, and migrate an existing application with relatively few code changes. The cost is operational responsibility: patching the guest OS, configuring backups, hardening network access, and monitoring capacity are still the customer's work.

| Good fit | Poor fit |
|---|---|
| Legacy/custom OS workloads, unusual runtimes, lift-and-shift migration | Teams that do not want to manage OS patching or servers |

## What an IaaS environment contains

IaaS is more than “a VM in somebody else's data center.” A normal environment combines several virtual resources:

| Resource | What it provides | Typical decisions for the consumer |
|---|---|---|
| Virtual machine | Compute, memory, and a guest operating system | Instance size, OS image, CPU/RAM, patch schedule |
| Virtual network | Private IP addresses, subnets, routes, and firewall rules | Which systems can communicate and which are Internet-facing |
| Block/object storage | Persistent disks, backups, files, and snapshots | Capacity, performance tier, encryption, retention |
| Identity and API | Accounts, roles, service identities, automation | Least privilege, MFA, key rotation, audit access |
| Load balancer | Traffic distribution across instances | Health checks, TLS certificates, routing, scaling |

The provider exposes these resources through a console, command-line tools, and APIs. That API-driven nature is important: a team can define an entire environment in code, review it like source code, and create the same design repeatedly for development, test, and production.

## Typical VM lifecycle

1. Select an approved machine image, such as a current Linux image.
2. Choose CPU, memory, disk, network, and identity settings.
3. Place the VM in a private subnet and grant only the required firewall rules.
4. Start it with a small initialization script or configuration-management tool.
5. Monitor resource use, application health, logs, and security events.
6. Snapshot/backup persistent data according to a recovery policy.
7. Stop, replace, resize, or delete the VM when its role changes.

This lifecycle is why “pets versus cattle” is a useful cloud idea. A **pet** VM is manually maintained and unique: if it fails, someone tries to repair it. A **cattle** VM is reproducible from an image and configuration: if it fails, automation replaces it. Critical data must live on managed persistent storage or backups, not only inside a replaceable VM.

## Security perspective

The provider protects the data center and hypervisor; the customer protects accounts, VM images, operating systems, keys, security groups, and data. An exposed management port or an unpatched VM is normally a customer configuration failure, even though it runs “in the cloud.”

### Network and identity controls

Most IaaS compromise paths begin with an identity or network mistake. Management services such as SSH, RDP, and administration dashboards should not be open to every Internet address. Use VPN/bastion access or an identity-aware management service, require MFA, and give applications service identities with narrowly scoped permissions. A VM that only reads one storage bucket should not also have permission to create users or delete all backups.

Encryption is needed both **in transit** (TLS for application traffic and administrative connections) and **at rest** (encrypted disks, snapshots, and backups). Encryption keys require their own access policy and audit trail; a key stored as plaintext in the VM image defeats much of the benefit.

---

## Operational baseline

Create IaaS VMs from versioned, patched images instead of configuring each machine manually. Use private networks by default, expose only required ports, use identity-based administration, and collect logs centrally. These controls reduce drift and make compromised instances replaceable.

## Cost and capacity

IaaS charges are usually based on running time, selected capacity, storage, backups, and network egress. An instance that is stopped may stop charging for compute but still charge for attached disks and snapshots. Tag resources by project/owner, set budgets and alerts, and delete test resources when finished. Right-sizing also matters: allocating 16 vCPUs to a service that normally uses one wastes money, but allocating too little capacity produces latency and failures.

## Worked example: hosting a departmental portal

A department has an existing portal written for Linux. It needs a custom library and cannot easily be moved to PaaS, so IaaS is a reasonable starting model. The design might use two identical web VMs behind a load balancer, a private database subnet, encrypted persistent disks, scheduled backups, and a least-privilege service identity. The team must decide how VM images are patched, how database recovery is tested, who may change firewall rules, and how it will scale during registration week. Those decisions are the real operational content of IaaS — creating a VM is the easy part.

← [1. Cloud Service Models](01_cloud_service_models.md) · [Contents](README.md) · [3. PaaS](03_paas.md) →
