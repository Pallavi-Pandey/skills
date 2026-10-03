# Module 1: Introduction to Distributed Systems

---

## Part A: Introduction

---

### 1. Definition of a Distributed System

#### What is it?

A **distributed system** is a collection of independent computers (called **nodes**) that are connected through a network and work together as a single coherent system. To the end user, the system appears as one unified computer, even though it is made up of multiple machines located in different places.

> **Simple analogy:** Think of a team of chefs in different kitchens, all connected by phone, working together to prepare one large banquet. Each chef works on their own dish independently, but they coordinate with each other so that the entire meal is ready on time. The guests at the banquet see one seamless dinner — they don't know (or care) that it was prepared across multiple kitchens.

#### Formal Definition

> *"A distributed system is a collection of autonomous computers linked by a computer network and equipped with distributed system software."*
> — Andrew S. Tanenbaum

The key word here is **autonomous** — each computer has its own processor, memory, and operating system. No single machine controls the others.

#### Why do we use distributed systems?

| Reason | Explanation |
|--------|-------------|
| **Resource Sharing** | Share hardware (printers, storage), software, and data across multiple users and locations |
| **Scalability** | Easily add more machines to handle more users or data — no need to buy one giant supercomputer |
| **Reliability & Fault Tolerance** | If one machine fails, others can take over. The system doesn't crash entirely |
| **Performance** | Divide a big task among many machines so it finishes faster (parallel processing) |
| **Geographic Distribution** | Users in different cities/countries can access the same system (e.g., Google, Amazon) |

#### Where do we see distributed systems?

- **The Internet** — the largest distributed system in the world
- **Cloud Computing** — AWS, Google Cloud, Azure (your data and apps run on many servers)
- **Online Banking** — ATMs, mobile banking apps, all connected to central and regional servers
- **Social Media** — Facebook, Instagram serve billions of users from thousands of servers worldwide
- **Blockchain/Cryptocurrency** — Bitcoin is a fully distributed system with no central authority

#### 🔐 Security Perspective

Distributed systems introduce a larger **attack surface**. Since data travels across networks between nodes, attackers can intercept, modify, or spoof communications. Understanding distributed systems is essential for cybersecurity professionals because securing these systems requires knowledge of how they communicate, synchronize, and handle failures.

---

### 2. Characteristics of Distributed Systems

A distributed system has several defining characteristics that set it apart from a single standalone computer:

#### a) No Common Physical Clock

Each machine in a distributed system has its own internal clock. These clocks may drift apart over time, making it difficult to determine the exact order of events. This is why distributed systems need special **synchronization algorithms** (covered later).

> **Example:** If Server A timestamps a transaction at 10:00:01 and Server B timestamps another at 10:00:01, which happened first? Without a shared clock, it's ambiguous.

#### b) No Shared Memory

Each node has its own local memory (RAM). Nodes cannot directly access each other's memory — they must communicate by **passing messages** over the network.

> **Example:** Unlike threads in a single computer that share the same RAM, two servers in different cities communicate by sending data packets over the internet.

#### c) Geographical Separation

Nodes can be in the same room, same building, same city, or spread across continents. The system must work correctly regardless of physical distance.

#### d) Autonomy and Heterogeneity

Each node operates independently and can even run different hardware and software. A distributed system may include Linux servers, Windows servers, and mobile devices all working together.

#### e) Concurrency

Multiple processes run simultaneously across different nodes. Managing concurrent access to shared resources (like a database) is a core challenge.

#### f) Scalability

The system should be designed to handle growth — more users, more data, more nodes — without a complete redesign.

#### g) Fault Tolerance

The system should continue to function even when some components fail. This is achieved through **redundancy** (keeping copies of data) and **failover mechanisms** (switching to a backup when a primary fails).

#### h) Transparency

The system hides its distributed nature from the user. There are several types of transparency:

| Type | What it Hides | Example |
|------|---------------|---------|
| **Access Transparency** | Differences in data representation and access methods | Same API works whether data is local or remote |
| **Location Transparency** | Where a resource is physically located | A URL like `google.com` doesn't tell you which server you're hitting |
| **Migration Transparency** | That a resource may move to a new location | Your cloud VM migrates to another physical host without downtime |
| **Replication Transparency** | That multiple copies of a resource exist | You read from a database — you don't know if it came from a replica |
| **Concurrency Transparency** | That multiple users access a resource simultaneously | Two people edit a Google Doc at the same time without conflicts |
| **Failure Transparency** | That a component has failed and recovered | Netflix continues streaming even if one server fails |

---

### 3. Hardware Concepts

