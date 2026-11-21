"""
Mini Hypervisor Simulator — a Module 3 (Virtualization and Cloud Computing) project.

This program simulates ONE physical host and the hypervisor (VMM) that manages
virtual machines on it. It does not use a network, Docker, or any external
service — everything happens inside one Python process, so it is easy to read,
run, and modify in a single class session.

WHICH THEORY FILE EACH PART OF THIS FILE CAME FROM, AND WHY IT'S HERE
----------------------------------------------------------------------
  theory 01 (Virtualization Basics)
      Host / Guest / VM / Hypervisor terminology. Needed so the names in
      this code (Hypervisor, VM, "host capacity") mean the same thing they
      mean in the slides, instead of inventing new vocabulary.

  theory 02 (Hardware Abstraction Layer and VMM)
      The idea that the VMM (hypervisor) is the ONLY layer allowed to map
      virtual resources onto physical ones. Needed so students see *why*
      the Hypervisor class owns used_vcpu/used_memory_mb and no VM object
      ever touches host capacity itself — that's not a style choice, it's
      the real architectural rule.

  theory 03 (CPU Management)
      vCPU vs. physical core, shares/limits, overcommitment, and "CPU ready
      time" (a VM that's runnable but waiting for a free core). Needed to
      explain PHYSICAL_CORES vs. TOTAL_VCPU_CAPACITY, why start_vm() can
      be denied even though create_vm() succeeded, and what tick() is
      demonstrating.

  theory 04 (Memory Management)
      Memory is reserved/released as a simple allocation, no overcommit.
      Needed to explain why create_vm() checks memory immediately but
      start_vm() does not — memory must exist the instant a VM exists.

  theory 05 (Storage Management)
      Each VM also has a (very simplified) virtual disk size. Needed just
      so VMs carry a disk_gb field like a real VM spec would, even though
      this simulator doesn't do anything else with storage.

  theory 09 (VM Resource and State Models)
      A VM is modelled as two things at once: a resource spec (vcpu,
      memory_mb, disk_gb) and a current state. Needed to explain why the
      VM class stores exactly those four fields and nothing else.

  theory 10 (VM Allocation and Template Models)
      A template separates "the shape of a VM" from "one instance of it."
      Needed to explain save_template()/create_from_template().

  theory 12 (VM Lifecycle, Persistence, and Migration Models)
      The state machine created -> running -> paused -> stopped -> deleted,
      and which resources a VM holds in each state. Needed to explain every
      transition method below (start_vm, pause_vm, resume_vm, stop_vm,
      delete_vm) and exactly which resource each one gives back.

  theory 14 (Cloud Mathematical Models)
      Utilization = used capacity / total capacity. Needed to explain the
      percentage math inside host_status().
"""

# `random` is only used by tick() below, to randomly decide which running VMs
# get a physical core this round when there are more VMs than cores.
import random

# ----------------------------------------------------------------------
# Host capacity (the physical machine the hypervisor manages)
# Theory: 03 CPU Management, 04 Memory Management.
#
# These four names are written in ALL CAPS because, by Python convention,
# ALL CAPS means "this is a constant — read it, but never reassign it while
# the program runs." They represent the fixed physical machine the whole
# simulation runs on top of.
# ----------------------------------------------------------------------
PHYSICAL_CORES = 4          # real physical CPU cores available on the host

# Why this constant exists (theory 03): real hypervisors let administrators
# admit more total vCPUs than there are physical cores, betting that not
# every VM will demand 100% CPU at the same instant. That bet is called
# "overcommitment" — it raises utilization but risks "CPU ready time" if the
# bet is wrong and VMs do peak together. 1.5 means "admit up to 50% more
# vCPUs than we have cores for."
OVERCOMMIT_RATIO = 1.5      # how many vCPUs we allow to be admitted per physical core

# The admission ceiling: how many TOTAL vCPUs we're willing to let VMs claim,
# even though there are only PHYSICAL_CORES real cores underneath. Multiplying
# by OVERCOMMIT_RATIO (1.5) means 4 cores can admit up to 6 vCPUs, because real
# workloads rarely all peak their CPU at the exact same moment. int(...) rounds
# the result down to a whole number, since you can't have half a vCPU slot.
TOTAL_VCPU_CAPACITY = int(PHYSICAL_CORES * OVERCOMMIT_RATIO)   # admission ceiling

TOTAL_MEMORY_MB = 8192      # physical RAM, in megabytes, that the hypervisor can hand out


