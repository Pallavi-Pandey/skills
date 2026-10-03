# Module 1: Introduction to Distributed Systems — Hands-On Labs

> **Duration:** 8 hours (3h Introduction + 5h Communication & Synchronization)  
> **Audience:** Postgraduate students & working professionals  
> **Approach:** 20% theory (context-setting) → 80% hands-on labs  
> **Languages:** Python · Go · Java (best tool per topic)  
> **Infrastructure:** Docker / Docker Compose for multi-node simulation

Every lab explains new concepts from scratch, in plain language, before you need them — you just need to be willing to type commands into a terminal and read error messages carefully.

A quick note on why three different languages show up across the 8 labs: this module deliberately uses "the best tool per topic" rather than forcing everything into one language, because that's also how real distributed systems are built (different services in different languages talking to each other over the network). Python is used first because its syntax reads closest to plain English, so you can focus on the *distributed systems ideas* rather than fighting the language. Go and Java are introduced later, one small piece at a time, and each new piece of syntax is explained when you first encounter it.

---

## Prerequisites

Before touching any code, you need a few pieces of software installed on your machine. Here's *why* each one matters, in plain terms, before you look at the table:

- **Docker** lets you run several small, isolated "pretend computers" (called containers) on your one physical laptop, each with its own network address, so that a "3-node distributed system" can actually exist and talk over a network — without you needing 3 real machines. Docker Compose is just the tool that starts/stops a whole group of these containers together with one command.
- **Python** is the first language you'll write code in. It's used for the earliest, most from-scratch labs (raw **sockets** — a socket is just a program's handle on an open network connection, the same way a phone handset is your handle on an open phone call: you can "speak" into it and "listen" from it — plus a hand-rolled key-value store, and a hand-rolled RPC framework) because its syntax gets out of your way while you learn the underlying networking concepts.
- **Go** is a newer, simpler-than-Java language that real companies (Google, in particular) use heavily for distributed systems, because it makes writing many things happening "at once" (concurrency) easy and lightweight. You'll meet it for the first time in Lab 05 onward, and each new keyword is explained when it shows up.
- **JDK (Java Development Kit)** is what you need to write and run Java code. Java is used specifically for Lab 08 because its tooling for inspecting a "stuck" program (a deadlock) is mature and easy to read.
- **gRPC** (say "gee-arr-pee-see") is a popular, ready-made framework that two programs — even written in *different* languages — can use to call functions on each other over the network, without you having to hand-write the networking code yourself. You'll first build RPC "the hard way" in Python, then see how gRPC does the same job for you automatically, across a Python client and a Go server.
- **protoc** (the "Protocol Buffer Compiler") is a code-generator tool that gRPC relies on: you describe your service's function signatures once in a small `.proto` text file, and `protoc` generates matching client/server code for you in whatever language you need.

### Required Software

| Software | Minimum Version | Purpose | Installation |
|----------|----------------|---------|-------------|
| Docker Desktop | 20.x+ | Multi-node container simulation | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| Docker Compose | v2.x+ (bundled with Docker Desktop) | Orchestrating lab containers | Included with Docker Desktop |
| Python | 3.9+ | Labs 01–05 (sockets, RPC, KV store) | [python.org/downloads](https://www.python.org/downloads/) |
| Go | 1.25+ | Labs 05–07 (gRPC, concurrency, mutex) | [go.dev/dl](https://go.dev/dl/) |
| JDK | 17+ (Eclipse Temurin recommended) | Lab 08 (deadlock detection) | [adoptium.net](https://adoptium.net/) |
| Git | 2.x+ | Version control | [git-scm.com](https://git-scm.com/) |

### Python Packages

These are extra, third-party pieces of code (packages) that Python doesn't include by default, but the labs need. `pip` is Python's built-in package installer — running the command below downloads and installs all four in one go: `grpcio` and `grpcio-tools` give you gRPC support and the `protoc` code generator, `requests` makes it easy to make HTTP calls, and `redis` lets Python talk to a Redis server (used in Lab 02).

```bash
pip install grpcio grpcio-tools requests redis
```

### Go Packages

Similarly, these two commands install Go's own `protoc` plugins — the pieces that let the Protocol Buffer Compiler generate Go-specific client/server code for gRPC. You'll only need these once you reach Lab 05.

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

### Optional (Recommended)

These aren't required to complete the labs, but they make a couple of concepts easier to *see* with your own eyes:

| Tool | Purpose |
|------|---------|
| Wireshark / tcpdump | Lets you watch the actual network packets flying between programs, in Lab 03 (TCP/IP) — useful for seeing "under the hood" of what a socket is doing |
| Protobuf Compiler (`protoc`) | The code-generator tool mentioned above, used to generate gRPC code for Lab 05 (installed automatically if you installed the Python/Go packages above) |
| A terminal multiplexer (tmux / Windows Terminal tabs) | Several labs ask you to run 3+ programs (nodes) at once — this just makes it easier to have multiple terminal windows/tabs open side by side |

### Verify Installation

Once everything above is installed, run these commands to double-check each tool is actually on your system and recent enough — if any of these fail with "command not found," go back and reinstall that tool before starting Lab 01.

```bash
docker --version            # Docker version 20.x+
docker compose version      # Docker Compose version v2.x+
python3 --version           # Python 3.9+
go version                  # go1.25+
javac -version              # javac 17+
git --version               # git 2.x+
```

---

## Repository Structure

Here's how everything in this module is organized on disk. You mostly only need `guides/` (if you're an instructor) and `labs/` (if you're a student working through the exercises) — `solutions/` and `docker/` are supporting material you'll be pointed to when needed.

```
module_1/
├── README.md                          ← You are here
├── agenda.md                          ← Original syllabus
│
├── guides/                            ← Instructor-facing session guides
│   ├── session_1_introduction.md      ← 3h: Intro to Distributed Systems
│   └── session_2_communication.md     ← 5h: Communication & Synchronization
│
├── labs/                              ← Starter code with TODOs (student-facing)
│   ├── lab_01_what_is_distributed/    ← Centralized vs Distributed comparison
│   ├── lab_02_dos_vs_nos/             ← Docker: DOS vs NOS behavior
│   ├── lab_03_tcp_ip_sockets/         ← Python: Raw TCP/UDP socket programming
│   ├── lab_04_client_server/          ← Python: Multi-client chat server
│   ├── lab_05_rpc/                    ← Python + Go: RPC from scratch → gRPC
│   ├── lab_06_processes_threads/      ← Go: Goroutines, channels, thread pools
│   ├── lab_07_mutual_exclusion/       ← Go: Distributed mutual exclusion algorithms
│   └── lab_08_deadlocks/             ← Java: Deadlock creation, detection & resolution
│
├── solutions/                         ← Full working solutions (instructor-facing)
│   ├── lab_01_solution/
│   ├── lab_02_solution/
│   ├── lab_03_solution/
│   ├── lab_04_solution/
│   ├── lab_05_solution/
│   ├── lab_06_solution/
│   ├── lab_07_solution/
│   └── lab_08_solution/
│
└── docker/                            ← Shared Docker infrastructure
    ├── Dockerfile.python
    ├── Dockerfile.go
    ├── Dockerfile.java
    └── network-setup.yml
```

---

## Session Breakdown

The 8 hours of estimated effort are split into two sessions. Each row below is one topic block: a short theory explanation followed immediately by a hands-on lab that makes the idea concrete. These are rough pacing guides, not a fixed clock schedule — if you're working through this on your own, feel free to take longer on anything that needs more time. You don't need to read ahead — each lab's own README re-explains what you need, right before you need it.

### Session 1: Introduction (~3 hours)

| Duration | Topic | Lab | What You Build |
|------|-------|-----|----------------|
| ~30 min | What is a Distributed System? | — | Context-setting with live demo |
| ~45 min | Characteristics + Hardware/Software | **Lab 01** | Centralized vs distributed latency benchmark |
| ~15 min | Break | — | — |
| ~60 min | DOS vs NOS | **Lab 02** | Docker cluster: shared memory (DOS) vs message passing (NOS) |
| ~30 min | Case Study + Quiz | — | Google Spanner / Netflix architecture discussion |

### Session 2: Communication & Synchronization (~5 hours)

| Duration | Topic | Lab | What You Build |
|------|-------|-----|----------------|
| ~45 min | Layered Protocols + TCP/IP | **Lab 03** | Raw TCP/UDP sockets: packet sniffer & custom protocol |
| ~60 min | Client-Server Model | **Lab 04** | Multi-client chat server with Docker networking |
| ~15 min | Break | — | — |
| ~60 min | Remote Procedure Call | **Lab 05** | RPC from scratch (Python) → gRPC (Go) |
| ~45 min | Processes & Threads | **Lab 06** | Go goroutines: parallel web scraper + worker pool |
| ~15 min | Break | — | — |
| ~30 min | Mutual Exclusion | **Lab 07** | Distributed mutex: Token Ring |
| ~30 min | Deadlocks | **Lab 08** | Java: Create, detect (wait-for graph), and resolve deadlocks |

---

## Quick Start

```bash
# Build and start lab containers
cd docker/
docker compose -f network-setup.yml up -d

# Start Lab 01
cd ../labs/lab_01_what_is_distributed/
cat README.md           # Read the lab instructions
```

---

## Learning Outcomes

After completing all 8 labs, you will be able to:

1. **Explain** why distributed systems exist and their core tradeoffs (CAP, latency, fault tolerance)
2. **Differentiate** DOS vs NOS with hands-on evidence from Docker clusters
3. **Implement** TCP/UDP socket communication from scratch
4. **Build** a working client-server application with multiple concurrent clients
5. **Create** both raw RPC and gRPC services across language boundaries
6. **Manage** concurrent processes/threads and understand their tradeoffs
7. **Implement** a distributed mutual exclusion algorithm (Token Ring)
8. **Detect and resolve** deadlocks using wait-for graphs
