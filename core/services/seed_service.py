from datetime import timedelta

from django.utils import timezone

from core.models import Project
from core.services.project_service import ProjectService
from core.services.task_service import TaskService
from core.services.worker_service import WorkerService


class SeedService:
    DEMO_PROJECT_NAME = "Portal e-commerce Krakow"

    def __init__(self):
        self.projects = ProjectService()
        self.workers = WorkerService()
        self.tasks = TaskService()

    def seed(self, force=False):
        project_rows = self._project_rows()
        names = []
        for project_data in project_rows:
            names.append(project_data["name"])

        existing_any = Project.objects.filter(name__in=names).first()
        if existing_any is not None and force is False:
            return {
                "created": False,
                "project": existing_any,
                "message": "Demo data already exists. Use --force to recreate.",
            }

        if force is True:
            for name in names:
                existing = Project.objects.filter(name=name).first()
                if existing is not None:
                    self.projects.delete_project(existing)

        created_projects = []
        total_workers = 0
        total_tasks = 0

        for project_data in project_rows:
            project, errors = self.projects.create_project(
                project_data["name"],
                project_data["description"],
                project_data["status"],
            )
            if errors:
                return {"created": False, "project": None, "message": str(errors)}

            for item in project_data["workers"]:
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
                total_workers = total_workers + 1

            for item in project_data["tasks"]:
                due_date = self._due_date_text(item.get("due_in_days"))
                task, task_errors = self.tasks.create_task(
                    project.id,
                    item["title"],
                    item["description"],
                    item["skills"],
                    item["estimated_hours"],
                    item["priority"],
                    item["status"],
                    due_date,
                )
                if task_errors:
                    return {
                        "created": False,
                        "project": project,
                        "message": "Task error: " + str(task_errors),
                    }
                total_tasks = total_tasks + 1

            created_projects.append(project)

        return {
            "created": True,
            "project": created_projects[0],
            "worker_count": total_workers,
            "task_count": total_tasks,
            "message": "Demo data loaded ("
            + str(len(created_projects))
            + " projects).",
        }

    def _due_date_text(self, due_in_days):
        if due_in_days is None:
            return ""
        due = timezone.localdate() + timedelta(days=int(due_in_days))
        return due.isoformat()

    def _project_rows(self):
        return [
            {
                "name": self.DEMO_PROJECT_NAME,
                "description": (
                    "Online store for a local retail chain. "
                    "Backend in Django, storefront in React."
                ),
                "status": "active",
                "workers": [
                    {
                        "name": "Anna Kowalska",
                        "skills": "python, django, sql, api",
                        "capacity_hours": "40",
                    },
                    {
                        "name": "Piotr Wisniewski",
                        "skills": "javascript, react, css, ui",
                        "capacity_hours": "36",
                    },
                    {
                        "name": "Marta Zielinska",
                        "skills": "python, api, sql, testing",
                        "capacity_hours": "32",
                    },
                    {
                        "name": "Tomasz Nowak",
                        "skills": "react, javascript, ui, css",
                        "capacity_hours": "40",
                    },
                    {
                        "name": "Kasia Lewandowska",
                        "skills": "sql, python, django",
                        "capacity_hours": "28",
                    },
                ],
                "tasks": [
                    {
                        "title": "Configure Django project and environments",
                        "description": "Create project skeleton, settings for local and staging.",
                        "skills": "python, django",
                        "estimated_hours": "6",
                        "priority": "1",
                        "status": "todo",
                        "due_in_days": 2,
                    },
                    {
                        "title": "Design product and order API",
                        "description": "REST endpoints for catalog, cart and checkout.",
                        "skills": "python, api, django",
                        "estimated_hours": "10",
                        "priority": "1",
                        "status": "todo",
                        "due_in_days": 5,
                    },
                    {
                        "title": "Build product list page",
                        "description": "React catalog with filters and pagination.",
                        "skills": "javascript, react, css",
                        "estimated_hours": "8",
                        "priority": "2",
                        "status": "todo",
                        "due_in_days": 7,
                    },
                    {
                        "title": "Implement checkout form",
                        "description": "Customer data form, validation and order submit.",
                        "skills": "react, javascript, ui",
                        "estimated_hours": "7",
                        "priority": "2",
                        "status": "todo",
                        "due_in_days": 9,
                    },
                    {
                        "title": "Prepare PostgreSQL schema",
                        "description": "Tables for products, stock, customers and orders.",
                        "skills": "sql, python",
                        "estimated_hours": "5",
                        "priority": "1",
                        "status": "todo",
                        "due_in_days": 3,
                    },
                    {
                        "title": "Write API integration tests",
                        "description": "Cover main order flow and error cases.",
                        "skills": "python, django, testing",
                        "estimated_hours": "6",
                        "priority": "3",
                        "status": "todo",
                        "due_in_days": 12,
                    },
                    {
                        "title": "Admin panel for store managers",
                        "description": "Simple screens to edit products and stock.",
                        "skills": "django, python, ui",
                        "estimated_hours": "9",
                        "priority": "3",
                        "status": "todo",
                        "due_in_days": 14,
                    },
                    {
                        "title": "Responsive UI polish",
                        "description": "Mobile layout fixes and visual consistency.",
                        "skills": "css, ui, react",
                        "estimated_hours": "4",
                        "priority": "4",
                        "status": "todo",
                        "due_in_days": 16,
                    },
                    {
                        "title": "Payment provider sandbox integration",
                        "description": "Connect test payment API and handle callbacks.",
                        "skills": "python, api",
                        "estimated_hours": "8",
                        "priority": "2",
                        "status": "todo",
                        "due_in_days": 10,
                    },
                    {
                        "title": "Order status email notifications",
                        "description": "Send confirmation and shipping emails.",
                        "skills": "python, django",
                        "estimated_hours": "5",
                        "priority": "4",
                        "status": "todo",
                        "due_in_days": 18,
                    },
                ],
            },
            {
                "name": "Internal HR Leave System",
                "description": (
                    "Small internal tool for leave requests in a Warsaw office. "
                    "Used to compare allocation strategies on a second dataset."
                ),
                "status": "active",
                "workers": [
                    {
                        "name": "Jakub Wojcik",
                        "skills": "python, django, sql",
                        "capacity_hours": "30",
                    },
                    {
                        "name": "Natalia Kamińska",
                        "skills": "javascript, react, css",
                        "capacity_hours": "34",
                    },
                    {
                        "name": "Oliwia Szymanska",
                        "skills": "python, api, testing",
                        "capacity_hours": "28",
                    },
                ],
                "tasks": [
                    {
                        "title": "Leave request data model",
                        "description": "Employees, leave types, approvals and dates.",
                        "skills": "python, django, sql",
                        "estimated_hours": "5",
                        "priority": "1",
                        "status": "todo",
                        "due_in_days": 4,
                    },
                    {
                        "title": "Employee leave form",
                        "description": "Frontend form to submit a leave request.",
                        "skills": "react, javascript, css",
                        "estimated_hours": "6",
                        "priority": "2",
                        "status": "todo",
                        "due_in_days": 8,
                    },
                    {
                        "title": "Manager approval API",
                        "description": "Endpoints to approve or reject requests.",
                        "skills": "python, api, django",
                        "estimated_hours": "7",
                        "priority": "1",
                        "status": "todo",
                        "due_in_days": 11,
                    },
                    {
                        "title": "Calendar overview page",
                        "description": "Show team absences on a monthly calendar.",
                        "skills": "react, css, javascript",
                        "estimated_hours": "8",
                        "priority": "3",
                        "status": "todo",
                        "due_in_days": 15,
                    },
                    {
                        "title": "Basic validation tests",
                        "description": "Tests for overlapping leave and limits.",
                        "skills": "python, testing",
                        "estimated_hours": "4",
                        "priority": "3",
                        "status": "todo",
                        "due_in_days": 17,
                    },
                    {
                        "title": "Export leave report to CSV",
                        "description": "Download monthly report for HR.",
                        "skills": "python, django",
                        "estimated_hours": "3",
                        "priority": "4",
                        "status": "todo",
                        "due_in_days": 20,
                    },
                ],
            },
        ]
