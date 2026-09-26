# Lab 07: Distributed Mutual Exclusion — Token Ring

> **Time:** 15 minutes | **Language:** Go | **Infrastructure:** Docker

## Objective
Implement the Token Ring mutual exclusion algorithm across Docker containers.

## How Token Ring Works
```
  Node 0 → Node 1 → Node 2 → Node 3
    ↑                                ↓
    ←─────────────────────────────────
```
1. One token circulates around the ring
2. Only the node holding the token can enter the critical section
3. After finishing, pass the token to the next node

## Instructions

Open `token_ring.go` — fill in the TODOs:

```bash
# Start 4 nodes in separate terminals
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --id 0 --total 4
docker exec -it ds-go-node2 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --id 1 --total 4

# Or run the all-in-one simulation:
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --simulate --total 4
```

## Checkpoint
- Does any node ever enter the critical section simultaneously?
- Kill the token holder. What happens? (Token loss problem!)
- How would you detect and regenerate a lost token?
