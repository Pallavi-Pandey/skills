"""
Lab 02 - DOS Simulation (Starter Code)
=======================================
Simulates a Distributed OS: shared memory via Redis.
Location transparency — you don't know where data lives.

Fill in the TODOs.

Prerequisites: pip install redis
"""

# What each import is for (docs link = where to read more):
#   argparse  -> reads --action/--key/--value/--task-id/--progress from
#                the command line
#                docs: https://docs.python.org/3/library/argparse.html
#   json      -> json.dumps()/json.loads() turn the task_state dict into
#                a string (and back), since Redis only stores strings
#                docs: https://docs.python.org/3/library/json.html
#   time      -> imported but not actually used anywhere in this file —
#                harmless, but a good example that not every import in
#                real code ends up needed
#                docs: https://docs.python.org/3/library/time.html
#   os        -> os.environ.get("HOSTNAME") reads this container's own
#                hostname, just to print which node did what
#                docs: https://docs.python.org/3/library/os.html
#   redis     -> the actual "shared memory": a client library for Redis,
#                a separate container every node can read/write (third-
#                party package, not in Python's standard library)
#                docs: https://redis-py.readthedocs.io/
import argparse
import json
import time
import os
import redis


# Redis acts as our "kernel" — the shared memory layer
# Any node can read/write without knowing where data physically lives
def get_redis():
    """Connect to the shared memory (Redis)."""
    return redis.Redis(host="ds-redis", port=6379, decode_responses=True)


def write_shared_memory(key, value):
    """Write to shared memory. ANY node can call this."""
    r = get_redis()
    # TODO: Use r.set(key, value) to store the value
    # TODO: Print a message showing what was written and from which hostname
    # Hint: os.environ.get("HOSTNAME", "unknown") gives you the hostname
    pass


def read_shared_memory(key):
    """Read from shared memory. ANY node can call this — location transparent."""
    r = get_redis()
    # TODO: Use r.get(key) to retrieve the value
    # TODO: Print the value and which node is reading it
    # NOTE: You did NOT specify which node wrote it. That's transparency!
    pass


def start_task(task_id, initial_progress):
    """
    Start a long-running task and save its state to shared memory.
    This simulates a process that can be migrated to another node.
    """
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")

    task_state = {
        "task_id": task_id,
        "progress": initial_progress,
        "started_on": hostname,
        "data": [i * 2 for i in range(initial_progress, initial_progress + 5)],
    }

    # TODO: Serialize task_state to JSON and store it in Redis with key f"task:{task_id}"
    # TODO: Print that the task started on this node with its current progress
    # Hint: json.dumps(task_state)
    pass


def resume_task(task_id):
    """
    Resume a task that was started on ANOTHER node.
    This simulates process migration — the task state was saved to shared memory.
    """
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")

    # TODO: Retrieve the task state from Redis using key f"task:{task_id}"
    # TODO: Deserialize from JSON
    # TODO: Print that this node is resuming the task (show original node + current progress)
    # TODO: Continue the computation: extend the data list with 5 more values
    # TODO: Update progress and save back to Redis
    # This is process migration — the task moved from one node to another!
    pass


def list_all_keys():
    """Show all keys in shared memory — demonstrates global view."""
    r = get_redis()
    keys = r.keys("*")
    hostname = os.environ.get("HOSTNAME", "unknown")
    print(f"\n[{hostname}] All keys in shared memory:")
    for key in sorted(keys):
        value = r.get(key)
        print(f"  {key} = {value[:50]}..." if value and len(value) > 50 else f"  {key} = {value}")
    print(f"\nTotal: {len(keys)} keys (visible from ANY node — that's DOS!)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOS Shared Memory Simulation")
    parser.add_argument("--action", choices=["write", "read", "start-task", "resume-task", "list"],
                        required=True)
    parser.add_argument("--key", help="Key for read/write")
    parser.add_argument("--value", help="Value for write")
    parser.add_argument("--task-id", help="Task ID for migration")
    parser.add_argument("--progress", type=int, default=0, help="Initial progress")
    args = parser.parse_args()

    if args.action == "write":
        write_shared_memory(args.key, args.value)
    elif args.action == "read":
        read_shared_memory(args.key)
    elif args.action == "start-task":
        start_task(args.task_id, args.progress)
    elif args.action == "resume-task":
        resume_task(args.task_id)
    elif args.action == "list":
        list_all_keys()
