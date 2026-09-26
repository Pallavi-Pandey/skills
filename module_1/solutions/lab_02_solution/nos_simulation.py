"""Lab 02 - NOS Simulation (SOLUTION)"""

import socket
import threading
import argparse
import os

SHARED_DIR = "/shared"


class NOSFileServer:
    def __init__(self, host="0.0.0.0", port=6000):
        self.host = host
        self.port = port

    def handle_client(self, conn, addr):
        try:
            filename = conn.recv(1024).decode("utf-8").strip()
            filepath = os.path.join(SHARED_DIR, filename)

            if os.path.exists(filepath):
                with open(filepath, "r") as f:
                    contents = f.read()
                conn.sendall(contents.encode("utf-8"))
            else:
                conn.sendall(b"ERROR: File not found\n")
        finally:
            conn.close()

    def start(self):
        os.makedirs(SHARED_DIR, exist_ok=True)
        with open(os.path.join(SHARED_DIR, "test.txt"), "w") as f:
            f.write(f"Hello from the NOS file server! PID={os.getpid()}\n")
            f.write("This file lives on a specific node.\n")
            f.write("You had to know which node to ask. That's NOS.\n")

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"Serving on {self.host}:{self.port}")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


class NOSFileClient:
    def __init__(self, server_host, server_port=6000):
        self.server_host = server_host
        self.server_port = server_port

    def get_file(self, filename):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_host, self.server_port))
        sock.sendall(filename.encode("utf-8"))
        response = sock.recv(4096).decode("utf-8")
        print(f"Received from {self.server_host}:\n{response}")
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--server", default="node1")
    parser.add_argument("--file", default="test.txt")
    args = parser.parse_args()

    if args.mode == "server":
        NOSFileServer().start()
    else:
        NOSFileClient(args.server).get_file(args.file)
