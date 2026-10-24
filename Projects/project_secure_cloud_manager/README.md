# Mini Project: Secure Cloud VM Manager

> **Level:** Beginner | **Time:** 60–90 minutes | **Language:** Python 3.9+ | **Dependencies:** None

Build and run a tiny cloud-control-plane simulation. A client connects to a server, signs in, and asks it to create, list, or delete virtual machines. The server tracks a small CPU/memory pool, protects shared state with a lock, checks a user's role, and writes tamper-evident audit records.

This is deliberately a simulation: it does **not** create real virtual machines or encrypt network traffic. It makes the concepts visible without requiring Docker, a cloud account, or a hypervisor.

## Docker Version

For the same project with the server and each client running in separate Docker containers on an isolated virtual network, use [the containerized version](../project_secure_cloud_manager_docker/README.md).

## Project Statement

Create a small **Secure Cloud VM Manager** in Python. The program must simulate the control plane of a cloud provider: authenticated users connect to a central server and request virtual machines with CPU and memory. The server must allocate only the resources it has, protect shared state when several clients connect, enforce what each user is allowed to do, and record security-relevant actions in an audit log.

The aim is not to build a real cloud platform. The aim is to demonstrate how the ideas from distributed systems, security, virtualization, and cloud resource management fit together in one understandable program.

## What You Need to Do

Complete and demonstrate the following requirements.

| # | Requirement | Where it is implemented |
|---|---|---|
| 1 | Run a TCP server that accepts more than one client. | `cloud_server.py` |
| 2 | Define a simple JSON request/response protocol. | `cloud_server.py`, `cloud_client.py` |
| 3 | Authenticate users with the supplied demo accounts. | `login` action |
| 4 | Issue a session token after a successful login; require it for later requests. | `CloudManager.login()` and `_identity()` |
| 5 | Let a logged-in user create a VM with a name, CPU count, and memory size. | `create` command |
| 6 | Reject requests when CPU or memory capacity is exhausted. | `create_vm()` |
| 7 | Protect VM allocation/deletion with a lock so concurrent clients cannot corrupt the resource pool. | `self.lock` |
| 8 | Let regular users list only their own VMs. | `list` command |
| 9 | Let only an administrator delete VMs and read audit events. | `delete` and `audit` commands |
| 10 | Record logins, VM creation/deletion, and denied actions in an audit log. | `_audit()` |
| 11 | Attach an HMAC to each audit record and verify the audit log before displaying it. | `verify_audit_log()` |
| 12 | Demonstrate the system with at least one user and one administrator session. | Terminal output / screenshots |

## Minimum Demonstration

Your final demonstration should show these four scenarios:

1. Log in as `alice`, create a VM, and list it.
2. Attempt `delete study-vm` as `alice`; the server must deny it.
3. Log in as `admin`, list or delete the VM, and view the audit log.
4. Start two clients and submit VM-creation requests close together. Explain that the server lock protects the shared CPU/memory allocation.

## Deliverables

Submit or show:

- `cloud_server.py` and `cloud_client.py`.
- A short README containing the run commands and demo credentials.
- A terminal transcript or screenshots of the four required scenarios.
- A brief explanation (about one paragraph each) of: authentication vs authorization; why the lock is necessary; and what the HMAC adds to the audit log.

## What this connects

| Earlier module | Idea used here |
|---|---|
| Module 1 | TCP client-server communication, a simple request protocol, one thread per client, and a lock around shared state |
| Module 2 | Authentication, role-based authorization, resource quotas/availability, integrity with HMAC, and audit logging |
| Module 3 | VM resource allocation, lifecycle states, CPU/memory management, and a cloud control plane |

## Run it

Open two terminals in this directory.

```bash
# Terminal 1: start the cloud controller
python3 cloud_server.py

# Terminal 2: connect as a regular user
python3 cloud_client.py
```

At the prompts, use either account below. These credentials are intentionally hard-coded for the exercise — never do this in a real system.

| User | Password | Role | Permissions |
|---|---|---|---|
| `alice` | `alice123` | user | Create and list her own VMs |
| `admin` | `admin123` | admin | Create, list, delete any VM, view audit records |

Example regular-user session:

```text
Username: alice
Password: alice123
cloud> create study-vm 1 512
Created study-vm: 1 CPU, 512 MB memory
cloud> list
study-vm  owner=alice  state=running  cpu=1  memory=512MB
cloud> quit
```

Try `help` at the `cloud>` prompt. To test concurrency, start two clients and create VMs at the same time. The server's `threading.Lock` prevents both requests from allocating the same capacity.

## Commands

| Command | Description |
|---|---|
| `list` | List visible virtual machines |
| `create NAME CPU MEMORY_MB` | Create a running VM; regular users own their own VM |
| `delete NAME` | Delete a VM (admin only) |
| `audit` | Show the audit log (admin only) |
| `help` / `quit` | Show commands / leave |

## Things to notice

1. The client/server protocol uses one JSON message per line. JSON makes request fields explicit, just as an RPC interface does.
2. The server authenticates first and returns a random session token. Every later command includes that token.
3. The server, not the client, enforces ownership and administrator permissions. This is authorization, not merely hiding a command in the client UI.
4. Every important event is stored with an HMAC. `verify_audit_log()` checks whether someone edited an old record without the secret key.
5. The project has no TLS, password hashing, durable database, rate limiting, or production-grade session management. Those are intentional simplifications, and excellent next improvements.

## Suggested extensions

- Add a `stop NAME` command and model the `stopped` lifecycle state.
- Persist VMs and audit events to a JSON file, then discuss secure storage and recovery.
- Add CPU and memory quotas per user.
- Run the server/client in separate Module 1 Docker containers.
- Replace the plaintext demo login with TLS, password hashes, and a real identity provider.
