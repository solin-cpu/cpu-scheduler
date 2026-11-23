import copy

def read_processes(filename):
    processes = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            name = parts[0]
            arrival = int(parts[1])
            burst = int(parts[2])
            priority = int(parts[3])
            proc_num = int(''.join(filter(str.isdigit, name)))
            processes.append({
                "name": name,
                "num": proc_num,
                "arrival": arrival,
                "burst": burst,
                "priority": priority
            })
    return processes

def run_fcfs(processes):
    procs = sorted(copy.deepcopy(processes), key=lambda p: (p["arrival"], p["num"]))
    current_time = 0
    gantt = []
    for p in procs:
        if current_time < p["arrival"]:
            gantt.append(f"IDLE {current_time}-{p['arrival']}")
            current_time = p["arrival"]
        start = current_time
        finish = start + p["burst"]
        p["finish"] = finish
        p["turnaround"] = finish - p["arrival"]
        p["waiting"] = p["turnaround"] - p["burst"]
        p["response"] = start - p["arrival"]
        gantt.append(f"{p['name']} {start}-{finish}")
        current_time = finish
    return gantt, procs

def run_priority(processes):
    procs = copy.deepcopy(processes)
    n = len(procs)
    completed = 0
    current_time = 0
    gantt = []
    for p in procs:
        p["done"] = False
    while completed < n:
        ready = [p for p in procs if not p["done"] and p["arrival"] <= current_time]
        if not ready:
            next_arrival = min(p["arrival"] for p in procs if not p["done"])
            gantt.append(f"IDLE {current_time}-{next_arrival}")
            current_time = next_arrival
            continue
        chosen = min(ready, key=lambda p: (p["priority"], p["arrival"], p["num"]))
        start = current_time
        finish = start + chosen["burst"]
        chosen["finish"] = finish
        chosen["turnaround"] = finish - chosen["arrival"]
        chosen["waiting"] = chosen["turnaround"] - chosen["burst"]
        chosen["response"] = start - chosen["arrival"]
        chosen["done"] = True
        gantt.append(f"{chosen['name']} {start}-{finish}")
        current_time = finish
        completed += 1
    return gantt, procs

def print_results(title, gantt, procs):
    print(f"\n=== {title} ===")
    print("Gantt: | " + " | ".join(gantt) + " |")
    print(f"{'Proc':<6} {'Finish':<8} {'Turnaround':<12} {'Waiting':<9} {'Response':<9}")
    for p in sorted(procs, key=lambda x: x["num"]):
        print(f"{p['name']:<6} {p['finish']:<8} {p['turnaround']:<12} {p['waiting']:<9} {p['response']:<9}")
    n = len(procs)
    avg_wait = sum(p["waiting"] for p in procs) / n
    avg_turn = sum(p["turnaround"] for p in procs) / n
    avg_resp = sum(p["response"] for p in procs) / n
    print(f"Average: waiting = {avg_wait:.2f}  turnaround = {avg_turn:.2f}  response = {avg_resp:.2f}")
    return avg_wait, avg_turn, avg_resp

def compare_algorithms(fcfs_avg, prio_avg):
    print("\n=== Comparison ===")
    metrics = ["Waiting", "Turnaround", "Response"]
    for i, metric in enumerate(metrics):
        f_val = fcfs_avg[i]
        p_val = prio_avg[i]
        if f_val < p_val:
            print(f"{metric}: FCFS is better ({f_val:.2f} vs {p_val:.2f})")
        elif p_val < f_val:
            print(f"{metric}: Priority is better ({p_val:.2f} vs {f_val:.2f})")
        else:
            print(f"{metric}: Both are equal ({f_val:.2f} vs {p_val:.2f})")

processes = read_processes("input.txt")
fcfs_gantt, fcfs_procs = run_fcfs(processes)
fcfs_avg = print_results("FCFS", fcfs_gantt, fcfs_procs)
prio_gantt, prio_procs = run_priority(processes)
prio_avg = print_results("Priority (Non-Preemptive)", prio_gantt, prio_procs)
compare_algorithms(fcfs_avg, prio_avg)
