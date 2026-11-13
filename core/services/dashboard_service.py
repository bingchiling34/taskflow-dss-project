from core.repositories import (
    AllocationRunRepository,
    ProjectRepository,
    TaskRepository,
    WorkerRepository,
)


class DashboardService:
    def __init__(self):
        self.projects = ProjectRepository()
        self.workers = WorkerRepository()
        self.tasks = TaskRepository()
        self.allocation_runs = AllocationRunRepository()

    def get_overview(self):
        data = {}
        data["project_count"] = self.projects.count()
        data["worker_count"] = self.workers.count()
        data["task_count"] = self.tasks.count()
        data["allocation_run_count"] = self.allocation_runs.count()
        return data
