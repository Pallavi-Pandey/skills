# Lab 05 Solution — RPC from Scratch → gRPC

Instructor-facing answer key for [`labs/lab_05_rpc/`](../../labs/lab_05_rpc/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the containers: Python nodes for Part A, Go nodes for Part B
cd module_1/docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 go-node1 go-node2

# 2. Part A — RPC from scratch (Python)
docker exec -it ds-python-node1 python3 /app/solutions/lab_05_solution/rpc_server.py
docker exec -it ds-python-node2 python3 /app/solutions/lab_05_solution/rpc_client.py --host node1

# 3. Part B — gRPC (Go): already generated, go.mod/go.sum already resolved —
#    no need to re-run protoc, just run the server and client directly
docker exec -it ds-go-node1 sh
cd /app/solutions/lab_05_solution/grpc_go/
go run server/main.go

# 4. Part B — gRPC client (on go-node2, separate terminal)
docker exec -it ds-go-node2 sh
cd /app/solutions/lab_05_solution/grpc_go/
go run client/main.go --server go-node1:50051
```

**Note:** unlike the starter (`labs/lab_05_rpc/grpc_go/`), this solution's `calculator/` package is already generated and committed, and `go.mod`/`go.sum` are already resolved — so you can run it directly without the `protoc` codegen step the starter's README walks students through.
