"""
Lab 01 - Centralized Key-Value Store (SOLUTION)
================================================
"""

import socket
import threading


class CentralizedKVStore:
    def __init__(self, host="0.0.0.0", port=5000):
        self.host = host
        self.port = port
        self.store = {}
        self.lock = threading.Lock()

    def handle_client(self, conn, addr):
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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"=== Centralized KV Store on {self.host}:{self.port} ===")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


if __name__ == "__main__":
    server = CentralizedKVStore()
    server.start()
