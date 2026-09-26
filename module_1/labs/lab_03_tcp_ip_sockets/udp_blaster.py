"""
Lab 03 - UDP Message Blaster (Starter Code)
============================================
Send N UDP messages and count how many arrive.
Demonstrates UDP's unreliable, best-effort delivery.

Fill in the TODOs.
"""

import socket
import argparse
import time


def run_receiver(host="0.0.0.0", port=7001, timeout=5):
    """Receive UDP messages and count them."""
    # TODO: Create a UDP socket (AF_INET, SOCK_DGRAM)
    # TODO: Bind to (host, port)
    # TODO: Set a timeout (so it stops after `timeout` seconds of silence)
    
    print(f"UDP Receiver listening on {host}:{port}")
    print(f"Will stop after {timeout}s of silence...")
    
    received = 0
    try:
        while True:
            # TODO: recvfrom(1024) to receive data
            # TODO: Increment received counter
            # TODO: Every 100 messages, print progress
            pass
    except socket.timeout:
        pass
    
    print(f"\n{'='*40}")
    print(f"Total messages received: {received}")
    print(f"{'='*40}")


def run_sender(host, port=7001, count=1000):
    """Blast N UDP messages as fast as possible."""
    # TODO: Create a UDP socket (AF_INET, SOCK_DGRAM)
    
    print(f"Sending {count} UDP messages to {host}:{port}...")
    start = time.perf_counter()
    
    for i in range(count):
        msg = f"MSG-{i:05d}".encode("utf-8")
        # TODO: sendto(msg, (host, port))
        pass
    
    elapsed = time.perf_counter() - start
    print(f"Sent {count} messages in {elapsed:.3f}s")
    print(f"Rate: {count/elapsed:.0f} msgs/sec")
    print(f"\nNow check the receiver — did all {count} arrive?")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UDP Message Blaster")
    parser.add_argument("--mode", choices=["receiver", "sender"], required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7001)
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()

    if args.mode == "receiver":
        run_receiver(port=args.port)
    else:
        run_sender(args.host, args.port, args.count)
