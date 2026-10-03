# Lab 08: Deadlock — Create, Detect, Resolve

> **Time:** 15 minutes | **Language:** Java | **Infrastructure:** Docker

## Objective

1. **Create** a deadlock on purpose, so you understand exactly what has to go wrong for one to happen.
2. **Detect** it using `jstack` (a tool that prints what every thread in a running Java program is doing) and a **wait-for graph**.
3. **Resolve** it by changing the order in which locks are acquired.
4. **Prevent** it a second way, using `tryLock()` with a timeout instead of a blocking lock.

## Why This Matters for Security

A deadlock freezes a program without crashing it — which makes it a quiet, deniable way to cause a **denial-of-service**. If an attacker can control the order or timing in which a service acquires locks on shared resources (for example, by sending specially-crafted concurrent requests), and that service acquires multiple locks in an inconsistent order like `DeadlockDemo.java` does on purpose, the attacker may be able to force exactly the kind of deadlock you're about to create — permanently freezing that part of the service with no exception, no crash, and no obvious error in the logs. This is why the fix you'll implement (consistent lock ordering, or `tryLock()` with a timeout so a thread can back off instead of waiting forever) isn't just a performance best practice — it's a defense against an entire class of resource-exhaustion attacks on concurrent, security-critical code (authentication services, payment processing, anything using locks around shared state).

---

## How to Run This Lab (Quick Reference)

```bash
# 1. Start the Java container
cd docker/
docker compose -f network-setup.yml up -d java-node1

# 2. Part 1 — create the deadlock
docker exec -it ds-java-node1 sh
cd /app/labs/lab_08_deadlocks/
javac DeadlockDemo.java && java DeadlockDemo

# 3. Part 2 — while it's hanging, in a SECOND terminal, detect it with jstack
docker exec -it ds-java-node1 jstack $(jps | grep DeadlockDemo | awk '{print $1}')

# 4. Part 3 — run the fixed version (back in the first terminal, Ctrl+C the hung one first)
javac DeadlockFixed.java && java DeadlockFixed
```

## Concepts you need before you start

You've never written Java before, so this section starts from the absolute basics of what you'll see in the code, then builds up to what a deadlock actually is. Read it fully before opening `DeadlockDemo.java`.

### 1. The tiny bit of Java syntax you need to recognize

You don't need to *learn* Java for this lab, just be able to read it. Here's everything unfamiliar in these two files:

- **`public class DeadlockDemo { ... }`** — Java code must live inside a `class`. Think of a class here as just a named container/box for the program's code; you can treat `public class DeadlockDemo` as roughly "this file's program is called DeadlockDemo."
- **`public static void main(String[] args) { ... }`** — every runnable Java program needs exactly one `main` method. It's the equivalent of `if __name__ == "__main__":` in Python — this is where execution starts.
- **`new Thread(() -> { ... }, "Transfer-A-to-B")`** — this creates a **thread**: a separate worker that can run code at the same time as the rest of the program (same idea as Python's `threading.Thread`, if that's familiar — if not, think of it as spinning up a second worker who starts doing their own task while the main program keeps going). The `() -> { ... }` part is a **lambda** — an inline, unnamed block of code to run — and the string at the end is just a human-readable name for the thread (useful when you read thread dumps later). Nothing runs yet until you call `.start()` on it.
- **`.start()`** — actually launches the thread to run in the background.
- **`.join(5000)`** — makes the *current* thread (here, `main`) pause and wait up to 5000ms for that thread to finish. It's how the demo waits around to see if the two threads ever complete.

### 2. Locks and the `synchronized` keyword

Two threads running "at the same time" can both try to read and modify the same shared data (here, `accountA` and `accountB`) at the same instant, corrupting it. To prevent that, Java lets you wrap a block of code in `synchronized(someObject) { ... }`. This means: "only one thread at a time may be inside this block while holding `someObject`'s lock — every other thread that wants in has to wait its turn."

The object you synchronize on (here, `LOCK_A` and `LOCK_B` — plain, otherwise-meaningless `Object` instances created just to be locked on) is often called a **monitor**. Holding a lock is like holding a "talking stick": only whoever holds the stick may touch the shared data; everyone else waits for their turn.

