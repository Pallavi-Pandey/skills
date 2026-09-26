# Lab 04: Multi-Client Chat Server — Many Clients, One Server

> **Time:** 55 minutes | **Language:** Python | **Infrastructure:** Docker
> If you've done Lab 01, sections 2, 3, and 7 below will feel familiar — skim them.

## Objective

Build a real TCP chat server: many people connect to it at once, and a message typed by any one of them is instantly delivered ("broadcast") to everyone else who's connected — a bare-bones version of a group chat app, with no history and no images, just live text. This lab is your hands-on introduction to the **client-server model**, which is the foundation almost every distributed system in this course builds on.

## What You Build

A chat server that:
- Accepts multiple simultaneous TCP clients (not just one at a time)
- Broadcasts a message from one client to ALL the others
- Handles a client disconnecting (even abruptly, like its container being killed) without crashing
- Runs across separate Docker containers, so the server and each client are genuinely on different "machines"

---

## Concepts you need before you start

Read this whole section before opening any code. Every term used later in the instructions is explained here first.

### 1. What is the "client-server model"?

Formally: a **server** is a program that (a) sits at a known, fixed address, and (b) passively waits for others to contact it. A **client** is a program that knows the server's address and actively initiates contact. The server usually talks to *many* clients; a client usually only talks to one (or a few) servers.

In this lab: `chat_server.py` is the server — one copy of it runs and waits. `chat_client.py` is the client — every person in the chat runs their *own* copy of it, and each copy connects out to the one server.

### 2. Sockets and TCP — the short version

A **socket** is Python's handle for "an open connection over the network that I can send bytes into and read bytes out of." Picture a phone call:

- `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` — pick up the phone. (`AF_INET` = "use a normal IPv4 address like `127.0.0.1` or a hostname"; `SOCK_STREAM` = "use TCP," a connection that guarantees bytes arrive in order and none go missing — unlike UDP.)
- `.bind((host, port))` — claim a phone number as your own (server only).
- `.listen()` — put the phone on "ready to receive calls" (server only).
- `.accept()` — answer an incoming call; this returns a **new** socket object representing that one specific call, separate from the "listening" socket.
- `.connect((host, port))` — dial someone else's number (client only).
- `.send()` / `.sendall()` / `.recv()` — speak into the phone / listen to what's said.
- `.close()` — hang up.

### 3. Bytes vs. text: why you'll see `.encode()` and `.decode()`

Sockets only understand raw **bytes**, not Python strings. So before you can `.send()` a string, you must turn it into bytes with `.encode("utf-8")`. When you `.recv()`, you get bytes back, so you turn them into a readable string with `.decode("utf-8")`. Think of it as translating your message into "network language" on the way out, and back into "human language" on the way in.

### 4. Blocking calls — why a naive server gets stuck

Several socket operations **block**, meaning: the program stops and waits right there on that line until something happens. `accept()` blocks until someone tries to connect. `recv()` blocks until data arrives (or the other side disconnects). `input()` (reading keyboard input) also blocks until the user presses Enter.

This matters a lot here: if a server's main loop is stuck inside `recv()` waiting for *this* client to type something, it cannot simultaneously be sitting in `accept()` waiting for a *new* client to connect. A server with only one thread of execution can only be blocked on one thing at a time — so a second person trying to join gets left hanging while the server is busy with the first person. That's the "single-threaded version blocks on one client" problem this lab has you observe and then fix.

### 5. Threads: doing more than one blocking thing at once

A **thread** is a separate, lightweight "worker" running inside the same program, able to do its own thing while the rest of the program keeps going. This is exactly the fix for the blocking problem above:

- **On the server**: spawn one new thread per connected client to run that client's `recv()` loop, while the *main* thread stays free to keep calling `accept()` for new clients.
- **On the client**: you need to simultaneously (a) wait for the user to type something (`input()`, blocking) and (b) wait for new messages arriving from the server (`recv()`, blocking). One thread can't block on two things at once, so the client runs `receive_messages()` in a background thread while the main thread handles typing.

