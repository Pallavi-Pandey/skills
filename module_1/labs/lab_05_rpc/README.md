# Lab 05: Remote Procedure Call — From Scratch to gRPC

> **Time:** 55 minutes | **Language:** Python (Part A) + Go (Part B) | **Infrastructure:** Docker
> If you haven't done Lab 01 yet, do that first — this lab reuses its socket concepts (`socket`, `bind`, `accept`, threads) without re-explaining them in full.

## Objective

1. Build a simple RPC framework **from scratch** in Python, using nothing but sockets and JSON — so you understand what's actually happening underneath every RPC system.
2. Use **real gRPC** with Protocol Buffers in Go — the industry-standard way most companies actually do this, so you can see what all that hand-written plumbing from Part A buys you when it's automated.

---

## Concepts you need before you start

Read this whole section before opening any code. Part A needs concepts 1–3. Part B needs all of them, since it also introduces a brand-new programming language (Go).

### 1. What does "RPC" actually mean?

**RPC (Remote Procedure Call)** is an old, simple idea: you write code that *calls a function*, but that function actually runs on a **different machine**, over the network — and the calling code is written to look as close as possible to an ordinary, local function call.

```python
# Without RPC — you deal with the network by hand
sock.send(b'{"func": "add", "args": [5, 3]}')
result = json.loads(sock.recv(1024))

# With RPC — it FEELS local, but the network call still happens underneath
result = client.add(5, 3)
```

Nothing magical is happening — `client.add(5, 3)` still opens a socket, sends bytes, and waits for a reply, exactly like Lab 01. RPC is just a wrapper that hides those mechanics behind something that reads like a normal function call, so the programmer using it doesn't have to think about sockets every time.

### 2. Why do we have to "serialize" the arguments?

A network socket only understands one thing: **bytes** (raw 0s and 1s). It has no idea what a Python list, dictionary, or integer object is. So before you can send `add(5, 3)`'s arguments over a socket, you need to convert them into bytes — this is called **serialization**. On the receiving end, you convert those bytes back into usable data — **deserialization**.

In Part A, we use **JSON** (JavaScript Object Notation) as the serialization format — a plain-text way of writing structured data that both Python's `json.dumps()` (object → JSON string) and `json.loads()` (JSON string → object) understand natively. The protocol for this lab is:

```
Request:  {"method": "add", "args": [5, 3], "id": 1}
Response: {"result": 8, "error": null, "id": 1}
```

