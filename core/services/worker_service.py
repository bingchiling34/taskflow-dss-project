from decimal import Decimal, InvalidOperation

from core.repositories import ProjectRepository, WorkerRepository


class WorkerService:
    def __init__(self):
        self.workers = WorkerRepository()
        self.projects = ProjectRepository()

    def list_workers(self, project_id=None):
        if project_id:
            return self.workers.list_by_project(project_id)
        return self.workers.list_all()

    def get_worker(self, worker_id):
        return self.workers.get_by_id(worker_id)

    def create_worker(self, project_id, name, skills_text="", capacity_hours="40"):
        clean = self._clean_fields(project_id, name, skills_text, capacity_hours)
        if clean["errors"]:
            return None, clean["errors"]
        worker = self.workers.create(
            clean["project"],
            clean["name"],
            clean["skills"],
            clean["capacity_hours"],
        )
        return worker, {}

    def update_worker(self, worker, project_id, name, skills_text="", capacity_hours="40"):
        clean = self._clean_fields(project_id, name, skills_text, capacity_hours)
        if clean["errors"]:
            return None, clean["errors"]
        updated = self.workers.update(
            worker,
            clean["project"],
            clean["name"],
            clean["skills"],
            clean["capacity_hours"],
        )
        return updated, {}

    def delete_worker(self, worker):
        self.workers.delete(worker)

    def skills_to_text(self, skills):
        if not skills:
            return ""
        return ", ".join(skills)

    def _clean_fields(self, project_id, name, skills_text, capacity_hours):
        errors = {}
        clean_name = (name or "").strip()
        project = None

        if not project_id:
            errors["project_id"] = "Project is required."
        else:
            project = self.projects.get_by_id(project_id)
            if project is None:
                errors["project_id"] = "Selected project was not found."

        if not clean_name:
            errors["name"] = "Name is required."
        elif len(clean_name) > 200:
            errors["name"] = "Name must be at most 200 characters."

        skills = self._parse_skills(skills_text)

        try:
            hours = Decimal(str(capacity_hours).strip())
            if hours <= 0:
                errors["capacity_hours"] = "Capacity must be greater than 0."
        except (InvalidOperation, AttributeError):
            hours = None
            errors["capacity_hours"] = "Capacity must be a number."

        return {
            "project": project,
            "name": clean_name,
            "skills": skills,
            "capacity_hours": hours,
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
