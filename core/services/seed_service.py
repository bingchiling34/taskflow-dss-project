from core.models import Project
from core.services.project_service import ProjectService
from core.services.task_service import TaskService
from core.services.worker_service import WorkerService


class SeedService:
    DEMO_PROJECT_NAME = "Demo Allocation Project"

    def __init__(self):
        self.projects = ProjectService()
        self.workers = WorkerService()
        self.tasks = TaskService()

    def seed(self, force=False):
        existing = Project.objects.filter(name=self.DEMO_PROJECT_NAME).first()
        if existing is not None:
            if force is False:
                return {
                    "created": False,
                    "project": existing,
                    "message": "Demo project already exists. Use --force to recreate.",
                }
            self.projects.delete_project(existing)

        project, errors = self.projects.create_project(
            self.DEMO_PROJECT_NAME,
            "Seeded demo data for allocation algorithm comparison.",
            "active",
        )
        if errors:
            return {"created": False, "project": None, "message": str(errors)}

        worker_count = 0
        for item in self._worker_rows():
            worker, worker_errors = self.workers.create_worker(
                project.id,
                item["name"],
                item["skills"],
                item["capacity_hours"],
            )
            if worker_errors:
                return {
                    "created": False,
                    "project": project,
                    "message": "Worker error: " + str(worker_errors),
                }
            worker_count += 1

        task_count = 0
        for item in self._task_rows():
            task, task_errors = self.tasks.create_task(
                project.id,
                item["title"],
                item["description"],
                item["skills"],
                item["estimated_hours"],
                item["priority"],
                item["status"],
            )
            if task_errors:
                return {
                    "created": False,
                    "project": project,
                    "message": "Task error: " + str(task_errors),
                }
            task_count += 1

        return {
            "created": True,
            "project": project,
            "worker_count": worker_count,
            "task_count": task_count,
            "message": "Demo data loaded.",
        }

    def _worker_rows(self):
        return [
            {
                "name": "Anna Kowalska",
                "skills": "python, django, sql",
                "capacity_hours": "40",
            },
            {
                "name": "Piotr Wisniewski",
                "skills": "javascript, react, css",
                "capacity_hours": "35",
            },
            {
                "name": "Marta Zielinska",
                "skills": "python, api, sql",
                "capacity_hours": "30",
            },
            {
                "name": "Tomasz Nowak",
                "skills": "react, javascript, ui",
                "capacity_hours": "40",
            },
        ]

    def _task_rows(self):
        return [
            {
                "title": "Setup Django backend",
                "description": "Create Django project structure and settings.",
                "skills": "python, django",
                "estimated_hours": "8",
                "priority": "1",
                "status": "todo",
            },
            {
                "title": "Design REST API",
                "description": "Define endpoints for projects and tasks.",
                "skills": "python, api",
                "estimated_hours": "6",
                "priority": "1",
                "status": "todo",
            },
            {
                "title": "Build login page",
                "description": "Implement frontend login form.",
                "skills": "javascript, react",
                "estimated_hours": "5",
                "priority": "2",
                "status": "todo",
            },
            {
                "title": "Create dashboard UI",
                "description": "Build dashboard layout and widgets.",
                "skills": "react, css",
                "estimated_hours": "8",
                "priority": "2",
                "status": "todo",
            },
            {
                "title": "Database schema and queries",
                "description": "Prepare SQL queries and indexes.",
                "skills": "sql, python",
                "estimated_hours": "4",
                "priority": "3",
                "status": "todo",
            },
            {
                "title": "Write integration tests",
                "description": "Cover main allocation flows with tests.",
                "skills": "python, django",
                "estimated_hours": "6",
                "priority": "3",
                "status": "todo",
            },
            {
                "title": "Landing page polish",
                "description": "Improve visual details on landing page.",
                "skills": "css, ui",
                "estimated_hours": "3",
                "priority": "4",
                "status": "todo",
            },
        ]
