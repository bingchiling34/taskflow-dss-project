from core.repositories import ProjectRepository


class ProjectService:
    VALID_STATUSES = ("active", "archived")

    def __init__(self):
        self.projects = ProjectRepository()

    def list_projects(self):
        return self.projects.list_all()

    def get_project(self, project_id):
        return self.projects.get_by_id(project_id)

    def create_project(self, name, description="", status="active"):
        clean = self._clean_fields(name, description, status)
        if clean["errors"]:
            return None, clean["errors"]
        project = self.projects.create(
            clean["name"],
            clean["description"],
            clean["status"],
        )
        return project, {}

    def update_project(self, project, name, description="", status="active"):
        clean = self._clean_fields(name, description, status)
        if clean["errors"]:
            return None, clean["errors"]
        updated = self.projects.update(
            project,
            clean["name"],
            clean["description"],
            clean["status"],
        )
        return updated, {}

    def delete_project(self, project):
        self.projects.delete(project)

    def _clean_fields(self, name, description, status):
        errors = {}
        clean_name = (name or "").strip()
        clean_description = (description or "").strip()
        clean_status = (status or "active").strip()

        if not clean_name:
            errors["name"] = "Name is required."
        elif len(clean_name) > 200:
            errors["name"] = "Name must be at most 200 characters."

        if clean_status not in self.VALID_STATUSES:
            errors["status"] = "Status must be active or archived."

        return {
            "name": clean_name,
            "description": clean_description,
            "status": clean_status,
            "errors": errors,
        }
