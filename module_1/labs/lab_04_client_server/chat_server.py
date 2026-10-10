"""
Lab 04 - Multi-Client Chat Server (Starter Code)
==================================================
A TCP chat server that broadcasts messages to all connected clients.

Fill in the TODOs.
"""

# What each import is for (docs link = where to read more):
#   socket     -> TCP networking: the listening socket, plus one
#                 connection per connected chat client
#                 docs: https://docs.python.org/3/library/socket.html
#   threading  -> runs each client's conversation on its own thread, so
#                 the server can keep accepting new clients at any time
#                 docs: https://docs.python.org/3/library/threading.html
#   argparse   -> reads --port from the command line
#                 docs: https://docs.python.org/3/library/argparse.html
import socket
import threading
import argparse


class ChatServer:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.clients = {}  # {conn: nickname}
        self.lock = threading.Lock()

    def broadcast(self, message, sender_conn=None):
        """Send a message to all connected clients except the sender."""
        # TODO: Iterate over self.clients
        # TODO: For each client that is NOT sender_conn, send the message
        # TODO: If sending fails, mark that client for removal
        # TODO: Remove failed clients
        # Hint: Use self.lock to protect self.clients
        pass

    def handle_client(self, conn, addr):
        """Handle a single chat client."""
        # Receive nickname
        try:
            nickname = conn.recv(1024).decode("utf-8").strip()
        except Exception:
            conn.close()
            return

        with self.lock:
            self.clients[conn] = nickname

        print(f"[+] {nickname} joined from {addr}")
        self.broadcast(f"[INFO] {nickname} has joined the chat.\n", sender_conn=conn)

        try:
            while True:
                data = conn.recv(1024).decode("utf-8").strip()
                if not data:
                    break
                message = f"[{nickname}] {data}\n"
                print(f"  {message.strip()}")
                # TODO: Broadcast this message to all OTHER clients
                pass
        except ConnectionResetError:
            pass
        finally:
            with self.lock:
                if conn in self.clients:
                    del self.clients[conn]
            conn.close()
            print(f"[-] {nickname} left")
            self.broadcast(f"[INFO] {nickname} has left the chat.\n")

    def start(self):
        """Start the chat server."""
        # TODO: Create TCP socket, set SO_REUSEADDR, bind, listen
        # TODO: In a loop, accept connections
        # TODO: For each connection, spawn a thread running handle_client
        # IMPORTANT: Without threading, the server blocks on one client!
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Server")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    print(f"=== Chat Server on port {args.port} ===")
    server = ChatServer(port=args.port)
    server.start()