Distributed systems rely on specific hardware configurations. The two main classifications are based on how memory is shared:

#### a) Multiprocessors (Shared Memory Systems)

- Multiple processors (CPUs) share **one common memory** through a shared bus or interconnection network.
- Communication is fast because processors read/write to the same memory.
- **Limitation:** Hard to scale beyond a few dozen processors because the shared bus becomes a bottleneck.
- **Example:** A modern multi-core laptop or a high-end server with 64 cores.

#### b) Multicomputers (Private Memory Systems)

- Each computer has its **own private memory** — no shared memory.
- Communication happens by **message passing** over a network.
- Easier to scale to hundreds or thousands of nodes.
- This is the typical architecture of a distributed system.

**Sub-categories of Multicomputers:**

| Type | Description | Example |
|------|-------------|---------|
| **Homogeneous Multicomputer (MPP)** | Identical machines, tightly connected, same location | Supercomputers (e.g., in research labs) |
| **Heterogeneous Multicomputer** | Different machines, loosely connected, different locations | The Internet, a university network |

#### 🔐 Security Perspective

In shared memory systems, if one process is compromised, it could potentially read or corrupt another process's data in shared memory — a classic **privilege escalation** risk. In message-passing systems, messages can be intercepted (**eavesdropping**) or tampered with (**man-in-the-middle attacks**), making encryption and authentication essential.

---

### 4. Software Concepts

The software that manages a distributed system determines how users and applications interact with the underlying hardware. There are three broad categories:

#### a) Tightly Coupled Software (Distributed Operating System)

- A single operating system manages all the nodes.
- The OS decides where to run processes, how to allocate resources across machines.
- Users see one unified system.
- **Example (concept):** Amoeba OS (academic distributed OS developed by Tanenbaum).

#### b) Loosely Coupled Software (Network Operating System)

- Each machine runs its **own independent operating system**.
- Users are aware that there are multiple machines.
- They explicitly log into specific machines and transfer files between them.
- **Example:** A network of Linux and Windows machines where you use SSH to access different servers.

#### c) Middleware-Based Systems

- A software layer (**middleware**) sits between the OS and applications.
- It provides a unified interface, hiding the heterogeneity of underlying systems.
- **Examples:** Java RMI, CORBA, DCOM, Web Services, gRPC.

---

### 5. Distributed Operating System (DOS)

#### What is it?

A Distributed Operating System is an OS that manages a group of independent computers and makes them appear to be a single computer. It controls all the hardware and software resources and provides a unified interface to the user.

#### Key Features

- **Single System Image:** The user sees one computer, not many.
- **Process Migration:** The OS can move a running process from one machine to another for load balancing or fault tolerance.
- **Global File System:** Files are accessible from any node without the user needing to know where they are physically stored.
- **Unified Process Management:** The OS schedules processes across all nodes to optimize performance.

#### Why use it?

- True transparency — users and applications don't need to worry about distribution.
- Efficient resource utilization — the OS can distribute workload intelligently.
- Easier programming model — developers write code as if for a single machine.

#### Where is it used?

- Mostly in **research and academic** settings (e.g., Amoeba, Sprite, V-System).
- Not widely used commercially because of the complexity of building and maintaining them.
- Concepts from DOS are used in modern **cluster operating systems** and **container orchestration** (e.g., Kubernetes abstracts away individual machines).

---

### 6. Network Operating System (NOS)

#### What is it?

A Network Operating System is an OS that provides services to computers connected over a network. Unlike a DOS, each machine retains its own local operating system and identity. The NOS adds networking capabilities on top.

#### Key Features

- Each machine has its **own OS** (could be different — Windows, Linux, macOS).
- Users are **aware** of multiple machines and explicitly access resources on specific machines.
- Provides services like **remote login** (SSH, Telnet), **file transfer** (FTP, SCP), and **file sharing** (NFS, SMB).

#### Why use it?

- Simple to set up and manage compared to a distributed OS.
- Allows heterogeneous machines to coexist and share resources.
- Each machine can be administered independently.

#### Where is it used?

- **Corporate networks** — employees access shared printers, file servers, and applications.
- **University labs** — students SSH into different servers for different courses.
- **Home networks** — sharing files between a Windows PC and a Mac.

#### Comparison: Distributed OS vs Network OS