This is *exactly* the kind of mechanism that makes deadlocks possible: if a thread is waiting to grab a lock that's held by someone else, it just... waits. Forever, if nothing ever tells the lock-holder to let go.

### 3. What is a deadlock? (plain-English analogy)

Picture two cars that meet nose-to-nose in a narrow alley — too narrow for either to pass. Each driver is waiting for the *other* one to reverse first, and neither will budge. Nobody is broken, nobody made an error in any single instant — but because each side is waiting on the other, both cars sit there forever.

A software deadlock is the same shape: Thread 1 is holding Lock A and waiting for Lock B. Thread 2 is holding Lock B and waiting for Lock A. Neither thread will ever release the lock it's holding until it gets the other one — which never happens. Both threads freeze permanently.

In this lab, that's modeled as two bank transfers happening at once:
- **Transfer 1** (A → B) locks `LOCK_A`, then tries to lock `LOCK_B`.
- **Transfer 2** (B → A) locks `LOCK_B`, then tries to lock `LOCK_A`.

If both threads grab their first lock before either reaches for its second one, each is now stuck waiting for a lock the other thread refuses to give up.

### 4. The Four Coffman Conditions

These are named after Edward G. Coffman Jr., who identified them as the four things that must **all** be true simultaneously for a deadlock to be possible. Break even one, and deadlock becomes impossible.

