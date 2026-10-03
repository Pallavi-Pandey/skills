# Lab 03: TCP/UDP Socket Programming — Reliable vs Best-Effort Delivery

> **Time:** 35 minutes | **Language:** Python | **Infrastructure:** Docker

## Objective

Build a TCP server and a UDP server "from scratch" using raw sockets (no libraries doing the networking for you), then deliberately compare them so you can *see* — not just read about — the core tradeoff in distributed systems: TCP guarantees your data arrives, in order, but costs more overhead; UDP is fast and cheap but can silently lose data. Finally, you'll build a tiny custom binary protocol on top of TCP, which is basically what every real network protocol (HTTP, gRPC, database wire protocols) does under the hood.

## Why This Matters for Security

This lab is the foundation for a huge amount of network security work. Tools like Wireshark and tcpdump (mentioned in the Session 2 guide) work by reading exactly the kind of raw bytes-on-the-wire you're producing here — once you've hand-parsed a header yourself, packet captures stop looking like magic. The custom protocol you build in Part 3 also has a real vulnerability class baked into it on purpose: it trusts the `LENGTH` field a client sends without validating it against how much data actually arrived. Real protocol parsers that make this same mistake are the root cause of many actual buffer-overread and memory-corruption CVEs — a hostile client can lie about the length field to make a server read past the end of a buffer. Also notice that nothing in this protocol is encrypted or authenticated: anyone who can see the traffic can read it or tamper with it in transit, which is exactly the gap that TLS exists to close on top of raw TCP.

---

## How to Run This Lab (Quick Reference)

```bash
# 1. Start the 2 Python containers
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2

# 2. Part 1 — TCP echo server
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode server
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode client --host node1

# 3. Part 2 — UDP blaster (start the receiver FIRST)
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode receiver
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode sender --host node1 --count 1000

# 4. Part 3 — custom binary protocol
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/custom_protocol.py --mode server
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/custom_protocol.py --mode client --host node1
```

## Concepts you need before you start

You don't need to be a networking expert for this lab — you mainly need to understand the nine ideas below. Read this section fully before opening any code. If you did Lab 01, ideas 1, 2, and 8 will be a quick recap; everything else is new.

### 1. Quick recap: what is a socket?

A **socket** is Python's handle for "an open connection over the network that I can send bytes into and read bytes out of." Think of it like a phone: `socket.socket(...)` picks up the phone, `.bind()` claims your own phone number, `.listen()` + `.accept()` wait for and answer incoming calls, `.connect()` dials someone else's number, and `.send()`/`.recv()` are speaking and listening. `socket.AF_INET` means "use a normal IPv4 address like `127.0.0.1` or `node1`."

### 2. TCP vs UDP — the two ways to send bytes over a network

This whole lab is about this one distinction, so read it twice.

