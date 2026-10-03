# Lab 07: Distributed Mutual Exclusion — Token Ring

> **Time:** 15 minutes | **Language:** Go | **Infrastructure:** Docker

## Objective

Implement the **Token Ring** algorithm: a way for a group of independent processes (nodes) to take turns using a shared resource, one at a time, *without* any of them sharing memory or having a central boss to ask for permission. You'll fill in a few TODOs in `token_ring.go`, run the simulation, and watch the algorithm guarantee that no two nodes ever do the protected work at the same time.

## Why This Matters for Security

Distributed mutual exclusion isn't just an academic exercise — it's what protects things like "only one process may redeem this coupon code," "only one node may write to this shared record right now," or "only one service instance may hold this lease." When mutual exclusion breaks — say, the token gets lost or duplicated, which is exactly what Checkpoint Question 2 asks you to think about — the result is a **race condition**, and race conditions in security-critical code are a genuine, exploitable vulnerability class: a double-spend on a payment, two processes both believing they own the same lock, or a coupon getting redeemed twice because two requests slipped through "at the same time." Understanding exactly how and why an algorithm like Token Ring guarantees exclusivity is the same skill as understanding how an attacker might try to break that guarantee.

---

## How to Run This Lab (Quick Reference)

```bash
# 1. Start the Go container
cd docker/
docker compose -f network-setup.yml up -d go-node1

# 2. Run the simulation (all 4 nodes run inside this one command)
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --total 4

# Optional: change the ring size / how many critical-section rounds to run
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --total 6 --rounds 5
```

## Concepts you need before you start

Read this section fully before opening `token_ring.go`. Nothing here is solved for you — it's just the background you need to understand what the TODOs are asking.

### 1. What is "mutual exclusion", and why is it hard when there's no shared memory?

**Mutual exclusion** just means "only one at a time." If you've programmed before (even a little), you may have seen a `lock` or `mutex` variable used to protect a piece of code so that only one thread touches it at once — e.g. `lock.acquire()` ... `lock.release()`.

That trick works because all the threads live inside **one program, on one machine**, so they can all see and fight over the *same* lock variable sitting in shared memory.

In a **distributed system**, there is no shared memory. Node 0 and Node 2 might be on different machines (or, in this lab, different goroutines that only talk to each other by passing messages). Node 0 cannot "check a shared lock variable" because there isn't one it can see — Node 2 has its own separate memory. So distributed mutual exclusion has to be solved entirely through **message passing**: nodes send each other messages, and the *rules* for how those messages are sent and handled are what create the "only one at a time" guarantee. Token Ring is one such set of rules.

### 2. What is a "critical section"?

The **critical section** is the piece of work that must never be done by two nodes at the same time — for example, updating a shared counter, writing to a shared file, or (in real systems) something like "only one server may currently be the leader." In this lab, the critical section is simulated: a node just prints "entering," sleeps for a random amount of time (pretending to do important work), then prints "leaving." The whole point of the lab is to prove that no two nodes are ever inside that simulated critical section simultaneously.

### 3. The Token Ring algorithm

Imagine a group of people sitting in a circle, passing around a single **talking stick**. The rule is simple: **you may only speak while you are holding the stick.** When you're done talking (or if you have nothing to say), you pass the stick to the person on your right. Since there is only one stick, it is physically impossible for two people to be speaking "with the stick" at the same time.

Token Ring works exactly the same way, except the "stick" is a **token** (just a signal with no real content — think of it as an empty envelope being passed around), and the "circle" is a **ring topology**: each node has exactly one neighbor it receives the token from, and exactly one neighbor it sends the token to.

```
  Node 0 → Node 1 → Node 2 → Node 3
    ↑                                ↓
    ←─────────────────────────────────
```

The algorithm, from any one node's point of view, is:

1. Wait until you receive the token from your predecessor.
2. While you hold it, you are *allowed* to enter the critical section (you don't have to — maybe you don't need to right now).
3. If you enter the critical section, do your work, then leave it.
4. Pass the token to your successor, whether or not you used it.
5. Go back to step 1.

