from decimal import Decimal


def build_worker_loads(workers, pairs):
    loads = {}
    for worker in workers:
        loads[worker.id] = Decimal("0")
    for task, worker in pairs:
        loads[worker.id] = loads[worker.id] + Decimal(task.estimated_hours)
    return loads


def calculate_metrics(workers, pairs):
    loads = build_worker_loads(workers, pairs)
    values = list(loads.values())

    if not values:
        return {
            "total_duration_hours": Decimal("0"),
            "load_balance_score": Decimal("0"),
            "completed_tasks_count": 0,
            "loads": loads,
        }

    total_duration = values[0]
    min_load = values[0]
    for value in values:
        if value > total_duration:
            total_duration = value
        if value < min_load:
            min_load = value

    load_balance_score = total_duration - min_load

    return {
        "total_duration_hours": total_duration,
        "load_balance_score": load_balance_score,
        "completed_tasks_count": len(pairs),
        "loads": loads,
    }
