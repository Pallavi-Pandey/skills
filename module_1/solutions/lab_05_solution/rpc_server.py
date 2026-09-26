"""Lab 05 - RPC Server (SOLUTION)"""
import socket
import threading
import json


class RPCServer:
    def __init__(self, host="0.0.0.0", port=9000):
        self.host = host
        self.port = port
        self.functions = {}

    def register(self, name, func):
        self.functions[name] = func
        print(f"  Registered: {name}")

    def handle_client(self, conn, addr):
        print(f"[+] RPC client: {addr}")
        try:
            while True:
                data = conn.recv(4096).decode("utf-8").strip()
                if not data:
                    break

                request = json.loads(data)
                method = request.get("method")
                args = request.get("args", [])
                req_id = request.get("id", 0)

                if method in self.functions:
                    try:
                        result = self.functions[method](*args)
                        response = {"result": result, "error": None, "id": req_id}
                    except Exception as e:
                        response = {"result": None, "error": str(e), "id": req_id}
                else:
                    response = {"result": None, "error": f"Method '{method}' not found", "id": req_id}

                print(f"  {method}({args}) → {response['result']}")
                conn.sendall((json.dumps(response) + "\n").encode("utf-8"))

        except (ConnectionResetError, json.JSONDecodeError) as e:
            print(f"  Error: {e}")
        finally:
            conn.close()

    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"=== RPC Server on {self.host}:{self.port} ===")
        print(f"Methods: {list(self.functions.keys())}\n")

        while True:
            conn, addr = server.accept()
            t = threading.Thread(target=self.handle_client, args=(conn, addr))
            t.daemon = True
            t.start()


def add(a, b): return a + b
def multiply(a, b): return a * b
def fibonacci(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(2, n + 1): a, b = b, a + b
    return b
def string_reverse(s): return s[::-1]


if __name__ == "__main__":
    server = RPCServer()
    server.register("add", add)
    server.register("multiply", multiply)
    server.register("fibonacci", fibonacci)
    server.register("string_reverse", string_reverse)
    server.start()
