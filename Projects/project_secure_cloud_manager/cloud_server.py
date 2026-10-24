"""A beginner-sized, in-memory cloud VM manager server.

Protocol: one JSON object followed by a newline for every request and response.
This is a teaching example, not a production cloud controller.
"""

import hashlib
import hmac
import json
import secrets
import socket
import threading
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 5050
TOTAL_CPU = 4
TOTAL_MEMORY_MB = 4096

# Deliberately simple demo identities. Do not store real passwords this way.
USERS = {
    "alice": {"password": "alice123", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}
AUDIT_KEY = b"demo-key-change-me"  # HMAC makes audit edits detectable in this demo.


class CloudManager:
    def __init__(self):
        self.vms = {}
        self.sessions = {}
        self.audit_events = []
        self.lock = threading.Lock()

    def _used_resources(self):
        cpu = sum(vm["cpu"] for vm in self.vms.values() if vm["state"] == "running")
        memory = sum(vm["memory_mb"] for vm in self.vms.values() if vm["state"] == "running")
        return cpu, memory

    def _audit(self, user, action, detail):
        event = {
            "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "user": user,
            "action": action,
            "detail": detail,
        }
        encoded = json.dumps(event, sort_keys=True).encode("utf-8")
        event["hmac"] = hmac.new(AUDIT_KEY, encoded, hashlib.sha256).hexdigest()
        self.audit_events.append(event)

    def verify_audit_log(self):
        """Return False if any event was changed after it was recorded."""
        for event in self.audit_events:
            unsigned = {key: value for key, value in event.items() if key != "hmac"}
            encoded = json.dumps(unsigned, sort_keys=True).encode("utf-8")
            expected = hmac.new(AUDIT_KEY, encoded, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(event["hmac"], expected):
                return False
        return True

    def login(self, username, password):
        account = USERS.get(username)
        if not account or not hmac.compare_digest(account["password"], password):
            self._audit(username or "unknown", "login_failed", "invalid credentials")
            return {"ok": False, "error": "Invalid username or password."}

        token = secrets.token_urlsafe(24)
        self.sessions[token] = {"username": username, "role": account["role"]}
        self._audit(username, "login", "successful")
        return {"ok": True, "token": token, "role": account["role"]}

    def _identity(self, token):
        return self.sessions.get(token)

    def list_vms(self, identity):
        if identity["role"] == "admin":
            visible = self.vms.values()
        else:
            visible = (vm for vm in self.vms.values() if vm["owner"] == identity["username"])
        return {"ok": True, "vms": list(visible)}

    def create_vm(self, identity, name, cpu, memory_mb):
        if not name or not isinstance(cpu, int) or not isinstance(memory_mb, int) or cpu < 1 or memory_mb < 128:
            return {"ok": False, "error": "Use a name, CPU >= 1, and memory >= 128 MB."}

        # The lock is essential: several client threads can reach this code together.
        with self.lock:
            if name in self.vms:
                return {"ok": False, "error": "A VM with that name already exists."}
            used_cpu, used_memory = self._used_resources()
            if used_cpu + cpu > TOTAL_CPU or used_memory + memory_mb > TOTAL_MEMORY_MB:
                return {"ok": False, "error": "Not enough free CPU or memory."}

            vm = {
                "name": name,
                "owner": identity["username"],
                "state": "running",
                "cpu": cpu,
                "memory_mb": memory_mb,
            }
            self.vms[name] = vm
            self._audit(identity["username"], "create_vm", name)
        return {"ok": True, "vm": vm}

    def delete_vm(self, identity, name):
        if identity["role"] != "admin":
            self._audit(identity["username"], "delete_denied", name)
            return {"ok": False, "error": "Only an admin may delete VMs."}

        with self.lock:
            if name not in self.vms:
                return {"ok": False, "error": "VM not found."}
            del self.vms[name]
            self._audit(identity["username"], "delete_vm", name)
        return {"ok": True, "message": f"Deleted {name}."}

    def handle(self, request):
        action = request.get("action")
        if action == "login":
            return self.login(request.get("username", ""), request.get("password", ""))

        identity = self._identity(request.get("token"))
        if not identity:
            return {"ok": False, "error": "Log in first (invalid or missing session token)."}
        if action == "list":
            return self.list_vms(identity)
        if action == "create":
            return self.create_vm(identity, request.get("name", ""), request.get("cpu"), request.get("memory_mb"))
        if action == "delete":
            return self.delete_vm(identity, request.get("name", ""))
        if action == "audit":
            if identity["role"] != "admin":
                self._audit(identity["username"], "audit_denied", "")
                return {"ok": False, "error": "Only an admin may view audit events."}
            return {"ok": True, "events": self.audit_events, "integrity_ok": self.verify_audit_log()}
        return {"ok": False, "error": "Unknown action."}


def receive_json(reader):
    line = reader.readline()
    if not line:
        return None
    return json.loads(line.decode("utf-8"))


def client_thread(conn, manager):
    with conn:
        reader = conn.makefile("rb")
        writer = conn.makefile("wb")
        try:
            while request := receive_json(reader):
                response = manager.handle(request)
                writer.write((json.dumps(response) + "\n").encode("utf-8"))
                writer.flush()
        except (json.JSONDecodeError, OSError) as error:
            print(f"Client disconnected or sent invalid data: {error}")


def main():
    manager = CloudManager()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"Cloud manager listening on {HOST}:{PORT} ({TOTAL_CPU} CPU, {TOTAL_MEMORY_MB} MB)")
        while True:
            conn, address = server.accept()
            print(f"Connected: {address}")
            threading.Thread(target=client_thread, args=(conn, manager), daemon=True).start()


if __name__ == "__main__":
    main()
