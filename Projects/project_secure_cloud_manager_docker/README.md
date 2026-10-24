# Docker Project: Containerized Secure Cloud VM Manager

> **Level:** Beginner | **Prerequisite:** Docker Desktop / Docker Engine with Docker Compose

This is the Docker version of the [Secure Cloud VM Manager](../project_secure_cloud_manager/README.md). It uses the same Python application, but runs the **cloud controller** and every **user client** in separate containers. Docker Compose creates a private bridge network named `cloud-control-network`, and the client reaches the server by its service name, `cloud-server`.

It is a local cloud-style environment, not an AWS/Azure/GCP deployment. The goal is to make Module 1's networked client-server model and Module 3's virtual networking visible in a simple, safe setup.

## Architecture

```text
client container ─┐
                  ├── cloud-control-network ── cloud-server container
client container ─┘                                │
                                                    └── VM/resource simulation
```

- The **cloud-server** container owns the shared VM inventory, capacity checks, sessions, and audit log.
- Each **cloud-client** container represents an independent user.
- Compose service discovery resolves `cloud-server` to the server container's IP address; no hard-coded container IP is needed.
- The host port `5050` is exposed only for optional host-side testing. The normal project flow uses the internal Docker network.

## Run the Project

From this directory:

```bash
# Build the shared image and start the controller in the background.
docker compose up --build -d cloud-server

# Follow the server log (optional).
docker compose logs -f cloud-server
```

Open a second terminal in the same directory and start a user client:

```bash
docker compose run --rm cloud-client
```

Use a demo account:

| User | Password | Role |
|---|---|---|
| `alice` | `alice123` | User: create/list her VMs |
| `admin` | `admin123` | Administrator: delete VMs and view audits |

Example:

```text
Username: alice
Password: alice123
cloud> create docker-vm 1 512
Created docker-vm: 1 CPU, 512 MB memory
cloud> list
docker-vm  owner=alice  state=running  cpu=1  memory=512MB
```

Start a second client in another terminal to observe concurrent requests:

```bash
docker compose run --rm cloud-client
```

When finished, remove the containers and the Compose network:

```bash
docker compose down
```

## What to Demonstrate

1. Start `cloud-server` and connect as `alice` from a separate container.
2. Create and list a VM. Explain that the request travels through Docker's bridge network to a service name, not `localhost`.
3. Run another client concurrently; create VMs until the simulated 4 CPU / 4096 MB pool is exhausted.
4. Try `delete docker-vm` as `alice`; authorization must deny it.
5. Start an `admin` client, run `audit`, and show that the audit log integrity check is `OK`.

## Files

| File | Purpose |
|---|---|
| `Dockerfile` | Builds a small Python image containing the shared project code. |
| `docker-compose.yml` | Defines the server, on-demand client, port mapping, and isolated bridge network. |
| `../project_secure_cloud_manager/` | Shared application source; `CLOUD_HOST` / `CLOUD_PORT` make it work both locally and in containers. |

## Important Limits

The server state is in memory: restarting `cloud-server` clears VMs, sessions, and audit records. The example also has no TLS, persistent database, secrets manager, or real cloud provider integration. Those are suitable next steps after the containerized version works.
