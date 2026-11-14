from core.repositories import (
    AllocationRunRepository,
    ProjectRepository,
    TaskRepository,
    WorkerRepository,
)
from core.repositories.assignment_repository import AssignmentRepository
from core.services.algorithms import ALGORITHM_CHOICES, ALGORITHM_FUNCTIONS
from core.services.allocation_metrics import calculate_metrics


class AllocationService:
    def __init__(self):
        self.projects = ProjectRepository()
        self.workers = WorkerRepository()
        self.tasks = TaskRepository()
        self.runs = AllocationRunRepository()
        self.assignments = AssignmentRepository()

    def list_algorithms(self):
        return ALGORITHM_CHOICES

    def list_runs(self, project_id=None):
        if project_id:
            return self.runs.list_by_project(project_id)
        return self.runs.list_all()

    def get_run(self, run_id):
        return self.runs.get_by_id(run_id)

    def get_run_assignments(self, run_id):
        return self.assignments.list_by_run(run_id)

    def run_algorithm(self, project_id, algorithm_key):
        project = self.projects.get_by_id(project_id)
        if project is None:
            return None, {"project_id": "Selected project was not found."}

        allocate = ALGORITHM_FUNCTIONS.get(algorithm_key)
        if allocate is None:
            return None, {"algorithm": "Unknown algorithm."}

        workers = self.workers.list_by_project(project_id)
        tasks = self.tasks.list_by_project(project_id)
        if not workers:
            return None, {"workers": "Project has no workers."}
        if not tasks:
            return None, {"tasks": "Project has no tasks."}

        pairs = allocate(tasks, workers)
        metrics = calculate_metrics(workers, pairs)
        notes = self._build_notes(algorithm_key, workers, metrics["loads"])

        run = self.runs.create(
            project,
            algorithm_key,
            metrics["total_duration_hours"],
            metrics["load_balance_score"],
            metrics["completed_tasks_count"],
            notes,
        )
        self.assignments.create_many(run, pairs)
        return run, {}

    def run_all_algorithms(self, project_id):
        created = []
        errors = {}
        for key, _label in ALGORITHM_CHOICES:
            run, run_errors = self.run_algorithm(project_id, key)
            if run_errors:
                errors[key] = run_errors
            else:
                created.append(run)
        return created, errors

    def delete_run(self, run):
        self.runs.delete(run)

    def _build_notes(self, algorithm_key, workers, loads):
        lines = ["algorithm=" + algorithm_key]
        for worker in workers:
            lines.append(
                worker.name + "=" + str(loads.get(worker.id, 0)) + "h"
            )
        return "; ".join(lines)
