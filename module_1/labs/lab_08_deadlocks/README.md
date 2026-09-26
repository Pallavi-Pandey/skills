# Lab 08: Deadlock — Create, Detect, Resolve

> **Time:** 15 minutes | **Language:** Java

## Objective
1. **Create** a deadlock on purpose (understand the conditions)
2. **Detect** it with `jstack` and a wait-for graph
3. **Resolve** it with lock ordering
4. **Prevent** it with `tryLock()` + timeout

## Four Conditions for Deadlock (ALL must be true)
1. **Mutual Exclusion** — only one thread holds a lock at a time
2. **Hold and Wait** — thread holds one lock while waiting for another
3. **No Preemption** — locks can't be forcibly taken away
4. **Circular Wait** — T1 waits for T2, T2 waits for T1

## Instructions

```bash
docker exec -it ds-java-node1 sh
cd /app/labs/lab_08_deadlocks/

# Step 1: Create a deadlock
javac DeadlockDemo.java && java DeadlockDemo

# Step 2: While it's stuck, detect it from another terminal
docker exec -it ds-java-node1 jstack $(jps | grep DeadlockDemo | awk '{print $1}')

# Step 3: Run the fixed version
javac DeadlockFixed.java && java DeadlockFixed
```

## Checkpoint
- Did the program hang? That's the deadlock!
- What did `jstack` show in the thread dump?
- Which of the 4 conditions did the fix break?
