"""
Lab 04 - Multi-Client Chat Client
"""

import socket
import threading
import argparse
import sys


def receive_messages(sock):
    """Receive and print messages from the server."""
    try:
        while True:
            data = sock.recv(1024)

            if not data:
                print("\nServer disconnected.")
                break

            print(data.decode("utf-8").rstrip())

    except (ConnectionResetError, OSError):
        print("\nDisconnected from server.")

    finally:
        try:
            sock.close()
        except OSError:
            pass


def main(host, port, nickname):
    """Connect to the chat server and start chatting."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        sock.sendall(nickname.encode("utf-8"))

        print(f"Connected to {host}:{port} as '{nickname}'")
        print("Type your messages (Ctrl+C to quit):\n")

        receiver = threading.Thread(
            target=receive_messages,
            args=(sock,),
            daemon=True,
        )
        receiver.start()

        while True:
            msg = input()
            if msg:
                sock.sendall(msg.encode("utf-8"))

    except (KeyboardInterrupt, EOFError):
        print("\nLeaving chat...")

    except (ConnectionRefusedError, OSError) as error:
        print(f"Could not connect or send message: {error}")

    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chat Client")
    parser.add_argument("--host", default="localhost", help="Server hostname")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--name", default="Anonymous", help="Your nickname")
    args = parser.parse_args()

    main(args.host, args.port, args.name)
