"""
Lab 01 - Centralized Key-Value Store (Starter Code)
====================================================
A single-node TCP key-value store.
Supports: SET key value | GET key

Fill in the TODOs to make it work.
"""

import socket
import threading


class CentralizedKVStore:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.store = {}  # Our in-memory key-value store

    def handle_client(self, conn, addr):
        """Handle a single client connection."""
        print(f"[+] Client connected: {addr}")
        try:
            while True:
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    break

                response = self.process_command(data)
                conn.sendall(response.encode("utf-8"))
        except ConnectionResetError:
            pass
        finally:
            conn.close()
            print(f"[-] Client disconnected: {addr}")

    def process_command(self, command):
        """
        Parse and execute a command.
        
        Commands:
            SET key value  -> stores the key-value pair, returns "OK"
            GET key        -> returns the value, or "NOT_FOUND"
        """
        parts = command.split(" ", 2)
        op = parts[0].upper()

        if op == "SET" and len(parts) == 3:
            # TODO: Store parts[1] as key and parts[2] as value in self.store
            # TODO: Return "OK\n"
            pass

        elif op == "GET" and len(parts) == 2:
            # TODO: Look up parts[1] in self.store
            # TODO: Return the value + "\n" if found, or "NOT_FOUND\n" if not
            pass

        else:
            return "ERROR: Unknown command\n"

    def start(self):
        """Start the TCP server."""
        # TODO: Create a TCP socket (socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Set SO_REUSEADDR option
        # TODO: Bind to (self.host, self.port)
        # TODO: Listen for connections (backlog=5)
        # TODO: In a loop:
        #   - Accept a connection
        #   - Spawn a thread to handle_client
        pass


if __name__ == "__main__":
    print("=== Centralized Key-Value Store ===")
    print("Listening on port 5000...")
    server = CentralizedKVStore()
    server.start()
