from core.models import Worker


class WorkerRepository:
    def count(self):
        return Worker.objects.count()
