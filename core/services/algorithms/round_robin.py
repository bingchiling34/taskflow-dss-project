from decimal import Decimal

from .common import empty_loads, remaining_capacity, sort_tasks, sort_workers


def allocate_round_robin(tasks, workers):
    ordered_tasks = sort_tasks(tasks)
    ordered_workers = sort_workers(workers)
    if not ordered_workers:
        return []

    loads = empty_loads(ordered_workers)
    pairs = []
    index = 0

    for task in ordered_tasks:
        assigned = None
        for _ in range(len(ordered_workers)):
            worker = ordered_workers[index % len(ordered_workers)]
            index += 1
            hours = Decimal(task.estimated_hours)
            if remaining_capacity(worker, loads[worker.id]) >= hours:
                assigned = worker
                loads[worker.id] = loads[worker.id] + hours
                break
        if assigned is not None:
            pairs.append((task, assigned))

    return pairs
