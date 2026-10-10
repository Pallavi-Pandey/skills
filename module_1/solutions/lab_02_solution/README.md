# Lab 02 Solution — DOS vs NOS

Instructor-facing answer key for [`labs/lab_02_dos_vs_nos/`](../../labs/lab_02_dos_vs_nos/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the 3 Python containers + Redis
cd module_1/docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3 redis

# 2. Part 1 — NOS: file server on node1, clients request it explicitly by name
docker exec -it ds-python-node1 python3 /app/solutions/lab_02_solution/nos_simulation.py --mode server
docker exec -it ds-python-node2 python3 /app/solutions/lab_02_solution/nos_simulation.py --mode client --server node1 --file test.txt
docker exec -it ds-python-node3 python3 /app/solutions/lab_02_solution/nos_simulation.py --mode client --server node1 --file test.txt

# 3. Part 2 — DOS: any node can write/read without naming a server
docker exec -it ds-python-node1 python3 /app/solutions/lab_02_solution/dos_simulation.py --action write --key greeting --value "Hello from node1"
docker exec -it ds-python-node2 python3 /app/solutions/lab_02_solution/dos_simulation.py --action read --key greeting
docker exec -it ds-python-node1 python3 /app/solutions/lab_02_solution/dos_simulation.py --action start-task --task-id job42 --progress 0
docker exec -it ds-python-node2 python3 /app/solutions/lab_02_solution/dos_simulation.py --action resume-task --task-id job42
docker exec -it ds-python-node3 python3 /app/solutions/lab_02_solution/dos_simulation.py --action list
```

**Note:** `nos_simulation.py`'s `start()` always (re)writes `/shared/test.txt` with its own content on startup — if you create a test file manually beforehand, the server will overwrite it the moment it starts. That's expected, not a bug.
