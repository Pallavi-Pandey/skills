# Lab 01: Centralized vs Distributed — See the Difference

> **Time:** 40 minutes | **Language:** Python | **Infrastructure:** Docker

## Objective

Build a simple key-value store (think of it as a tiny, in-memory database that only supports "save this value under this name" and "give me back the value saved under this name") in two versions:

- **Centralized** — everything lives on ONE machine.
- **Distributed** — the data is spread across THREE machines.

Then you'll benchmark both, kill a machine in each, and see with your own eyes why distributed systems exist.

## Why This Matters for Security

A centralized system is a single point of failure — and a single *target*. If an attacker can knock out or overload the one machine holding all the data (a denial-of-service, or DoS, attack), the entire service goes down at once. That's exactly what you'll see in Part 3's chaos test: kill the one centralized server and 100% of the data becomes unreachable. Spreading data across multiple nodes — the same idea behind Content Delivery Networks and DNS root servers — is a core defense against DoS: an attacker now has to take down *several* independent targets, not one, to cause total outage. This tradeoff between "one thing to defend" and "many things to defend, but no single point of failure" comes up constantly when designing secure, resilient infrastructure.

---

## Concepts you need before you start

You don't need to be a Python expert for this lab — you mainly need to understand five ideas. Read this section fully before opening any code.

### 1. What is a "socket"?

A **socket** is just Python's way of saying "an open connection over the network, that I can send bytes into and read bytes out of." Think of it like a phone call:

- `socket.socket(...)` — pick up the phone (create the connection object, not yet connected to anyone).
- `.bind((host, port))` — tell the phone company "this is MY number" (claim an address so others can call you).
- `.listen()` — put the phone on "ready to receive calls."
- `.accept()` — actually answer an incoming call. This gives you a *new* socket object representing that one call.
- `.connect((host, port))` — dial someone else's number (used by a client, not a server).
- `.send()` / `.recv()` — speak into the phone / listen to what's said.
- `.close()` — hang up.

In this lab we use `socket.AF_INET` (meaning "use a normal IPv4 address like `127.0.0.1`") and `socket.SOCK_STREAM` (meaning "use TCP" — a connection that guarantees your bytes arrive in order, unlike UDP).

### 2. Why `SO_REUSEADDR`?

When a server shuts down, the operating system holds onto its port for a short while "just in case." Without `setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)`, restarting your server quickly would fail with "Address already in use." This one line just tells the OS "let me reuse it immediately."

### 3. Why threads?