- `"method"` — the name of the function to call.
- `"args"` — a list of arguments to call it with.
- `"id"` — a number tagging this specific request, so a response can be matched back to the request that caused it (real-world RPC systems often have several requests in flight at once; this lab only ever has one at a time, but the field is there so you see the pattern).
- `"error"` — `null` (Python's `None`) on success, or an error message string on failure.

### 3. Python's `__getattr__` magic (how `client.add(5, 3)` works)

You'll notice `RPCClient` never defines a method called `add`, `multiply`, or `fibonacci` — yet `client.add(5, 3)` works. This is because of `__getattr__`, a special Python method that gets called *automatically* whenever you access an attribute that doesn't otherwise exist on the object. This class's `__getattr__` is already written for you:

```python
def __getattr__(self, method):
    def remote_call(*args):
        return self.call(method, *args)
    return remote_call
```

So `client.add(5, 3)` is really just Python quietly translating that into `client.call("add", 5, 3)`. This is the trick that makes the "network call disguised as a local call" illusion actually work.

### 4. What is gRPC, and how is it different from what you're building in Part A?

**gRPC** is Google's production-grade RPC framework. It solves the exact same problem as Part A (call a remote function that looks local), but instead of you hand-writing the socket handling, the JSON encoding, and the client wrapper class yourself, gRPC and a companion tool **generate all of that code for you automatically** from a single description file. It also uses a faster, more compact binary format instead of human-readable JSON, and runs over HTTP/2 instead of a plain raw socket. Conceptually, everything you learn by hand-building Part A is exactly what's happening inside gRPC's generated code in Part B — you just don't have to write it yourself.

### 5. What are Protocol Buffers, and what does a `.proto` file do?

**Protocol Buffers** ("protobuf") is Google's schema-based serialization format — the gRPC equivalent of the JSON envelope from Part A, but stricter and faster. Instead of writing free-form JSON, you first declare, in a `.proto` file, exactly what your messages and remote functions look like. Open `grpc_go/calculator.proto` and read it alongside this explanation:

```protobuf
service Calculator {
  rpc Calculate (CalcRequest) returns (CalcResponse);
  rpc FibonacciStream (FibRequest) returns (stream FibResponse);
}

message CalcRequest {
  string operation = 1;
  double a = 2;
  double b = 3;
}
```

- `service Calculator { ... }` declares which remote functions ("RPCs") exist — here, `Calculate` and `FibonacciStream` — and what each one takes in and returns. This plays the same role as `self.functions` (the registry) in Part A's `RPCServer`, except it's declared up front in a file instead of built at runtime.
- `message CalcRequest { ... }` defines the *shape* of a piece of data, similar to defining a class with only data fields (no behavior) — comparable to the JSON request dict in Part A, but with explicit, fixed field names and types (`string`, `double`, `int32`, ...) instead of arbitrary JSON.
- The `= 1`, `= 2`, `= 3` after each field are **not default values** — they're field numbers, an internal bookkeeping detail Protocol Buffers uses to identify fields compactly in the binary encoding. You don't need to do anything with them beyond knowing they aren't the field's value.
- `rpc FibonacciStream (FibRequest) returns (stream FibResponse);` — the keyword `stream` means the server doesn't send back one single response; it sends back *many* `FibResponse` messages, one at a time, over the same call. Think of the difference between downloading a whole file before playing it versus streaming a video — the data arrives incrementally instead of all at once.

### 6. What does "code generation" mean here, concretely?

The `.proto` file by itself is just a text description — it doesn't run anything. A separate tool, `protoc` (the **proto**col buffer **c**ompiler), reads the `.proto` file and **writes actual Go source code for you**: Go structs matching every `message` (e.g. a real `CalcRequest` struct with `Operation`, `A`, `B` fields), functions that convert those structs to and from bytes, and — because we also use the `--go-grpc_out` gRPC plugin — a ready-made server interface you must implement (`CalculatorServer`) and a ready-made **client stub** (`CalculatorClient`) whose methods you can call directly (`client.Calculate(...)`), fully wired up to open connections and send bytes for you. This is the command that does it (you'll run it yourself in Part B):

```bash
protoc --go_out=. --go-grpc_out=. calculator.proto
```

Nobody hand-writes the generated files — that's the entire point. Compare this to Part A, where *you* wrote the equivalent of all of that by hand (the request dict, the socket calls, the client wrapper).

### 7. Reading Go for the first time: packages, imports, and modules

Every Go source file starts with a **package** declaration, e.g. `package main` — this says which "namespace" the file's code belongs to; `main` is special and marks a program with a runnable entry point (like Python's `if __name__ == "__main__":`, but mandatory and file-wide rather than a single `if`). Below that, an `import (...)` block lists other packages this file needs, similar to Python's `import` statements:

```go
import (
    "fmt"                       // Go's standard library, like Python's built-ins
    "google.golang.org/grpc"    // a third-party package, identified by a URL-like path
)
```

