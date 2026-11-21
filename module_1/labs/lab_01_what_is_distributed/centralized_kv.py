"""
Lab 01 - Centralized Key-Value Store (Starter Code)
====================================================
A single-node TCP key-value store.
Supports: SET key value | GET key

Fill in the TODOs to make it work.
"""

# What each import is for (docs link = where to read more):
#   socket     -> low-level TCP networking: creates the listening socket and
#                 the per-client connection socket
#                 docs: https://docs.python.org/3/library/socket.html
#   threading  -> runs handle_client on its own thread per connection, so
#                 multiple clients can be served at the same time
#                 docs: https://docs.python.org/3/library/threading.html
import socket
import threading


class CentralizedKVStore:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.store = {}  # Our in-memory key-value store
        self.lock = threading.Lock()

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
            with self.lock:
                self.store[parts[1]] = parts[2]
            return "OK\n"

        elif op == "GET" and len(parts) == 2:
            with self.lock:
                value = self.store.get(parts[1])
            if value is not None:
                return f"{value}\n"
            return "NOT_FOUND\n"

        else:
            return "ERROR: Unknown command\n"

    def start(self):
        """Start the TCP server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"=== Centralized KV Store on {self.host}:{self.port} ===")

        while True:
            conn, addr = server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()


if __name__ == "__main__":
    print("=== Centralized Key-Value Store ===")
    print("Listening on port 5000...")
    server = CentralizedKVStore()
    server.start()
