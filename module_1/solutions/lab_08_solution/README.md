# Lab 08 Solution — Deadlock: Create, Detect, Resolve

Instructor-facing answer key for [`labs/lab_08_deadlocks/`](../../labs/lab_08_deadlocks/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the Java container
cd module_1/docker/
docker compose -f network-setup.yml up -d java-node1

# 2. Part 1 — create the deadlock
docker exec -it ds-java-node1 sh
cd /app/solutions/lab_08_solution/
javac DeadlockDemo.java && java DeadlockDemo

# 3. Part 2 — while it's hanging, in a SECOND terminal, detect it with jstack
docker exec -it ds-java-node1 jstack $(jps | grep DeadlockDemo | awk '{print $1}')

# 4. Part 3 — run the fixed version (back in the first terminal, Ctrl+C the hung one first)
javac DeadlockFixed.java && java DeadlockFixed
```
