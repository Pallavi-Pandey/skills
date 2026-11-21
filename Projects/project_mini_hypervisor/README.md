# Mini Project: Mini Hypervisor Simulator

> **Level:** Beginner | **Time:** 45–60 minutes | **Language:** Python 3.9+ | **Dependencies:** None

Simulate one physical host and the hypervisor (VMM) that manages virtual machines on it, all inside a single Python program. There is no network, no Docker, and no cloud account — just the host's CPU and memory pool, a command prompt, and the VMs you create.

This project is **Module 3 only**. It does not touch Module 1 (networking/RPC) or Module 2 (authentication/auditing) — it is purely about virtualization, resource management, and the VM lifecycle.

## Project Statement

Create a small **Mini Hypervisor** in Python. The program must track a fixed pool of vCPU and memory capacity, let an operator create, start, pause, resume, stop, and delete virtual machines, enforce admission control so a VM cannot be started or created beyond host capacity, and report host utilization.

The aim is not to build a real hypervisor. The aim is to make the ideas from Module 3 — hardware abstraction, vCPU-to-core mapping, overcommitment, the VM lifecycle, templates, and utilization — visible and interactive in one small program.

## What You Need to Do

Complete and demonstrate the following requirements.

| #  | Requirement                                                                                                                  | Where it is implemented                                                         |
| -- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1  | Track total vs. used vCPU and memory for a single simulated host.                                                            | `Hypervisor.__init__`, `TOTAL_VCPU_CAPACITY`, `TOTAL_MEMORY_MB`           |
| 2  | Create a VM with a name, vCPU count, memory size, and an optional disk size.                                                 | `create_vm()`                                                                 |
| 3  | Reject creation if memory capacity is exhausted.                                                                             | `create_vm()`                                                                 |
| 4  | Model the VM lifecycle: created → running → paused → stopped, plus delete.                                                | `start_vm()`, `pause_vm()`, `resume_vm()`, `stop_vm()`, `delete_vm()` |
| 5  | Reject starting/resuming a VM if there isn't enough free vCPU capacity.                                                      | `start_vm()`, `resume_vm()`                                                 |
| 6  | Allow vCPU **overcommitment** up to a configurable ratio above physical cores.                                         | `OVERCOMMIT_RATIO`, `TOTAL_VCPU_CAPACITY`                                   |
| 7  | Release the right resources at the right lifecycle transition (pause releases vCPU only; stop releases vCPU *and* memory). | `pause_vm()`, `stop_vm()`                                                   |
| 8  | Save a VM's resource spec as a reusable template, and create new VMs from it.                                                | `save_template()`, `create_from_template()`                                 |
| 9  | Report host utilization (vCPU % and memory %) on demand.                                                                     | `host_status()`                                                               |
| 10 | Demonstrate CPU scheduling when running VMs outnumber physical cores.                                                        | `tick()`                                                                      |

## Minimum Demonstration

Your final demonstration should show these scenarios:

1. Create three VMs, then start all three so that running vCPU exceeds the physical core count — show `host` reporting the overcommitment, then run `tick` to see some VMs scheduled and others waiting.
2. Pause one running VM and show `host` again — vCPU usage drops but memory usage does not.
3. Attempt to create a VM asking for more memory than is free; the simulator must deny it.
4. Save a VM's spec as a template and create a second VM from that template.
5. Stop and then delete a VM, and show that `host` reports its vCPU and memory fully returned to the pool.

## Deliverables

Submit or show:

- `hypervisor_sim.py`.
- A terminal transcript or screenshots of the five scenarios above.
- A brief explanation (about one paragraph each) of: the difference between a vCPU and a physical core; why pausing a VM releases CPU but not memory; and what overcommitment trades off against CPU ready time.

## What this connects

| Module 3 theory file                                                                                   | Idea used here                                                         |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------- |
| [01 Virtualization Basics](../../module_3/theory/01_virtualization_basics.md)                           | Host, guest, VM, and hypervisor terminology                            |
| [02 HAL and VMM](../../module_3/theory/02_hardware_abstraction_and_vmm.md)                              | The hypervisor as the only layer allowed to allocate/reclaim resources |
| [03 CPU Management](../../module_3/theory/03_cpu_management.md)                                         | vCPU vs. physical core, overcommitment, CPU ready time (`tick`)      |
| [04 Memory Management](../../module_3/theory/04_memory_management.md)                                   | Memory reservation on create, release on stop                          |
| [05 Storage Management](../../module_3/theory/05_storage_management.md)                                 | A simple virtual disk size field per VM                                |
| [09 VM Resource &amp; State Models](../../module_3/theory/09_vm_resource_and_state_models.md)           | `VM` holds a resource spec plus a lifecycle state                    |
| [10 VM Allocation &amp; Template Models](../../module_3/theory/10_vm_allocation_and_template_models.md) | `save_template()` / `create_from_template()`                       |
| [12 VM Lifecycle Model](../../module_3/theory/12_vm_lifecycle_persistence_and_migration.md)             | created → running → paused → stopped → deleted                     |
| [14 Cloud Mathematical Models](../../module_3/theory/14_cloud_mathematical_models.md)                   | Utilization = used capacity / total capacity, shown by `host`        |

