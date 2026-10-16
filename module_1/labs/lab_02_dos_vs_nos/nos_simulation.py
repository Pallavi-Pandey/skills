
"""
Lab 02 - NOS Simulation
Network Operating System: explicit file sharing over TCP.
"""

import socket
import threading
import argparse
import os

SHARED_DIR = "/shared"


class NOSFileServer:
    """Serves files to clients over TCP."""

    def __init__(self, host="0.0.0.0", port=6000):
        self.host = host
        self.port = port

    def handle_client(self, conn, addr):
        try:
            filename = conn.recv(1024).decode("utf-8").strip()
            print(f"Request from {addr}: {filename}", flush=True)

            # Accept only a filename, not a path.
            if not filename or os.path.basename(filename) != filename:
                conn.sendall(b"ERROR: Invalid filename\n")
                return

            filepath = os.path.join(SHARED_DIR, filename)

            if os.path.isfile(filepath):
                with open(filepath, "rb") as file:
                    contents = file.read()
                conn.sendall(contents)
            else:
                conn.sendall(b"ERROR: File not found\n")

        except OSError as error:
            print(f"Client error: {error}", flush=True)
            try:
                conn.sendall(b"ERROR: Could not read file\n")
            except OSError:
                pass
        finally:
            conn.close()

    def start(self):
        os.makedirs(SHARED_DIR, exist_ok=True)

        # Create a sample file for the demonstration.
        sample_path = os.path.join(SHARED_DIR, "test.txt")
        if not os.path.exists(sample_path):
            with open(sample_path, "w", encoding="utf-8") as file:
                file.write(
                    f"Hello from the NOS file server! "
                    f"PID={os.getpid()}\n"
                )
                file.write("This file lives on a specific node.\n")
                file.write("You had to know which node to ask. That's NOS.\n")

        # Create the TCP server socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.host, self.port))
            server.listen()

            print(
                f"Listening on {self.host}:{self.port}",
                flush=True
            )

            # Keep running and accept client connections.
            while True:
                conn, addr = server.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()



class NOSFileClient:
    """Requests a file from a known server."""

    def __init__(self, server_host, server_port=6000):
        self.server_host = server_host
        self.server_port = server_port

    def get_file(self, filename):
        """Request a file and save a local copy on the client."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(10)
                client.connect((self.server_host, self.server_port))
                client.sendall(filename.encode("utf-8"))

                chunks = []
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    chunks.append(data)

            response = b"".join(chunks)

            if response.startswith(b"ERROR:"):
                print(response.decode("utf-8"), end="")
                return

            destination = os.path.join(
                "/tmp", os.path.basename(filename)
            )
            with open(destination, "wb") as file:
                file.write(response)

            print("File received successfully!")
            print(f"Server: {self.server_host}:{self.server_port}")
            print(f"Saved local copy: {destination}")
            print(f"Bytes received: {len(response)}")
            print("\n--- Received contents ---")
            print(response.decode("utf-8", errors="replace"), end="")

        except (OSError, socket.timeout) as error:
            print(f"Request failed: {error}")




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NOS File Sharing Simulation"
    )
    parser.add_argument(
        "--mode", choices=["server", "client"], required=True
    )
    parser.add_argument(
        "--server", default="node1",
        help="Server hostname (client mode)"
    )
    parser.add_argument(
        "--file", default="test.txt",
        help="File to request (client mode)"
    )
    args = parser.parse_args()

    if args.mode == "server":
        print("=== NOS File Server ===", flush=True)
        print(f"Serving files from {SHARED_DIR}", flush=True)
        NOSFileServer().start()
    else:
        print("=== NOS File Client ===")
        print(f"Requesting '{args.file}' from {args.server}")
        NOSFileClient(args.server).get_file(args.file)
