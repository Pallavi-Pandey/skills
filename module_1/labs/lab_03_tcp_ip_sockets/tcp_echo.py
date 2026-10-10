"""
Lab 03 - TCP Echo Server (Starter Code)
========================================
A TCP echo server that returns messages in UPPERCASE.

Fill in the TODOs.
"""

# What each import is for (docs link = where to read more):
#   socket     -> low-level TCP networking for both the echo server and
#                 the client that talks to it
#                 docs: https://docs.python.org/3/library/socket.html
#   threading  -> lets the server handle each connected client on its
#                 own thread instead of one at a time
#                 docs: https://docs.python.org/3/library/threading.html
#   argparse   -> reads --mode/--host/--port from the command line
#                 docs: https://docs.python.org/3/library/argparse.html
import socket
import threading
import argparse


def run_server(host="0.0.0.0", port=7000):
    """TCP Echo Server — echoes messages back in UPPERCASE."""
    # TODO: Create a TCP socket (AF_INET, SOCK_STREAM)
    # TODO: Set SO_REUSEADDR
    # TODO: Bind to (host, port)
    # TODO: Listen with backlog=5
    
    print(f"TCP Echo Server listening on {host}:{port}")
    
    # TODO: In a loop:
    #   - Accept a connection (conn, addr)
    #   - Print "[+] Connected: {addr}"
    #   - Spawn a thread to handle_echo(conn, addr)
    pass


def handle_echo(conn, addr):
    """Handle a single client: read message, echo UPPERCASE."""
    try:
        while True:
            # TODO: Receive up to 1024 bytes
            # TODO: If no data, break
            # TODO: Decode to string, convert to UPPERCASE
            # TODO: Send the uppercased message back
            # TODO: Print what was received and what was sent back
            pass
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")


def run_client(host, port=7000):
    """TCP Echo Client — sends messages, receives echoes."""
    # TODO: Create a TCP socket
    # TODO: Connect to (host, port)
    
    print(f"Connected to {host}:{port}. Type messages (Ctrl+C to quit):")
    
    try:
        while True:
            msg = input("> ")
            if not msg:
                continue
            # TODO: Send the message (encoded)
            # TODO: Receive the echo (up to 1024 bytes)
            # TODO: Print the response
            pass
    except (KeyboardInterrupt, EOFError):
        print("\nDisconnected.")
    finally:
        # TODO: Close the socket
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Echo Server/Client")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--host", default="localhost", help="Server host (client mode)")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port)
    else:
        run_client(args.host, args.port)
