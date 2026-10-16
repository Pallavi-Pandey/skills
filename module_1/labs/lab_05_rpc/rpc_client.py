"""
Lab 05 - RPC Client from Scratch
Makes remote function calls over TCP using JSON.
"""

import socket
import json
import argparse


class RPCClient:
    def __init__(self, host, port=9000):
        self.host = host
        self.port = port
        self.request_id = 0

    def call(self, method, *args):
        """Call a remote function and return its result."""
        self.request_id += 1

        request = {
            "method": method,
            "args": list(args),
            "id": self.request_id,
        }

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.settimeout(10)
            client_socket.connect((self.host, self.port))

            message = json.dumps(request) + "\n"
            client_socket.sendall(message.encode("utf-8"))

            response_data = b""
            while b"\n" not in response_data:
                chunk = client_socket.recv(4096)
                if not chunk:
                    break
                response_data += chunk

        if not response_data:
            raise Exception("Server closed the connection without a response")

        response = json.loads(response_data.decode("utf-8").strip())

        if response.get("error") is not None:
            raise Exception(response["error"])

        return response["result"]

    def __getattr__(self, method):
        """Allow calls like client.add(5, 3)."""
        def remote_call(*args):
            return self.call(method, *args)
        return remote_call


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RPC Client")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    client = RPCClient(args.host, args.port)

    print("=== RPC Client Demo ===\n")

    print(f"add(5, 3)           = {client.call('add', 5, 3)}")
    print(f"multiply(7, 6)      = {client.call('multiply', 7, 6)}")
    print(f"fibonacci(10)       = {client.call('fibonacci', 10)}")
    print(f"string_reverse('hello') = {client.call('string_reverse', 'hello')}")

    print("\n--- Using magic method syntax ---")
    print(f"client.add(100, 200)       = {client.add(100, 200)}")
    print(f"client.fibonacci(20)       = {client.fibonacci(20)}")

    try:
        client.call("nonexistent", 1, 2)
    except Exception as error:
        print(f"\nclient.nonexistent(1, 2) -> Error: {error}")
