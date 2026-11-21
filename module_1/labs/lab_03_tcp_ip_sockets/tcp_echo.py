"""
Lab 03 - TCP Echo Server
A TCP server that returns messages in UPPERCASE.
"""

import socket
import threading
import argparse


def run_server(host="0.0.0.0", port=7000):
    """Start a TCP echo server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    print(f"TCP Echo Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[+] Connected: {addr}")
            thread = threading.Thread(
                target=handle_echo,
                args=(conn, addr),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nServer stopping.")
    finally:
        server.close()


def handle_echo(conn, addr):
    """Receive messages and return them in uppercase."""
    try:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            message = data.decode("utf-8")
            response = message.upper()
            conn.sendall(response.encode("utf-8"))

            print(f"[{addr}] Received: {message!r}")
            print(f"[{addr}] Sent: {response!r}")

    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        conn.close()
        print(f"[-] Disconnected: {addr}")


def run_client(host, port=7000):
    """Send messages to the server and print its replies."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    print(f"Connected to {host}:{port}. Type messages (Ctrl+C to quit):")

    try:
        while True:
            msg = input("> ")

            if not msg:
                continue

            client.sendall(msg.encode("utf-8"))
            response = client.recv(1024)

            if not response:
                print("Server disconnected.")
                break

            print(f"Echo: {response.decode('utf-8')}")

    except (KeyboardInterrupt, EOFError):
        print("\nDisconnected.")
    finally:
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TCP Echo Server/Client")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--host", default="localhost", help="Server host (client mode)")
    parser.add_argument("--port", type=int, default=7000)
    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port)
    else:
        run_client(args.host, args.port)
