from django.db import models

from .allocation_run import AllocationRun
from .task import Task
from .worker import Worker


class Assignment(models.Model):
    allocation_run = models.ForeignKey(
        AllocationRun,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    worker = models.ForeignKey(
        Worker,
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        unique_together = ("allocation_run", "task")

    def __str__(self):
        return str(self.task) + " -> " + str(self.worker)
