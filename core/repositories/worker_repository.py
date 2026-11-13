from core.models import Worker


class WorkerRepository:
    def count(self):
        return Worker.objects.count()

    def list_all(self):
        return list(Worker.objects.select_related("project").all())

    def list_by_project(self, project_id):
        return list(
            Worker.objects.filter(project_id=project_id)
            .select_related("project")
            .all()
        )

    def get_by_id(self, worker_id):
        return (
            Worker.objects.filter(pk=worker_id)
            .select_related("project")
            .first()
        )

    def create(self, project, name, skills, capacity_hours):
        return Worker.objects.create(
            project=project,
            name=name,
            skills=skills,
            capacity_hours=capacity_hours,
        )

    def update(self, worker, project, name, skills, capacity_hours):
        worker.project = project
        worker.name = name
        worker.skills = skills
        worker.capacity_hours = capacity_hours
        worker.save()
        return worker

    def delete(self, worker):
        worker.delete()
