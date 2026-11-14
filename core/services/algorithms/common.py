from decimal import Decimal


def sort_tasks(tasks):
    result = list(tasks)
    i = 0
    while i < len(result):
        j = i + 1
        while j < len(result):
            left = result[i]
            right = result[j]
            left_key = (left.priority, left.id)
            right_key = (right.priority, right.id)
            if right_key < left_key:
                result[i] = right
                result[j] = left
            j = j + 1
        i = i + 1
    return result


def sort_workers(workers):
    result = list(workers)
    i = 0
    while i < len(result):
        j = i + 1
        while j < len(result):
            left = result[i]
            right = result[j]
            left_key = (left.name, left.id)
            right_key = (right.name, right.id)
            if right_key < left_key:
                result[i] = right
                result[j] = left
            j = j + 1
        i = i + 1
    return result


def empty_loads(workers):
    loads = {}
    for worker in workers:
        loads[worker.id] = Decimal("0")
    return loads


def skill_overlap(worker, task):
    required = task.required_skills or []
    owned = worker.skills or []
    count = 0
    for skill in required:
        if skill in owned:
            count = count + 1
    return count


def has_all_skills(worker, task):
    required = task.required_skills or []
    owned = worker.skills or []
    for skill in required:
        if skill not in owned:
            return False
    return True


def remaining_capacity(worker, load):
    return Decimal(worker.capacity_hours) - load
