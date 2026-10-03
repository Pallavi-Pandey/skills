# Lab 02: DOS vs NOS — Feel the Difference

> **Time:** 55 minutes | **Language:** Python | **Infrastructure:** Docker + Redis

## Objective

There are two classic ways an operating system can present a group of networked machines to a programmer:

- **Network Operating System (NOS)** — each machine keeps its own private resources (files, memory, etc.). If you want something that lives on another machine, you must **explicitly** ask for it — copy the file, mount a network drive, SSH in, whatever. You always know exactly *where* the thing you want lives.
- **Distributed Operating System (DOS)** — the whole cluster is made to *look and feel* like one single big machine. You just ask for a piece of data by name, and the system quietly figures out where it actually lives and hands it to you. This is called **location transparency**.

In this lab you'll build a tiny, working simulation of each style and feel the difference with your own hands, instead of just reading about it.

## Why This Matters for Security

Location transparency is convenient, but it also hides where your actual trust and network boundaries are. In NOS mode, every cross-machine request is an explicit, visible network call — an obvious place to add authentication, check permissions, or log access. In DOS mode, the system deliberately hides that a request just crossed the network at all, which is exactly what makes it easy to forget that a "local-looking" read or write might actually be exposed to network-level attacks (eavesdropping, spoofing, man-in-the-middle) that a truly local operation never would be. When you're auditing a real distributed system for security, one of the first questions to ask is: "which of these operations that *look* local are secretly going over a network?"

## How to Run This Lab (Quick Reference)

```bash
# 1. Start the 3 Python containers + Redis
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3 redis

# 2. Part 1 — NOS: file server on node1, clients request it explicitly by name
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode server
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt
docker exec -it ds-python-node3 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt

# 3. Part 2 — DOS: any node can write/read without naming a server
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action write --key greeting --value "Hello from node1"
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action read --key greeting
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action start-task --task-id job42 --progress 0
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action resume-task --task-id job42
docker exec -it ds-python-node3 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action list
```

## What You'll Do

1. **NOS Mode:** Build a file server + client where node2 and node3 must explicitly say "give me the file that's on node1" over a plain TCP connection.
2. **DOS Mode:** Build a shared-memory system (backed by Redis) where any node can read/write data without ever saying which node it's talking to — plus a "process migration" demo where a task started on one node is resumed on another.
3. Compare the two: lines of code needed, how much you had to know about the cluster's layout, and what breaks when a node dies.

---

## Concepts you need before you start

Read this whole section before opening any code. Every term used in `nos_simulation.py` and `dos_simulation.py` is explained here first.

### 1. NOS vs DOS, in plain terms

Imagine two different offices:

- **The NOS office:** every employee has their own personal filing cabinet, locked, in their own room. If you need a document that Priya has, you must physically walk to Priya's room and ask her for it by name. You always know exactly whose cabinet has what.
- **The DOS office:** there's one shared filing room in the middle of the building. Any employee can walk in, open any drawer, and get what they need — they never have to know or care which specific shelf a document happens to sit on. From the employee's point of view, it's all just "the filing room."

Neither office is "better" in every way — the NOS office is simple to reason about but requires everyone to remember who has what; the DOS office is convenient but relies on the shared filing room staying up and working correctly. That trade-off is exactly what this lab makes you feel.

### 2. What is a socket? (quick recap)

A **socket** is Python's way of saying "an open network connection I can send bytes into and read bytes out of." Think of it like a phone call:

- `socket.socket(...)` — pick up the phone.
- `.bind((host, port))` — claim "this is my phone number" so others can call you.
- `.listen()` — put the phone on "ready to receive calls."
- `.accept()` — answer an incoming call; this gives you a *new* socket representing that one call.
- `.connect((host, port))` — dial someone else's number (used by a client).
- `.send()` / `.sendall()` / `.recv()` — speak into the phone / listen to what's said. `recv(1024)` means "read up to 1024 bytes right now."
- `.close()` — hang up.

We use `socket.AF_INET` (a normal IPv4 address) and `socket.SOCK_STREAM` (TCP — bytes arrive in order, nothing goes missing silently). If any of this is brand new to you, see Lab 01's README, which walks through it in more depth — this lab assumes you can follow it at the level above.

### 3. Why does the file server need threads?

A server that can only talk to one client at a time would make node3 wait until node2's request is completely finished before it could even connect. A **thread** is a lightweight "worker" that runs inside the same program and can handle one client's conversation while the main program goes right back to `accept()`-ing new connections. That's why the server's TODO asks you to spawn a new thread per accepted connection, the same pattern as Lab 01:

```python
t = threading.Thread(target=self.handle_client, args=(conn, addr))
t.daemon = True
t.start()
```

