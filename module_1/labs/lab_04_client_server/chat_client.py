"""
Lab 04 - Chat Client (Starter Code)
=====================================
Connects to the chat server and allows sending/receiving messages.

Fill in the TODOs.
"""

import socket
import threading
import argparse
import sys


def receive_messages(sock):
    """Background thread: continuously receive and print messages."""
    try:
        while True:
            # TODO: Receive up to 1024 bytes from sock
            # TODO: If no data, break (server disconnected)
            # TODO: Decode and print the message
            pass
    except (ConnectionResetError, OSError):
        print("\nDisconnected from server.")
        sys.exit(0)


def main(host, port, nickname):
    """Connect to chat server and start chatting."""
    # TODO: Create a TCP socket
    # TODO: Connect to (host, port)
    
    # TODO: Send nickname as the first message
    
    print(f"Connected to {host}:{port} as '{nickname}'")
    print("Type your messages (Ctrl+C to quit):\n")
    
    # TODO: Start a background thread running receive_messages(sock)
    # Hint: Set daemon=True so it dies when main thread exits
    
    try:
        while True:
            msg = input()
            if msg:
                # TODO: Send the message to the server
                pass
    except (KeyboardInterrupt, EOFError):
        print("\nLeaving chat...")
    finally:
        # TODO: Close the socket
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument("--host", default="localhost", help="Server hostname")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--name", default="Anonymous", help="Your nickname")
    args = parser.parse_args()

    main(args.host, args.port, args.name)