1. **Mutual Exclusion** — a resource (here, a lock) can only be held by one thread at a time. (`synchronized` guarantees this by design.)
2. **Hold and Wait** — a thread is allowed to hold one lock while it goes and waits for another one, instead of being forced to give up what it has first. (Transfer 1 holds `LOCK_A` while waiting on `LOCK_B` — that's hold-and-wait.)
3. **No Preemption** — nothing can forcibly take a lock away from the thread holding it. It has to release it voluntarily.
4. **Circular Wait** — there's a cycle of threads each waiting on the next: T1 waits for a lock T2 holds, and T2 waits for a lock T1 holds (with more threads, this can be a longer loop, e.g. T1→T2→T3→T1).

The two "fixes" you'll implement later each break one of these conditions on purpose — lock ordering removes circular wait, and `tryLock()` removes no-preemption (a thread can now voluntarily back off instead of waiting forever).

### 5. What is a "wait-for graph"?

A wait-for graph is a simple diagram (you can sketch it on paper) with an arrow from Thread X to Thread Y meaning "X is stuck waiting for a lock that Y currently holds." If you follow the arrows and ever loop back to where you started, that loop is a **cycle** — and a cycle in a wait-for graph is the formal definition of a deadlock. This lab's deadlock has the simplest possible cycle, of length two:

```
T1 (holds Lock A) → waits for Lock B → held by T2
T2 (holds Lock B) → waits for Lock A → held by T1
```

Follow the arrows: T1 → T2 → T1. That's the cycle — and it's exactly what the demo prints out once it detects it's stuck.

### 6. `jps` and `jstack` — looking inside a running Java program

- **`jps`** ("Java Process Status") lists the process IDs of all currently-running Java programs, along with their class names — it's how the command finds the numeric PID of your stuck `DeadlockDemo` program so it can point `jstack` at it.
- **`jstack <pid>`** dumps the current state of every thread inside that running Java process: what each thread is doing right now, and — crucially — which lock (if any) it's blocked waiting on, and who owns that lock. When two threads are deadlocked, `jstack` actually detects the cycle for you and prints a section literally titled "Found one Java-level deadlock," listing exactly which threads and locks are involved. This is the real-world, automated version of drawing the wait-for graph by hand.

### 7. `ReentrantLock` and `tryLock()` (used in the second fix)

`synchronized` is convenient but rigid: once a thread asks for the lock, it waits *indefinitely* — there's no way to say "try for a bit, then give up." Java's `java.util.concurrent.locks.ReentrantLock` class is a more flexible, explicit alternative to `synchronized`: you call `.lock()` to acquire it and `.unlock()` to release it yourself (usually in a `finally` block, so it's always released even if something goes wrong).

Its key extra feature is `tryLock(timeout, unit)`: instead of waiting forever, it waits **up to** the timeout and returns `true` if it got the lock or `false` if it gave up. That means a thread that can't get its second lock can voluntarily release the first one and retry later — breaking the "No Preemption" condition, since the thread is effectively giving up a lock it holds rather than blocking forever.

---

## What You'll Do

1. Fill in and run `DeadlockDemo.java` to produce a real deadlock between two threads.
2. While it's frozen, use `jstack` from a second terminal to see Java detect and report the deadlock itself.
3. Fill in and run `DeadlockFixed.java`, which fixes the same scenario two different ways.

## Instructions

### Part 1: Create a deadlock (`DeadlockDemo.java`)

Open `DeadlockDemo.java`. The two `Thread` objects (`transfer1` and `transfer2`) are already created for you, along with the shared `LOCK_A` / `LOCK_B` objects and the account balances — but the bodies of both threads are currently commented out as `TODO` blocks.

Your job: uncomment the `synchronized` blocks inside each thread's lambda.

- **`transfer1`** should lock `LOCK_A` first, sleep briefly (this just makes the race easy to hit reliably), then lock `LOCK_B` inside that, and finally move $100 from account A to account B.
- **`transfer2`** should lock `LOCK_B` first, sleep briefly, then lock `LOCK_A` inside that, and finally move $200 from account B to account A.

Notice the two threads reach for the locks in **opposite order** — that's the circular-wait condition from the concepts section, planted on purpose. Once both `TODO` blocks are uncommented exactly as written in the file, run it:

```bash
docker exec -it ds-java-node1 sh
cd /app/labs/lab_08_deadlocks/

# Step 1: Create a deadlock
javac DeadlockDemo.java && java DeadlockDemo
```

If the two threads each grab their first lock before either reaches for its second one, the program will hang and eventually print `[FATAL] DEADLOCK DETECTED!` along with the wait-for graph described above. (Since threading timing is involved, it's not 100% guaranteed on every run — the `Thread.sleep(100)` calls exist specifically to make it happen almost every time.)

### Part 2: Detect it with `jstack`

While `DeadlockDemo` is still hanging, open a **second terminal** and run:

```bash
docker exec -it ds-java-node1 jstack $(jps | grep DeadlockDemo | awk '{print $1}')
```

This finds the process ID of your stuck `DeadlockDemo` program (`jps | grep ... | awk ...`) and feeds it to `jstack`. Read the output: find the section describing the deadlock, and see which thread is waiting on which lock, and who owns it — this is Java confirming the exact same cycle you already reasoned about in Part 1.

### Part 3: Resolve it (`DeadlockFixed.java`)

Open `DeadlockFixed.java`. It contains **two separate fixes**, each in its own method, each with its own `TODO` blocks to uncomment.

1. **`fixedWithOrdering()`** — Strategy 1: consistent lock ordering. Both `t1` and `t2` should acquire `LOCK_A` **first**, then `LOCK_B`, regardless of which direction money is moving — even `t2`, which is transferring B→A, still locks A before B. Since neither thread can ever be holding B while waiting on A, the circular-wait condition is now structurally impossible.
2. **`fixedWithTryLock()`** — Strategy 2: `tryLock()` with a timeout. Both `t1` and `t2` should try to acquire their first `ReentrantLock` with a 1-second timeout, and — only if that succeeds — try to acquire the second one, also with a timeout. If either attempt fails, the thread should release anything it's holding and retry from the top, rather than block forever. (`t1` mirrors the commented-out logic already given for it; `t2` needs the same pattern in reverse order — locking B first, then A.)

Once both methods are filled in, run it:

```bash
# Step 3: Run the fixed version
javac DeadlockFixed.java && java DeadlockFixed
```

Both strategies should complete without hanging, and the program will print which of the four Coffman conditions each strategy breaks.

## Checkpoint Questions

1. When you ran `DeadlockDemo`, did the program hang instead of finishing? That hang **is** the deadlock — explain in your own words why it happened, using the lock-order argument from Part 1.
2. What did the `jstack` thread dump show — which thread was waiting on which lock, and did it match the wait-for graph `DeadlockDemo` printed itself?
3. Look at both fixes in `DeadlockFixed.java`. Which of the four Coffman conditions does each one break, and why does breaking that one condition alone make deadlock impossible?