A server that only ever talks to **one** client at a time is useless — real servers handle many clients simultaneously. A **thread** is a separate, lightweight "worker" running inside the same program that can do its own thing (like handling one client's conversation) while the main program keeps accepting new connections. That's why you'll see:

```python
t = threading.Thread(target=self.handle_client, args=(conn, addr))
t.daemon = True
t.start()
```

This says: "run `handle_client` in the background, for this specific `conn` (the connection to one client), and keep going." Without this, the server would freeze on the first client and never accept a second one.

### 4. What does "hash partitioning" mean, and why do we need it?

In the distributed version, we have 3 nodes but only want each node to store **some** of the keys — not all of them (otherwise we haven't actually distributed anything). To decide *which* node owns a given key, we turn the key into a number using a **hash function** (`hashlib.md5` — a function that turns any text into a fixed-size, unpredictable-looking number), then use the remainder after dividing by 3 (`% 3`) to pick a node: 0, 1, or 2.

```
hash("username123") = 987654321...   (some huge number)
987654321 % 3 = 0                     → this key belongs to node 0
```

Every node runs the *exact same* hash formula, so they all agree on who owns what — with no need to ask each other "hey, who has this key?"

### 5. What is "forwarding"?

If a client connects to node 1 but asks for a key that node 0 actually owns, node 1 doesn't just fail — it acts like a receptionist: it opens its **own** connection to node 0, asks node 0 for the answer, and relays that answer back to the original client. This is what `forward_to_node` does.

---

## What You'll Do

1. Run a centralized KV store → benchmark it → kill it → **everything dies**.
2. Run a 3-node distributed KV store → benchmark it → kill one node → **it survives (partially)**.
3. Compare throughput, latency, and fault tolerance between the two.

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3
```

This starts 3 empty Linux containers named `python-node1`, `python-node2`, `python-node3` that can all talk to each other over a private Docker network — think of them as 3 separate computers on the same office network.

---

## Instructions

### Part 1: Centralized KV Store (15 min)

Open `centralized_kv.py`. You'll see a class `CentralizedKVStore` with a Python dictionary `self.store = {}` as its "database." A dictionary is just a lookup table: `self.store["name"] = "pallavi"` saves a value, `self.store["name"]` reads it back, and `"name" in self.store` checks if the key exists.

Fill in the 3 TODOs:

1. **In `process_command`**: for `SET key value`, save `parts[2]` into `self.store` under the key `parts[1]`, and return the string `"OK\n"`. For `GET key`, look up `parts[1]` in `self.store` — if it's there, return `value + "\n"`; if not, return `"NOT_FOUND\n"`.
   *(The trailing `\n` matters — the client reads until a newline, so forgetting it will make the client hang waiting for more data.)*
2. **In `start`**: create the socket, set `SO_REUSEADDR`, `bind`, `listen`, then loop forever calling `accept()` and spawning a thread per client — using the concepts explained above.

**Test it:**
```bash
# Terminal 1 (inside python-node1) — starts the server
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/centralized_kv.py

# Terminal 2 — runs the benchmark against it
docker exec -it ds-python-node2 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --host node1 --port 5000
```

### Part 2: Distributed KV Store (20 min)

Open `distributed_kv.py`. Same idea as Part 1, but now `self.store` only holds a *slice* of the data, and `CLUSTER_NODES` at the top tells every node the address of every other node.

Fill in the TODOs:

1. **`get_owning_node`**: hash the key with `hashlib.md5(key.encode()).hexdigest()`, convert that hex string to an integer with `int(hex_hash, 16)`, then `% self.num_nodes` to get the owning node's ID (0, 1, or 2).
2. **`forward_to_node`**: open a *new* socket, connect to the given node's `(host, port)`, send the command (encoded, with a trailing `\n`), read the response, close the socket, and return the response.
3. **In `process_command`**: if `self.get_owning_node(key) == self.node_id`, handle it locally (same SET/GET logic as Part 1, but say which node stored it). Otherwise, call `forward_to_node` and return what it gives you.

**Test it:**
```bash
# Start all 3 nodes (each in its own terminal/container)
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 0 --port 5000
docker exec -it ds-python-node2 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 1 --port 5000
docker exec -it ds-python-node3 python3 /app/labs/lab_01_what_is_distributed/distributed_kv.py --node-id 2 --port 5000

# Benchmark — this connects to all 3 nodes in round-robin
docker exec -it ds-python-node1 python3 /app/labs/lab_01_what_is_distributed/benchmark.py --distributed --nodes node1:5000,node2:5000,node3:5000
```

### Part 3: Chaos Test (5 min)

"Chaos testing" simply means: deliberately break something on purpose, to see how the system reacts.

```bash
# Kill node 2 (simulates a server crashing)
docker stop ds-python-node2

# Try to GET a key that was on node 2
# → Error! That partition of data is gone with the node.

# Try to GET a key on node 1
# → Still works! One node's failure didn't bring down the whole system.
```

Compare this to Part 1: killing the *single* centralized server made 100% of your data unreachable. Killing *one out of three* distributed nodes only made ~33% of your data unreachable. That gap is the entire point of this lab.

## Checkpoint Questions

1. Which mode had higher throughput for writes, and why do you think that is?
2. What happened when you killed a node in each mode — was the failure "all or nothing," or partial?
3. How would you make the distributed version survive a node failure entirely, so that even keys owned by the dead node stay available? *(Hint: what if more than one node kept a copy of each key? Look up the word "replication.")*
