from django.db import models

from .project import Project


class Worker(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="workers",
    )
    name = models.CharField(max_length=200)
    skills = models.JSONField(default=list, blank=True)
    capacity_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=40,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name + " (" + self.project.name + ")"
