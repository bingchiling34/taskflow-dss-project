from decimal import Decimal

from core.repositories import AllocationRunRepository
from core.repositories.assignment_repository import AssignmentRepository


class WorkloadService:
    def __init__(self):
        self.runs = AllocationRunRepository()
        self.assignments = AssignmentRepository()

    def build_rows(self, workers):
        rows = []
        latest_run_by_project = {}

        for worker in workers:
            project_id = worker.project_id
            if project_id not in latest_run_by_project:
                latest_run_by_project[project_id] = self.runs.get_latest_by_project(
                    project_id
                )

        hours_by_run_and_worker = {}
        for project_id, run in latest_run_by_project.items():
            if run is None:
                continue
            assignments = self.assignments.list_by_run(run.id)
            hours_map = {}
            for item in assignments:
                worker_id = item.worker_id
                task_hours = Decimal(item.task.estimated_hours)
                if worker_id not in hours_map:
                    hours_map[worker_id] = Decimal("0")
                hours_map[worker_id] = hours_map[worker_id] + task_hours
            hours_by_run_and_worker[run.id] = hours_map

        for worker in workers:
            capacity = Decimal(worker.capacity_hours)
            used = Decimal("0")
            run = latest_run_by_project.get(worker.project_id)
            if run is not None:
                hours_map = hours_by_run_and_worker.get(run.id, {})
                used = hours_map.get(worker.id, Decimal("0"))

            percent = 0
            if capacity > 0:
                percent = int((used * 100) / capacity)

            level = "ok"
            if percent >= 100:
                level = "full"
            elif percent >= 70:
                level = "warn"

            if percent > 100:
                bar_width = 100
            else:
                bar_width = percent

            rows.append(
                {
                    "worker": worker,
                    "used_hours": used,
                    "capacity_hours": capacity,
                    "percent": percent,
                    "level": level,
                    "bar_width": bar_width,
                    "has_run": run is not None,
                }
            )

        return rows

    def build_one(self, worker):
        rows = self.build_rows([worker])
        if not rows:
            return None
        return rows[0]
