# Lab 07 Solution — Token Ring Mutual Exclusion

Instructor-facing answer key for [`labs/lab_07_mutual_exclusion/`](../../labs/lab_07_mutual_exclusion/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the Go container
cd module_1/docker/
docker compose -f network-setup.yml up -d go-node1

# 2. Run the simulation (all 4 nodes run inside this one command)
docker exec -it ds-go-node1 go run /app/solutions/lab_07_solution/token_ring.go --total 4

# Optional: change the ring size / how many critical-section rounds to run
docker exec -it ds-go-node1 go run /app/solutions/lab_07_solution/token_ring.go --total 6 --rounds 5
```
