"""
Lab 05 - RPC Client from Scratch (Starter Code)
=================================================
Makes remote function calls LOOK like local calls.

Usage:
    client = RPCClient("node1", 9000)
    result = client.call("add", 5, 3)  # Returns 8
    
Fill in the TODOs.
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
        """
        Call a remote function as if it were local.
        
        This is the magic of RPC:
          result = client.call("add", 5, 3)
        looks like:
          result = add(5, 3)
        but it actually goes over the network!
        """
        self.request_id += 1

        # TODO: Build the request dict: {"method": method, "args": list(args), "id": self.request_id}
        # TODO: Create a TCP socket
        # TODO: Connect to (self.host, self.port)
        # TODO: Send the request as JSON (encoded, with newline)
        # TODO: Receive the response (up to 4096 bytes)
        # TODO: Parse the JSON response
        # TODO: Close the socket
        # TODO: If response["error"] is not None, raise an Exception with the error
        # TODO: Return response["result"]
        pass

    def __getattr__(self, method):
        """
        Python magic: allows calling client.add(5, 3) instead of client.call("add", 5, 3)
        """
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

    # These look like local function calls, but they go over the network!
    print(f"add(5, 3)           = {client.call('add', 5, 3)}")
    print(f"multiply(7, 6)      = {client.call('multiply', 7, 6)}")
    print(f"fibonacci(10)       = {client.call('fibonacci', 10)}")
    print(f"string_reverse('hello') = {client.call('string_reverse', 'hello')}")

    # Using __getattr__ magic (even cleaner!):
    print(f"\n--- Using magic method syntax ---")
    print(f"client.add(100, 200)       = {client.add(100, 200)}")
    print(f"client.fibonacci(20)       = {client.fibonacci(20)}")

    # Error case
    try:
        client.call("nonexistent", 1, 2)
    except Exception as e:
        print(f"\nclient.nonexistent(1, 2) → Error: {e}")