- **TCP (`socket.SOCK_STREAM`)** is like a **phone call**. Before you can talk, both sides do a little handshake to set up the connection (see idea #3). Once connected, whatever bytes you `send()` are *guaranteed* to arrive at the other end, *in the order you sent them* — and if something gets lost in transit, TCP quietly detects it and resends it behind the scenes. You never see the loss; you just see it arrive a bit later. This reliability costs a little extra overhead (the handshake, tracking what's been acknowledged, etc.).
- **UDP (`socket.SOCK_DGRAM`)** is like **dropping postcards in a mailbox**. Each postcard (called a **datagram**) is sent independently, with no setup, no handshake, and no guarantee. It might arrive, it might arrive out of order, or it might just vanish — and nobody tells you if it does. In exchange, UDP has almost no overhead, so it's fast and lightweight.

Neither one is "better" — they exist for different jobs. TCP is used when correctness matters more than speed (loading a web page, transferring a file, a database connection — you can't afford a missing byte). UDP is used when speed/low-overhead matters more than perfect delivery (live video calls, multiplayer games, DNS lookups — a dropped video frame is fine, but waiting for it to be resent would make the call laggier, not better). Part 2 of this lab makes UDP's "best effort" behavior visible by literally counting lost messages.

### 3. The TCP three-way handshake (why TCP needs setup and UDP doesn't)

Before any data flows over a TCP connection, the two sides exchange three small control messages to agree "yes, we're both here, and we're both ready":

1. Client → Server: **SYN** ("I'd like to start a connection")
2. Server → Client: **SYN-ACK** ("Okay, got it, I'd like to too")
3. Client → Server: **ACK** ("Confirmed, let's go")

Only after this handshake completes does your `connect()` call return successfully and actual data start flowing. This is the "phone ringing and being answered" part of the phone-call analogy. UDP skips all of this entirely — there's no setup step, which is a big part of why it's faster and has less overhead, but also why there's no built-in way to know if the other side is even listening.

### 4. Ports — how one machine can run many network programs at once

An IP address (or a Docker container name like `node1`, which gets resolved to one) identifies *which machine*. A **port** is a number from 0–65535 that identifies *which program on that machine* should receive the data — like an apartment number within a building's street address. A server picks a specific, known port and `bind()`s to it so clients know where to find it (this lab uses `7000` for the TCP echo server, `7001` for the UDP blaster, `7002` for the custom protocol server). A client usually doesn't care which port it uses, so it lets the OS assign it an unused one automatically.

### 5. Bytes vs text: why you'll see `.encode()` and `.decode()`

Sockets only ever send and receive raw **bytes** (numbers 0–255) — they know nothing about "text." Python strings (`str`), on the other hand, are text. So every time you want to send a string over a socket, you must first convert it to bytes with `.encode("utf-8")`, and every time you receive bytes that represent text, you convert them back with `.decode("utf-8")`. `utf-8` is just the specific, near-universal rule for how to turn characters into byte values and back.

### 6. What "big-endian" byte order means, and why the custom protocol cares

A number bigger than 255 needs more than one byte to represent (e.g. the number 4 as a 2-byte value is the bytes `0x00 0x04`). But when you use *multiple* bytes to store one number, which byte comes first — the most significant one or the least significant one? Different computer architectures historically disagreed, so to avoid two machines misreading each other's numbers, network protocols pick one fixed rule: **big-endian** ("network byte order"), meaning the most significant byte comes first. In Part 3, you'll encode a length field as 2 bytes, and you must encode/decode it as big-endian on both ends, or the two sides will disagree about how many bytes a message is.

### 7. `struct.pack` / `struct.unpack` — converting numbers to exact byte layouts

Python's `struct` module converts between Python values (ints) and a precise sequence of bytes, using a tiny format-string language. In this lab you'll see the format string `"!BH"`:

- `!` — use network byte order (big-endian, from idea #6)
- `B` — one **unsigned char**: exactly 1 byte, holding a value 0–255
- `H` — one **unsigned short**: exactly 2 bytes, holding a value 0–65535

So `struct.pack("!BH", msg_type, length)` takes two Python integers and turns them into exactly 3 raw bytes laid out as `[msg_type][length_high_byte][length_low_byte]`. `struct.unpack("!BH", some_3_bytes)` does the reverse: given exactly those 3 bytes, it hands you back `(msg_type, length)` as Python integers. You don't need to memorize the format language beyond this — just recognize that `B` = 1 byte and `H` = 2 bytes.

### 8. What a "binary protocol" is, and why messages need a length prefix (framing)

A **protocol** is just an agreed-upon set of rules for what bytes mean. A **binary protocol** (as opposed to a text-based one, like typing raw commands) packs information into raw byte layouts, like the header format from idea #7, rather than human-readable text.

Here's the subtle problem this solves: TCP is a **stream** of bytes with no built-in concept of "messages." If you call `send()` twice in a row with two separate messages, TCP might deliver them to the receiver's `recv()` as one call that returns both messages glued together, or split across two `recv()` calls in the middle of a message — you cannot rely on "one `send()` = one `recv()`." (UDP doesn't have this problem: each `sendto()` arrives as exactly one `recvfrom()`, or not at all.)

The fix is **framing**: agree that every message starts with a small, fixed-size **header** that says how long the **payload** (the actual content) is. In Part 3's protocol, the header is always exactly 3 bytes: `[MSG_TYPE: 1 byte][LENGTH: 2 bytes]`. So a receiver always knows the recipe: read exactly 3 bytes first, decode the length from them, then read exactly that many more bytes for the payload — no matter how the bytes happened to arrive in individual `recv()` calls. This "read the header, then read exactly N more bytes" pattern is already written for you in `run_server` in `custom_protocol.py` — study it, because you'll need to do the same thing yourself for the client.

### 9. A few smaller things you'll run into

- **`SO_REUSEADDR`**: without this socket option, restarting a server right after stopping it can fail with "Address already in use," because the OS briefly holds the port. Setting it tells the OS to let you reuse the port immediately.
- **`listen(backlog=5)`**: the backlog is how many incoming connections the OS will queue up (waiting for your `accept()` call) before it starts rejecting new ones. 5 is a small, reasonable number for a lab.
- **Threads**: like in Lab 01, a server that only handles one client at a time is useless, so the TCP echo server spawns a background `threading.Thread` per connected client so it can keep accepting new clients.
- **`socket.settimeout(seconds)`**: normally, a blocking call like `recv()` or `recvfrom()` waits forever until data arrives. `settimeout()` makes it give up and raise a `socket.timeout` exception after N seconds of nothing happening. The UDP receiver uses this because, unlike TCP, there's no "connection" it can watch for a clean close — the only way it knows the sender is finished is "nothing arrived for a while."
- **Getting `b""` (empty bytes) back from `recv()`**: this specifically means "the other side closed the connection." It's different from *no data yet* (which just blocks/waits) — an empty result is the signal to stop reading and close your end too.
- **`recvfrom()` vs `recv()`**: UDP has no persistent connection, so a UDP socket can receive datagrams from many different senders. `recvfrom()` returns both the data *and* the sender's address `(data, addr)`, because otherwise you'd have no way to know who sent it. `recv()` (used with TCP) doesn't need this, since a TCP connection is always with one specific, already-known peer.
- **`ConnectionResetError`**: raised when the other side of a TCP connection disconnects abruptly (e.g. the client process was killed) instead of closing cleanly. The starter code simply catches and ignores it.

---

## What You'll Do

1. Build a TCP echo server/client and confirm every message you send comes back, in order, uppercased.
2. Build a UDP "blaster" that fires 1000 messages at a receiver and see that some don't arrive.
3. Design and implement a tiny binary protocol on top of TCP, with a proper header and framing.

## Setup

```bash
cd docker/
docker compose -f network-setup.yml up -d python-node1 python-node2
```

This starts two Linux containers, `python-node1` and `python-node2`, on a private Docker network so they can reach each other by name (e.g. `node1`).

---

## Instructions

### Part 1: TCP Echo Server (15 min)

Open `tcp_echo.py`. The goal: a server that accepts a connection, reads whatever text a client sends, converts it to UPPERCASE, and sends it back — and a matching client you can type into interactively.

Fill in the TODOs:

1. **`run_server`**: create a TCP socket (`AF_INET`, `SOCK_STREAM`), set `SO_REUSEADDR` (idea #9), `bind` it to `(host, port)`, and `listen` with `backlog=5`. Then, forever: `accept()` a connection (which gives you `conn` — a socket specific to that one client — and `addr`, the client's address), print that it connected, and spawn a thread running `handle_echo(conn, addr)` so the server can immediately go back to accepting the *next* client (idea #9, threads).
2. **`handle_echo`**: in a loop, receive up to 1024 bytes from `conn`. If what came back is empty (`b""`), that means the client disconnected (idea #9) — break out of the loop. Otherwise, decode the bytes to a string (idea #5), uppercase it, encode it back to bytes, and send it back to `conn`. Print what you received and what you sent, for visibility.
3. **`run_client`**: create a TCP socket and `connect()` it to `(host, port)`. Then, for each line of input the user types, send it (encoded) to the server, receive the echoed response (up to 1024 bytes), decode it, and print it. On exit (Ctrl+C or EOF), close the socket.

**Test it:**
```bash
# Terminal 1 (inside python-node1) — starts the server
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode server

# Terminal 2 (inside python-node2) — connects as a client
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode client --host node1
```

Type a few messages into the client terminal — you should see each one echoed back in UPPERCASE, every single time, in the order you sent it. That reliability is TCP doing its job.

### Part 2: UDP Message Blaster (10 min)

Open `udp_blaster.py`. The goal: send 1000 independent UDP datagrams as fast as possible, and see how many the receiver actually counts — demonstrating UDP's "best effort, no guarantee" delivery model (idea #2).

Fill in the TODOs:

1. **`run_receiver`**: create a UDP socket (`AF_INET`, `SOCK_DGRAM` — note: no `listen`/`accept`, UDP has no connections to accept), `bind` it to `(host, port)`, and call `settimeout(timeout)` so the receive loop gives up after a few seconds of silence (idea #9). Then, in a loop, call `recvfrom(1024)` to get each datagram, increment your `received` counter, and every 100 messages print a progress line. Let the `socket.timeout` exception (already caught outside the loop) end things naturally once the sender is done.
2. **`run_sender`**: create a UDP socket (no `connect()` needed — you specify the destination on every single send). For each of `count` messages, call `sendto(msg, (host, port))`.

**Test it:**
```bash
# Terminal 1 (inside python-node1) — the receiver, start this FIRST
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode receiver

# Terminal 2 (inside python-node2) — the sender
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode sender --host node1 --count 1000
```

**Expected:** the receiver's final count will very likely be *less than* 1000. Those aren't bugs in your code — that's UDP quietly dropping datagrams, exactly as designed. Compare this to Part 1, where TCP never lost or reordered a single message.

### Part 3: Custom Binary Protocol (10 min)

Open `custom_protocol.py`. The goal: build a tiny message format on top of TCP with a proper header (idea #8), and a request/response exchange using it. The format, as given in the file:

```
[MSG_TYPE: 1 byte] [LENGTH: 2 bytes big-endian] [PAYLOAD: N bytes]

MSG_TYPE:
  0x01 = PING    (no payload)
  0x02 = PONG    (no payload)
  0x03 = DATA    (payload = arbitrary data)
  0x04 = ERROR   (payload = error message)
```

Fill in the TODOs:

1. **`encode_message(msg_type, payload)`**: build the 3-byte header with `struct.pack("!BH", msg_type, len(payload))` (idea #7), then return that header with the payload bytes appended after it — this is the single bytes blob you'd pass to `send()`.
2. **`decode_message(data)`**: given a blob of bytes that already contains a full header + payload, unpack the first 3 bytes with `struct.unpack("!BH", data[:3])` to recover `msg_type` and `payload_len`, then slice out `data[3:3+payload_len]` as the payload, and return `(msg_type, payload)`.
3. **`run_server`'s TODO** (message handling): the framing/reading part is already written for you — study it, since it's exactly the "read header, then read exactly N more bytes" pattern from idea #8. You just need to react based on `msg_type`: if it's `PING`, send back an encoded `PONG` (no payload); if it's `DATA`, send back an encoded `DATA` message whose payload is `"ACK: "` followed by the original payload; otherwise, send back an encoded `ERROR` with payload `"Unknown message type"`.
4. **`run_client`'s TODOs**: send a `PING` (via `encode_message`), then receive and decode the response. Because TCP gives you no message boundaries (idea #8), you can't just call `recv()` once and hope it's the whole message — apply the same "read exactly 3 header bytes, then read exactly `payload_len` more" approach used in `run_server` before calling `decode_message` on the result. Then do the same thing again, this time sending a `DATA` message with payload `"Hello, custom protocol!"`, and print what comes back.

**Test it:**
```bash
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/custom_protocol.py --mode server
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/custom_protocol.py --mode client --host node1
```

## Checkpoint Questions

1. Out of the 1000 UDP messages you sent in Part 2, how many did the receiver actually count? Run it a couple of times — does the number change?
2. If you tried to send a large (say, 10MB) file over UDP instead of TCP, what would go wrong that doesn't happen with TCP?
3. Why does TCP need the three-way handshake described in idea #3 before it can send any data, while UDP can just start firing datagrams immediately?
