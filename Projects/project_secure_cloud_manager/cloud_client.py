"""Interactive client for the Secure Cloud VM Manager mini project."""

import json
import socket

HOST = "127.0.0.1"
PORT = 5050


def request(reader, writer, message):
    writer.write((json.dumps(message) + "\n").encode("utf-8"))
    writer.flush()
    response = reader.readline()
    if not response:
        raise ConnectionError("Server closed the connection.")
    return json.loads(response.decode("utf-8"))


def print_response(response):
    if not response["ok"]:
        print("Error:", response["error"])
        return
    if "vms" in response:
        if not response["vms"]:
            print("No visible VMs.")
        for vm in response["vms"]:
            print(f"{vm['name']}  owner={vm['owner']}  state={vm['state']}  "
                  f"cpu={vm['cpu']}  memory={vm['memory_mb']}MB")
    elif "events" in response:
        print("Audit integrity:", "OK" if response["integrity_ok"] else "FAILED")
        for event in response["events"]:
            print(f"{event['time']}  {event['user']}  {event['action']}  {event['detail']}")
    elif "vm" in response:
        vm = response["vm"]
        print(f"Created {vm['name']}: {vm['cpu']} CPU, {vm['memory_mb']} MB memory")
    else:
        print(response.get("message", "OK"))


def main():
    with socket.create_connection((HOST, PORT)) as sock:
        reader = sock.makefile("rb")
        writer = sock.makefile("wb")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        login = request(reader, writer, {"action": "login", "username": username, "password": password})
        if not login["ok"]:
            print_response(login)
            return
        token = login["token"]
        print(f"Logged in as {username} ({login['role']}). Type 'help' for commands.")

        while True:
            words = input("cloud> ").strip().split()
            if not words:
                continue
            if words[0] in {"quit", "exit"}:
                return
            if words[0] == "help":
                print("list | create NAME CPU MEMORY_MB | delete NAME | audit | quit")
                continue
            if words[0] == "list":
                message = {"action": "list", "token": token}
            elif words[0] == "audit":
                message = {"action": "audit", "token": token}
            elif words[0] == "delete" and len(words) == 2:
                message = {"action": "delete", "token": token, "name": words[1]}
            elif words[0] == "create" and len(words) == 4:
                try:
                    message = {"action": "create", "token": token, "name": words[1],
                               "cpu": int(words[2]), "memory_mb": int(words[3])}
                except ValueError:
                    print("CPU and MEMORY_MB must be whole numbers.")
                    continue
            else:
                print("Invalid command. Type 'help'.")
                continue
            print_response(request(reader, writer, message))


if __name__ == "__main__":
    main()
