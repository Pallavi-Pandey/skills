# Lab 03 Solution — TCP/UDP Sockets + Custom Protocol

Instructor-facing answer key for [`labs/lab_03_tcp_ip_sockets/`](../../labs/lab_03_tcp_ip_sockets/). See that lab's README for the full explanation — this file only has the commands to run the completed solution.

```bash
# 1. Start the 2 Python containers
cd module_1/docker/
docker compose -f network-setup.yml up -d python-node1 python-node2

# 2. Part 1 — TCP echo server
docker exec -it ds-python-node1 python3 /app/solutions/lab_03_solution/tcp_echo.py --mode server
docker exec -it ds-python-node2 python3 /app/solutions/lab_03_solution/tcp_echo.py --mode client --host node1

# 3. Part 2 — UDP blaster (start the receiver FIRST)
docker exec -it ds-python-node1 python3 /app/solutions/lab_03_solution/udp_blaster.py --mode receiver
docker exec -it ds-python-node2 python3 /app/solutions/lab_03_solution/udp_blaster.py --mode sender --host node1 --count 1000

# 4. Part 3 — custom binary protocol
docker exec -it ds-python-node1 python3 /app/solutions/lab_03_solution/custom_protocol.py --mode server
docker exec -it ds-python-node2 python3 /app/solutions/lab_03_solution/custom_protocol.py --mode client --host node1
```
