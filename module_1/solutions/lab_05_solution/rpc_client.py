"""Lab 05 - RPC Client (SOLUTION)"""
import socket
import json
import argparse


class RPCClient:
    def __init__(self, host, port=9000):
        self.host = host
        self.port = port
        self.request_id = 0

    def call(self, method, *args):
        self.request_id += 1
        request = {"method": method, "args": list(args), "id": self.request_id}

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.sendall((json.dumps(request) + "\n").encode("utf-8"))
        response = json.loads(sock.recv(4096).decode("utf-8"))
        sock.close()

        if response.get("error"):
            raise Exception(response["error"])
        return response["result"]

    def __getattr__(self, method):
        def remote_call(*args):
            return self.call(method, *args)
        return remote_call


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    client = RPCClient(args.host, args.port)
    print("=== RPC Client Demo ===\n")
    print(f"add(5, 3)               = {client.add(5, 3)}")
    print(f"multiply(7, 6)          = {client.multiply(7, 6)}")
    print(f"fibonacci(10)           = {client.fibonacci(10)}")
    print(f"string_reverse('hello') = {client.string_reverse('hello')}")

    try:
        client.nonexistent(1, 2)
    except Exception as e:
        print(f"\nnonexistent(1, 2) → Error: {e}")
