# Lab 05: Remote Procedure Call — From Scratch to gRPC

> **Time:** 55 minutes | **Language:** Python (Part A) + Go (Part B)

## Objective
1. Build a simple RPC framework from scratch in Python (understand the internals)
2. Use real gRPC with Protocol Buffers in Go (industry standard)

## Part A: RPC from Scratch (Python, 25 min)

### The Idea
RPC makes a remote function call LOOK like a local one:
```python
# Without RPC (manual socket work)
sock.send(b'{"func": "add", "args": [5, 3]}')
result = json.loads(sock.recv(1024))

# With RPC (feels local!)
result = server.add(5, 3)  # This actually goes over the network
```

Open `rpc_server.py` and `rpc_client.py` — fill in the TODOs.

```bash
# Server
docker exec -it ds-python-node1 python3 /app/labs/lab_05_rpc/rpc_server.py

# Client
docker exec -it ds-python-node2 python3 /app/labs/lab_05_rpc/rpc_client.py --host node1
```

## Part B: gRPC with Go (30 min)

### Setup
```bash
docker exec -it ds-go-node1 sh
cd /app/labs/lab_05_rpc/grpc_go/

# Generate Go code from .proto file
protoc --go_out=. --go-grpc_out=. calculator.proto

# Run server
go run server/main.go

# In another terminal — run client
docker exec -it ds-go-node2 sh
cd /app/labs/lab_05_rpc/grpc_go/
go run client/main.go --server go-node1:50051
```

## Checkpoint
- Call `add(100, 200)` from the Python RPC client. What do you see on the server?
- Call the Go gRPC `Calculate` method from a Python gRPC client. Cross-language RPC!
- What happens if the server is down when you call? How would you add retries?
