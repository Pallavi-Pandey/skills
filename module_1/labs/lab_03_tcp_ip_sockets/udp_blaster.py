"""
Lab 03 - UDP Message Blaster
Send N UDP messages and count how many arrive.
Demonstrates UDP's best-effort delivery.
"""

import socket
import argparse
import time


def run_receiver(host="0.0.0.0", port=7001, timeout=30):
    """Receive UDP messages and count them."""
    receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver.bind((host, port))
    receiver.settimeout(timeout)

    print(f"UDP Receiver listening on {host}:{port}")
    print(f"Will stop after {timeout}s of silence...")

    received = 0

    try:
        while True:
            data, address = receiver.recvfrom(1024)
            received += 1

            if received % 100 == 0:
                print(f"Received {received} messages so far")

    except socket.timeout:
        pass
    except KeyboardInterrupt:
        print("\nReceiver stopped manually.")
    finally:
        receiver.close()

    print(f"\n{'=' * 40}")
    print(f"Total messages received: {received}")
    print(f"{'=' * 40}")


def run_sender(host, port=7001, count=1000):
    """Send N UDP messages as fast as possible."""
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print(f"Sending {count} UDP messages to {host}:{port}...")
    start = time.perf_counter()

    try:
        for i in range(count):
            msg = f"MSG-{i:05d}".encode("utf-8")
            sender.sendto(msg, (host, port))
    finally:
        sender.close()

    elapsed = time.perf_counter() - start

    print(f"Sent {count} messages in {elapsed:.3f}s")
    print(f"Rate: {count / elapsed:.0f} msgs/sec")
    print(f"\nCheck the receiver to see how many arrived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Message Blaster")
    parser.add_argument(
        "--mode", choices=["receiver", "sender"], required=True
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7001)
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()

    if args.mode == "receiver":
        run_receiver(port=args.port)
    else:
        run_sender(args.host, args.port, args.count)
