# Lab 02: DOS vs NOS — Feel the Difference

> **Time:** 55 minutes | **Language:** Python | **Infrastructure:** Docker + Redis

## Objective
Build two Docker setups that simulate a **Network Operating System** (explicit resource sharing) and a **Distributed Operating System** (transparent shared memory). Experience the difference firsthand.

## What You'll Do

1. **NOS Mode:** 3 containers with separate filesystems, shared via Docker volumes (like NFS)
2. **DOS Mode:** 3 containers sharing state via Redis (simulating shared memory)
3. Compare: lines of code, ease of use, transparency

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3 redis
```

---

## Part A: Network OS Simulation (25 min)

### Concept
In a **Network OS**, each machine has its own resources. Sharing requires explicit actions (copy, mount, SSH).

Open `nos_simulation.py` — fill in the TODOs:

### What to build:
1. **File Server** (on node1): Serves files from a local directory over TCP
2. **File Client** (on node2/3): Requests files explicitly by sending filename

The key experience: **You always know where the file is.** There's no transparency.

```bash
# Node 1: Start file server
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode server

# Node 2: Request a file
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt

# Node 3: Also request a file
docker exec -it ds-python-node3 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt
```

### Discussion Points:
- You had to specify `--server node1` explicitly. That's NOS — no location transparency.
- If node1 dies, the file is gone. No automatic failover.

---

## Part B: Distributed OS Simulation (25 min)

### Concept
In a **Distributed OS**, resources appear to be local even when they're not. The system provides **transparency** — you don't know (or care) which node has the data.

Open `dos_simulation.py` — fill in the TODOs:

### What to build:
1. **Shared Memory** (via Redis): Any node writes → all nodes see it instantly
2. **Process Migration**: Start a computation on node1, save state, resume on node2

```bash
# Any node can write
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action write --key greeting --value "Hello from node1"

# Any OTHER node can read — instantly!
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action read --key greeting

# Process migration: start on node1, migrate to node2
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action start-task --task-id job42 --progress 0
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action resume-task --task-id job42
```

### Discussion Points:
- You didn't specify which node has the data — that's **location transparency**
- The process "migrated" — it started on node1 and continued on node2
- Redis is the hidden infrastructure making this work (like the kernel in a real DOS)

---

## Checkpoint Challenge

| Question | NOS | DOS |
|----------|-----|-----|
| How many lines of code to share a file? | ? | ? |
| Did you specify which node to read from? | Yes / No | Yes / No |
| What happens when the data node dies? | ? | ? |
| Is there a single point of failure? | ? | ? |

**Final discussion:** *"Modern systems like Kubernetes borrow ideas from both. Which features do you see?"*
