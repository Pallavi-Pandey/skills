"""
Lab 03 - Custom Binary Protocol

Message format:
[MSG_TYPE: 1 byte] [LENGTH: 2 bytes big-endian] [PAYLOAD: N bytes]

Message types:
0x01 = PING
0x02 = PONG
0x03 = DATA
0x04 = ERROR
"""

import socket
import struct
import argparse

MSG_PING = 0x01
MSG_PONG = 0x02
MSG_DATA = 0x03
MSG_ERROR = 0x04

MSG_NAMES = {
    MSG_PING: "PING",
    MSG_PONG: "PONG",
    MSG_DATA: "DATA",
    MSG_ERROR: "ERROR"
}


def encode_message(msg_type, payload=b""):
    """Encode a message using a 3-byte header and payload."""
    if not isinstance(payload, bytes):
        raise TypeError("Payload must be bytes")

    if not 0 <= msg_type <= 255:
        raise ValueError("Message type must fit in one byte")

    if len(payload) > 65535:
        raise ValueError("Payload is too large")

    header = struct.pack("!BH", msg_type, len(payload))
    return header + payload


def receive_exact(sock, size):
    """Read exactly size bytes from a TCP connection."""
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if not chunk:
            if not data:
                return None
            raise ConnectionError("Connection closed before message was complete")

        data.extend(chunk)

    return bytes(data)


def receive_message(sock):
    """Read and decode one complete protocol message."""
    header = receive_exact(sock, 3)

    if header is None:
        return None

    msg_type, payload_length = struct.unpack("!BH", header)
    payload = receive_exact(sock, payload_length) if payload_length else b""

    if payload is None:
        raise ConnectionError("Connection closed before payload was received")

    return msg_type, payload


def decode_message(data):
    """Decode a complete protocol message."""
    if len(data) < 3:
        raise ValueError("Message is shorter than the 3-byte header")

    msg_type, payload_length = struct.unpack("!BH", data[:3])

    if len(data) != 3 + payload_length:
        raise ValueError("Message length does not match its header")

    payload = data[3:]
    return msg_type, payload


def run_server(host="0.0.0.0", port=7002):
    """Server that handles messages using our custom protocol."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)

    print(f"Custom Protocol Server on {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            print(f"[+] Client connected: {addr}")

            with conn:
                try:
                    while True:
                        message = receive_message(conn)

                        if message is None:
                            break

                        msg_type, payload = message
                        readable = payload.decode("utf-8", errors="replace")
                        print(
                            f"Received: {MSG_NAMES.get(msg_type, 'UNKNOWN')} "
                            f"| payload={readable!r}"
                        )

                        if msg_type == MSG_PING:
                            response = encode_message(MSG_PONG)
                        elif msg_type == MSG_DATA:
                            response = encode_message(
                                MSG_DATA, b"ACK: " + payload
                            )
                        else:
                            response = encode_message(
                                MSG_ERROR, b"Unknown message type"
                            )

                        conn.sendall(response)

                except (ConnectionError, ConnectionResetError) as error:
                    print(f"Connection ended: {error}")

                print(f"[-] Client disconnected: {addr}")

    except KeyboardInterrupt:
        print("\nServer stopping.")
    finally:
        server.close()


def run_client(host, port=7002):
    """Send PING and DATA messages and print the responses."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")

        sock.sendall(encode_message(MSG_PING))
        response = receive_message(sock)

        if response is None:
            raise ConnectionError("Server closed without replying to PING")

        msg_type, payload = response
        print(f"Response: {MSG_NAMES.get(msg_type, 'UNKNOWN')}")

        sock.sendall(
            encode_message(MSG_DATA, b"Hello, custom protocol!")
        )
        response = receive_message(sock)

        if response is None:
            raise ConnectionError("Server closed without replying to DATA")

        msg_type, payload = response
        print(
            f"Response: {MSG_NAMES.get(msg_type, 'UNKNOWN')} "
            f"| payload={payload.decode('utf-8', errors='replace')}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Custom Binary Protocol")
    parser.add_argument(
        "--mode", choices=["server", "client"], required=True
    )
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=7002)
    args = parser.parse_args()

    if args.mode == "server":
        run_server(port=args.port)
    else:
        run_client(args.host, args.port)