class VM:
    """One virtual machine: a resource request plus a lifecycle state.

    Theory: 09 VM Resource and State Models (this class IS that model —
    a resource spec of vcpu/memory_mb/disk_gb, plus a `state` field),
    05 Storage Management (the disk_gb field)."""

    def __init__(self, name, vcpu, memory_mb, disk_gb):
        # __init__ runs once, automatically, every time someone writes VM(...).
        # Each parameter becomes an attribute stored on "self" (this particular
        # VM object), so other methods and print statements can read vm.name,
        # vm.vcpu, and so on later.
        self.name = name
        self.vcpu = vcpu
        self.memory_mb = memory_mb
        self.disk_gb = disk_gb
        # Lifecycle Management Model: created -> running -> paused -> stopped -> (deleted)
        # Every VM starts life in the "created" state — it exists and has
        # reserved memory, but it has not been started yet.
        self.state = "created"

    def __str__(self):
        # __str__ controls what text appears when you do print(some_vm) or
        # f"{some_vm}". Here it formats the VM's fields into one aligned,
        # human-readable line, e.g.:
        #   web1         state=running   vcpu=2   memory=2048  MB disk=10GB
        # The ":<12" / ":<9" / ":<3" / ":<6" parts are string-formatting
        # instructions meaning "pad this value with spaces on the right until
        # it's at least that many characters wide," purely so columns line up
        # neatly when several VMs are printed one after another.
        return (f"{self.name:<12} state={self.state:<9} "
                f"vcpu={self.vcpu:<3} memory={self.memory_mb:<6}MB disk={self.disk_gb}GB")