| Feature | Distributed OS | Network OS |
|---------|---------------|------------|
| **System Image** | Single unified image | Multiple independent machines |
| **User Awareness** | User doesn't know about multiple machines | User is aware of individual machines |
| **OS on Each Node** | One OS manages all nodes | Each node has its own OS |
| **Transparency** | High (location, migration, replication) | Low (user must specify machine) |
| **Heterogeneity** | Typically homogeneous | Supports heterogeneous machines |
| **Complexity** | Very complex to build | Simpler to implement |
| **Examples** | Amoeba, Sprite | Windows Server, Linux + NFS |
| **Real-world Adoption** | Rare (mostly research) | Very common |

---

## Part B: Communication and Synchronization

---

### 7. Layered Protocols

#### What are they?

When computers communicate over a network, the process involves many steps: converting data to electrical signals, routing it through the internet, ensuring it arrives correctly, and presenting it to the application. **Layered protocols** organize these steps into distinct layers, where each layer handles a specific responsibility.

#### Why do we use layers?

- **Modularity:** Each layer does one job well. You can change one layer without affecting others.
- **Abstraction:** Higher layers don't need to know the details of lower layers. Your web browser doesn't care whether you're on Wi-Fi or Ethernet.
- **Standardization:** Layers allow different vendors to build compatible products. Any browser can talk to any web server because they both follow HTTP (application layer) and TCP/IP (transport/network layers).
- **Easier Debugging:** If something goes wrong, you can isolate the problem to a specific layer.

#### The OSI Model (7 Layers)

The **Open Systems Interconnection** model is a conceptual framework with 7 layers:

| Layer | Name | Function | Protocol Examples |
|-------|------|----------|-------------------|
| 7 | **Application** | User-facing services (email, web browsing) | HTTP, FTP, SMTP, DNS |
| 6 | **Presentation** | Data formatting, encryption, compression | SSL/TLS, JPEG, ASCII |
| 5 | **Session** | Establishes, manages, and terminates sessions | NetBIOS, RPC |
| 4 | **Transport** | Reliable data transfer, error recovery | TCP, UDP |
| 3 | **Network** | Routing and logical addressing | IP, ICMP, ARP |
| 2 | **Data Link** | Framing, error detection on physical link | Ethernet, Wi-Fi (802.11) |
| 1 | **Physical** | Transmitting raw bits over a physical medium | Cables, Radio waves, Fiber |

> **Memory trick (top to bottom):** **A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing

#### How it works

When you send a message:
1. Your data starts at the **Application layer** (Layer 7).
2. Each layer adds its own **header** (and sometimes a trailer) as the data moves down — this is called **encapsulation**.
3. At the **Physical layer**, data is transmitted as bits over the wire/airwaves.
4. At the receiving end, each layer removes its header as data moves up — this is called **decapsulation**.

#### 🔐 Security Perspective

Security mechanisms operate at different layers:
- **Layer 2:** MAC address filtering, port security
- **Layer 3:** IPsec (encrypts IP packets), firewalls
- **Layer 4:** TLS/SSL (secures TCP connections)
- **Layer 7:** HTTPS, application-level authentication

Understanding layered protocols helps cybersecurity professionals know **where** to implement security controls and **what** attacks target which layer (e.g., ARP spoofing targets Layer 2, IP spoofing targets Layer 3).

---

### 8. TCP/IP Protocol Suite

#### What is it?

The **TCP/IP Protocol Suite** (Transmission Control Protocol / Internet Protocol) is the set of communication protocols actually used on the Internet. While the OSI model is a theoretical framework, TCP/IP is the **practical implementation** that powers real-world networking.

#### Why do we use TCP/IP?

- It's the **standard** protocol suite of the Internet — every device connected to the Internet uses it.
- It's **battle-tested** — developed since the 1970s (ARPANET) and continuously improved.
- It's **platform-independent** — works on any hardware or OS.

#### TCP/IP Layers (4 Layers)

| TCP/IP Layer | Equivalent OSI Layers | Function | Key Protocols |
|--------------|----------------------|----------|---------------|
| **Application** | 7, 6, 5 | Application services and data representation | HTTP, FTP, SMTP, DNS, SSH |
| **Transport** | 4 | End-to-end communication, reliability | TCP, UDP |
| **Internet** | 3 | Logical addressing and routing | IP (IPv4, IPv6), ICMP, ARP |
| **Network Access** | 2, 1 | Physical transmission over the medium | Ethernet, Wi-Fi, PPP |

#### Key Protocols Explained

**IP (Internet Protocol):**
- Provides **logical addressing** (IP addresses) and **routing** (finding a path from source to destination).
- **Connectionless** — each packet is routed independently; packets may arrive out of order.
- IP does **not** guarantee delivery — it's a "best effort" protocol.

