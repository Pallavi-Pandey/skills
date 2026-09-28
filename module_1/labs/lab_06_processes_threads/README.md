# Lab 06: Processes, Threads & Go Concurrency

> **Time:** 35 minutes | **Language:** Go | **Infrastructure:** Docker

## Objective

Experience Go's concurrency model firsthand by building:

- **A URL fetcher** — fetch 20 web pages one at a time, then fetch all 20 "at once," and watch the dramatic speedup.
- **A worker pool** — a fixed team of background workers that pull jobs from a shared queue, instead of spawning one task per job with no limit.

Both labs use **goroutines**, Go's built-in tool for running things concurrently. If you've used Python's `threading` module, some of this will feel familiar — but Go's version is cheaper, more common in everyday Go code, and comes with its own vocabulary. If you haven't used threads in Python either, that's fine too — everything is explained from scratch below.

## Why This Matters for Security

Part 1's naive "spawn a goroutine per URL, no limit" approach is more than just a performance lesson — unbounded concurrency is a real denial-of-service vector. If a server spawns one goroutine (or thread, or process) per incoming request with no cap, an attacker can send a flood of requests and exhaust the server's memory or CPU long before any "real" logic runs — this is the mechanism behind many resource-exhaustion DoS attacks. Part 2's worker pool is literally the defensive pattern against this: by fixing the number of workers up front, the system puts a hard ceiling on how much concurrent work an attacker (or just a burst of legitimate traffic) can force it to do at once. Rate limiting and connection pooling in real production systems are direct descendants of this same idea.

---

## Concepts you need before you start

Read this section fully before opening `url_fetcher.go` or `worker_pool.go`. It explains every Go-specific idea the two files rely on.

### 0. The absolute minimum Go syntax you need to recognize

You don't need to "know Go" to do this lab, but you do need to recognize these landmarks when you see them in the code, so they don't distract you from the actual concurrency concepts:

