# Lab 06: Processes, Threads & Go Concurrency

> **Time:** 35 minutes | **Language:** Go

## Objective
Experience Go's concurrency model: goroutines (lightweight threads), channels (communication), and worker pools.

## Part 1: Sequential vs Concurrent URL Fetcher (15 min)

Open `url_fetcher.go` — fill in the TODOs:

1. Fetch 20 URLs sequentially → measure time
2. Fetch 20 URLs concurrently with goroutines → measure time
3. See the 10-50x speedup!

```bash
docker exec -it ds-go-node1 sh
cd /app/labs/lab_06_processes_threads/
go run url_fetcher.go
```

## Part 2: Worker Pool Pattern (20 min)

Open `worker_pool.go` — fill in the TODOs:

1. Create a channel of jobs
2. Spawn N worker goroutines that read from the jobs channel
3. Collect results in a results channel
4. Fan-out/Fan-in pattern

```bash
go run worker_pool.go --workers 5 --jobs 20
```

## Checkpoint
- How many goroutines can you spawn before performance degrades?
- What happens if a goroutine panics? Does it kill other goroutines?
- Compare: `go func()` vs `new Thread()` in Java — which is cheaper?
