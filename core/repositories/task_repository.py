from core.models import Task


class TaskRepository:
    def count(self):
        return Task.objects.count()

    def list_all(self):
        return list(Task.objects.select_related("project").all())

    def list_by_project(self, project_id):
        return list(
            Task.objects.filter(project_id=project_id)
            .select_related("project")
            .all()
        )

    def get_by_id(self, task_id):
        return (
            Task.objects.filter(pk=task_id)
            .select_related("project")
            .first()
        )

    def create(
        self,
        project,
        title,
        description,
        required_skills,
        estimated_hours,
        priority,
        status,
    ):
        return Task.objects.create(
            project=project,
            title=title,
            description=description,
            required_skills=required_skills,
            estimated_hours=estimated_hours,
            priority=priority,
            status=status,
        )

    def update(
        self,
        task,
        project,
        title,
        description,
        required_skills,
        estimated_hours,
        priority,
        status,
    ):
        task.project = project
        task.title = title
        task.description = description
        task.required_skills = required_skills
        task.estimated_hours = estimated_hours
        task.priority = priority
        task.status = status
        task.save()
        return task

    def delete(self, task):
        task.delete()