- `package main` — every runnable Go program starts with this line. It just says "this file is a program, not a library."
- `import (...)` — like Python's `import`, but Go groups all imports into one block at the top.
- `func fetchURL(url string) (int, error) { ... }` — this is how you define a function. `func` is the keyword (like Python's `def`). `(url string)` means "one parameter named `url`, of type `string`" — Go always writes the type *after* the name. `(int, error)` means this function returns **two** values: an `int` and an `error`.
- **Multiple return values + error handling** — this is a huge Go idiom you'll see constantly:
  ```go
  size, err := fetchURL(url)
  if err != nil {
      // something went wrong, "err" describes it
  }
  ```
  Go doesn't have exceptions for normal error handling. Instead, functions that can fail return an extra `error` value as their *last* return value. `nil` is Go's version of Python's `None` — "no error occurred" is represented as `err == nil`. You'll see this `if err != nil` check after almost every operation that can fail (opening a network connection, reading a file, etc.). It's repetitive on purpose — Go wants errors to be impossible to silently ignore.
- `:=` — the "short variable declaration" operator. `size, err := fetchURL(url)` both creates the variables `size` and `err` *and* assigns them in one step, with Go figuring out their types automatically. Roughly equivalent to just writing `size, err = fetchURL(url)` in Python, except Python doesn't need to declare variables at all.
- `struct` — Go's version of a plain data class. For example:
  ```go
  type Job struct {
      ID       int
      Duration time.Duration
  }
  ```
  This defines a `Job` "type" that bundles an `ID` and a `Duration` together, similar to a Python class whose `__init__` just sets a couple of fields, or a `dataclass`. You create one with `Job{ID: 7, Duration: d}`.
- `defer` — schedules a line of code to run right before the current function returns, no matter how it returns. `defer resp.Body.Close()` means "close this response body when `fetchURL` is done, whatever happens." It's used because it keeps the "cleanup" line right next to the "setup" line, instead of you having to remember to add it before every possible `return`.

None of this needs to be memorized — just recognize it so the concurrency logic (the actual point of this lab) doesn't get lost in unfamiliar punctuation.

### 1. What is a goroutine?

A **goroutine** is Go's version of "run this function in the background, concurrently with everything else." You start one by putting the keyword `go` in front of a function call:

```go
go fetchURL(url)
```

This line means "start running `fetchURL(url)`, but don't wait for it to finish — immediately continue to the next line." The function now runs concurrently with the rest of your program.

**How is this different from a Python thread?** Conceptually they solve the same problem — "do several things at once without writing separate programs" — but goroutines are dramatically cheaper:

- A Python `threading.Thread` (and an OS-level thread in general) typically reserves around **1 MB** of memory just for its stack, and creating one involves the operating system.
- A goroutine starts with a stack of only around **2 KB**, managed entirely by the Go runtime (not the OS), and grows automatically if needed. This means a Go program can comfortably run **thousands or even millions** of goroutines, where a program would struggle to create even a few thousand OS threads.
- Go's runtime automatically spreads many goroutines across a small number of real OS threads for you. You never manage that mapping yourself — you just write `go someFunc()` and let Go handle the scheduling.

This is why `url_fetcher.go` can fire off a goroutine per URL without a second thought — in Go, that's normal, not wasteful.

### 2. Why can't goroutines just share a variable?

If two goroutines both read and write the same variable at the same time with no coordination, you get a **race condition** — the final result depends on unpredictable timing, and can be wrong in a different way each run. This is true in Python too (it's why `threading.Lock` exists), but Go pushes you toward a different default solution: **don't share memory to communicate — communicate to share memory.** In practice, that means passing values through a **channel** instead of writing directly into a shared variable from multiple goroutines.

### 3. What is a channel?

A **channel** is a typed pipe that goroutines use to send values to each other safely. Think of it like a conveyor belt between two workers: one goroutine puts a value on one end (`results <- value`), another goroutine takes it off the other end (`job := <-jobs`), and Go guarantees this handoff can never corrupt data or happen "half-way," even if many goroutines are pushing and pulling at once.

You create one with `make`:

```go
jobs := make(chan Job, 10)
```

This makes a channel that carries values of type `Job`, with room to hold up to 10 values before a sender has to wait (this is called a **buffered** channel — the `10` is the buffer size). If the buffer fills up, `jobs <- someJob` will pause ("block") until a worker takes something off the other end. This blocking behavior is exactly what lets a channel replace a lock: it naturally paces producers and consumers against each other.

You'll also see channel types written as function parameters, like `jobs <-chan Job` and `results chan<- Result`. The arrow just says which direction that function is allowed to use the channel:

- `<-chan Job` — "a channel I can only **receive** `Job` values from" (read-only, from this function's point of view).
- `chan<- Result` — "a channel I can only **send** `Result` values into" (write-only).

This is Go's way of documenting intent: a `worker` function that takes `jobs <-chan Job, results chan<- Result` is telling you, just from its signature, "I consume jobs and I produce results — I will never accidentally push something back onto `jobs`."

Closing a channel (`close(jobs)`) means "no more values will ever be sent on this channel." A goroutine doing `for job := range jobs` will keep receiving jobs as they arrive and automatically stop looping once the channel is closed **and** drained — this is how workers know when to shut down.

### 4. What is a WaitGroup, and why do you need to "wait"?

Here's the problem: if your `main` function launches five goroutines and then immediately reaches the end of the program, Go doesn't automatically pause to let those goroutines finish — the whole program just exits, goroutines and all, mid-flight. Unlike Python's main thread, which by default waits for non-daemon threads, Go's `main` function has to be told explicitly to wait.

A `sync.WaitGroup` is a simple counter built for exactly this:

- `wg.Add(1)` — "one more goroutine is about to start; increment the counter."
- `wg.Done()` — "this goroutine is finished; decrement the counter." (Usually called via `defer wg.Done()` right at the top of the goroutine, so it's guaranteed to run even if the function returns early.)
- `wg.Wait()` — "block here until the counter reaches zero." This is what `main` (or whichever function launched the goroutines) calls once it's launched everything, so it doesn't move on — or exit — before the work is actually done.

Without a `WaitGroup` (or a channel used the same way), you'd have no reliable way to know "have all my background fetches actually completed yet?"

### 5. What is a worker pool, and why not just spawn a goroutine per job?

In Part 1, spawning one goroutine per URL is fine for 20 URLs. But imagine 200,000 jobs, or jobs that each open a network connection or hit a rate-limited API — spawning 200,000 goroutines all at once could exhaust memory, overwhelm a downstream server, or hit connection limits, even though each individual goroutine is cheap.

The **worker pool pattern** fixes this by capping concurrency at a known number, `N`:

1. Start exactly `N` worker goroutines up front (not one per job).
2. Put all the jobs onto a shared `jobs` channel.
3. Each worker loops (`for job := range jobs`), pulling one job at a time, processing it, and going back for the next one — so at most `N` jobs are ever in flight simultaneously.
4. Each worker sends its finished `Result` onto a shared `results` channel.

This is often called the **fan-out / fan-in** pattern: work "fans out" from one channel to `N` workers, and results "fan in" from those `N` workers back into one channel. It gives you the speed of concurrency while keeping a predictable, controllable ceiling on how much work happens at once — which is exactly the kind of tradeoff real distributed systems have to make (you'll see this same "bounded concurrency" idea again later in the course).

---

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d go-node1
```

This starts a Linux container named `go-node1` (visible as `ds-go-node1`) with the Go toolchain installed and this repo mounted at `/app`.

---

## Instructions

### Part 1: Sequential vs Concurrent URL Fetcher (15 min)

Open `url_fetcher.go`. `fetchSequential` is already complete — read it first, since `fetchConcurrent` needs to produce the same observable behavior (fetch every URL, print each result), just concurrently instead of one-by-one.

Your job is to fill in `fetchConcurrent` using the concepts above:

1. Create a `sync.WaitGroup`.
2. For each URL, before launching its goroutine, tell the WaitGroup "one more is starting" — then launch a goroutine (using `go`) that fetches that URL and prints the result, making sure it tells the WaitGroup "I'm done" when it finishes (even if it errors out — that's exactly the situation `defer` is built for).
3. **Watch out for a classic Go trap:** the loop variable `url` is reused on every iteration. If your goroutine closure reaches back and reads the *loop variable* directly instead of a value that was handed to it as its own argument, every goroutine can end up seeing the *same, final* URL by the time they actually run, instead of "their" URL. The fix is to pass the current value into the goroutine explicitly as a parameter, so each goroutine gets its own private copy. (The comment block already in the file shows the shape of this — study *why* it passes `u` as a parameter instead of capturing `url` directly.)
4. After the loop, make `main` (well, `fetchConcurrent`) actually wait for every fetch to finish before it measures the elapsed time and returns — otherwise you'd print a "finished in X seconds" time before the fetches have actually finished.

**Run it:**
```bash
docker exec -it ds-go-node1 sh
cd /app/labs/lab_06_processes_threads/
go run url_fetcher.go
```

You should see the concurrent version finish in roughly the time of the *single slowest* URL, instead of the *sum* of all 20 — because now they're all in flight together instead of queued up one after another.

### Part 2: Worker Pool Pattern (20 min)

Open `worker_pool.go`. This time, instead of "one goroutine per job" (Part 1's approach), you're building a fixed-size pool of workers that share a queue — the pattern explained in concept 5 above.

Fill in the TODOs:

1. **The `worker` function**: this is the function each of your `N` worker goroutines will run. It needs to keep pulling jobs from the `jobs` channel until that channel is closed and empty, and for each job: simulate doing the work (there's already a `time.Sleep` hint for this), build a `Result` struct recording which worker did it and how long it took, and send that `Result` onto the `results` channel. Also print a line so you can watch, in real time, which worker picked up which job — this is what will let you *see* the concurrency actually happening.
2. **In `main`**: create the two channels described in concept 3 — a `jobs` channel and a `results` channel, both buffered with enough capacity to hold all the jobs up front so that sending jobs doesn't block.
3. **Start the pool**: launch exactly `*numWorkers` goroutines running `worker`, *before* you start sending jobs — otherwise nothing is listening on the `jobs` channel yet.
4. **Feed the pool**: send `*numJobs` `Job` values onto the `jobs` channel, then `close(jobs)` once you're done — this is the signal each worker's `for job := range jobs` loop needs in order to eventually stop looping.
5. **Collect the results**: receive exactly `*numJobs` values off the `results` channel. (Notice you know in advance exactly how many results to expect — that's why a WaitGroup isn't strictly required here; the act of receiving `*numJobs` results *is* your synchronization point.)

**Run it:**
```bash
go run worker_pool.go --workers 5 --jobs 20
```

Try re-running with different `--workers` values (1, 5, 20) against the same `--jobs 20` and compare the total time — this is where you'll feel the effect of bounding concurrency instead of just maximizing it.

---

## Checkpoint Questions

1. How many goroutines can you spawn before performance starts to degrade? (Try cranking up the URL list or `--jobs`/`--workers` numbers and see where things stop improving — or start getting worse.)
2. What happens if a goroutine panics (Go's version of an unhandled exception)? Does it take down only itself, or the whole program, including other goroutines? Why might that matter when deciding how many goroutines to trust with unreliable work (like network calls)?
3. Compare `go someFunc()` in Go with `new Thread(...).start()` in Java (or `threading.Thread(...).start()` in Python) — which is cheaper to create, and why? Tie your answer back to the stack-size numbers in concept 1 above.
