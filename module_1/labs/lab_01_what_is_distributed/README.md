# Lab 01: Centralized vs Distributed — See the Difference

> **Time:** 40 minutes | **Language:** Python | **Infrastructure:** Docker

## Objective
Build a simple key-value store in two modes: centralized (1 node) and distributed (3 nodes). Benchmark both. See why distribution matters.

## What You'll Do

1. Run a centralized KV store → benchmark it → kill it → everything dies
2. Run a 3-node distributed KV store → benchmark it → kill a node → it survives
3. Compare throughput, latency, and fault tolerance

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3
```

## Instructions

### Part 1: Centralized KV Store (15 min)

Open `centralized_kv.py` — fill in the TODOs:

1. Create a TCP server that stores key-value pairs in a dictionary
2. Support two operations: `SET key value` and `GET key`
3. Handle one client at a time

**Test it:**
```bash
# Terminal 1 (inside python-node1)
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/centralized_kv.py

# Terminal 2 (run the benchmark)
docker exec -it ds-python-node2 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --host node1 --port 5000
```

### Part 2: Distributed KV Store (20 min)

Open `distributed_kv.py` — fill in the TODOs:

1. Partition keys across 3 nodes using hash partitioning: `node = hash(key) % 3`
2. Each node stores only its partition
3. A client can connect to ANY node — if the key isn't local, forward to the right node

**Test it:**
```bash
# Start all 3 nodes
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 0 --port 5000
docker exec -it ds-python-node2 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 1 --port 5000
docker exec -it ds-python-node3 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 2 --port 5000

# Benchmark
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --distributed --nodes node1:5000,node2:5000,node3:5000
```

### Part 3: Chaos Test (5 min)

```bash
# Kill node 2
docker stop ds-python-node2

# Try to GET a key that was on node 2
# What happens? → Error! That partition is gone.

# Try to GET a key on node 1
# What happens? → Still works! Partial failure, not total failure.
```

## Checkpoint Questions

1. Which mode had higher throughput for writes?
2. What happened when you killed a node in each mode?
3. How would you make the distributed version survive a node failure? (Hint: replication)
