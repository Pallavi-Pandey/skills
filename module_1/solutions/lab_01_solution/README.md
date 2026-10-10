# Lab 01 Solution — Centralized vs Distributed KV Store

Instructor-facing answer key for [`labs/lab_01_what_is_distributed/`](../../labs/lab_01_what_is_distributed/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the 3 Python containers
cd module_1/docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3

# 2. Part 1 — centralized: start the server, then benchmark it
docker exec -it ds-python-node1 python3 /app/solutions/lab_01_solution/centralized_kv.py
docker exec -it ds-python-node2 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --host node1 --port 5000

# 3. Part 2 — distributed: start all 3 nodes, then benchmark
docker exec -it ds-python-node1 python3 /app/solutions/lab_01_solution/distributed_kv.py --node-id 0 --port 5000
docker exec -it ds-python-node2 python3 /app/solutions/lab_01_solution/distributed_kv.py --node-id 1 --port 5000
docker exec -it ds-python-node3 python3 /app/solutions/lab_01_solution/distributed_kv.py --node-id 2 --port 5000
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --distributed --nodes node1:5000,node2:5000,node3:5000

# 4. Part 3 — chaos test
docker stop ds-python-node2
```

**Note:** `centralized_kv.py` here also adds a `threading.Lock()` around the dict access — not strictly required by the lab's TODOs, but good practice since multiple client threads can hit `self.store` concurrently. Worth pointing out if a student asks why the answer key has more code than the instructions described.
