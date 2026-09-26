"""
Lab 02 - NOS Simulation (Starter Code)
=======================================
Simulates a Network OS: explicit file sharing over TCP.
No transparency — you must know which node has the file.

Fill in the TODOs.
"""

import socket
import threading
import argparse
import os

SHARED_DIR = "/shared"


class NOSFileServer:
    """A simple TCP file server — serves files from SHARED_DIR."""

    def __init__(self, host="0.0.0.0", port=6000):
        self.host = host
        self.port = port

    def handle_client(self, conn, addr):
        try:
            filename = conn.recv(1024).decode("utf-8").strip()
            filepath = os.path.join(SHARED_DIR, filename)

            if os.path.exists(filepath):
                # TODO: Read the file contents
                # TODO: Send the contents back over the connection
                pass
            else:
                conn.sendall(b"ERROR: File not found\n")
        finally:
            conn.close()

    def start(self):
        # Create a sample file so there's something to serve
        os.makedirs(SHARED_DIR, exist_ok=True)
        with open(os.path.join(SHARED_DIR, "test.txt"), "w") as f:
            f.write(f"Hello from the NOS file server! PID={os.getpid()}\n")
            f.write("This file lives on a specific node.\n")
            f.write("You had to know which node to ask. That's NOS.\n")

        # TODO: Create a TCP socket, bind, listen
        # TODO: Accept connections in a loop, spawn threads
        pass


class NOSFileClient:
    """Explicitly requests a file from a known server."""

    def __init__(self, server_host, server_port=6000):
        self.server_host = server_host
        self.server_port = server_port

    def get_file(self, filename):
        """Request a file from the server."""
        # TODO: Create a TCP socket
        # TODO: Connect to (self.server_host, self.server_port)
        # TODO: Send the filename
        # TODO: Receive and print the response
        # NOTE: You MUST know the server address. That's the NOS experience.
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NOS File Sharing Simulation")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--server", default="node1", help="Server hostname (client mode)")
    parser.add_argument("--file", default="test.txt", help="File to request (client mode)")
    args = parser.parse_args()

    if args.mode == "server":
        print("=== NOS File Server ===")
        print(f"Serving files from {SHARED_DIR}")
        server = NOSFileServer()
        server.start()
    else:
        print(f"=== NOS File Client ===")
        print(f"Requesting '{args.file}' from {args.server}")
        client = NOSFileClient(args.server)
        client.get_file(args.file)