### 4. What is Redis, and why are we using it here?

**Redis** is a separate program (already running for you as the `ds-redis` container) that stores key-value pairs **in memory** (RAM, not disk) and lets any program on the network read/write them over a very simple protocol. Think of it as a shared whiteboard that every node can walk up to and read or write on.

We're using it to *simulate* "shared memory" — the thing a real Distributed OS provides transparently at the kernel level. Your Python code talks to Redis using the `redis` library:

- `redis.Redis(host="ds-redis", port=6379, decode_responses=True)` — connect to the whiteboard. `decode_responses=True` just means "give me back normal Python strings instead of raw bytes."
- `r.set(key, value)` — write a value under a name.
- `r.get(key)` — read the value back (returns `None` if the key doesn't exist).
- `r.keys("*")` — list every key currently stored (used by the already-working `list_all_keys()` helper, described below).

Nobody has to know or configure *which* container physically holds a given key — Redis handles that internally, and every node just talks to the same `ds-redis` address. That's the "transparency" this lab is trying to make concrete.

### 5. Why does the code use JSON (`json.dumps` / `json.loads`)?

Redis only stores plain strings — it has no idea what a Python dictionary is. But the "task state" you need to save (progress, which node started it, a list of numbers) is a whole structured object, not a single string. **JSON** is a simple text format for writing structured data (dictionaries, lists, numbers) as one string, so it can travel through anything that only understands text.

- `json.dumps(some_dict)` — turn a Python dictionary into a JSON string, ready to store in Redis.
- `json.loads(some_string)` — turn a JSON string back into a Python dictionary.

So the pattern for saving a task is: build a dictionary → `json.dumps` it → `r.set` the resulting string. Reading it back is the reverse: `r.get` → `json.loads` → you have your dictionary again.

### 6. How does one container find another by name (`node1`, `ds-redis`)?

All the containers for this course run on one Docker-created private network (`ds-network`, set up in `docker/network-setup.yml`). Docker gives every container on that network a DNS name equal to its `hostname` (`node1`, `node2`, `node3`) or `container_name` (`ds-redis`). So when code says `redis.Redis(host="ds-redis", ...)` or the client is told `--server node1`, it's not a real internet address — it's a name that only resolves *inside* this private Docker network, the same way you'd refer to a colleague's desk by name instead of by GPS coordinates.

### 7. What is an environment variable, and what does `os.environ.get("HOSTNAME")` do?

An **environment variable** is a small piece of text the operating system makes available to every program running on it — like a sticky note attached to the process. Docker automatically sets the `HOSTNAME` environment variable inside each container to that container's own hostname (`node1`, `node2`, or `node3`). So `os.environ.get("HOSTNAME", "unknown")` just means "ask the OS what machine I'm running on right now" (falling back to the string `"unknown"` if that variable somehow isn't set). This is how the code can print things like "written from node1" without you having to hardcode it.

### 8. What does `argparse` do?

`argparse` is Python's built-in tool for reading command-line flags like `--mode server` or `--action write --key greeting --value hello`. `parser.add_argument("--mode", choices=["server", "client"], required=True)` tells Python: "expect a `--mode` flag, only accept the value `server` or `client`, and refuse to run without it." After `args = parser.parse_args()`, you access the values as `args.mode`, `args.key`, etc. You don't need to modify any `argparse` code in this lab — just understand that it's *how* the `--server node1 --file test.txt` style flags in the commands below reach your Python code.

### 9. Two terms you'll be asked about directly: "location transparency" and "process migration"

- **Location transparency** means: you access a resource (a file, a value) *by name*, without needing to know or state which physical machine holds it. Part A (NOS) has none of this — you must pass `--server node1`. Part B (DOS) has it — nothing you type says which node's memory actually holds the value.
- **Process migration** means: a running computation's state is saved somewhere, and a *different* machine can pick it up and continue from where it left off, as if it had been running there all along. Part B simulates this: node1 "starts" a task and saves its progress to Redis; node2 "resumes" it by reading that saved state and continuing the computation — the task effectively moved machines.

---

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3 redis
```

This starts the 3 Python containers from Lab 01 plus a `redis` container (visible on the network as `ds-redis`) that all three can reach.

---

## Instructions

### Part 1: Network OS Simulation (25 min)

**Concept:** In a Network OS, each machine has its own resources, and sharing requires an explicit action (copy, mount, SSH, or — in our case — a direct request over a socket). Even though the lab's Docker setup happens to give all three containers access to the same underlying `/shared` volume for convenience, your code is **not allowed to just read the file directly** — the whole point of this part is to go through an explicit client/server request, exactly the way a real NOS forces you to.

Open `nos_simulation.py`. There are two classes to fill in:

1. **`NOSFileServer.handle_client`**: once the server has confirmed the requested file exists at `filepath`, read that file's contents (open it and `.read()` it) and send those contents back to the client over `conn` (encode the string to bytes first, e.g. with `.encode("utf-8")`, and use `sendall` so all the bytes are guaranteed to go out). If the file doesn't exist, the "not found" branch is already written for you.
2. **`NOSFileServer.start`**: this is the same server-startup pattern as Lab 01 — create a TCP socket, set `SO_REUSEADDR` (so restarting the server quickly doesn't fail with "address already in use"), `bind` to `(self.host, self.port)`, `listen`, then loop forever: `accept()` a connection and hand it off to `self.handle_client` on its own thread, so the server can keep accepting new clients while an earlier one is still being served.
3. **`NOSFileClient.get_file`**: create a TCP socket, `connect` to `(self.server_host, self.server_port)`, send the requested `filename` (encoded to bytes), then `recv` the server's response and print it. Notice that *you* (the caller) had to supply `self.server_host` — the client has no way to find the file without being told exactly which machine to ask.

**Test it:**

```bash
# Node 1: Start file server
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode server

# Node 2: Request a file
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt

# Node 3: Also request a file
docker exec -it ds-python-node3 python3 /app/labs/lab_02_dos_vs_nos/nos_simulation.py --mode client --server node1 --file test.txt
```

**Discussion points:**
- You had to type `--server node1` explicitly. That's NOS — no location transparency.
- If node1 dies, the file server is gone, and there is no automatic failover to another node.

### Part 2: Distributed OS Simulation (25 min)

**Concept:** In a Distributed OS, resources appear local even when they physically aren't — the system (here, Redis, standing in for the "kernel") provides transparency. You never tell your code which node's memory actually holds a value; you just read and write by key name.

Open `dos_simulation.py`. There are four functions with TODOs (a fifth, `list_all_keys`, is already fully implemented for you — see the note below):

1. **`write_shared_memory(key, value)`**: use `r.set(key, value)` to store the value in Redis, then print a message showing what was written and from which hostname (use `os.environ.get("HOSTNAME", "unknown")`, as explained above).
2. **`read_shared_memory(key)`**: use `r.get(key)` to fetch the value, then print it along with which node is doing the reading. Notice nothing in this function says which node *wrote* the value — that's the transparency this lab is demonstrating.
3. **`start_task(task_id, initial_progress)`**: the `task_state` dictionary is already built for you. Turn it into a JSON string with `json.dumps(...)` and store it in Redis under the key `f"task:{task_id}"`. Print a message saying the task started on this node with its current progress.
4. **`resume_task(task_id)`**: fetch the saved state from Redis with the same key pattern (`f"task:{task_id}"`), turn the JSON string back into a dictionary with `json.loads(...)`, and print which node originally started it plus its current progress (this is the "process migration" moment — you're picking up a task that began somewhere else). Then continue the computation by appending 5 more values to `task_state["data"]`, bump `task_state["progress"]` accordingly, and save the updated dictionary back to Redis (`json.dumps` it and `r.set` it under the same key) so the new progress is visible to everyone.

**Bonus tool (no TODO needed):** `list_all_keys()` is already working. Run it any time with `--action list` to see every key currently stored in Redis, from any node — a handy way to check your work without guessing.

**Test it:**

```bash
# Any node can write
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action write --key greeting --value "Hello from node1"

# Any OTHER node can read — instantly!
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action read --key greeting

# Process migration: start on node1, migrate to node2
docker exec -it ds-python-node1 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action start-task --task-id job42 --progress 0
docker exec -it ds-python-node2 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action resume-task --task-id job42

# Optional: peek at everything currently in shared memory, from any node
docker exec -it ds-python-node3 python3 /app/labs/lab_02_dos_vs_nos/dos_simulation.py --action list
```

**Discussion points:**
- You never specified which node has the data — that's **location transparency**.
- The task "migrated" — it started on node1 and continued on node2, picking up exactly where it left off.
- Redis is the hidden infrastructure making this work (like the kernel in a real DOS).

---

## Checkpoint Challenge

| Question | NOS | DOS |
|----------|-----|-----|
| How many lines of code did you need to write to share one piece of data? | ? | ? |
| Did you have to specify which node to read from? | Yes / No | Yes / No |
| What happens when the node holding the data dies? | ? | ? |
| Is there a single point of failure (one component whose crash breaks everything)? | ? | ? |

**Final discussion:** *Modern systems like Kubernetes borrow ideas from both NOS and DOS. Which features do you recognize from each?*
