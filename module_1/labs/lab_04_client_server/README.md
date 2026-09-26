# Lab 04: Multi-Client Chat Server

> **Time:** 55 minutes | **Language:** Python | **Infrastructure:** Docker

## Objective
Build a real multi-client chat server demonstrating the client-server model with concurrent connections.

## What You Build
A chat server that:
- Accepts multiple simultaneous TCP clients
- Broadcasts messages from one client to ALL others
- Handles disconnects gracefully
- Runs across Docker containers

## Instructions

### Phase 1: Single-Threaded Server (15 min)
Open `chat_server.py` — the single-threaded version blocks on one client!

### Phase 2: Multi-Threaded Server (25 min)
Fix it — use `threading.Thread` so each client gets its own thread.

### Phase 3: Docker Networking (15 min)
Run server on node1, connect clients from node2 and node3.

```bash
# Server
docker exec -it ds-python-node1 python3 /app/labs/lab_04_client_server/chat_server.py

# Client 1 (different container!)
docker exec -it ds-python-node2 python3 /app/labs/lab_04_client_server/chat_client.py --host node1 --name Alice

# Client 2 (another container!)
docker exec -it ds-python-node3 python3 /app/labs/lab_04_client_server/chat_client.py --host node1 --name Bob
```

## Checkpoint
- Connect 3+ clients. Send a message from one. Did all others receive it?
- Kill one client's container (`docker stop ds-python-node2`). Did the server crash?
- What's the max number of concurrent clients your server can handle?
