"""Lab 03 - Custom Binary Protocol (SOLUTION)"""
import socket
import struct
import argparse

MSG_PING = 0x01
MSG_PONG = 0x02
MSG_DATA = 0x03
MSG_ERROR = 0x04

MSG_NAMES = {MSG_PING: "PING", MSG_PONG: "PONG", MSG_DATA: "DATA", MSG_ERROR: "ERROR"}


def encode_message(msg_type, payload=b""):
    header = struct.pack("!BH", msg_type, len(payload))
    return header + payload


def decode_message(data):
    msg_type, payload_len = struct.unpack("!BH", data[:3])
    payload = data[3:3 + payload_len]
    return msg_type, payload


def run_server(host="0.0.0.0", port=7002):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Custom Protocol Server on {host}:{port}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Client connected: {addr}")
        try:
            while True:
                header = conn.recv(3)
                if len(header) < 3:
                    break

                msg_type, payload_len = struct.unpack("!BH", header)

                payload = b""
                if payload_len > 0:
                    payload = conn.recv(payload_len)

                print(f"  Received: {MSG_NAMES.get(msg_type, '?')} | payload={payload.decode('utf-8', errors='replace')}")

                if msg_type == MSG_PING:
                    response = encode_message(MSG_PONG)
                elif msg_type == MSG_DATA:
                    response = encode_message(MSG_DATA, b"ACK: " + payload)
                else:
                    response = encode_message(MSG_ERROR, b"Unknown message type")

                conn.sendall(response)

        except ConnectionResetError:
            pass
        finally:
            conn.close()


def run_client(host, port=7002):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")

    sock.sendall(encode_message(MSG_PING))
    header = sock.recv(3)
    msg_type, _ = struct.unpack("!BH", header)
    print(f"  Response: {MSG_NAMES.get(msg_type, '?')}")

    sock.sendall(encode_message(MSG_DATA, b"Hello, custom protocol!"))
    header = sock.recv(3)
    msg_type, payload_len = struct.unpack("!BH", header)
    payload = sock.recv(payload_len) if payload_len > 0 else b""
    print(f"  Response: {MSG_NAMES.get(msg_type, '?')} | payload={payload.decode('utf-8')}")

    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom Binary Protocol")
    parser.add_argument("--mode", choices=["server", "client"], required=True)
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7002)
    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port)
    else:
        run_client(args.host, args.port)
