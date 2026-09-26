"""Lab 03 - UDP Blaster (SOLUTION)"""
import socket
import argparse
import time


def run_receiver(host="0.0.0.0", port=7001, timeout=5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.settimeout(timeout)
    print(f"UDP Receiver on {host}:{port} (timeout={timeout}s)")

    received = 0
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            received += 1
            if received % 100 == 0:
                print(f"  Received {received} messages so far...")
    except socket.timeout:
        pass

    print(f"\n{'='*40}")
    print(f"Total messages received: {received}")
    print(f"{'='*40}")
    sock.close()


def run_sender(host, port=7001, count=1000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending {count} UDP messages to {host}:{port}...")

    start = time.perf_counter()
    for i in range(count):
        msg = f"MSG-{i:05d}".encode("utf-8")
        sock.sendto(msg, (host, port))
    elapsed = time.perf_counter() - start

    print(f"Sent {count} messages in {elapsed:.3f}s ({count/elapsed:.0f} msgs/sec)")
    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["receiver", "sender"], required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7001)
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()

    if args.mode == "receiver":
        run_receiver(port=args.port)
    else:
        run_sender(args.host, args.port, args.count)