class Hypervisor:
    """The VMM: the only thing allowed to hand out or reclaim host resources.

    Theory: 02 Hardware Abstraction Layer and VMM. A real VMM is the sole
    layer that maps virtual resources (what a guest thinks it has) onto
    physical ones (what the host actually has); a guest never touches
    hardware directly. Every method below exists to enforce that same rule
    in software: only Hypervisor methods ever change used_vcpu/used_memory_mb."""

    def __init__(self):
        # This runs once, when we create the single Hypervisor object in main().
        self.vms = {}            # maps a VM's name (str) -> its VM object
        self.templates = {}      # maps a template name (str) -> (vcpu, memory_mb, disk_gb)
        self.used_vcpu = 0        # vCPU currently committed to RUNNING vms
        self.used_memory_mb = 0   # memory currently reserved (created/running/paused vms)
        # Note that no individual VM ever touches used_vcpu or used_memory_mb
        # directly — only the Hypervisor's own methods do. That mirrors the
        # real rule that a guest OS never manages physical hardware directly;
        # it always goes through the VMM.

    # -------------------- admission control --------------------
    # Theory: 03 CPU Management (the vCPU half) and 04 Memory Management
    # (the memory half). "Admission control" means: before letting an
    # action happen, check whether the host actually has enough spare
    # capacity for it — this is what stops a hypervisor from promising more
    # than the physical machine can deliver.

    def _free_vcpu(self):
        # The leading underscore is a Python convention meaning "this is an
        # internal helper, not meant to be called from outside this class."
        # It simply returns how many vCPUs are still unclaimed.
        return TOTAL_VCPU_CAPACITY - self.used_vcpu

    def _free_memory(self):
        # Same idea, but for memory: total capacity minus whatever is
        # currently reserved by existing VMs.
        return TOTAL_MEMORY_MB - self.used_memory_mb

    # -------------------- lifecycle operations --------------------
    # Theory: 12 VM Lifecycle, Persistence, and Migration Models. Each of the
    # next five methods implements one arrow in the lifecycle diagram:
    # created -> running -> paused -> stopped -> (deleted). Pay attention to
    # *which* resource (vCPU, memory, or both) each method releases or
    # claims — that's the actual content of the lifecycle model, not just
    # the state names.

    def create_vm(self, name, vcpu, memory_mb, disk_gb=10):
        # Theory 09 (VM Resource Model) + 05 (Storage Management): this is
        # where a VM's resource spec (vcpu, memory_mb, disk_gb) is captured.
        # disk_gb=10 is a *default argument*: if the caller doesn't supply a
        # disk size, 10 GB is used automatically.
        if name in self.vms:
            # Refuse to silently overwrite an existing VM of the same name.
            print(f"[denied] a VM named '{name}' already exists.")
            return
        if memory_mb > self._free_memory():
            # Admission control: a brand-new VM reserves its memory the
            # moment it's created (even before it's ever started), because a
            # real VM's memory image has to exist somewhere regardless of
            # whether the VM is powered on.
            print(f"[denied] not enough memory: need {memory_mb}MB, "
                  f"only {self._free_memory()}MB free.")
            return
        vm = VM(name, vcpu, memory_mb, disk_gb)   # build the new VM object
        self.vms[name] = vm                        # register it by name
        self.used_memory_mb += memory_mb   # memory is reserved as soon as the VM exists
        print(f"[ok] created {vm}")   # {vm} calls VM.__str__ automatically

    def start_vm(self, name):
        vm = self._get(name)   # look the VM up by name (helper defined below)
        if vm is None:
            # _get() already printed a "[denied] no such VM" message, so we
            # just stop here — there is nothing valid left to do.
            return
        if vm.state == "running":
            print(f"[info] '{name}' is already running.")
            return
        if vm.vcpu > self._free_vcpu():
            # This is the other half of admission control: vCPU is only
            # checked and claimed at START time, not at creation time —
            # because only a RUNNING VM actually needs CPU time.
            print(f"[denied] not enough vCPU capacity: need {vm.vcpu}, "
                  f"only {self._free_vcpu()} free out of {TOTAL_VCPU_CAPACITY} "
                  f"(admission ceiling = {PHYSICAL_CORES} cores x {OVERCOMMIT_RATIO}).")
            return
        vm.state = "running"
        self.used_vcpu += vm.vcpu
        print(f"[ok] started {vm}")

    def pause_vm(self, name):
        vm = self._get(name)
        if vm is None:
            return
        if vm.state != "running":
            # You can only pause a VM that is currently running.
            print(f"[denied] '{name}' is not running (state={vm.state}).")
            return
        vm.state = "paused"
        self.used_vcpu -= vm.vcpu   # a paused VM keeps its memory image but needs no CPU time
        # Notice self.used_memory_mb is NOT touched here — that's the whole
        # teaching point of "pause": the VM's memory image stays resident so
        # it can resume instantly, only its CPU claim is released.
        print(f"[ok] paused {vm}  (vCPU released back to the pool; memory still reserved)")

    def resume_vm(self, name):
        vm = self._get(name)
        if vm is None:
            return
        if vm.state != "paused":
            print(f"[denied] '{name}' is not paused (state={vm.state}).")
            return
        if vm.vcpu > self._free_vcpu():
            # Resuming re-claims vCPU, so it must pass admission control
            # again — the host might have filled up with other VMs while
            # this one was paused.
            print(f"[denied] not enough vCPU capacity to resume '{name}' right now.")
            return
        vm.state = "running"
        self.used_vcpu += vm.vcpu
        print(f"[ok] resumed {vm}")

    def stop_vm(self, name):
        vm = self._get(name)
        if vm is None:
            return
        if vm.state in ("stopped",):
            # A one-item tuple here works the same as vm.state == "stopped";
            # written this way so it's easy to add more "already-done" states
            # later without changing the comparison style.
            print(f"[info] '{name}' is already stopped.")
            return
        if vm.state == "running":
            # Only give back vCPU if the VM currently holds any (a paused VM
            # already gave its vCPU back, so there's nothing to subtract).
            self.used_vcpu -= vm.vcpu
        self.used_memory_mb -= vm.memory_mb   # stopping releases the memory image too
        vm.state = "stopped"
        print(f"[ok] stopped {vm}  (vCPU and memory released back to the pool)")

    def delete_vm(self, name):
        vm = self._get(name)
        if vm is None:
            return
        if vm.state == "running":
            # If it's still running, its vCPU hasn't been released yet, so
            # release it now as part of deletion.
            self.used_vcpu -= vm.vcpu
        if vm.state != "stopped":
            # If it was never stopped first, its memory is still reserved —
            # release that too. (A "stopped" VM already gave its memory back
            # in stop_vm(), so we must not subtract it twice.)
            self.used_memory_mb -= vm.memory_mb
        del self.vms[name]   # remove the VM's entry from the dictionary entirely
        print(f"[ok] deleted '{name}'. Resources fully returned to the host pool.")

    # -------------------- templates (Template Model) --------------------
    # Theory: 10 VM Allocation and Template Models. A template separates
    # "what a VM looks like" (its vcpu/memory/disk spec) from "one specific
    # running instance" of that spec — the same idea as a cloud provider's
    # saved machine image or instance type.

    def save_template(self, vm_name, template_name):
        vm = self._get(vm_name)
        if vm is None:
            return
        # Store just the three numbers that describe the VM's shape, as a
        # tuple, keyed by the template's name.
        self.templates[template_name] = (vm.vcpu, vm.memory_mb, vm.disk_gb)
        print(f"[ok] saved template '{template_name}' = "
              f"vcpu={vm.vcpu}, memory={vm.memory_mb}MB, disk={vm.disk_gb}GB")

    def create_from_template(self, template_name, new_vm_name):
        if template_name not in self.templates:
            print(f"[denied] no such template '{template_name}'. Use 'templates' to list them.")
            return
        # Unpack the stored tuple back into three separate variables...
        vcpu, memory_mb, disk_gb = self.templates[template_name]
        # ...and hand them straight to create_vm(), so a template-based VM
        # goes through exactly the same admission control as any other.
        self.create_vm(new_vm_name, vcpu, memory_mb, disk_gb)

    # -------------------- visibility / reporting --------------------

    def list_vms(self):
        if not self.vms:
            # An empty dict is "falsy" in Python, so "not self.vms" is True
            # when there are no VMs at all.
            print("(no virtual machines yet)")
            return
        for vm in self.vms.values():
            print(vm)   # again, this calls VM.__str__ for each VM

    def list_templates(self):
        if not self.templates:
            print("(no templates saved yet)")
            return
        for name, (vcpu, mem, disk) in self.templates.items():
            # .items() gives us (key, value) pairs; here we immediately
            # unpack the value tuple into vcpu/mem/disk for easy printing.
            print(f"{name:<12} vcpu={vcpu:<3} memory={mem:<6}MB disk={disk}GB")

    def host_status(self):
        # Theory: 14 Cloud Mathematical Models (the utilization percentages)
        # and 03 CPU Management (the overcommitment note below).
        # How many vCPUs are committed right now by VMs that are actually
        # RUNNING (paused/created/stopped VMs don't count toward CPU use).
        running_vcpu = sum(vm.vcpu for vm in self.vms.values() if vm.state == "running")

        # Utilization = used capacity / total capacity, expressed as a
        # percentage — this is the Cloud Mathematical Models idea from
        # theory file 14, applied to both vCPU and memory.
        vcpu_util = (self.used_vcpu / TOTAL_VCPU_CAPACITY) * 100
        mem_util = (self.used_memory_mb / TOTAL_MEMORY_MB) * 100

        print(f"Physical cores:        {PHYSICAL_CORES}")
        print(f"vCPU admission ceiling: {TOTAL_VCPU_CAPACITY} "
              f"({PHYSICAL_CORES} cores x {OVERCOMMIT_RATIO} overcommit ratio)")
        print(f"vCPU committed (running VMs): {running_vcpu} / {TOTAL_VCPU_CAPACITY}"
              f"  -> utilization {vcpu_util:.1f}%")
        print(f"Memory reserved:       {self.used_memory_mb} / {TOTAL_MEMORY_MB} MB"
              f"  -> utilization {mem_util:.1f}%")

        if running_vcpu > PHYSICAL_CORES:
            # This is the overcommitment warning: more vCPUs are running
            # than there are physical cores to run them on simultaneously,
            # so the hypervisor must time-slice between them.
            print(f"[note] {running_vcpu} vCPUs are running on only {PHYSICAL_CORES} physical "
                  f"cores. The hypervisor must time-slice them, so some VMs may experience "
                  f"'CPU ready time' (runnable but waiting for a core).")

    def tick(self):
        """A tiny illustration of CPU scheduling when vCPUs outnumber physical cores.

        Theory: 03 CPU Management — specifically "CPU ready time": a VM that
        is runnable (state=running) but has no physical core free for it
        this instant, so it must wait for the hypervisor's scheduler."""
        # Build a list of only the VMs that are currently running — paused,
        # created, or stopped VMs don't need a core this round.
        running = [vm for vm in self.vms.values() if vm.state == "running"]
        if not running:
            print("(no running VMs to schedule)")
            return
        if len(running) <= PHYSICAL_CORES:
            # Easy case: there's a free physical core for every running VM,
            # so nobody has to wait.
            print("Every running VM gets its own physical core this tick:")
            for vm in running:
                print(f"  core assigned -> {vm.name}")
            return
        # More running VMs than cores: round-robin a random subset onto the cores.
        # random.sample picks PHYSICAL_CORES distinct VMs at random to represent
        # "whoever the scheduler picked this round."
        scheduled = random.sample(running, PHYSICAL_CORES)
        # Everyone else who is running but didn't get picked is left waiting
        # this round — that waiting time is what real hypervisors call
        # "CPU ready time."
        waiting = [vm for vm in running if vm not in scheduled]
        print(f"Only {PHYSICAL_CORES} physical cores for {len(running)} running VMs this tick:")
        for vm in scheduled:
            print(f"  core assigned -> {vm.name}")
        for vm in waiting:
            print(f"  WAITING (CPU ready time) -> {vm.name}")

    # -------------------- helpers --------------------

    def _get(self, name):
        # A small shared lookup used by every lifecycle method above, so the
        # "VM not found" error message and behaviour is written in one place
        # instead of being repeated in start_vm, pause_vm, stop_vm, etc.
        vm = self.vms.get(name)   # dict.get returns None instead of raising
        # an error when the key doesn't exist, which is exactly what we want
        # here — we handle the "missing VM" case ourselves below.
        if vm is None:
            print(f"[denied] no such VM '{name}'.")
        return vm


