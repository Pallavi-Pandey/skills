"""
Lab 04 - Multi-Client Chat Server
"""

import socket
import threading
import argparse


class ChatServer:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.clients = {}
        self.lock = threading.Lock()

    def broadcast(self, message, sender_conn=None):
        failed_clients = []

        with self.lock:
            clients = list(self.clients.items())

        for conn, nickname in clients:
            if conn == sender_conn:
                continue
            try:
                conn.sendall(message.encode("utf-8"))
            except OSError:
                failed_clients.append(conn)

        with self.lock:
            for conn in failed_clients:
                self.clients.pop(conn, None)
                try:
                    conn.close()
                except OSError:
                    pass

    def handle_client(self, conn, addr):
        nickname = ""

        try:
            data = conn.recv(1024)
            if not data:
                return

            nickname = data.decode("utf-8").strip()
            if not nickname:
                return

            with self.lock:
                self.clients[conn] = nickname

            print(f"[+] {nickname} joined from {addr}")
            self.broadcast(
                f"[INFO] {nickname} has joined the chat.\n",
                sender_conn=conn,
            )

            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message_text = data.decode("utf-8").strip()
                if not message_text:
                    continue

                message = f"[{nickname}] {message_text}\n"
                print(message.strip())
                self.broadcast(message, sender_conn=conn)

        except (OSError, ConnectionError, UnicodeDecodeError):
            pass

        finally:
            with self.lock:
                was_connected = conn in self.clients
                self.clients.pop(conn, None)

            try:
                conn.close()
            except OSError:
                pass

            if nickname:
                print(f"[-] {nickname} left")
                if was_connected:
                    self.broadcast(
                        f"[INFO] {nickname} has left the chat.\n"
                    )

    def start(self):
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        server_socket.setsockopt(
            socket.SOL_SOCKET, socket.SO_REUSEADDR, 1
        )

        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Chat server listening on {self.host}:{self.port}")

            while True:
                conn, addr = server_socket.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()

        except KeyboardInterrupt:
            print("\nShutting down chat server.")
        finally:
            server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    server = ChatServer(port=args.port)
    server.start()
