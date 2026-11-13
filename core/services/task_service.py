from decimal import Decimal, InvalidOperation

from core.repositories import ProjectRepository, TaskRepository


class TaskService:
    VALID_STATUSES = ("todo", "in_progress", "done")
    MIN_PRIORITY = 1
    MAX_PRIORITY = 5

    def __init__(self):
        self.tasks = TaskRepository()
        self.projects = ProjectRepository()

    def list_tasks(self, project_id=None):
        if project_id:
            return self.tasks.list_by_project(project_id)
        return self.tasks.list_all()

    def get_task(self, task_id):
        return self.tasks.get_by_id(task_id)

    def create_task(
        self,
        project_id,
        title,
        description="",
        skills_text="",
        estimated_hours="1",
        priority="3",
        status="todo",
    ):
        clean = self._clean_fields(
            project_id,
            title,
            description,
            skills_text,
            estimated_hours,
            priority,
            status,
        )
        if clean["errors"]:
            return None, clean["errors"]
        task = self.tasks.create(
            clean["project"],
            clean["title"],
            clean["description"],
            clean["required_skills"],
            clean["estimated_hours"],
            clean["priority"],
            clean["status"],
        )
        return task, {}

    def update_task(
        self,
        task,
        project_id,
        title,
        description="",
        skills_text="",
        estimated_hours="1",
        priority="3",
        status="todo",
    ):
        clean = self._clean_fields(
            project_id,
            title,
            description,
            skills_text,
            estimated_hours,
            priority,
            status,
        )
        if clean["errors"]:
            return None, clean["errors"]
        updated = self.tasks.update(
            task,
            clean["project"],
            clean["title"],
            clean["description"],
            clean["required_skills"],
            clean["estimated_hours"],
            clean["priority"],
            clean["status"],
        )
        return updated, {}

    def delete_task(self, task):
        self.tasks.delete(task)

    def skills_to_text(self, skills):
        if not skills:
            return ""
        return ", ".join(skills)

    def _clean_fields(
        self,
        project_id,
        title,
        description,
        skills_text,
        estimated_hours,
        priority,
        status,
    ):
        errors = {}
        clean_title = (title or "").strip()
        clean_description = (description or "").strip()
        clean_status = (status or "todo").strip()
        project = None

        if not project_id:
            errors["project_id"] = "Project is required."
        else:
            project = self.projects.get_by_id(project_id)
            if project is None:
                errors["project_id"] = "Selected project was not found."

        if not clean_title:
            errors["title"] = "Title is required."
        elif len(clean_title) > 255:
            errors["title"] = "Title must be at most 255 characters."

        required_skills = self._parse_skills(skills_text)

        try:
            hours = Decimal(str(estimated_hours).strip())
            if hours <= 0:
                errors["estimated_hours"] = "Estimated hours must be greater than 0."
        except (InvalidOperation, AttributeError):
            hours = None
            errors["estimated_hours"] = "Estimated hours must be a number."

        try:
            priority_value = int(str(priority).strip())
            if priority_value < self.MIN_PRIORITY or priority_value > self.MAX_PRIORITY:
                errors["priority"] = "Priority must be between 1 and 5."
        except (TypeError, ValueError):
            priority_value = None
            errors["priority"] = "Priority must be a whole number."

        if clean_status not in self.VALID_STATUSES:
            errors["status"] = "Status must be todo, in_progress, or done."

        return {
            "project": project,
            "title": clean_title,
            "description": clean_description,
            "required_skills": required_skills,
            "estimated_hours": hours,
            "priority": priority_value,
            "status": clean_status,
            "errors": errors,
        }

    def _parse_skills(self, skills_text):
        text = (skills_text or "").strip()
        if text == "":
            return []
        skills = []
        for part in text.split(","):
            skill = part.strip()
            if skill != "" and skill not in skills:
                skills.append(skill)
        return skills
