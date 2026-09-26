"""
Lab 01 - Distributed Key-Value Store (Starter Code)
====================================================
A 3-node partitioned key-value store.
Keys are assigned to nodes via: hash(key) % num_nodes

Each node:
  - Stores keys assigned to it
  - Forwards requests for other keys to the correct node

Fill in the TODOs to make it work.
"""

import socket
import threading
import argparse
import hashlib


# Cluster configuration — all nodes must know about each other
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
        self.store = {}  # Local partition only
        self.num_nodes = len(CLUSTER_NODES)

    def get_owning_node(self, key):
        """Determine which node owns a given key using hash partitioning."""
        # TODO: Hash the key and return hash_value % self.num_nodes
        # Hint: Use hashlib.md5(key.encode()).hexdigest() to get a hex hash,
        #       then int(hex_hash, 16) % self.num_nodes to get the node ID
        pass

    def forward_to_node(self, node_id, command):
        """Forward a command to another node and return its response."""
        host, port = CLUSTER_NODES[node_id]
        try:
            # TODO: Create a TCP socket
            # TODO: Connect to (host, port)
            # TODO: Send the command (don't forget to encode + add newline)
            # TODO: Receive and return the response (decoded)
            # TODO: Close the socket
            pass
        except ConnectionRefusedError:
            return f"ERROR: Node {node_id} is unreachable\n"

    def process_command(self, command):
        """Process a SET or GET command, forwarding if necessary."""
        parts = command.split(" ", 2)
        op = parts[0].upper()

        if op == "SET" and len(parts) == 3:
            key = parts[1]
            value = parts[2]
            owner = self.get_owning_node(key)

            if owner == self.node_id:
                # TODO: Store locally and return "OK (stored on node {self.node_id})\n"
                pass
            else:
                # TODO: Forward to the owning node using forward_to_node
                pass

        elif op == "GET" and len(parts) == 2:
            key = parts[1]
            owner = self.get_owning_node(key)

            if owner == self.node_id:
                # TODO: Look up locally and return value or "NOT_FOUND"
                pass
            else:
                # TODO: Forward to the owning node
                pass

        else:
            return "ERROR: Unknown command\n"

    def handle_client(self, conn, addr):
        """Handle a single client connection."""
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
        """Start the node's TCP server."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[Node {self.node_id}] Listening on {self.host}:{self.port}")
        print(f"[Node {self.node_id}] Cluster: {CLUSTER_NODES}")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed KV Node")
    parser.add_argument("--node-id", type=int, required=True, help="Node ID (0, 1, or 2)")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    args = parser.parse_args()

    node = DistributedKVNode(node_id=args.node_id, port=args.port)
    node.start()
