"""
Lab 01 - Distributed Key-Value Store (SOLUTION)
================================================
"""

import socket
import threading
import argparse
import hashlib


CLUSTER_NODES = {
    0: ("node1", 5000),
    1: ("node2", 5000),
    2: ("node3", 5000),
}


class DistributedKVNode:
    def __init__(self, node_id, host="0.0.0.0", port=5000):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.store = {}
        self.num_nodes = len(CLUSTER_NODES)
        self.lock = threading.Lock()

    def get_owning_node(self, key):
        hex_hash = hashlib.md5(key.encode()).hexdigest()
        return int(hex_hash, 16) % self.num_nodes

    def forward_to_node(self, node_id, command):
        host, port = CLUSTER_NODES[node_id]
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((host, port))
            sock.sendall((command + "\n").encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            sock.close()
            return response
        except ConnectionRefusedError:
            return f"ERROR: Node {node_id} is unreachable\n"

    def process_command(self, command):
        parts = command.split(" ", 2)
        op = parts[0].upper()

        if op == "SET" and len(parts) == 3:
            key, value = parts[1], parts[2]
            owner = self.get_owning_node(key)

            if owner == self.node_id:
                with self.lock:
                    self.store[key] = value
                return f"OK (stored on node {self.node_id})\n"
            else:
                return self.forward_to_node(owner, command)

        elif op == "GET" and len(parts) == 2:
            key = parts[1]
            owner = self.get_owning_node(key)

            if owner == self.node_id:
                with self.lock:
                    value = self.store.get(key)
                if value is not None:
                    return f"{value} (from node {self.node_id})\n"
                return "NOT_FOUND\n"
            else:
                return self.forward_to_node(owner, command)

        else:
            return "ERROR: Unknown command\n"

    def handle_client(self, conn, addr):
        print(f"[Node {self.node_id}] Client connected: {addr}")
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

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[Node {self.node_id}] Listening on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--node-id", type=int, required=True)
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()

    node = DistributedKVNode(node_id=args.node_id, port=args.port)
    node.start()
