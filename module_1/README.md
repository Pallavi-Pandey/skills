# Module 1: Introduction to Distributed Systems — Hands-On Labs

> **Duration:** 8 hours (3h Introduction + 5h Communication & Synchronization)  
> **Audience:** Postgraduate students & working professionals  
> **Approach:** 20% theory (context-setting) → 80% hands-on labs  
> **Languages:** Python · Go · Java (best tool per topic)  
> **Infrastructure:** Docker / Docker Compose for multi-node simulation

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose | Installation |
|----------|----------------|---------|-------------|
| Docker Desktop | 20.x+ | Multi-node container simulation | [docs.docker.com/get-docker](https://docs.docker.com/get-docker/) |
| Docker Compose | v2.x+ (bundled with Docker Desktop) | Orchestrating lab containers | Included with Docker Desktop |
| Python | 3.9+ | Labs 01–05 (sockets, RPC, KV store) | [python.org/downloads](https://www.python.org/downloads/) |
| Go | 1.21+ | Labs 05–07 (gRPC, concurrency, mutex) | [go.dev/dl](https://go.dev/dl/) |
| JDK | 17+ (Eclipse Temurin recommended) | Lab 08 (deadlock detection) | [adoptium.net](https://adoptium.net/) |
| Git | 2.x+ | Version control | [git-scm.com](https://git-scm.com/) |

### Python Packages

```bash
pip install grpcio grpcio-tools requests redis
```

### Go Packages

```bash
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

### Optional (Recommended)

| Tool | Purpose |
|------|---------|
| Wireshark / tcpdump | Packet inspection for Lab 03 (TCP/IP) |
| Protobuf Compiler (`protoc`) | Generating gRPC code for Lab 05 |
| A terminal multiplexer (tmux / Windows Terminal tabs) | Running multiple nodes simultaneously |

### Verify Installation

```bash
docker --version            # Docker version 20.x+
docker compose version      # Docker Compose version v2.x+
python3 --version           # Python 3.9+
go version                  # go1.21+
javac -version              # javac 17+
git --version               # git 2.x+
```

---

## Repository Structure

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

### Session 1: Introduction (3 hours)

| Time | Topic | Lab | What You Build |
|------|-------|-----|----------------|
| 0:00–0:30 | What is a Distributed System? | — | Context-setting with live demo |
| 0:30–1:15 | Characteristics + Hardware/Software | **Lab 01** | Centralized vs distributed latency benchmark |
| 1:15–1:30 | Break | — | — |
| 1:30–2:30 | DOS vs NOS | **Lab 02** | Docker cluster: shared memory (DOS) vs message passing (NOS) |
| 2:30–3:00 | Case Study + Quiz | — | Google Spanner / Netflix architecture discussion |

### Session 2: Communication & Synchronization (5 hours)

| Time | Topic | Lab | What You Build |
|------|-------|-----|----------------|
| 0:00–0:45 | Layered Protocols + TCP/IP | **Lab 03** | Raw TCP/UDP sockets: packet sniffer & custom protocol |
| 0:45–1:45 | Client-Server Model | **Lab 04** | Multi-client chat server with Docker networking |
| 1:45–2:00 | Break | — | — |
| 2:00–3:00 | Remote Procedure Call | **Lab 05** | RPC from scratch (Python) → gRPC (Go) |
| 3:00–3:45 | Processes & Threads | **Lab 06** | Go goroutines: parallel web scraper + worker pool |
| 3:45–4:00 | Break | — | — |
| 4:00–4:30 | Mutual Exclusion | **Lab 07** | Distributed mutex: Token Ring + Ricart-Agrawala |
| 4:30–5:00 | Deadlocks | **Lab 08** | Java: Create, detect (wait-for graph), and resolve deadlocks |

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
7. **Implement** distributed mutual exclusion algorithms
8. **Detect and resolve** deadlocks using wait-for graphs
