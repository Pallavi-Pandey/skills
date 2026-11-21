"""
Lab 05 - RPC Server from Scratch
JSON-over-TCP Remote Procedure Call server.
"""

import socket
import threading
import json


class RPCServer:
    def __init__(self, host="0.0.0.0", port=9000):
        self.host = host
        self.port = port
        self.functions = {}

    def register(self, name, func):
        """Register a function that can be called remotely."""
        self.functions[name] = func
        print(f"Registered function: {name}")

    def handle_client(self, conn, addr):
        """Handle an RPC client connection."""
        print(f"[+] RPC client connected: {addr}")

        try:
            with conn:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        break

                    try:
                        request = json.loads(data.decode("utf-8").strip())
                        method = request.get("method")
                        args = request.get("args", [])
                        request_id = request.get("id")

                        if method not in self.functions:
                            response = {
                                "result": None,
                                "error": "Method not found",
                                "id": request_id,
                            }
                        else:
                            try:
                                result = self.functions[method](*args)
                                response = {
                                    "result": result,
                                    "error": None,
                                    "id": request_id,
                                }
                            except Exception as error:
                                response = {
                                    "result": None,
                                    "error": str(error),
                                    "id": request_id,
                                }

                    except (json.JSONDecodeError, UnicodeDecodeError) as error:
                        response = {
                            "result": None,
                            "error": f"Invalid request: {error}",
                            "id": None,
                        }

                    reply = json.dumps(response) + "\n"
                    conn.sendall(reply.encode("utf-8"))

        except OSError as error:
            print(f"  Connection error: {error}")

        finally:
            print(f"[-] RPC client disconnected: {addr}")

    def start(self):
        """Start the RPC server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            server.bind((self.host, self.port))
            server.listen(5)

            print(f"=== RPC Server on {self.host}:{self.port} ===")
            print(f"Registered methods: {list(self.functions.keys())}")

            while True:
                conn, addr = server.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()

        except KeyboardInterrupt:
            print("\nShutting down RPC server.")

        finally:
            server.close()


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
