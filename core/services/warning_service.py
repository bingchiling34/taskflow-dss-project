from core.repositories import TaskRepository, WorkerRepository
from core.services.algorithms.common import has_all_skills
from core.services.workload_service import WorkloadService


class WarningService:
    def __init__(self):
        self.tasks = TaskRepository()
        self.workers = WorkerRepository()
        self.workload = WorkloadService()

    def build_for_project(self, project_id):
        if not project_id:
            return []

        workers = self.workers.list_by_project(project_id)
        tasks = self.tasks.list_by_project(project_id)
        warnings = []

        skill_warnings = self._skill_warnings(tasks, workers)
        for item in skill_warnings:
            warnings.append(item)

        load_warnings = self._full_load_warnings(workers)
        for item in load_warnings:
            warnings.append(item)

        return warnings

    def annotate_assignments(self, assignments):
        rows = []
        for item in assignments:
            missing = self._missing_skills(item.worker, item.task)
            rows.append(
                {
                    "assignment": item,
                    "missing_skills": missing,
                    "has_skill_gap": len(missing) > 0,
                }
            )
        return rows

    def _skill_warnings(self, tasks, workers):
        warnings = []
        for task in tasks:
            if task.status == "done":
                continue
            required = task.required_skills or []
            if len(required) == 0:
                continue

            covered = False
            for worker in workers:
                if has_all_skills(worker, task):
                    covered = True
                    break

            if covered:
                continue

            uncovered = []
            for skill in required:
                if not self._team_has_skill(workers, skill):
                    if skill not in uncovered:
                        uncovered.append(skill)

            if len(uncovered) > 0:
                text = (
                    'Task "'
                    + task.title
                    + '": no worker has skills '
                    + ", ".join(uncovered)
                    + "."
                )
            else:
                text = (
                    'Task "'
                    + task.title
                    + '": no single worker has all required skills ('
                    + ", ".join(required)
                    + ")."
                )

            warnings.append(
                {
                    "kind": "skills",
                    "text": text,
                }
            )

        return warnings

    def _full_load_warnings(self, workers):
        warnings = []
        rows = self.workload.build_rows(workers)
        for row in rows:
            if row["level"] != "full":
                continue
            warnings.append(
                {
                    "kind": "full_load",
                    "text": (
                        row["worker"].name
                        + " is fully loaded ("
                        + str(row["percent"])
                        + "%)."
                    ),
                }
            )
        return warnings

    def _team_has_skill(self, workers, skill):
        for worker in workers:
            owned = worker.skills or []
            if skill in owned:
                return True
        return False

    def _missing_skills(self, worker, task):
        missing = []
        required = task.required_skills or []
        owned = worker.skills or []
        for skill in required:
            if skill not in owned:
                missing.append(skill)
        return missing