Because the token only ever exists in one place at a time, and only the current holder is allowed into the critical section, mutual exclusion is guaranteed **as long as there is exactly one token circulating and it is never lost or duplicated.** (We'll come back to what happens if it *is* lost — see the Checkpoint questions.)

### 4. Goroutines — Go's version of a lightweight thread

If you've never written Go before: a **goroutine** is Go's answer to a thread (similar to the Python `threading.Thread` idea, if you've seen that) — a separate unit of execution that runs concurrently with the rest of your program. You start one by writing `go someFunction(...)` instead of just `someFunction(...)`. The `go` keyword says "start running this in the background and don't wait for it to finish before moving to the next line." Goroutines are much cheaper than OS threads, so Go programs routinely start thousands of them. In this lab, **each node in the ring is one goroutine.**

### 5. Channels — how goroutines talk to each other

A **channel** is a typed pipe that one goroutine can send values into and another can receive values out of. Declared as `chan bool` (a channel that carries `true`/`false` values), you use it with two operators:

- `ch <- true` — **send** the value `true` into the channel. In this lab we never care about the actual `true`/`false` value; sending *anything* on the channel just means "here is the token."
- `token := <-ch` — **receive** a value from the channel. This line **blocks** — meaning the goroutine pauses right there and does nothing else — until some other goroutine sends something on that channel. This blocking behavior is exactly what makes "wait until you receive the token" work: a node simply cannot proceed past this line until its predecessor passes it the token.

The starter code creates its channels as **buffered with capacity 1** (`make(chan bool, 1)`), which just means a send can complete even if no one is receiving *yet* — the value sits in the channel until someone reads it. You don't need to change this; it's already set up for you.

### 6. How the ring is simulated with channels

This lab runs entirely inside **one Go program** (unlike some other labs, there's no real networking here — no sockets, no separate node processes). The "ring" is built purely out of channels:

- There are `N` channels, one per node.
- Node `i` **receives** the token on channel `i` (its own channel).
- Node `i` **sends** the token on channel `(i+1) % N` — i.e., the *next* node's channel, wrapping back around to node `0` after the last node.

That `% N` (remainder after dividing by the total number of nodes) is exactly what turns a simple numbered list of nodes into a *circle*: node `N-1`'s "next" node is node `0`, closing the loop. This wiring is already done for you in `main()` — you don't need to touch it, but you should understand it, since it's the reason the token keeps circulating forever instead of falling off the end.

### 7. A few other Go building blocks you'll see in the file

- **`sync.WaitGroup`** — a counter that lets the main program wait for a group of goroutines to all finish (`wg.Add(1)` before starting one, `wg.Done()` when it finishes, `wg.Wait()` blocks until the count reaches zero). Already wired up for you.
- **`sync.Mutex`** — a plain old lock, used here *not* for the ring's mutual exclusion (that's what the token does) but just to safely let multiple goroutines append to the same `csLog` slice for printing a summary at the end. Already wired up for you.
- **`rand.Float64() < 0.6`** — generates a random decimal between 0 and 1, so this expression is true about 60% of the time. It's used to simulate "sometimes this node needs the critical section, sometimes it doesn't" — real nodes don't need a shared resource on every single turn.
- **`flag.Int("total", 4, ...)`** — Go's way of reading command-line flags, e.g. `--total 4`. You'll use these flags when running the program below.

---

## What You'll Do

Run a simulated ring of nodes (all inside one Go program, communicating only through channels), inject a single token at Node 0, and watch it circulate — with each node randomly deciding whether it needs the critical section on its turn. You'll confirm from the printed log that entries into the critical section never overlap, then think about what would break the guarantee.

## Instructions

Open `token_ring.go`. Skim the whole file first:

- The `Node` struct holds each node's state: its `ID`, whether it currently `HasToken`, whether it `WantCS` (wants the critical section) or `InCS` (is in the critical section), and its two channels, `NextChan` (to send the token onward) and `PrevChan` (to receive the token).
- `CriticalSection(...)` is already fully written for you — it prints an "ENTERING" message, sleeps for a random duration to simulate work, records the event, then prints "LEAVING." You don't need to change it, but read it so you know what to call.
- `main()` is already fully written for you — it creates the channels, wires them into a ring (as described in Concept 6 above), starts one goroutine per node, injects the token at Node 0, waits for everyone to finish, then prints the summary log.
- `Run(...)` is the node's main loop, and this is where **all the TODOs live.**

Fill in the TODOs inside `Run`, following the algorithm from Concept 3:

1. **Receive the token.** Use a blocking channel receive on `n.PrevChan` to wait for the token to arrive from your predecessor.
2. **Acknowledge it.** Print a message so you can see in the output when each node gets the token (this is just for visibility — it doesn't affect correctness).
3. **Decide whether you want the critical section.** Use the random-chance approach from Concept 7 (`rand.Float64() < 0.6`) to set `n.WantCS`.
4. **Act on that decision:**
   - If `n.WantCS` is true: call `n.CriticalSection(csLog, mu)` (the method already written for you), and increment the local round counter (`csCount`) so the loop knows to eventually stop.
   - If not: just print that you're passing without using it.
5. **Pass the token onward.** Send on `n.NextChan` so the next node in the ring can proceed — do this regardless of whether you used the critical section or not (this is essential: if you only pass the token when you used it, a node that doesn't want the critical section would freeze the whole ring).
6. Once your TODOs are in place, delete the placeholder `break` statement at the bottom of the loop — it's only there so the unfinished starter code compiles and exits immediately instead of hanging forever.

**Run it:**

```bash
# Start the Go container (once)
cd docker/
docker compose -f network-setup.yml up -d go-node1

# Run the simulation — everything (all 4 nodes) runs inside this one command,
# since the whole ring lives in a single Go program
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --total 4

# Optional flags: change the ring size or how many times each node must
# enter the critical section before the program ends
docker exec -it ds-go-node1 go run /app/labs/lab_07_mutual_exclusion/token_ring.go --total 6 --rounds 5
```

Watch the console output: you should see the token being received, sometimes used (ENTER/LEAVE pairs), sometimes passed straight through, circulating node by node. At the end, check the "Critical Section Log" summary.

## Checkpoint Questions

1. Looking at the interleaved `[LOCK]`/`[UNLOCK]` output, does any node ever enter the critical section while another node is still inside it? Why is that impossible *by construction* in this algorithm (think about how many tokens exist)?
2. Suppose the token holder crashes (or, in this simulation, a node's goroutine never sends on `NextChan`). What happens to the rest of the ring? (This is the classic **token loss problem** — think about what a blocking channel receive does when nothing is ever sent.)
3. How would you detect that the token has been lost, and regenerate a new one, in a real distributed deployment where nodes are on separate machines rather than goroutines in one program?