# A plain multi-line string (triple-quoted) holding the help text shown when
# someone types "help" at the prompt. Defining it once up here, instead of
# inside main(), keeps main()'s command loop shorter and easier to read.
HELP_TEXT = """
Commands:
  create NAME VCPU MEMORY_MB [DISK_GB]   Create a VM (state: created)
  start NAME                             Start a VM (state -> running)
  pause NAME                             Pause a running VM (state -> paused)
  resume NAME                            Resume a paused VM (state -> running)
  stop NAME                              Stop a VM, releasing vCPU + memory
  delete NAME                            Permanently remove a VM
  list                                   List all VMs and their state
  host                                   Show host capacity and utilization
  tick                                   Simulate one round of CPU scheduling
  save-template VM_NAME TEMPLATE_NAME    Save a VM's spec as a template
  create-from-template TEMPLATE NEWNAME  Create a new VM from a saved template
  templates                              List saved templates
  help                                   Show this help
  quit                                   Exit
"""


def main():
    # Create the one and only Hypervisor object for this run of the program.
    # Everything typed at the prompt below operates on this single object.
    hv = Hypervisor()
    print("Mini Hypervisor Simulator (Module 3). Type 'help' for commands.")
    hv.host_status()   # show the starting capacity (0 used, out of the totals) immediately

    # This is the main command loop: it runs forever (while True) until an
    # explicit "quit" or Ctrl+D ends it.
    while True:
        try:
            # input(...) prints its argument as a prompt, then waits for the
            # user to type a line and press Enter. .strip() removes any
            # leading/trailing spaces or the newline character.
            line = input("hypervisor> ").strip()
        except EOFError:
            # Ctrl+D (end-of-file) raises EOFError from input(); treat that
            # the same as typing "quit" — just leave the loop.
            break

        if not line:
            # An empty line (the user just pressed Enter): skip straight back
            # to the top of the loop and prompt again, instead of treating it
            # as an unrecognized command.
            continue

        # Split "create web1 2 2048" into ["create", "web1", "2", "2048"].
        parts = line.split()
        # The first word is the command name (lower-cased so "Create"/"create"
        # both work); everything after it is the list of arguments.
        cmd, args = parts[0].lower(), parts[1:]

        # One big if/elif chain: figure out which command was typed, check it
        # has the right number of arguments, and call the matching Hypervisor
        # method. Every branch below converts text arguments (args is always
        # a list of strings) into the right type, e.g. int(args[1]) for a
        # vCPU count, before handing them to the Hypervisor.
        if cmd == "quit":
            break   # leave the while-loop, which ends main()
        elif cmd == "help":
            print(HELP_TEXT)
        elif cmd == "create" and len(args) >= 3:
            # args[0]=name, args[1]=vcpu, args[2]=memory_mb, optional args[3]=disk_gb
            disk = int(args[3]) if len(args) > 3 else 10
            hv.create_vm(args[0], int(args[1]), int(args[2]), disk)
        elif cmd == "start" and len(args) == 1:
            hv.start_vm(args[0])
        elif cmd == "pause" and len(args) == 1:
            hv.pause_vm(args[0])
        elif cmd == "resume" and len(args) == 1:
            hv.resume_vm(args[0])
        elif cmd == "stop" and len(args) == 1:
            hv.stop_vm(args[0])
        elif cmd == "delete" and len(args) == 1:
            hv.delete_vm(args[0])
        elif cmd == "list":
            hv.list_vms()
        elif cmd == "host":
            hv.host_status()
        elif cmd == "tick":
            hv.tick()
        elif cmd == "save-template" and len(args) == 2:
            hv.save_template(args[0], args[1])
        elif cmd == "create-from-template" and len(args) == 2:
            hv.create_from_template(args[0], args[1])
        elif cmd == "templates":
            hv.list_templates()
        else:
            # Reached only if cmd didn't match any branch above, OR it
            # matched a command name but with the wrong number of arguments
            # (e.g. typing "start" with no VM name).
            print("Unrecognized command. Type 'help' for the list of commands.")


# This check is a standard Python idiom: the code inside only runs when this
# file is executed directly (python3 hypervisor_sim.py), not if it were ever
# imported from another file as a module.
if __name__ == "__main__":
    main()