**TCP (Transmission Control Protocol):**
- Provides **reliable, ordered, error-checked** delivery of data.
- **Connection-oriented** — establishes a connection before sending data (3-way handshake: SYN → SYN-ACK → ACK).
- Used when data must arrive correctly: web browsing (HTTP), email (SMTP), file transfer (FTP).

**UDP (User Datagram Protocol):**
- Provides **fast, connectionless** communication.
- **No guarantee** of delivery, ordering, or error checking.
- Used when speed matters more than reliability: video streaming, online gaming, DNS queries, VoIP.

#### TCP vs UDP

| Feature | TCP | UDP |
|---------|-----|-----|
| **Connection** | Connection-oriented (3-way handshake) | Connectionless |
| **Reliability** | Guaranteed delivery with acknowledgments | No guarantee — "fire and forget" |
| **Ordering** | Data arrives in order | Data may arrive out of order |
| **Speed** | Slower (due to overhead) | Faster (minimal overhead) |
| **Use Cases** | Web, email, file transfer | Streaming, gaming, DNS, VoIP |
| **Header Size** | 20 bytes minimum | 8 bytes |

#### Where is it used?

Literally everywhere on the Internet:
- When you open a webpage → HTTP over TCP over IP
- When you watch YouTube → Video stream over UDP/TCP over IP
- When you send an email → SMTP over TCP over IP
- When you type a URL → DNS query over UDP over IP

#### 🔐 Security Perspective

TCP/IP was designed for **reliability, not security**. This creates vulnerabilities:
- **IP Spoofing:** Attacker forges the source IP address to impersonate another machine.
- **TCP SYN Flood:** Attacker sends thousands of SYN requests without completing the handshake, exhausting server resources (Denial of Service).
- **ARP Spoofing:** Attacker sends fake ARP messages to redirect traffic through their machine (Man-in-the-Middle).
- **DNS Poisoning:** Attacker corrupts DNS cache to redirect users to malicious websites.

**Countermeasures:** IPsec, TLS/SSL, firewalls, intrusion detection systems (IDS), VPNs.

---

### 9. Client-Server Model

#### What is it?

The **Client-Server Model** is a computing architecture where tasks are divided between two roles:
- **Server:** A powerful machine that provides services or resources (e.g., web server, database server, file server).
- **Client:** A machine (or application) that requests services from the server (e.g., your web browser, a mobile app).

The client initiates communication by sending a **request**, and the server processes it and sends back a **response**.

#### How does it work?

```
Client                          Server
  |                               |
  |--- Request (e.g., GET page) →|
  |                               | (processes request)
  |← Response (e.g., HTML page) --|
  |                               |
```

1. The server starts and **listens** on a specific port (e.g., port 80 for HTTP, port 443 for HTTPS).
2. The client **connects** to the server's IP address and port.
3. The client sends a **request** (e.g., "Give me the homepage").
4. The server **processes** the request (e.g., reads the HTML file, queries a database).
5. The server sends a **response** back to the client.
6. The client **displays** or uses the response.

#### Why do we use it?

- **Centralized Management:** Data and services are managed in one place (the server), making updates and backups easier.
- **Security:** Access control and authentication can be enforced at the server.
- **Scalability:** Servers can be upgraded or scaled independently of clients.
- **Resource Sharing:** Multiple clients can share the same resources (database, files, printer).

#### Where is it used?

- **Web:** Browser (client) ↔ Web Server (server)
- **Email:** Email client (Outlook, Gmail app) ↔ Mail Server
- **Databases:** Application ↔ Database Server (MySQL, PostgreSQL)
- **Gaming:** Game client ↔ Game Server
- **File Sharing:** Client ↔ FTP Server

#### Variations

| Architecture | Description | Example |
|-------------|-------------|---------|
| **2-Tier** | Client communicates directly with the server | Desktop app connecting to a database |
| **3-Tier** | Client → Application Server → Database Server | Web app (browser → backend → database) |
| **N-Tier** | Multiple specialized layers | Microservices architecture |
| **Peer-to-Peer** | No dedicated server — every node is both client and server | BitTorrent, Bitcoin |

#### 🔐 Security Perspective

The client-server model centralizes security at the server, but also creates a **single point of attack**:
- **DDoS Attacks:** Overwhelming the server with requests from many clients.
- **SQL Injection:** Malicious input from client to exploit a database server.
- **Session Hijacking:** Stealing a client's session token to impersonate them on the server.
- **Man-in-the-Middle:** Intercepting communication between client and server.

**Countermeasures:** HTTPS/TLS, input validation, rate limiting, Web Application Firewalls (WAF), session management best practices.

---

### 10. Remote Procedure Call (RPC)

#### What is it?

