# Lab 06 Solution — Goroutines & Worker Pool

Instructor-facing answer key for [`labs/lab_06_processes_threads/`](../../labs/lab_06_processes_threads/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the Go container
cd module_1/docker/
docker compose -f network-setup.yml up -d go-node1

# 2. Part 1 — sequential vs concurrent URL fetcher
docker exec -it ds-go-node1 sh
cd /app/solutions/lab_06_solution/
go run url_fetcher.go

# 3. Part 2 — worker pool (try different --workers values against the same --jobs)
go run worker_pool.go --workers 5 --jobs 20
```
