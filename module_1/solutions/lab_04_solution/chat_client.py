"""Lab 04 - Chat Client (SOLUTION)"""
import socket
import threading
import argparse
import sys


def receive_messages(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"), end="", flush=True)
    except (ConnectionResetError, OSError):
        print("\nDisconnected from server.")
        sys.exit(0)


def main(host, port, nickname):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.sendall(nickname.encode("utf-8"))

    print(f"Connected as '{nickname}'. Type your messages:\n")

    recv_thread = threading.Thread(target=receive_messages, args=(sock,))
    recv_thread.daemon = True
    recv_thread.start()

    try:
        while True:
            msg = input()
            if msg:
                sock.sendall(msg.encode("utf-8"))
    except (KeyboardInterrupt, EOFError):
        print("\nLeaving chat...")
    finally:
        sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--name", default="Anonymous")
    args = parser.parse_args()
    main(args.host, args.port, args.name)