A **Remote Procedure Call (RPC)** is a protocol that allows a program on one computer to execute a procedure (function/method) on another computer over a network, **as if it were a local function call**. The programmer writes code that looks like a normal function call, but behind the scenes, the call is sent over the network to a remote machine, executed there, and the result is sent back.

#### How does it work?

```
Client Machine                          Server Machine
┌─────────────┐                        ┌──────────────┐
│ Application  │                        │ Server       │
│   ↓          │                        │ Function     │
│ Client Stub  │──── Network ──────────→│ Server Stub  │
│ (marshalling)│                        │(unmarshalling│
│              │←─── Network ───────────│  + execute)  │
│   ↓          │                        │              │
│ Result       │                        │              │
└─────────────┘                        └──────────────┘
```

**Step-by-step process:**

1. The client application calls a function (e.g., `add(3, 5)`).
2. The **client stub** intercepts this call and **marshals** (packs/serializes) the function name and parameters into a network message.
3. The message is sent over the network to the server.
4. The **server stub** receives the message and **unmarshals** (unpacks/deserializes) the parameters.
5. The server stub calls the actual function (`add(3, 5)`) on the server.
6. The result (`8`) is marshaled and sent back over the network to the client.
7. The client stub receives the result and returns it to the application.

#### Key Terms

- **Stub:** A piece of code that acts as a proxy. The client stub pretends to be the remote function; the server stub pretends to be the caller.
- **Marshalling (Serialization):** Converting function parameters into a format suitable for network transmission (e.g., binary or JSON).
- **Unmarshalling (Deserialization):** Converting the received network message back into usable parameters.

#### Why do we use RPC?

- **Simplicity:** Developers write function calls as if everything is local — the RPC system handles all the networking complexity.
- **Abstraction:** Hides the details of network communication, message formatting, and error handling.
- **Interoperability:** Allows programs written in different languages or running on different platforms to communicate.

#### Where is it used?

- **Microservices Communication:** Services within Netflix, Google, and Amazon communicate using RPC frameworks.
- **gRPC (Google RPC):** Modern, high-performance RPC framework used extensively in cloud services.
- **Sun RPC/ONC RPC:** Used in NFS (Network File System) for remote file access.
- **Windows DCOM/COM+:** Microsoft's distributed component model uses RPC.
- **XML-RPC and JSON-RPC:** Web-based RPC protocols.

#### Limitations of RPC

| Issue | Explanation |
|-------|-------------|
| **Network Failure** | Unlike local calls, RPC can fail due to network issues — the client may not know if the server received the request |
| **Latency** | Network calls are orders of magnitude slower than local function calls |
| **Partial Failure** | The server may crash after executing the function but before sending the response — did it succeed or not? |
| **Security** | Data travels over the network and can be intercepted or tampered with |

#### 🔐 Security Perspective

RPC is a significant attack vector in distributed systems:
- **Unauthorized RPC calls:** If the server doesn't authenticate the caller, anyone can invoke remote functions.
- **Data exposure:** Parameters and return values travel over the network in plaintext unless encrypted.
- **Buffer overflow:** Poorly implemented marshalling/unmarshalling can lead to buffer overflow vulnerabilities.
- **Replay attacks:** An attacker captures an RPC message and replays it to repeat an action (e.g., transferring money twice).

**Countermeasures:** Mutual TLS (mTLS), authentication tokens, input validation, encrypted channels, idempotent operations.

---

### 11. Processes

#### What is a Process?

A **process** is a **running instance of a program**. When you double-click an application (like a web browser or a text editor), the OS creates a process for it. The process includes:

- **Code (Text Segment):** The program's instructions.
- **Data Segment:** Global and static variables.
- **Heap:** Dynamically allocated memory (e.g., when you create objects at runtime).
- **Stack:** Function call stack, local variables, return addresses.
- **Process Control Block (PCB):** Metadata maintained by the OS — process ID (PID), state, CPU registers, memory maps, open files, etc.

#### Process States

A process goes through several states during its lifecycle:

```
        ┌──────────┐
 New ──→│  Ready   │←──────────────┐
        └────┬─────┘               │
             │ (scheduled)         │ (I/O complete
             ↓                     │  or event)
        ┌──────────┐          ┌────┴─────┐
        │ Running  │─────────→│ Waiting  │
        └────┬─────┘ (I/O     └──────────┘
             │        request)
             ↓
        ┌──────────┐
        │Terminated│
        └──────────┘
```

- **New:** Process is being created.
- **Ready:** Process is waiting for CPU time.
- **Running:** Process is actively executing on the CPU.
- **Waiting (Blocked):** Process is waiting for I/O or an event (e.g., reading a file, waiting for network data).
- **Terminated:** Process has finished execution.