## Run it

**Step 1 — go to this folder:**

```bash
cd /Users/pallavi/pallavi_repos/skills/Projects/project_mini_hypervisor
```

**Step 2 — start the program:**

```bash
python3 hypervisor_sim.py
```

You should immediately see:

```text
Mini Hypervisor Simulator (Module 3). Type 'help' for commands.
Physical cores:        4
vCPU admission ceiling: 6 (4 cores x 1.5 overcommit ratio)
vCPU committed (running VMs): 0 / 6  -> utilization 0.0%
Memory reserved:       0 / 8192 MB  -> utilization 0.0%
hypervisor>
```

**Step 3 — type one command at a time, pressing Enter after each, and wait for its reply before typing the next one.** Do not paste several lines at once — type (or paste) one, press Enter, confirm the reply, then move on.

| Type this | You should see |
|---|---|
| `help` | the full list of commands |
| `create web1 2 2048` | `[ok] created web1 ...` |
| `create web2 2 2048` | `[ok] created web2 ...` |
| `create db1 2 2048` | `[ok] created db1 ...` |
| `start web1` | `[ok] started web1 ...` |
| `start web2` | `[ok] started web2 ...` |
| `start db1` | `[ok] started db1 ...` |
| `host` | vCPU 6 / 6 → 100%, plus an overcommit note |
| `tick` | some VMs get a core, one shows `WAITING` |
| `pause web2` | `[ok] paused web2 ...` |
| `host` | vCPU drops to 4 / 6; memory is unchanged |
| `save-template web1 small-web` | `[ok] saved template 'small-web' ...` |
| `create-from-template small-web web3` | `[ok] created web3 ...` |
| `list` | all four VMs and their states |
| `delete web3` | `[ok] deleted 'web3'. ...` |

**Step 4 — exit:**

```text
quit
```

`exit` is **not** a valid command — only `quit` works. `Ctrl+C` force-quits if something goes wrong.

**If a command ever prints "Unrecognized command" when it shouldn't:** stop, press `Ctrl+C`, restart with `python3 hypervisor_sim.py`, and type just that one word by hand (not pasted) to confirm it works in isolation before continuing.

## Commands

| Command                                   | Description                                             |
| ----------------------------------------- | ------------------------------------------------------- |
| `create NAME VCPU MEMORY_MB [DISK_GB]`  | Create a VM (state: `created`)                        |
| `start NAME`                            | Start a VM (state → `running`)                       |
| `pause NAME`                            | Pause a running VM (state → `paused`, vCPU released) |
| `resume NAME`                           | Resume a paused VM (state → `running`)               |
| `stop NAME`                             | Stop a VM; releases vCPU *and* memory                 |
| `delete NAME`                           | Permanently remove a VM                                 |
| `list`                                  | List all VMs and their state                            |
| `host`                                  | Show host capacity and utilization                      |
| `tick`                                  | Simulate one round of CPU scheduling                    |
| `save-template VM_NAME TEMPLATE_NAME`   | Save a VM's spec as a template                          |
| `create-from-template TEMPLATE NEWNAME` | Create a new VM from a saved template                   |
| `templates`                             | List saved templates                                    |
| `help` / `quit`                       | Show commands / leave                                   |

## Things to notice

1. **Admission control happens at two different moments.** Memory is reserved as soon as a VM is *created* (even before it runs), but vCPU is only committed when a VM is *started*. This mirrors how a real hypervisor must keep a VM's memory image resident even while it's powered off, but only needs CPU time while it's actually running.
2. **Overcommitment is a deliberate policy choice**, not a bug: `OVERCOMMIT_RATIO = 1.5` lets the admission ceiling exceed the physical core count, because real workloads rarely all peak at once. The trade-off is visible in `tick`, where more running VMs than cores means some VMs wait.
3. **Pausing and stopping release different things.** Pause only releases vCPU (the VM is still "resident" in memory, ready to resume instantly). Stop releases both vCPU and memory (the VM is fully powered off).
4. **Templates separate "what a VM looks like" from "a specific running instance."** This is the same idea behind real VM images / instance types in a cloud console.

## Suggested extensions

- Add memory **overcommitment** with a ballooning-style warning, similar to the vCPU overcommit ratio.
- Add a `migrate NAME` command that moves a VM's resource reservation to a second simulated host, to illustrate live migration.
- Replace the random `tick` scheduler with a simple round-robin queue that remembers whose turn is next.
- Track and print a running VM's total "CPU ready time" (ticks spent waiting) across multiple `tick` calls.
- Persist VMs and templates to a JSON file so state survives a restart.
