from core.models import Project


class ProjectRepository:
    def count(self):
        return Project.objects.count()

    def list_all(self):
        return list(Project.objects.all())

    def get_by_id(self, project_id):
        return Project.objects.filter(pk=project_id).first()

    def create(self, name, description, status):
        return Project.objects.create(
            name=name,
            description=description,
            status=status,
        )

    def update(self, project, name, description, status):
        project.name = name
        project.description = description
        project.status = status
        project.save()
        return project

    def delete(self, project):
        project.delete()