#### Why are processes important in distributed systems?

- Each node in a distributed system runs multiple processes.
- **Process migration:** A process can be moved from one node to another for load balancing.
- **Inter-Process Communication (IPC):** Processes on different machines communicate via message passing, RPC, or shared files.
- **Fault tolerance:** If a process crashes on one node, it can be restarted on another.

#### Where do we see process management?

- **Web Servers:** Apache creates a new process for each client request (process-per-request model).
- **Operating Systems:** Every application you run is a process (check Task Manager on Windows or `ps` on Linux).
- **Distributed Computing:** MapReduce (Hadoop) creates processes across hundreds of machines to process big data.

---

### 12. Threads

#### What is a Thread?

A **thread** is a **lightweight unit of execution within a process**. While a process is a complete program in execution with its own memory space, a thread shares the process's memory and resources but has its own:

- **Thread ID**
- **Program Counter** (current instruction)
- **Register Set** (CPU state)
- **Stack** (local variables, function calls)

Multiple threads within the same process share:
- Code segment
- Data segment
- Heap memory
- Open files and other resources

#### Why use threads instead of processes?

| Advantage | Explanation |
|-----------|-------------|
| **Faster Creation** | Creating a thread is 10-100x faster than creating a process |
| **Lower Overhead** | Threads share memory, so no need for expensive inter-process communication |
| **Faster Context Switching** | Switching between threads of the same process is cheaper than switching between processes |
| **Better Resource Sharing** | Threads naturally share data through shared memory |
| **Parallelism** | On multi-core CPUs, threads can run truly in parallel |

#### Comparison: Processes vs Threads

| Feature | Process | Thread |
|---------|---------|--------|
| **Memory** | Own separate memory space | Shares memory with other threads in the same process |
| **Creation Time** | Slow (heavy) | Fast (lightweight) |
| **Communication** | IPC required (pipes, sockets, shared memory) | Direct access to shared variables |
| **Context Switch** | Expensive | Cheap |
| **Isolation** | Crash in one process doesn't affect others | Crash in one thread can crash the entire process |
| **Use Case** | Independent applications | Parallel tasks within one application |

#### Types of Threads

**a) User-Level Threads (ULT):**
- Managed by the application (user-space thread library), not the OS kernel.
- The OS sees only the process, not individual threads.
- Fast to create and switch, but if one thread blocks (e.g., I/O), the entire process blocks.
- **Examples:** Green threads in early Java, Python's threading module (limited by GIL).

**b) Kernel-Level Threads (KLT):**
- Managed directly by the OS kernel.
- The OS is aware of each thread and can schedule them independently.
- If one thread blocks, others can continue.
- Slower to create and switch (due to kernel involvement).
- **Examples:** POSIX Threads (pthreads) on Linux, Windows threads.

#### Where are threads used in distributed systems?

- **Web Servers:** Modern servers like Nginx and Tomcat use threads to handle multiple client requests concurrently (thread-per-request model).
- **RPC Servers:** Each incoming RPC request is handled by a separate thread.
- **Database Servers:** Multiple threads serve different client queries simultaneously.
- **Multithreaded Clients:** A web browser uses separate threads for rendering the page, downloading images, and running JavaScript.

#### 🔐 Security Perspective

Threads sharing memory is both powerful and dangerous:
- **Race Conditions:** If two threads access shared data simultaneously without proper synchronization, the result can be unpredictable — this can be exploited to bypass security checks.
- **Thread Safety Bugs:** A vulnerability in one thread can compromise the entire process (since all threads share the same memory space).
- **Side-Channel Attacks:** Techniques like Spectre exploit speculative execution across threads to leak sensitive data.

---

### 13. Mutual Exclusion

#### What is it?

**Mutual exclusion** is a fundamental concept in concurrent programming that ensures **only one process (or thread) can access a shared resource (critical section) at a time**. Without mutual exclusion, multiple processes accessing the same data simultaneously can lead to inconsistent or corrupted results.

#### What is a Critical Section?

A **critical section** is a block of code that accesses a shared resource (like a variable, file, or database record) that must not be accessed by more than one process at a time.

```
Process A:                    Process B:
  balance = read(account)       balance = read(account)
  balance = balance + 100       balance = balance - 50
  write(account, balance)       write(account, balance)
```

> **Problem (Race Condition):** If both processes read the balance ($1000) at the same time, Process A writes $1100, then Process B overwrites it with $950. The $100 deposit is lost! The correct answer should be $1050.

