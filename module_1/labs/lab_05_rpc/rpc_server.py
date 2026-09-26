"""
Lab 05 - RPC Server from Scratch (Starter Code)
=================================================
A simple RPC framework: register functions, call them over TCP.

Protocol: JSON over TCP
  Request:  {"method": "add", "args": [5, 3], "id": 1}
  Response: {"result": 8, "error": null, "id": 1}

Fill in the TODOs.
"""

import socket
import threading
import json


class RPCServer:
    def __init__(self, host="0.0.0.0", port=9000):
        self.host = host
        self.port = port
        self.functions = {}  # Registry of callable functions

    def register(self, name, func):
        """Register a function that can be called remotely."""
        # TODO: Store func in self.functions with the given name
        # TODO: Print that the function was registered
        pass

    def handle_client(self, conn, addr):
        """Handle an RPC client connection."""
        print(f"[+] RPC client connected: {addr}")
        try:
            while True:
                data = conn.recv(4096).decode("utf-8").strip()
                if not data:
                    break

                # TODO: Parse the JSON request
                # TODO: Extract "method", "args", and "id" from the request
                # TODO: Look up the method in self.functions
                # TODO: If found, call it with *args and build a success response
                # TODO: If not found, build an error response
                # TODO: Send the JSON response back
                #
                # Success response: {"result": <value>, "error": None, "id": <id>}
                # Error response:   {"result": None, "error": "Method not found", "id": <id>}
                pass

        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"  Error: {e}")
        finally:
            conn.close()
            print(f"[-] RPC client disconnected: {addr}")

    def start(self):
        """Start the RPC server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"=== RPC Server on {self.host}:{self.port} ===")
        print(f"Registered methods: {list(self.functions.keys())}")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


# ---- Register some functions ----

def add(a, b):
    """Add two numbers."""
    return a + b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def fibonacci(n):
    """Compute the nth Fibonacci number."""
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def string_reverse(s):
    """Reverse a string."""
    return s[::-1]


if __name__ == "__main__":
    server = RPCServer()
    server.register("add", add)
    server.register("multiply", multiply)
    server.register("fibonacci", fibonacci)
    server.register("string_reverse", string_reverse)
    server.start()
