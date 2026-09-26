"""Lab 04 - Chat Server (SOLUTION)"""
import socket
import threading


class ChatServer:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.clients = {}
        self.lock = threading.Lock()

    def broadcast(self, message, sender_conn=None):
        failed = []
        with self.lock:
            for conn, nickname in self.clients.items():
                if conn != sender_conn:
                    try:
                        conn.sendall(message.encode("utf-8"))
                    except Exception:
                        failed.append(conn)
            for conn in failed:
                del self.clients[conn]

    def handle_client(self, conn, addr):
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
                self.broadcast(message, sender_conn=conn)
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
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(10)
        print(f"=== Chat Server on {self.host}:{self.port} ===")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


if __name__ == "__main__":
    ChatServer().start()