#### Why do we need mutual exclusion?

- **Data Consistency:** Prevent race conditions that corrupt shared data.
- **Correctness:** Ensure that operations on shared resources produce correct results.
- **Predictability:** Make the system behave deterministically despite concurrent access.

#### Requirements for a Mutual Exclusion Solution

1. **Safety (Mutual Exclusion):** At most one process can be in the critical section at any time.
2. **Liveness (Progress):** If no process is in the critical section and some process wants to enter, it must eventually be allowed.
3. **Fairness (Bounded Waiting):** No process should wait forever to enter the critical section (no starvation).

#### Approaches to Mutual Exclusion in Distributed Systems

**a) Centralized Approach:**
- One node is elected as the **coordinator**.
- Any process wanting to enter the critical section sends a request to the coordinator.
- The coordinator grants permission to one process at a time.
- **Pros:** Simple, easy to implement.
- **Cons:** Single point of failure — if the coordinator crashes, the system is stuck.

**b) Distributed Approach (Ricart-Agrawala Algorithm):**
- A process wanting to enter the critical section sends a request to **all** other processes.
- It waits for **OK** replies from every other process.
- If another process is already in the critical section (or wants to enter with a higher priority), it defers its reply.
- **Pros:** No single point of failure.
- **Cons:** High message overhead — requires 2(n-1) messages per critical section entry.

**c) Token-Based Approach (Token Ring):**
- A special **token** circulates among processes in a logical ring.
- Only the process holding the token can enter the critical section.
- After finishing, it passes the token to the next process.
- **Pros:** Simple, fair (every process gets a turn).
- **Cons:** If the token is lost (e.g., the holding process crashes), a new token must be regenerated.

#### Comparison of Approaches

| Approach | Messages per Entry | Single Point of Failure | Fairness |
|----------|-------------------|------------------------|----------|
| **Centralized** | 3 (request, grant, release) | Yes (coordinator) | Depends on coordinator |
| **Distributed** | 2(n-1) | No | Yes (timestamp-based) |
| **Token Ring** | 1 to n-1 | Yes (token loss) | Yes (round-robin) |

#### 🔐 Security Perspective

Mutual exclusion is critical for security:
- **TOCTOU Attacks (Time-of-Check to Time-of-Use):** An attacker exploits the gap between checking a condition and acting on it. Proper mutual exclusion prevents this.
- **Privilege Escalation:** Race conditions in OS code can allow an attacker to gain unauthorized access.
- **Secure Resource Access:** Mutual exclusion ensures that cryptographic keys, authentication tokens, and audit logs are accessed atomically.

---

### 14. Deadlocks

#### What is a Deadlock?

A **deadlock** is a situation where two or more processes are **permanently blocked**, each waiting for a resource that another process holds. None of them can proceed — they're stuck forever.

> **Real-world analogy:** Four cars arrive at a 4-way intersection simultaneously, and each waits for the car on its right to go first. Nobody moves. Ever.

#### Another Example

```
Process A holds Resource 1 and wants Resource 2.
Process B holds Resource 2 and wants Resource 1.

Process A: "I'll release Resource 1 after I get Resource 2."
Process B: "I'll release Resource 2 after I get Resource 1."

Result: Both wait forever → DEADLOCK
```

#### Four Necessary Conditions for Deadlock (Coffman Conditions)

**All four** conditions must hold simultaneously for a deadlock to occur:

| Condition | Description | Example |
|-----------|-------------|---------|
| **1. Mutual Exclusion** | At least one resource is non-shareable (only one process can use it at a time) | A printer can only print one document at a time |
| **2. Hold and Wait** | A process holds at least one resource and is waiting to acquire additional resources | Process A holds the printer and waits for the scanner |
| **3. No Preemption** | Resources cannot be forcibly taken away from a process; they must be released voluntarily | The OS cannot take the printer away from Process A |
| **4. Circular Wait** | A circular chain of processes exists, where each process waits for a resource held by the next process in the chain | A waits for B's resource, B waits for C's resource, C waits for A's resource |

> **Key insight:** If you can **break any one** of these four conditions, you can prevent deadlock.

#### Deadlock Handling Strategies

**a) Deadlock Prevention:**
- Design the system so that at least one of the four Coffman conditions can never occur.
- **Break Mutual Exclusion:** Make resources shareable (not always possible).
- **Break Hold and Wait:** Require processes to request all resources at once before starting (inefficient but safe).
- **Break No Preemption:** Allow the OS to forcibly take resources from a process (can cause data corruption if not handled carefully).
- **Break Circular Wait:** Impose a global ordering on resources — processes must request resources in a fixed order.

