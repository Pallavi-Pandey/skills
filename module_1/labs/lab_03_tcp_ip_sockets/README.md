# Lab 03: TCP/UDP Socket Programming

> **Time:** 35 minutes | **Language:** Python | **Infrastructure:** Docker

## Objective
Build TCP and UDP servers from raw sockets. Understand the difference by measuring packet loss.

## Part 1: TCP Echo Server (15 min)

Open `tcp_echo.py` — fill in the TODOs to build a TCP echo server that:
1. Accepts a client connection
2. Reads messages
3. Echoes them back in UPPERCASE

```bash
# Server
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode server

# Client
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/tcp_echo.py --mode client --host node1
```

## Part 2: UDP Message Blaster (10 min)

Open `udp_blaster.py` — send 1000 UDP messages and count how many arrive:

```bash
# Receiver
docker exec -it ds-python-node1 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode receiver

# Sender
docker exec -it ds-python-node2 python3 /app/labs/lab_03_tcp_ip_sockets/udp_blaster.py --mode sender --host node1 --count 1000
```

**Expected:** Some messages will be lost! That's UDP — best effort.

## Part 3: Custom Binary Protocol (10 min)

Open `custom_protocol.py` — implement a simple protocol:
```
[MSG_TYPE: 1 byte] [LENGTH: 2 bytes big-endian] [PAYLOAD: N bytes]

MSG_TYPE:
  0x01 = PING
  0x02 = PONG
  0x03 = DATA
  0x04 = ERROR
```

## Checkpoint
- How many UDP messages out of 1000 arrived?
- What happens if you send a 10MB file over UDP vs TCP?
- Why does TCP need a 3-way handshake but UDP doesn't?
