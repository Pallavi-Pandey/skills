"""Lab 03 - TCP Echo Server (SOLUTION)"""
import socket
import threading
import argparse


def run_server(host="0.0.0.0", port=7000):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"TCP Echo Server listening on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Connected: {addr}")
        t = threading.Thread(target=handle_echo, args=(conn, addr))
        t.daemon = True
        t.start()


def handle_echo(conn, addr):
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = data.decode("utf-8")
            response = message.upper()
            conn.sendall(response.encode("utf-8"))
            print(f"  [{addr}] {message.strip()} → {response.strip()}")
    except ConnectionResetError:
        pass
    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")


def run_client(host, port=7000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}. Type messages (Ctrl+C to quit):")

    try:
        while True:
            msg = input("> ")
            if not msg:
                continue
            sock.sendall(msg.encode("utf-8"))
            response = sock.recv(1024).decode("utf-8")
            print(f"  Echo: {response}")
    except (KeyboardInterrupt, EOFError):
        print("\nDisconnected.")
    finally:
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port)
    else:
        run_client(args.host, args.port)