**b) Deadlock Avoidance:**
- Use algorithms to dynamically check whether granting a resource request could lead to a deadlock.
- **Banker's Algorithm:** Before granting a request, the system checks if a "safe state" can be maintained. If yes, grant the request; if no, make the process wait.
- Requires advance knowledge of each process's maximum resource needs.

**c) Deadlock Detection and Recovery:**
- Allow deadlocks to occur, but periodically check for them and recover.
- **Detection:** Build a **Resource Allocation Graph (RAG)** or **Wait-For Graph (WFG)**. If the graph contains a cycle, a deadlock exists.
- **Recovery options:**
  - **Kill one or more processes** involved in the deadlock.
  - **Roll back** a process to a previous checkpoint and restart it.
  - **Preempt resources** from one process and give them to another.

**d) Deadlock Ignorance (Ostrich Algorithm):**
- Simply ignore the problem and hope it doesn't happen.
- Used when deadlocks are extremely rare and the cost of prevention/detection is too high.
- **Surprisingly, this is what most general-purpose OSes do** (including Linux and Windows) for application-level deadlocks.

#### Deadlocks in Distributed Systems

Deadlocks are **harder to detect** in distributed systems because:
- Resources and processes are spread across multiple machines.
- There's no global view of the system — no single machine knows the state of all resources.
- Communication delays mean that the information used for detection may be outdated.

**Distributed Deadlock Detection approaches:**
- **Centralized Detection:** One coordinator collects information from all nodes and checks for cycles. (Single point of failure.)
- **Distributed Detection:** Each node maintains a local Wait-For Graph. Nodes exchange information to detect global cycles. (More complex but more robust.)
- **Hierarchical Detection:** Nodes are organized into a hierarchy; detection happens at multiple levels.

#### 🔐 Security Perspective

Deadlocks can be **weaponized** as a form of Denial of Service (DoS):
- An attacker deliberately creates conditions that cause deadlocks in a server, making it unresponsive.
- **Resource Exhaustion Attacks:** An attacker acquires and holds critical resources (file handles, database connections, locks) to cause other processes to deadlock.
- **Distributed DoS via Deadlock:** In a distributed transaction system, an attacker could manipulate transaction ordering to cause cross-node deadlocks.

**Countermeasures:** Timeouts on resource requests, deadlock detection daemons, resource quotas, and monitoring for abnormal resource holding patterns.

---

## Summary Table: All Topics at a Glance

| # | Topic | What | Why | Where |
|---|-------|------|-----|-------|
| 1 | **Distributed System** | Collection of independent networked computers working as one | Scalability, reliability, resource sharing | Internet, cloud, banking |
| 2 | **Characteristics** | No shared clock/memory, concurrency, transparency, fault tolerance | Defines what makes a system "distributed" | Design principles for all distributed systems |
| 3 | **Hardware Concepts** | Multiprocessors (shared memory) vs Multicomputers (message passing) | Determines communication model | Servers, supercomputers, the Internet |
| 4 | **Software Concepts** | Tightly coupled (DOS) vs Loosely coupled (NOS) vs Middleware | Determines user experience and management model | Research OS, corporate networks, cloud platforms |
| 5 | **Distributed OS** | Single OS managing multiple computers as one | True transparency and unified management | Research (Amoeba), concepts in Kubernetes |
| 6 | **Network OS** | Each machine has its own OS, connected via network | Simpler, supports heterogeneous machines | Corporate and university networks |
| 7 | **Layered Protocols** | Organizing communication into layers (OSI, TCP/IP) | Modularity, abstraction, standardization | All network communication |
| 8 | **TCP/IP Suite** | Practical protocol suite of the Internet | Standard, reliable, platform-independent | Every Internet-connected device |
| 9 | **Client-Server** | Clients request, servers respond | Centralized management, security, scalability | Web, email, databases, gaming |
| 10 | **RPC** | Call a function on a remote machine as if it were local | Simplifies distributed programming | Microservices, gRPC, NFS |
| 11 | **Processes** | A running instance of a program | Isolation, resource management | Every application on every OS |
| 12 | **Threads** | Lightweight execution unit within a process | Concurrency, performance, resource sharing | Web servers, databases, browsers |
| 13 | **Mutual Exclusion** | Only one process accesses a critical section at a time | Prevents race conditions and data corruption | Databases, file systems, distributed locks |
| 14 | **Deadlocks** | Processes stuck waiting for each other forever | Understanding prevents system hangs | OS resource management, distributed transactions |

---

*Module 1 — Theory Notes — Prepared for M.Tech Cyber Security Students*
