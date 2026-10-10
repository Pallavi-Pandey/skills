"""
Lab 01 - Benchmark Tool
========================
Benchmarks centralized and distributed KV stores.
Measures throughput (ops/sec) and latency (p50, p99).
"""

# What each import is for (docs link = where to read more):
#   socket      -> opens a fresh connection per command, to measure the
#                  round-trip time of a single SET/GET
#                  docs: https://docs.python.org/3/library/socket.html
#   time        -> time.perf_counter() times each operation precisely,
#                  so throughput/latency numbers are accurate
#                  docs: https://docs.python.org/3/library/time.html
#   argparse    -> reads --host/--port/--distributed/--nodes/--ops from
#                  the command line
#                  docs: https://docs.python.org/3/library/argparse.html
#   statistics  -> statistics.mean() computes average latency from a
#                  list of individual timings
#                  docs: https://docs.python.org/3/library/statistics.html
#   random      -> generates random keys/values so each benchmark run
#                  uses fresh, non-repeating data
#                  docs: https://docs.python.org/3/library/random.html
#   string      -> supplies the character sets (letters, digits) that
#                  random.choices() picks from
#                  docs: https://docs.python.org/3/library/string.html
import socket
import time
import argparse
import statistics
import random
import string


def random_key():
    return "".join(random.choices(string.ascii_lowercase, k=8))


def random_value():
    return "".join(random.choices(string.ascii_letters + string.digits, k=20))


def send_command(host, port, command):
    """Send a command and measure round-trip time."""
    start = time.perf_counter()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect((host, port))
        sock.sendall((command + "\n").encode("utf-8"))
        response = sock.recv(1024).decode("utf-8").strip()
        elapsed = time.perf_counter() - start
        return response, elapsed
    except Exception as e:
        elapsed = time.perf_counter() - start
        return f"ERROR: {e}", elapsed
    finally:
        sock.close()


def benchmark_centralized(host, port, num_ops=500):
    """Benchmark a single centralized server."""
    print(f"\n{'='*60}")
    print(f"  CENTRALIZED BENCHMARK — {host}:{port}")
    print(f"  Operations: {num_ops} SETs + {num_ops} GETs")
    print(f"{'='*60}\n")

    # --- SET benchmark ---
    set_latencies = []
    keys = []
    for i in range(num_ops):
        key = random_key()
        value = random_value()
        keys.append(key)
        _, latency = send_command(host, port, f"SET {key} {value}")
        set_latencies.append(latency)

    # --- GET benchmark ---
    get_latencies = []
    for key in keys:
        _, latency = send_command(host, port, f"GET {key}")
        get_latencies.append(latency)

    # --- Report ---
    print_report("SET", set_latencies, num_ops)
    print_report("GET", get_latencies, num_ops)


def benchmark_distributed(nodes_str, num_ops=500):
    """Benchmark a distributed cluster (round-robin across nodes)."""
    nodes = []
    for n in nodes_str.split(","):
        host, port = n.split(":")
        nodes.append((host, int(port)))

    print(f"\n{'='*60}")
    print(f"  DISTRIBUTED BENCHMARK — {len(nodes)} nodes")
    print(f"  Operations: {num_ops} SETs + {num_ops} GETs")
    print(f"{'='*60}\n")

    # --- SET benchmark (round-robin across nodes) ---
    set_latencies = []
    keys = []
    for i in range(num_ops):
        key = random_key()
        value = random_value()
        keys.append(key)
        host, port = nodes[i % len(nodes)]
        _, latency = send_command(host, port, f"SET {key} {value}")
        set_latencies.append(latency)

    # --- GET benchmark ---
    get_latencies = []
    for i, key in enumerate(keys):
        host, port = nodes[i % len(nodes)]
        _, latency = send_command(host, port, f"GET {key}")
        get_latencies.append(latency)

    print_report("SET", set_latencies, num_ops)
    print_report("GET", get_latencies, num_ops)


def print_report(op_name, latencies, num_ops):
    """Print a formatted benchmark report."""
    total_time = sum(latencies)
    throughput = num_ops / total_time if total_time > 0 else 0
    sorted_lat = sorted(latencies)
    p50 = sorted_lat[int(len(sorted_lat) * 0.50)] * 1000
    p99 = sorted_lat[int(len(sorted_lat) * 0.99)] * 1000
    avg = statistics.mean(latencies) * 1000

    print(f"  {op_name} Results:")
    print(f"    Throughput:   {throughput:>8.1f} ops/sec")
    print(f"    Avg Latency:  {avg:>8.2f} ms")
    print(f"    p50 Latency:  {p50:>8.2f} ms")
    print(f"    p99 Latency:  {p99:>8.2f} ms")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="KV Store Benchmark")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=5000, help="Server port")
    parser.add_argument("--distributed", action="store_true", help="Benchmark distributed mode")
    parser.add_argument("--nodes", default="node1:5000,node2:5000,node3:5000",
                        help="Comma-separated node list for distributed mode")
    parser.add_argument("--ops", type=int, default=500, help="Number of operations")
    args = parser.parse_args()

    if args.distributed:
        benchmark_distributed(args.nodes, args.ops)
    else:
        benchmark_centralized(args.host, args.port, args.ops)
