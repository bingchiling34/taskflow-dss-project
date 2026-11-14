from decimal import Decimal

from .common import (
    empty_loads,
    has_all_skills,
    remaining_capacity,
    skill_overlap,
    sort_tasks,
    sort_workers,
)


def allocate_skill_match(tasks, workers):
    ordered_tasks = sort_tasks(tasks)
    ordered_workers = sort_workers(workers)
    if not ordered_workers:
        return []

    loads = empty_loads(ordered_workers)
    pairs = []

    for task in ordered_tasks:
        hours = Decimal(task.estimated_hours)
        candidates = []
        for worker in ordered_workers:
            if remaining_capacity(worker, loads[worker.id]) < hours:
                continue
            candidates.append(worker)

        if not candidates:
            continue

        full_match = []
        for worker in candidates:
            if has_all_skills(worker, task):
                full_match.append(worker)

        if full_match:
            pool = full_match
        else:
            pool = candidates

        best = None
        for worker in pool:
            if best is None:
                best = worker
                continue

            worker_better = False
            if skill_overlap(worker, task) > skill_overlap(best, task):
                worker_better = True
            elif skill_overlap(worker, task) == skill_overlap(best, task):
                if loads[worker.id] < loads[best.id]:
                    worker_better = True
                elif loads[worker.id] == loads[best.id]:
                    if (worker.name, worker.id) < (best.name, best.id):
                        worker_better = True

            if worker_better:
                best = worker

        loads[best.id] = loads[best.id] + hours
        pairs.append((task, best))

    return pairs