The general pattern for starting one looks like this (you'll adapt it to the specific function and arguments your code needs):

```python
t = threading.Thread(target=some_function, args=(some_arg,))
t.daemon = True
t.start()
```

### 6. Daemon threads

Setting `t.daemon = True` tells Python "don't let this thread keep the program alive by itself." A normal (non-daemon) thread will keep your program running even after everything else has finished, until that thread finishes too. A **daemon** thread is killed automatically the instant the main thread exits — useful here because background threads (a client's message-receiver, a server's per-client handler) should never be the reason your program refuses to quit.

### 7. Why `SO_REUSEADDR`?

When a server shuts down, the OS holds its port reserved for a short while "just in case." Without `setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)` before `bind()`, restarting your server quickly fails with "Address already in use." This line just tells the OS "let me reuse this port immediately."

### 8. Broadcasting: why the server has to track *who's currently connected*

"Broadcasting a message" means: when one client sends something, the server re-sends it to every *other* connected client. To do that, the server needs to know, at all times, exactly who is currently connected — it can't broadcast to sockets it doesn't know about. That's what `self.clients` is for: a dictionary mapping each open connection (`conn`) to that person's nickname, `{conn: nickname}`. Broadcasting is then just: loop over everything currently in `self.clients`, and send the message to each one — except the sender, who doesn't need their own message echoed back.

If sending to some client fails partway through (their connection quietly died), that's a signal they've disconnected — remove them from `self.clients` so nobody keeps trying to broadcast to a dead connection.

### 9. Race conditions, and why `self.lock` exists

`self.clients` is a single dictionary that is *shared* across every client's thread — the thread for Alice might be adding herself to it at the very same instant the thread for Bob is looping over it to broadcast a message. Because threads can be paused and resumed by the OS at arbitrary points, "at the very same instant" is a real possibility, not just a theoretical one. This is called a **race condition**: the outcome (does it crash? does it corrupt the dictionary? does someone get skipped?) depends on unpredictable timing, and the same code can work fine ten times and then fail on the eleventh.

A **lock** (`threading.Lock`) fixes this by acting like a single bathroom key: whichever thread calls `with self.lock:` first gets to run that block of code alone, and every other thread that also wants the lock has to wait its turn. This guarantees that reads and writes to `self.clients` never happen "at the same time," even though many threads are running concurrently.

### 10. The nickname handshake — a tiny "protocol"

A **protocol**, informally, is just an agreed-upon order and format for messages between two sides. This chat has a very small one: the *very first* thing a client sends, right after connecting, must be its nickname (plain text, nothing else) — and the server's `handle_client` expects exactly that as its first `recv()`. Every message after that first one is treated as a chat message, not a nickname. Both sides have to agree on this order, or the server will treat someone's actual first chat message as if it were their nickname.

### 11. Handling disconnects gracefully

A client can leave in two different ways, and the server needs to survive both:
- **Cleanly**: the client closes its socket on purpose. The server's `recv()` then returns an *empty* byte string (`b""`), which is the signal "the other side hung up."
- **Abruptly**: the client's process (or container) is killed without warning. The server's `recv()` or `send()` can then raise a `ConnectionResetError`.

Either way, the server should remove that client from `self.clients`, close its socket, and — importantly — keep serving everyone else. One client disappearing should never crash the whole server or affect other clients' connections.

### 12. Docker networking recap

Each container in this course's Docker setup (`ds-python-node1`, `ds-python-node2`, `ds-python-node3`) behaves like a separate computer on the same private network, and each one can reach the others by **hostname** (`node1`, `node2`, `node3`) instead of needing a raw IP address — Docker's internal DNS resolves those names for you. That's why the chat client is given `--host node1`: it's being told "the server computer's name on this network is node1," even though `node1` is just a container, not a separate physical machine.

---

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2 python-node3
```

This starts 3 Linux containers — `python-node1`, `python-node2`, `python-node3` — that can all reach each other over a private Docker network, standing in for 3 separate computers.

## Instructions

### Phase 1: Get the core chat logic working, single-threaded first (15 min)

Open `chat_server.py`. Start with the parts that don't require threading knowledge yet:

1. **`broadcast`**: using the ideas from Concept 8 and 9 above — loop over `self.clients` (while holding `self.lock`, since this dictionary is shared across threads), send the message to every connection except `sender_conn`, and if sending to a connection fails, remember it and remove it from `self.clients` afterward.
2. **The one-line TODO inside `handle_client`**: once you've typed a chat message into `message`, hand it off to the `broadcast` method you just wrote (with the sender excluded, so people don't see their own message echoed back).
3. **`start`**: create the TCP socket, apply `SO_REUSEADDR`, `bind`, and `listen` (Concepts 2 and 7). Then, *for this first pass only*, write the `accept()` loop so it calls `self.handle_client(conn, addr)` **directly**, without starting a thread — i.e., skip the "spawn a thread" idea for now.

**Test it (single-threaded):**
```bash
docker exec -it ds-python-node1 python3 /app/labs/lab_04_client_server/chat_server.py
```
You won't be able to fully chat yet, since `chat_client.py` still has TODOs — but you can confirm the server starts and accepts one connection (e.g., with `nc` / telnet, or once you've done Phase 2's client TODOs, come back and try connecting two clients here). Notice that with this direct, non-threaded call, a second client trying to connect while the first is still active would have to wait — this is the blocking problem described in Concept 4.

### Phase 2: Make it truly multi-client and finish the client (25 min)

Now upgrade `start()` so it can serve everyone at once, and complete the client so a real person can use it:

**In `chat_server.py`:**
- Change the `accept()` loop so each connection is handed off to its own **thread** running `handle_client`, instead of being called directly (Concept 5 — remember `t.daemon = True`). This is the fix for Phase 1's blocking problem: the main thread stays free to keep accepting new clients while each connected client's conversation runs in the background.

**In `chat_client.py`:**
- **`receive_messages`**: in a loop, `recv()` up to 1024 bytes from `sock`; if you get back no data, the server has disconnected, so break out of the loop; otherwise decode the bytes and print them (Concepts 2, 3, 11).
- **`main`**: create a TCP socket and `connect()` it to `(host, port)`; then send the nickname as the very first message (Concept 10 — the handshake), encoded to bytes. Start a background **daemon** thread running `receive_messages(sock)` (Concepts 5, 6), so incoming messages can be printed while you're still typing. Inside the `while True` loop, send whatever the user typed to the server (encoded). In the `finally` block, close the socket so the connection is released cleanly when the user quits.

**Test it locally (two terminals, same container is fine for this quick check):**
```bash
docker exec -it ds-python-node1 python3 /app/labs/lab_04_client_server/chat_server.py
docker exec -it ds-python-node1 python3 /app/labs/lab_04_client_server/chat_client.py --host localhost --name Alice
```

### Phase 3: Docker Networking — Server and Clients on Different Machines (15 min)

Now run the server and each client in genuinely separate containers, connecting by hostname (Concept 12):

```bash
# Server (on node1)
docker exec -it ds-python-node1 python3 /app/labs/lab_04_client_server/chat_server.py

# Client 1 (different container!)
docker exec -it ds-python-node2 python3 /app/labs/lab_04_client_server/chat_client.py --host node1 --name Alice

# Client 2 (another container!)
docker exec -it ds-python-node3 python3 /app/labs/lab_04_client_server/chat_client.py --host node1 --name Bob
```

## Checkpoint Questions

1. Connect 3 or more clients from different containers and send a message from one of them. Did all the others receive it? Trace through `broadcast` and explain, in your own words, why the sender itself doesn't get an echo of its own message.
2. Kill one client's container mid-chat (`docker stop ds-python-node2`). Did the server crash, or did it keep running for the remaining clients? Which piece of code is responsible for that behavior (hint: Concept 11)?
3. What's the maximum number of concurrent clients your server can handle, and what (if anything) would eventually limit it? *(Hint: think about what resource each new thread and each new socket connection consumes.)*
