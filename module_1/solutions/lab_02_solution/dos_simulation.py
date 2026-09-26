"""Lab 02 - DOS Simulation (SOLUTION)"""

import argparse
import json
import os
import redis


def get_redis():
    return redis.Redis(host="ds-redis", port=6379, decode_responses=True)


def write_shared_memory(key, value):
    r = get_redis()
    r.set(key, value)
    hostname = os.environ.get("HOSTNAME", "unknown")
    print(f"[{hostname}] Wrote: {key} = {value}")
    print(f"  → This is now visible from ANY node (location transparency)")


def read_shared_memory(key):
    r = get_redis()
    value = r.get(key)
    hostname = os.environ.get("HOSTNAME", "unknown")
    if value:
        print(f"[{hostname}] Read: {key} = {value}")
        print(f"  → You didn't specify which node wrote it. That's DOS!")
    else:
        print(f"[{hostname}] Key '{key}' not found in shared memory")


def start_task(task_id, initial_progress):
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")
    task_state = {
        "task_id": task_id,
        "progress": initial_progress,
        "started_on": hostname,
        "data": [i * 2 for i in range(initial_progress, initial_progress + 5)],
    }
    r.set(f"task:{task_id}", json.dumps(task_state))
    print(f"[{hostname}] Started task '{task_id}' with progress={initial_progress}")
    print(f"  → Computed data: {task_state['data']}")
    print(f"  → State saved to shared memory. Any node can resume this task.")


def resume_task(task_id):
    r = get_redis()
    hostname = os.environ.get("HOSTNAME", "unknown")
    raw = r.get(f"task:{task_id}")
    if not raw:
        print(f"[{hostname}] Task '{task_id}' not found!")
        return

    state = json.loads(raw)
    original_node = state["started_on"]
    progress = state["progress"]
    data = state["data"]

    print(f"[{hostname}] Resuming task '{task_id}' (originally started on {original_node})")
    print(f"  → Previous progress: {progress}, data so far: {data}")

    # Continue the computation
    new_start = progress + 5
    new_data = [i * 2 for i in range(new_start, new_start + 5)]
    data.extend(new_data)
    state["progress"] = new_start + 5
    state["data"] = data
    state["resumed_on"] = hostname

    r.set(f"task:{task_id}", json.dumps(state))
    print(f"  → New data computed: {new_data}")
    print(f"  → Total data: {data}")
    print(f"  → PROCESS MIGRATION COMPLETE: {original_node} → {hostname}")


def list_all_keys():
    r = get_redis()
    keys = r.keys("*")
    hostname = os.environ.get("HOSTNAME", "unknown")
    print(f"\n[{hostname}] All keys in shared memory:")
    for key in sorted(keys):
        value = r.get(key)
        display = f"{value[:50]}..." if value and len(value) > 50 else value
        print(f"  {key} = {display}")
    print(f"\nTotal: {len(keys)} keys (visible from ANY node)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["write", "read", "start-task", "resume-task", "list"], required=True)
    parser.add_argument("--key")
    parser.add_argument("--value")
    parser.add_argument("--task-id")
    parser.add_argument("--progress", type=int, default=0)
    args = parser.parse_args()

    actions = {
        "write": lambda: write_shared_memory(args.key, args.value),
        "read": lambda: read_shared_memory(args.key),
        "start-task": lambda: start_task(args.task_id, args.progress),
        "resume-task": lambda: resume_task(args.task_id),
        "list": list_all_keys,
    }
    actions[args.action]()
