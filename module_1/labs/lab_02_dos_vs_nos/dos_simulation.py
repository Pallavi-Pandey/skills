import argparse
import json
import os
import redis


def get_redis():
    """Connect to the shared Redis memory."""
    return redis.Redis(
        host="ds-redis",
        port=6379,
        decode_responses=True,
    )


def write_shared_memory(key, value):
    """Write a value that any node can access."""
    r = get_redis()
    r.set(key, value)
    hostname = os.environ.get("HOSTNAME", "unknown")
    print(f"[{hostname}] Wrote key '{key}' = '{value}' to shared memory")


def read_shared_memory(key):
    """Read a value without specifying which node stores it."""
    r = get_redis()
    value = r.get(key)
    hostname = os.environ.get("HOSTNAME", "unknown")

    if value is None:
        print(f"[{hostname}] Key '{key}' was not found")
    else:
        print(f"[{hostname}] Read key '{key}' = '{value}' from shared memory")


def start_task(task_id, initial_progress):
    """Save a task's state so another node can resume it."""
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")

    task_state = {
        "task_id": task_id,
        "progress": initial_progress,
        "started_on": hostname,
        "data": [i * 2 for i in range(initial_progress, initial_progress + 5)],
    }

    r.set(f"task:{task_id}", json.dumps(task_state))
    print(
        f"[{hostname}] Started task '{task_id}' "
        f"with progress {task_state['progress']}"
    )


def resume_task(task_id):
    """Load and continue a task saved by another node."""
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")

    saved_state = r.get(f"task:{task_id}")
    if saved_state is None:
        print(f"[{hostname}] Task '{task_id}' was not found")
        return

    task_state = json.loads(saved_state)

    print(
        f"[{hostname}] Resuming task '{task_id}', "
        f"originally started on {task_state['started_on']}, "
        f"current progress {task_state['progress']}"
    )

    start_progress = task_state["progress"]
    task_state["data"].extend(
        i * 2 for i in range(start_progress + 5, start_progress + 10)
    )
    task_state["progress"] += 5

    r.set(f"task:{task_id}", json.dumps(task_state))
    print(
        f"[{hostname}] Task '{task_id}' continued. "
        f"New progress: {task_state['progress']}"
    )


def list_all_keys():
    """List all keys visible through shared Redis memory."""
    r = get_redis()
    keys = r.keys("*")
    hostname = os.environ.get("HOSTNAME", "unknown")

    print(f"\n[{hostname}] All keys in shared memory:")
    for key in sorted(keys):
        value = r.get(key)
        print(
            f"  {key} = {value[:50]}..."
            if value and len(value) > 50
            else f"  {key} = {value}"
        )
    print(f"\nTotal: {len(keys)} keys (visible from ANY node)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DOS Shared Memory Simulation")
    parser.add_argument(
        "--action",
        choices=["write", "read", "start-task", "resume-task", "list"],
        required=True,
    )
    parser.add_argument("--key", help="Key for read/write")
    parser.add_argument("--value", help="Value for write")
    parser.add_argument("--task-id", help="Task ID for migration")
    parser.add_argument("--progress", type=int, default=0, help="Initial progress")
    args = parser.parse_args()

    if args.action == "write":
        if args.key is None or args.value is None:
            parser.error("--action write requires --key and --value")
        write_shared_memory(args.key, args.value)
    elif args.action == "read":
        if args.key is None:
            parser.error("--action read requires --key")
        read_shared_memory(args.key)
    elif args.action == "start-task":
        if args.task_id is None:
            parser.error("--action start-task requires --task-id")
        start_task(args.task_id, args.progress)
    elif args.action == "resume-task":
        if args.task_id is None:
            parser.error("--action resume-task requires --task-id")
        resume_task(args.task_id)
    elif args.action == "list":
        list_all_keys()