Go identifies external packages by a path that looks like a web address instead of a short name (contrast with Python's `pip install grpc` + `import grpc`) — the path tells Go's tooling exactly where the package's source code lives online. You won't need to install anything by hand here; the lab's Docker image already has the Go toolchain and the `protoc` plugins pre-installed.

### 8. Reading Go for the first time: functions, structs, methods, and pointers

A few Go syntax landmarks you'll see throughout `server/main.go` and `client/main.go`:

- `func main() { ... }` — an ordinary function declaration. `func functionName(params) returnType { ... }` is the general shape.
- `type server struct { ... }` — a **struct** is Go's way of grouping related data fields together, comparable to a Python class that only holds attributes (no logic of its own yet).
- `func (s *server) Calculate(...) (*calculator.CalcResponse, error) { ... }` — this attaches (or "binds") a function to the `server` struct as a **method**. The `(s *server)` part is called a *receiver* — it plays the same role as Python's implicit `self`, except in Go you must name it and declare its type explicitly.
- `*server` and `&server{}` — Go uses pointers explicitly. `*server` means "a pointer to (the memory address of) a `server` value" rather than a copy of it; `&server{}` means "create a new, empty `server` struct and give me its address." You don't need to master pointers for this lab — just recognize that `*X` and `&X` are two sides of the same "point at this value instead of copying it" idea, which matters here because gRPC needs to call methods on your *actual* struct.

### 9. Go's error-handling style (no exceptions)

Go does not use `try`/`except` the way Python does. Instead, by convention, any function that can fail returns an extra value of type `error` as its **last** return value, and the caller is expected to check it immediately:

```go
lis, err := net.Listen("tcp", port)
if err != nil {
    log.Fatalf("failed to listen: %v", err)
}
```

`err` is `nil` (Go's version of `None`) when nothing went wrong, or a non-`nil` error value describing what failed. This is why you'll see `, err :=` and `if err != nil { ... }` repeated after nearly every operation in the Go files — it's the idiomatic Go equivalent of a `try/except` around every risky call.

### 10. Streaming, contexts/timeouts, and command-line flags in Go

A few more pieces you'll run into directly in the starter code:

- **`context.Context` and timeouts** — a `context.Context` is a small object Go passes alongside a call to carry cancellation/deadline information. `context.WithTimeout(context.Background(), 10*time.Second)` means "give up on this call automatically if it takes longer than 10 seconds" — similar in spirit to hanging up a phone call that's rung too long with no answer.
- **Reading a stream** — for `FibonacciStream`, the client calls `stream.Recv()` repeatedly in a loop, once per value the server sends, until the server signals it's done by returning the special value `io.EOF` ("end of file" — Go's conventional way of saying "there's nothing more to read," not an exception).
- **`flag.String(...)`** — Go's standard-library equivalent of Python's `argparse`. `flag.String("server", "localhost:50051", "gRPC server address")` declares a `--server` command-line flag with a default value and a help string.

---

## What You'll Do

1. **Part A (Python):** Fill in a from-scratch RPC client and server that speak a JSON-over-TCP protocol you define yourself, then call remote functions (`add`, `multiply`, `fibonacci`, `string_reverse`) as if they were local.
2. **Part B (Go):** Generate real gRPC client/server code from a `.proto` file, implement the server side of a `Calculator` service, and call it — including a streaming RPC — from a Go client.

---

## Instructions

### Part A: RPC from Scratch (Python, 25 min)

Open `rpc_server.py` and `rpc_client.py`. Both files already contain the class structure, the docstrings explaining the protocol, and every function you'll register — you're filling in the networking and dispatch logic.

**In `rpc_server.py`:**

1. **`register(name, func)`** — this builds the "menu" of remote functions the server knows how to run. Store `func` in `self.functions` under the key `name` (this is exactly the same idea as `CLUSTER_NODES`/dictionary lookups from earlier labs — a name maps to something callable), and print a line confirming it was registered.
2. **`handle_client(conn, addr)`** — this is the heart of the server. For each line of data received, you need to: parse it as JSON (turning the incoming bytes back into a Python dict — see Concept 2), pull out `"method"`, `"args"`, and `"id"`, look `method` up in `self.functions`, and either call it with `*args` and wrap the return value into a success response, or build an error response if the method name isn't registered. The exact response shapes are given to you in the file's header docstring — match them precisely, since the client checks specific dict keys (`"result"`, `"error"`) on the other end.
3. **`start()`** — this is the same server bootstrap pattern from Lab 01: create a TCP socket, set `SO_REUSEADDR`, `bind`, `listen`, then loop forever `accept()`-ing new connections and spawning a daemon thread per client so multiple clients can be served at once.

**In `rpc_client.py`:**

4. **`call(method, *args)`** — this is the function that makes the illusion work. Build the request dict described in Concept 2, open a fresh TCP socket, `connect()` to the server, send the JSON-encoded request (with a trailing newline), `recv()` the response, parse it back into a dict, close the socket, and finally: if `response["error"]` is set, `raise` an `Exception` with that message; otherwise return `response["result"]`. Note that a brand-new socket is opened for every single call — there's no persistent connection here, unlike gRPC in Part B.

The `__getattr__` method below `call` is already implemented for you — re-read Concept 3 to understand why you don't need to touch it.

**Test it:**
```bash
# Server
docker exec -it ds-python-node1 python3 /app/labs/lab_05_rpc/rpc_server.py

# Client
docker exec -it ds-python-node2 python3 /app/labs/lab_05_rpc/rpc_client.py --host node1
```

### Part B: gRPC with Go (30 min)

`calculator.proto` is already complete — read it alongside Concept 5 above before touching any Go code; it defines the whole contract both the server and client below must honor.

**Setup — generate the Go code from the `.proto` file:**
```bash
docker exec -it ds-go-node1 sh
cd /app/labs/lab_05_rpc/grpc_go/

# Generate Go code from .proto file
protoc --go_out=. --go-grpc_out=. calculator.proto
```

Running this creates a new `calculator` package (folder) next to `server/` and `client/`, containing Go structs and gRPC plumbing generated from the messages and service you just read (see Concept 6). You'll need to import that generated package from both `server/main.go` and `client/main.go` — each file has a `// TODO: Import your generated calculator package` comment with a hint pointing at where it lives.

**In `server/main.go`:**

1. Import the generated `calculator` package (see above).
2. Embed `calculator.UnimplementedCalculatorServer` inside the `server` struct. This is a Go convention for gRPC: if the `.proto` file ever grows new RPCs later, your struct still compiles because the embedded type provides placeholder versions of any method you haven't written yourself.
3. Implement `Calculate` — a commented-out sketch is already in the file showing the shape of the method (receiver, parameters, return types from Concept 8); your job is to un-comment and adapt it so it switches on `req.Operation` (`"add"`, `"subtract"`, `"multiply"`, `"divide"`) and returns the right `CalcResponse`. Notice that division by zero is reported by setting the `Error` *field* on the response, not by returning a Go `error` — that's a deliberate modeling choice in this `.proto`, distinct from the `error` return values discussed in Concept 9.
4. Implement `FibonacciStream` — instead of returning one value, it calls `stream.Send(...)` once per Fibonacci number inside a loop (see Concept 5's explanation of `stream`).
5. Register your implementation with the gRPC server object (`calculator.RegisterCalculatorServer(s, &server{})`) so incoming calls actually get routed to the methods you just wrote.

**Run it:**
```bash
go run server/main.go
```

**In `client/main.go`** (in a second terminal/container):

1. Dial the server with `grpc.Dial(*serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))` — this opens a connection the way `socket.connect()` did in Part A, except the gRPC library manages the socket for you. `insecure.NewCredentials()` explicitly disables transport encryption for this lab; real gRPC deployments normally use TLS instead.
2. Create a `Calculator` client stub from that connection — this generated object is the Go equivalent of Part A's `RPCClient`: calling a method on it (e.g. `client.Calculate(...)`) looks local but goes over the network.
3. Set up a timeout context (see Concept 10) to pass into your calls.
4. Call `Calculate` with a few different `operation` values and print the results.
5. Call `FibonacciStream` and loop over `stream.Recv()`, printing each value, until you get `io.EOF` (see Concept 10).

**Run it:**
```bash
docker exec -it ds-go-node2 sh
cd /app/labs/lab_05_rpc/grpc_go/
go run client/main.go --server go-node1:50051
```

## Checkpoint Questions

1. Call `add(100, 200)` from the Python RPC client (Part A). What shows up in the server's terminal, and why?
2. Call the Go gRPC `Calculate` method from your Go client (Part B). You've now made the exact same *kind* of call — "run this function on another machine" — using two very different implementations. What did you have to write by hand in Part A that `protoc` generated for you in Part B?
3. What happens if you try to call the server while it isn't running? Where in the code would you add retry logic, and why might a real distributed system want to retry a failed RPC automatically instead of giving up immediately?
