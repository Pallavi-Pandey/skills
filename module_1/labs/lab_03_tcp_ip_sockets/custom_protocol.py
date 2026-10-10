"""
Lab 03 - Custom Binary Protocol (Starter Code)
================================================
Design and implement a simple binary protocol over TCP.

Protocol Format:
  [MSG_TYPE: 1 byte] [LENGTH: 2 bytes big-endian] [PAYLOAD: N bytes]

MSG_TYPE values:
  0x01 = PING    (no payload)
  0x02 = PONG    (no payload)
  0x03 = DATA    (payload = arbitrary data)
  0x04 = ERROR   (payload = error message)

Fill in the TODOs.
"""

# What each import is for (docs link = where to read more):
#   socket    -> TCP networking for the custom-protocol server and client
#                docs: https://docs.python.org/3/library/socket.html
#   struct    -> struct.pack()/struct.unpack() convert between Python
#                values and the exact byte layout this protocol's
#                header needs (1-byte type + 2-byte length)
#                docs: https://docs.python.org/3/library/struct.html
#   argparse  -> reads --mode/--host/--port from the command line
#                docs: https://docs.python.org/3/library/argparse.html
import socket
import struct
import argparse

# Protocol constants
MSG_PING = 0x01
MSG_PONG = 0x02
MSG_DATA = 0x03
MSG_ERROR = 0x04

MSG_NAMES = {MSG_PING: "PING", MSG_PONG: "PONG", MSG_DATA: "DATA", MSG_ERROR: "ERROR"}


def encode_message(msg_type, payload=b""):
    """
    Encode a message into our custom protocol format.
    
    Returns: bytes in format [type:1][length:2][payload:N]
    """
    # TODO: Pack the header: msg_type (1 byte) + length of payload (2 bytes big-endian)
    # Hint: struct.pack("!BH", msg_type, len(payload))
    # TODO: Return header + payload
    pass


def decode_message(data):
    """
    Decode a message from our custom protocol format.
    
    Returns: (msg_type, payload_bytes)
    """
    # TODO: Unpack the header (first 3 bytes): msg_type and payload_length
    # Hint: struct.unpack("!BH", data[:3])
    # TODO: Extract the payload (data[3:3+payload_length])
    # TODO: Return (msg_type, payload)
    pass


def run_server(host="0.0.0.0", port=7002):
    """Server that speaks our custom protocol."""
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
                # Read header (3 bytes)
                header = conn.recv(3)
                if len(header) < 3:
                    break

                msg_type, payload_len = struct.unpack("!BH", header)

                # Read payload
                payload = b""
                if payload_len > 0:
                    payload = conn.recv(payload_len)

                print(f"  Received: {MSG_NAMES.get(msg_type, '?')} | payload={payload.decode('utf-8', errors='replace')}")

                # TODO: Handle the message:
                #   - If PING → respond with PONG
                #   - If DATA → respond with DATA containing "ACK: " + original payload
                #   - Otherwise → respond with ERROR "Unknown message type"
                pass

        except ConnectionResetError:
            pass
        finally:
            conn.close()


def run_client(host, port=7002):
    """Client that speaks our custom protocol."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")

    # TODO: Send a PING message using encode_message
    # TODO: Receive and decode the PONG response
    # TODO: Print the response

    # TODO: Send a DATA message with payload "Hello, custom protocol!"
    # TODO: Receive and decode the response
    # TODO: Print the response

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
