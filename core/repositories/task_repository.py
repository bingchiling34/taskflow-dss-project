from core.models import Task


class TaskRepository:
    def count(self):
        return Task.objects.count()
