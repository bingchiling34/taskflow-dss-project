from core.models import Project


class ProjectRepository:
    def count(self):
        return Project.objects.count()
