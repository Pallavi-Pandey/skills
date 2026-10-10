# Lab 04 Solution — Multi-Client Chat Server

Instructor-facing answer key for [`labs/lab_04_client_server/`](../../labs/lab_04_client_server/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the 3 Python containers
cd module_1/docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3

# 2. Phase 1/2 — quick local check (server + one client, same container)
docker exec -it ds-python-node1 python3 /app/solutions/lab_04_solution/chat_server.py
docker exec -it ds-python-node1 python3 /app/solutions/lab_04_solution/chat_client.py --host localhost --name Alice

# 3. Phase 3 — server and clients on separate containers
docker exec -it ds-python-node1 python3 /app/solutions/lab_04_solution/chat_server.py
docker exec -it ds-python-node2 python3 /app/solutions/lab_04_solution/chat_client.py --host node1 --name Alice
docker exec -it ds-python-node3 python3 /app/solutions/lab_04_solution/chat_client.py --host node1 --name Bob
```
